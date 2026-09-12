import os
import joblib
import pandas as pd

from sqlalchemy.orm import Session
from backend.app.database.models import EnergyConsumption

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "ml", "trained_models")

# ---------------------------------------------------------
# Load model once
# ---------------------------------------------------------

model = joblib.load(os.path.join(MODEL_DIR, "recommendation_model.joblib"))
scaler = joblib.load(os.path.join(MODEL_DIR, "recommendation_scaler.joblib"))
encoder = joblib.load(os.path.join(MODEL_DIR, "region_encoder.joblib"))

FEATURES = [
    "consumption",
    "region",
    "year",
    "month",
    "day",
    "hour",
    "weekend",
    "peak_hour",
]


def detect_recommendations(db: Session):

    rows = db.query(EnergyConsumption).all()

    if not rows:
        return {
            "total_records": 0,
            "recommendations": []
        }

    df = pd.DataFrame([
        {
            "datetime": r.datetime,
            "region": r.region,
            "consumption": r.consumption,
            "year": r.year,
            "month": r.month,
            "day": r.day,
            "hour": r.hour,
            "weekend": int(r.weekend),
            "peak_hour": int(r.peak_hour),
        }
        for r in rows
    ])

    # Encode region
    df["region_encoded"] = encoder.transform(df["region"])

    X = df.copy()

    X["region"] = df["region_encoded"]

    X = X[FEATURES]

    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)

    df["recommended_consumption"] = predictions

    df["saving"] = (
        df["consumption"] -
        df["recommended_consumption"]
    )

    df["saving_percent"] = (
        df["saving"] /
        df["consumption"]
    ) * 100

    def priority(x):
        if x >= 15:
            return "Critical"
        elif x >= 10:
            return "High"
        elif x >= 5:
            return "Medium"
        else:
            return "Low"

    df["priority"] = df["saving_percent"].apply(priority)

    recommendations = []

    for _, row in (
        df.sort_values("saving_percent", ascending=False)
        .head(100)
        .iterrows()
    ):

        recommendations.append({

            "datetime": str(row["datetime"]),

            "region": row["region"],

            "current_consumption": round(
                float(row["consumption"]), 2
            ),

            "recommended_consumption": round(
                float(row["recommended_consumption"]), 2
            ),

            "saving": round(
                float(row["saving"]), 2
            ),

            "saving_percent": round(
                float(row["saving_percent"]), 2
            ),

            "priority": row["priority"],

            "recommendation":
                "Reduce HVAC and shift non-essential load during peak hours."
                if row["priority"] in ["Critical", "High"]
                else
                "Current energy usage is acceptable."

        })

    return {

        "total_records": len(df),

        "recommendations": recommendations

    }