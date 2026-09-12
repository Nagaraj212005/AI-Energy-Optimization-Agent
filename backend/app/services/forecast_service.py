import logging
from datetime import timedelta
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sqlalchemy import desc

from backend.app.database.database import SessionLocal
from backend.app.database.models import EnergyConsumption

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "ml" / "trained_models" / "forecast_model.joblib"

FEATURES = [
    "consumption",
    "year",
    "month",
    "day",
    "hour",
    "weekend",
    "peak_hour",
]

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Forecast model not found: {MODEL_PATH}")

# Load the compact artifact once when the service module is imported.
model = joblib.load(MODEL_PATH)


def is_weekend(weekday):
    return 1 if weekday >= 5 else 0


def is_peak_hour(hour):
    return 1 if (7 <= hour <= 10) or (17 <= hour <= 21) else 0


def get_next_24_hour_forecast():
    db = SessionLocal()

    try:
        latest = (
            db.query(EnergyConsumption)
            .order_by(desc(EnergyConsumption.datetime))
            .first()
        )
    finally:
        db.close()

    if latest is None:
        raise Exception("No data found in energy_consumption table.")

    current_dt = pd.Timestamp(latest.datetime)
    current_consumption = float(latest.consumption)

    forecast = []

    for _ in range(24):

        next_dt = current_dt + timedelta(hours=1)

        feature = np.array([[
            current_consumption,
            next_dt.year,
            next_dt.month,
            next_dt.day,
            next_dt.hour,
            is_weekend(next_dt.weekday()),
            is_peak_hour(next_dt.hour),
        ]])

        prediction = float(model.predict(feature.astype(np.float32))[0])

        forecast.append(
            {
                "datetime": next_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "predicted_consumption": round(prediction, 2),
            }
        )

        current_dt = next_dt
        current_consumption = prediction

    return {
        "forecast": forecast
    }


# ------------------------------------------------------------------
# Compatibility function
# ------------------------------------------------------------------

def predict_forecast():
    """
    Alias for older imports.
    """
    return get_next_24_hour_forecast()