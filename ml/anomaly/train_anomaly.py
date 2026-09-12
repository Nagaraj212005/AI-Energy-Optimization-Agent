import os
import sqlite3
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler

from ml.anomaly.anomaly_model import build_anomaly_model

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "energy.db")
MODEL_DIR = os.path.join(BASE_DIR, "ml", "trained_models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    consumption,
    year,
    month,
    day,
    hour,
    weekend,
    peak_hour
FROM energy_consumption
"""

df = pd.read_sql(query, conn)
conn.close()

# ------------------------------------------------------------------
# Features
# ------------------------------------------------------------------

FEATURES = [
    "consumption",
    "year",
    "month",
    "day",
    "hour",
    "weekend",
    "peak_hour",
]

X = df[FEATURES]

# ------------------------------------------------------------------
# Scale Features
# ------------------------------------------------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------------
# Train Model
# ------------------------------------------------------------------

model = build_anomaly_model()
model.fit(X_scaled)

# ------------------------------------------------------------------
# Save Model
# ------------------------------------------------------------------

joblib.dump(
    model,
    os.path.join(MODEL_DIR, "anomaly_model.joblib"),
)

joblib.dump(
    scaler,
    os.path.join(MODEL_DIR, "anomaly_scaler.joblib"),
)

print("\n===================================")
print("Anomaly model trained successfully.")
print(f"Model saved to : {MODEL_DIR}")
print("===================================")