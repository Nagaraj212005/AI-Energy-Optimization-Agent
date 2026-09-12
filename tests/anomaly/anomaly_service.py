import os
import pandas as pd
from sklearn.ensemble import IsolationForest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "processed_energy_data.csv")

def detect_anomalies():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df = df.sort_values("Datetime").reset_index(drop=True)

    df["Weekday_Number"] = df["Datetime"].dt.weekday

    features = [
        "Consumption",
        "Hour",
        "Day",
        "Month",
        "Weekday_Number",
        "Weekend",
        "Peak_Hour"
    ]

    missing = [column for column in features if column not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    for column in features:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=features)

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    model.fit(df[features])

    df["anomaly_score"] = model.decision_function(df[features])

    df["anomaly"] = model.predict(df[features])

    df["anomaly"] = df["anomaly"].map({
        1: 0,
        -1: 1
    })

    return df