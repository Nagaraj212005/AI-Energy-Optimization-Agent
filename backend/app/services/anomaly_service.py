"""
anomaly_service.py — Optimized anomaly detection using pre-trained Isolation Forest.

Key optimizations vs previous version
──────────────────────────────────────
1. Raw SQL via SQLAlchemy text() + pd.read_sql()
   - Replaces ORM .all() which instantiates 1M Python objects (~30–60 s overhead)
   - Projects only the 9 columns actually needed (no SELECT *)
   - Drops the unnecessary ORDER BY datetime DESC (was sorting 1M rows for nothing)
   → Estimated saving: 25–50 s

2. Model & scaler loaded once at module import
   - Previously lazy-loaded on first request, fine for singleton; now loaded at
     startup so the very first request is also fast.
   → Saving: ~0.1–0.3 s per cold start

3. Single model pass: decision_function() only, no separate predict()
   - predict() internally calls decision_function() then thresholds.
   - We call decision_function() once and apply the threshold manually,
     eliminating a full redundant pass through all 200 trees × 1M samples.
   → Estimated saving: 3–8 s

4. NumPy boolean mask instead of DataFrame .replace() + filtering
   - Avoids an extra pandas pass over 1M rows.
   → Saving: ~0.2–0.5 s

5. Response built from pre-filtered NumPy arrays + Python zip()
   - Avoids itertuples() overhead and repeated DataFrame column accesses.
   → Saving: ~0.1–0.2 s

6. No scaler.fit() / fit_transform() anywhere
   - Training pipeline used scaler.fit_transform(X); inference uses only
     scaler.transform(X).  This constraint is enforced here.

Expected total response time
─────────────────────────────
Before optimizations  : ~60–120 s   (ORM loading alone for 1 M rows)
After optimizations   : ~3–8 s      (dominated by IsolationForest.decision_function
                                     on 1 M × 200 trees; unavoidable without
                                     reducing dataset size or using approximate
                                     nearest-neighbour methods)
"""

import logging
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sqlalchemy import text

from backend.app.database.database import SessionLocal


logger = logging.getLogger(__name__)

# ─── Paths ────────────────────────────────────────────────────────────────────

# FILE lives at: backend/app/services/anomaly_service.py
# parents[3]  →  project root  (services → app → backend → project_root)
_BASE_DIR    = Path(__file__).resolve().parents[3]
_MODEL_PATH  = _BASE_DIR / "ml" / "trained_models" / "anomaly_model.joblib"
_SCALER_PATH = _BASE_DIR / "ml" / "trained_models" / "anomaly_scaler.joblib"

# ─── Feature order — MUST match train_anomaly.py exactly ─────────────────────

FEATURES = [
    "consumption",
    "year",
    "month",
    "day",
    "hour",
    "weekend",
    "peak_hour",
]

# ─── SQL — project only columns required for inference + response metadata ────
# Omitting: id, weekday (unused after training), ORDER BY (unnecessary)

_SQL = text(
    """
    SELECT
        datetime,
        region,
        consumption,
        year,
        month,
        day,
        hour,
        CAST(weekend  AS INTEGER) AS weekend,
        CAST(peak_hour AS INTEGER) AS peak_hour
    FROM energy_consumption
    """
)

# ─── Load artifacts once at module import ─────────────────────────────────────
# This ensures both the first and all subsequent requests are fast.
# If the files are missing at startup the application will fail loudly rather
# than silently returning wrong results later.

_t0 = time.perf_counter()

if not _MODEL_PATH.exists():
    raise FileNotFoundError(f"Anomaly model not found: {_MODEL_PATH}")
if not _SCALER_PATH.exists():
    raise FileNotFoundError(f"Anomaly scaler not found: {_SCALER_PATH}")

_model: object  = joblib.load(_MODEL_PATH)
_scaler: object = joblib.load(_SCALER_PATH)

logger.info(
    "Anomaly artifacts loaded in %.3f s  |  model=%s  |  scaler=%s",
    time.perf_counter() - _t0,
    _MODEL_PATH.name,
    _SCALER_PATH.name,
)

# decision_function() already returns score_samples() - offset_.  Its output
# is therefore thresholded at zero; comparing it to offset_ would apply the
# offset twice and can suppress every anomaly.
_DECISION_THRESHOLD: float = 0.0


# ─── Service ──────────────────────────────────────────────────────────────────

def detect_anomalies() -> dict:
    """
    Detect anomalies in the full energy_consumption table using the
    pre-trained Isolation Forest model.

    Returns
    -------
    dict
        {
            "total_records":   int,
            "total_anomalies": int,
            "anomalies": [
                {
                    "datetime":      str,
                    "region":        str,
                    "consumption":   float,
                    "anomaly_score": float,
                }
            ]
        }
    """

    timings: dict[str, float] = {}

    # ------------------------------------------------------------------
    # 1. Database fetch — raw SQL, column-projected, no ORM overhead
    # ------------------------------------------------------------------
    t = time.perf_counter()
    db = SessionLocal()
    try:
        with db.connection() as conn:
            df = pd.read_sql(_SQL, con=conn)
    finally:
        db.close()
    timings["db_fetch_s"] = time.perf_counter() - t
    logger.info("DB fetch: %.3f s  — rows=%d", timings["db_fetch_s"], len(df))

    if df.empty:
        return {"total_records": 0, "total_anomalies": 0, "anomalies": []}

    # ------------------------------------------------------------------
    # 2. Preprocessing — cast booleans read as int/float to int, drop NaN
    # ------------------------------------------------------------------
    t = time.perf_counter()

    df["weekend"]   = df["weekend"].astype(int)
    df["peak_hour"] = df["peak_hour"].astype(int)
    df["datetime"]  = pd.to_datetime(df["datetime"])

    # Drop rows with missing feature values (should be zero for a clean DB)
    before = len(df)
    df.dropna(subset=FEATURES, inplace=True)
    dropped = before - len(df)
    if dropped:
        logger.warning("Dropped %d rows with NaN in features.", dropped)

    # Extract feature matrix as a contiguous NumPy array (C-order) for
    # maximum throughput into sklearn's Cython internals.
    X_raw: np.ndarray = np.ascontiguousarray(df[FEATURES].to_numpy(dtype=np.float64))

    timings["preprocess_s"] = time.perf_counter() - t
    logger.info("Preprocessing: %.3f s", timings["preprocess_s"])

    # ------------------------------------------------------------------
    # 3. Scaling — transform only (scaler was fit during training)
    # ------------------------------------------------------------------
    t = time.perf_counter()
    X_scaled: np.ndarray = _scaler.transform(X_raw)
    timings["scaling_s"] = time.perf_counter() - t
    logger.info("Scaling: %.3f s", timings["scaling_s"])

    # ------------------------------------------------------------------
    # 4. Prediction — single pass via decision_function()
    #
    #    WHY NOT model.predict()?
    #    predict() internally calls decision_function() and then applies
    #    model.offset_ as a threshold.  Calling both predict() AND
    #    decision_function() doubles the tree-traversal work for 1 M rows.
    #    We call decision_function() once and apply the threshold ourselves.
    #
    #    sklearn convention:
    #      score > offset_  →  normal  (predict = +1)
    #      score ≤ offset_  →  anomaly (predict = -1)
    #    We remap to:  anomaly flag = 1,  normal = 0
    # ------------------------------------------------------------------
    t = time.perf_counter()
    # ------------------------------------------------------------------
    # Single pass: decision_function() returns raw scores.
    # Applying _DECISION_THRESHOLD manually avoids a second full
    # tree-traversal that model.predict() would otherwise trigger.
    # sklearn convention: score <= offset_ → anomaly (predict = -1)
    # ------------------------------------------------------------------
    scores: np.ndarray = _model.decision_function(X_scaled)   # (N,)
    anomaly_mask: np.ndarray = scores <= _DECISION_THRESHOLD   # (N,) bool
    timings["prediction_s"] = time.perf_counter() - t
    logger.info(
        "Prediction: %.3f s  — anomalies=%d / %d  (%.2f%%)",
        timings["prediction_s"],
        anomaly_mask.sum(),
        len(scores),
        100.0 * anomaly_mask.mean(),
    )
    # ------------------------------------------------------------------
    # 5. Response creation — work entirely on filtered NumPy arrays,
    #    no itertuples / iterrows
    # ------------------------------------------------------------------
    t = time.perf_counter()

    total_records   = len(df)
    total_anomalies = int(anomaly_mask.sum())

    # Pull metadata columns as arrays once; index with bool mask
    datetimes_all   = df["datetime"].to_numpy()          # datetime64[ns]
    regions_all     = df["region"].to_numpy(dtype=object)
    consumptions_all = df["consumption"].to_numpy(dtype=np.float64)

    anom_datetimes    = datetimes_all[anomaly_mask]
    anom_regions      = regions_all[anomaly_mask]
    anom_consumptions = consumptions_all[anomaly_mask]
    anom_scores       = scores[anomaly_mask]

    # Sort by score ascending (most anomalous first) and take top 100
    sort_idx = np.argsort(anom_scores)[:100]

    anomalies_list = [
        {
            "datetime":      str(pd.Timestamp(anom_datetimes[i])),
            "region":        str(anom_regions[i]),
            "consumption":   round(float(anom_consumptions[i]), 2),
            "anomaly_score": round(float(anom_scores[i]), 5),
        }
        for i in sort_idx
    ]

    timings["response_build_s"] = time.perf_counter() - t
    logger.info("Response build: %.3f s", timings["response_build_s"])

    total_s = sum(timings.values())
    logger.info(
        "detect_anomalies complete in %.3f s total  |  %s",
        total_s,
        "  |  ".join(f"{k}={v:.3f}s" for k, v in timings.items()),
    )

    return {
        "total_records":   total_records,
        "total_anomalies": total_anomalies,
        "anomalies":       anomalies_list,
    }