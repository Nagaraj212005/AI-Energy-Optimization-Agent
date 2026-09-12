"""
Diagnostic script — run from project root:
    python .gemini/antigravity-ide/brain/a409a62e-e8fa-4312-ad7d-fe941e736d52/scratch/diagnose_anomaly.py

Checks every claim about the IsolationForest before we fix anything.
"""
import sys, os
from pathlib import Path

# ── resolve project root ──────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[5]   # scratch/brain/aid/antigravity-ide/.gemini/project
# simpler: walk up until we find energy.db
for p in Path(__file__).resolve().parents:
    if (p / "energy.db").exists():
        ROOT = p
        break
sys.path.insert(0, str(ROOT))

import sqlite3
import numpy as np
import pandas as pd
import joblib

MODEL_PATH  = ROOT / "ml" / "trained_models" / "anomaly_model.joblib"
SCALER_PATH = ROOT / "ml" / "trained_models" / "anomaly_scaler.joblib"
DB_PATH     = ROOT / "energy.db"

FEATURES = ["consumption", "year", "month", "day", "hour", "weekend", "peak_hour"]

print("=" * 70)
print("STEP 1 — Load model & scaler")
print("=" * 70)
model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print(f"  model type         : {type(model).__name__}")
print(f"  n_estimators (cfg) : {model.n_estimators}")
print(f"  n_estimators (fit) : {len(model.estimators_)}")
print(f"  contamination      : {model.contamination}")
print(f"  model.offset_      : {model.offset_}")
print(f"  scaler.mean_       : {scaler.mean_}")
print(f"  scaler.scale_      : {scaler.scale_}")

print()
print("=" * 70)
print("STEP 2 — Load a small sample from DB for quick diagnosis")
print("=" * 70)
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql(
    "SELECT consumption, year, month, day, hour, "
    "CAST(weekend AS INTEGER) AS weekend, "
    "CAST(peak_hour AS INTEGER) AS peak_hour "
    "FROM energy_consumption LIMIT 50000",
    conn
)
conn.close()
print(f"  rows loaded: {len(df)}")

X_raw    = np.ascontiguousarray(df[FEATURES].to_numpy(dtype=np.float64))
X_scaled = scaler.transform(X_raw)

print()
print("=" * 70)
print("STEP 3 — decision_function() and predict() on the sample")
print("=" * 70)
scores      = model.decision_function(X_scaled)
predictions = model.predict(X_scaled)

print(f"  scores.min()  : {scores.min():.6f}")
print(f"  scores.max()  : {scores.max():.6f}")
print(f"  scores.mean() : {scores.mean():.6f}")
print(f"  model.offset_ : {model.offset_:.6f}")

pred_counts = dict(zip(*np.unique(predictions, return_counts=True)))
print(f"  predict() counts (1=normal, -1=anomaly) : {pred_counts}")
print(f"  anomalies via predict()==-1              : {np.sum(predictions == -1)}")
print(f"  anomaly %  via predict()==-1             : {100*np.mean(predictions==-1):.2f}%")

print()
print("=" * 70)
print("STEP 4 — What does 'scores <= model.offset_' produce?   ← SERVICE BUG")
print("=" * 70)
buggy_mask = scores <= model.offset_
print(f"  scores <= model.offset_  →  anomalies = {buggy_mask.sum()}   ← THIS IS THE BUG")

print()
print("=" * 70)
print("STEP 5 — Correct threshold: scores < 0                  ← CORRECT")
print("=" * 70)
#
#  sklearn internal:
#    decision_function(X) = score_samples(X) - offset_
#    predict(X):  -1  if decision_function(X) < 0
#                 +1  otherwise
#
#  So the correct anomaly condition on decision_function output is:  score < 0
#
correct_mask = scores < 0
print(f"  scores < 0               →  anomalies = {correct_mask.sum()}   ← CORRECT")
print(f"  anomaly %                →  {100*correct_mask.mean():.2f}%")

print()
print("=" * 70)
print("STEP 6 — Why scores <= model.offset_ gives ZERO")
print("=" * 70)
print(f"  decision_function(X) = score_samples(X)  -  model.offset_")
print(f"  model.offset_        = {model.offset_:.6f}   (negative, calibrated from contamination)")
print(f"  scores range         = [{scores.min():.6f}, {scores.max():.6f}]")
print()
print(f"  The buggy condition:   scores <= model.offset_")
print(f"  Expands to:            (score_samples - offset_) <= offset_")
print(f"  Simplifies to:         score_samples <= 2 * offset_ = {2*model.offset_:.6f}")
print(f"  But score_samples min  = {(scores + model.offset_).min():.6f}")
print(f"  2*offset_              = {2*model.offset_:.6f}")
print(f"  → All score_samples > 2*offset_?  {((scores + model.offset_) > 2*model.offset_).all()}")
print(f"  → Result: ZERO anomalies (all masked out)")
print()
print(f"  The correct condition: scores < 0")
print(f"  Expands to:            score_samples - offset_ < 0")
print(f"  Simplifies to:         score_samples < offset_  ← exactly what predict() does")
