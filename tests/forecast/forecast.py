"""
forecast.py
-----------
Optimized PJM hourly energy-demand forecasting pipeline.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -------------------------------------------------
# PATH CONFIGURATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = BASE_DIR / "data" / "raw" / "PJM_Load_hourly.csv"
MODEL_FILE = BASE_DIR / "pjm_xgboost_model.json"
TEST_RESULT_FILE = BASE_DIR / "PJM_test_forecast_results.csv"

TARGET = "PJM_Load_MW"

FEATURES = [
    "hour",
    "day_of_week",
    "day_of_year",
    "month",
    "year",
    "is_weekend",
    "lag_1",
    "lag_24",
    "lag_168",
    "rolling_24",
    "rolling_168",
]


def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)

    required = {"Datetime", TARGET}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    df = df.dropna(subset=["Datetime", TARGET])
    df = (
        df.sort_values("Datetime")
        .drop_duplicates(subset=["Datetime"])
        .reset_index(drop=True)
    )

    df["hour"] = df["Datetime"].dt.hour
    df["day_of_week"] = df["Datetime"].dt.dayofweek
    df["day_of_year"] = df["Datetime"].dt.dayofyear
    df["month"] = df["Datetime"].dt.month
    df["year"] = df["Datetime"].dt.year
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    df["lag_1"] = df[TARGET].shift(1)
    df["lag_24"] = df[TARGET].shift(24)
    df["lag_168"] = df[TARGET].shift(168)

    shifted = df[TARGET].shift(1)

    df["rolling_24"] = shifted.rolling(24).mean()
    df["rolling_168"] = shifted.rolling(168).mean()

    df = df.dropna(subset=FEATURES + [TARGET]).reset_index(drop=True)

    return df


def train_and_evaluate(df):

    split_index = int(len(df) * 0.8)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        tree_method="hist",
        random_state=42,
        n_jobs=-1,
    )

    print("Training XGBoost model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print("=" * 60)
    print("Forecast Metrics")
    print("=" * 60)
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")
    print(f"MAPE : {mape:.2f}%")

    results = test_df[["Datetime", TARGET]].copy()
    results["Forecast_MW"] = y_pred
    results.to_csv(TEST_RESULT_FILE, index=False)

    model.save_model(str(MODEL_FILE))

    print("\nSaved:")
    print(TEST_RESULT_FILE)
    print(MODEL_FILE)


if __name__ == "__main__":

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}"
        )

    df = load_and_prepare_data(DATA_FILE)

    train_and_evaluate(df)