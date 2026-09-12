import os
import sqlite3
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from recommendation_model import build_recommendation_model

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "energy.db")

MODEL_DIR = os.path.join(BASE_DIR, "ml", "trained_models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------------

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    consumption,
    region,
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

print(f"Loaded {len(df)} rows")

# ------------------------------------------------------------------
# Encode Region
# ------------------------------------------------------------------

region_encoder = LabelEncoder()

df["region"] = region_encoder.fit_transform(df["region"])

# ------------------------------------------------------------------
# Create Target
# ------------------------------------------------------------------

def optimized_consumption(row):

    reduction = 0.03

    if row["peak_hour"]:
        reduction += 0.05

    if row["weekend"]:
        reduction += 0.02

    return row["consumption"] * (1 - reduction)

df["target"] = df.apply(optimized_consumption, axis=1)

# ------------------------------------------------------------------
# Features
# ------------------------------------------------------------------

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

X = df[FEATURES]

y = df["target"]

# ------------------------------------------------------------------
# Scaling
# ------------------------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------------
# Train Test Split
# ------------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
)

# ------------------------------------------------------------------
# Build Model
# ------------------------------------------------------------------

model = build_recommendation_model()

print("Training Recommendation Model...")

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("MAE :", mean_absolute_error(y_test, pred))
print("R2  :", r2_score(y_test, pred))

# ------------------------------------------------------------------
# Save Artifacts
# ------------------------------------------------------------------

joblib.dump(
    model,
    os.path.join(MODEL_DIR, "recommendation_model.joblib")
)

joblib.dump(
    scaler,
    os.path.join(MODEL_DIR, "recommendation_scaler.joblib")
)

joblib.dump(
    region_encoder,
    os.path.join(MODEL_DIR, "region_encoder.joblib")
)

print("\nRecommendation model trained successfully.")
print("Artifacts saved to:")
print(MODEL_DIR)