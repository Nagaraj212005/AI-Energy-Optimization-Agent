"""
forecast_service.py
-------------------
Reusable forecasting service for the optimized PJM XGBoost model.

It loads the trained model produced by forecast.py and generates the
next 24 hourly energy-demand forecasts.

Usage:
    from forecast_service import PJMForecastService

    service = PJMForecastService()
    forecast = service.forecast_next_24_hours("PJM_Load_hourly.csv")
    print(forecast)
"""

from pathlib import Path
import numpy as np
import pandas as pd
from xgboost import XGBRegressor


class PJMForecastService:
    """Production-style wrapper around the trained PJM XGBoost model."""

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

    TARGET = "PJM_Load_MW"

    def __init__(self, model_path: str = "pjm_xgboost_model.json"):
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}. "
                "Run forecast.py first to train and save the model."
            )

        self.model = XGBRegressor()
        self.model.load_model(str(self.model_path))

    @staticmethod
    def _make_features(history: pd.DataFrame) -> pd.DataFrame:
        """Create the same features used during model training."""
        df = history.copy()

        df["hour"] = df["Datetime"].dt.hour
        df["day_of_week"] = df["Datetime"].dt.dayofweek
        df["day_of_year"] = df["Datetime"].dt.dayofyear
        df["month"] = df["Datetime"].dt.month
        df["year"] = df["Datetime"].dt.year
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

        df["lag_1"] = df["PJM_Load_MW"].shift(1)
        df["lag_24"] = df["PJM_Load_MW"].shift(24)
        df["lag_168"] = df["PJM_Load_MW"].shift(168)

        shifted = df["PJM_Load_MW"].shift(1)
        df["rolling_24"] = shifted.rolling(24).mean()
        df["rolling_168"] = shifted.rolling(168).mean()

        return df

    def forecast_next_24_hours(self, data_file: str):
        """
        Generate recursive 24-hour demand forecasts.

        The forecast for each hour is appended to the history so that
        later hours can use the newly predicted values in lag features.
        """
        df = pd.read_csv(data_file)

        required = {"Datetime", self.TARGET}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}. "
                f"Found columns: {df.columns.tolist()}"
            )

        df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
        df[self.TARGET] = pd.to_numeric(df[self.TARGET], errors="coerce")
        df = df.dropna(subset=["Datetime", self.TARGET])
        df = df.sort_values("Datetime").drop_duplicates(
            subset=["Datetime"], keep="first"
        ).reset_index(drop=True)

        if len(df) < 169:
            raise ValueError(
                "At least 169 historical hourly observations are required "
                "for lag_168 and rolling_168 features."
            )

        history = df[["Datetime", self.TARGET]].copy()

        future_rows = []

        for _ in range(24):
            next_time = history["Datetime"].iloc[-1] + pd.Timedelta(hours=1)

            temp = pd.concat(
                [
                    history,
                    pd.DataFrame(
                        {
                            "Datetime": [next_time],
                            self.TARGET: [np.nan],
                        }
                    ),
                ],
                ignore_index=True,
            )

            temp_features = self._make_features(temp)
            X_next = temp_features.iloc[[-1]][self.FEATURES]

            if X_next.isna().any().any():
                raise ValueError(
                    "Unable to create complete features for the next hour."
                )

            prediction = float(self.model.predict(X_next)[0])

            future_rows.append(
                {
                    "Datetime": next_time,
                    "Forecast_MW": prediction,
                }
            )

            # Append prediction for recursive forecasting
            history = pd.concat(
                [
                    history,
                    pd.DataFrame(
                        {
                            "Datetime": [next_time],
                            self.TARGET: [prediction],
                        }
                    ),
                ],
                ignore_index=True,
            )

        return pd.DataFrame(future_rows)

    def save_24_hour_forecast(
        self,
        data_file: str,
        output_file: str = "PJM_next_24_hour_forecast.csv",
    ):
        """Generate and save the next 24-hour forecast."""
        forecast = self.forecast_next_24_hours(data_file)
        forecast.to_csv(output_file, index=False)

        print("=" * 60)
        print("PJM NEXT 24-HOUR ENERGY DEMAND FORECAST")
        print("=" * 60)
        print("\nForecast:")
        print(forecast.to_string(index=False))

        print("\nForecast statistics:")
        print(f"Minimum demand: {forecast['Forecast_MW'].min():.2f} MW")
        print(f"Maximum demand: {forecast['Forecast_MW'].max():.2f} MW")
        print(f"Average demand: {forecast['Forecast_MW'].mean():.2f} MW")

        print(f"\nSaved file: {output_file}")
        return forecast


if __name__ == "__main__":
    # Change this filename only if your input CSV has another name.
    DATA_FILE = "PJM_Load_hourly.csv"

    service = PJMForecastService()
    service.save_24_hour_forecast(DATA_FILE)
