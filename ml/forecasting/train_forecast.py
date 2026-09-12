import os
import sqlite3
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import mean_absolute_error, r2_score

from ml.forecasting.forecast_model import build_forecast_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "energy.db")
MODEL_DIR = os.path.join(BASE_DIR, "ml", "trained_models")

os.makedirs(MODEL_DIR, exist_ok=True)

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
ORDER BY datetime
"""

df = pd.read_sql(query, conn)
conn.close()

# Predict next hour consumption.  Keep one compact float32 matrix in memory;
# tree models do not need feature scaling.
features = [
    "consumption",
    "year",
    "month",
    "day",
    "hour",
    "weekend",
    "peak_hour",
]
X = df[features].to_numpy(dtype=np.float32, copy=True)
y = df["consumption"].shift(-1).to_numpy(dtype=np.float32, copy=True)

valid_rows = np.isfinite(y)
X = X[valid_rows]
y = y[valid_rows]
del df, valid_rows

split_index = int(len(X) * 0.8)
X_train = X[:split_index]
X_test = X[split_index:]
y_train = y[:split_index]
y_test = y[split_index:]

model = build_forecast_model()
model.fit(X_train, y_train)

predictions = model.predict(X_test).astype(np.float32, copy=False)

print("MAE:", mean_absolute_error(y_test, predictions))
print("R2 Score:", r2_score(y_test, predictions))

joblib.dump(model, os.path.join(MODEL_DIR, "forecast_model.joblib"))

del X, y, X_train, X_test, y_train, y_test, predictions, model

print("Forecast model saved successfully.")