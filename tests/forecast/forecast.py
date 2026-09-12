"""
forecast.py
-----------
Optimized PJM hourly energy-demand forecasting pipeline.

This file reproduces the forecasting workflow developed in Colab:
1. Load PJM hourly data
2. Clean and sort data
3. Create time/lag/rolling features
4. Chronological train/test split
5. Train optimized XGBoost
6. Evaluate with MAE, RMSE, R2 and MAPE
7. Save test predictions
8. Save the trained model for the forecasting service

Expected input columns:
    Datetime
    PJM_Load_MW

Usage:
    python forecast.py
"""

from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# CONFIGURATION
# -----------------------------
DATA_FILE = "PJM_Load_hourly.csv"
MODEL_FILE = "pjm_xgboost_model.json"
TEST_RESULT_FILE = "PJM_test_forecast_results.csv"

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


def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """Load PJM data and create forecasting features."""
    df = pd.read_csv(file_path)

    required = {"Datetime", TARGET}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}. "
            f"Found columns: {df.columns.tolist()}"
        )

    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    df = df.dropna(subset=["Datetime", TARGET])
    df = df.sort_values("Datetime").drop_duplicates(
        subset=["Datetime"], keep="first"
    ).reset_index(drop=True)

    # Time features
    df["hour"] = df["Datetime"].dt.hour
    df["day_of_week"] = df["Datetime"].dt.dayofweek
    df["day_of_year"] = df["Datetime"].dt.dayofyear
    df["month"] = df["Datetime"].dt.month
    df["year"] = df["Datetime"].dt.year
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Historical demand features
    df["lag_1"] = df[TARGET].shift(1)
    df["lag_24"] = df[TARGET].shift(24)
    df["lag_168"] = df[TARGET].shift(168)

    # Shift first to prevent the current target from leaking into rolling values
    shifted = df[TARGET].shift(1)
    df["rolling_24"] = shifted.rolling(24).mean()
    df["rolling_168"] = shifted.rolling(168).mean()

    df = df.dropna(subset=FEATURES + [TARGET]).reset_index(drop=True)

    return df


def train_and_evaluate(df: pd.DataFrame):
    """Chronological split, train XGBoost, evaluate and save results."""
    split_index = int(len(df) * 0.80)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    print("=" * 60)
    print("PJM OPTIMIZED ENERGY FORECASTING")
    print("=" * 60)
    print(f"Dataset shape: {df.shape}")
    print(f"Training rows: {len(train_df)}")
    print(f"Testing rows : {len(test_df)}")
    print()
    print("Training period:")
    print(train_df["Datetime"].iloc[0], "to", train_df["Datetime"].iloc[-1])
    print()
    print("Testing period:")
    print(test_df["Datetime"].iloc[0], "to", test_df["Datetime"].iloc[-1])

    # Optimized XGBoost configuration
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        tree_method="hist",
        n_jobs=-1,
        random_state=42,
    )

    print("\nTraining optimized XGBoost...")
    model.fit(X_train, y_train, verbose=False)
    print("Training completed successfully!")

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

    print("\n" + "=" * 60)
    print("FINAL FORECASTING RESULTS")
    print("=" * 60)
    print(f"MAE : {mae:.2f} MW")
    print(f"RMSE: {rmse:.2f} MW")
    print(f"R2  : {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")

    results = test_df[["Datetime", TARGET]].copy()
    results["Forecast_MW"] = y_pred
    results.to_csv(TEST_RESULT_FILE, index=False)

    model.save_model(MODEL_FILE)

    print("\nSaved files:")
    print(f"1. {TEST_RESULT_FILE}")
    print(f"2. {MODEL_FILE}")

    return model, results


if __name__ == "__main__":
    data_path = Path(DATA_FILE)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {DATA_FILE}\n"
            "Place PJM_Load_hourly.csv in the same folder as forecast.py."
        )

    data = load_and_prepare_data(DATA_FILE)
    train_and_evaluate(data)
