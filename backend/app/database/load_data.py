import pandas as pd
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import EnergyConsumption


# Project Root
BASE_DIR = Path(__file__).resolve().parents[3]

# Processed CSV Path
CSV_PATH = BASE_DIR / "data" / "processed" / "processed_energy_data.csv"


def load_data():

    db: Session = SessionLocal()

    print("Reading CSV...")

    df = pd.read_csv(CSV_PATH)

    # Convert Datetime column to Python datetime
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    print(f"Loaded {len(df)} rows")

    for _, row in df.iterrows():

        energy = EnergyConsumption(

            datetime=row["Datetime"].to_pydatetime(),

            consumption=float(row["Consumption"]),

            region=str(row["Region"]),

            year=int(row["Year"]),

            month=int(row["Month"]),

            day=int(row["Day"]),

            hour=int(row["Hour"]),

            weekday=str(row["Weekday"]),

            weekend=bool(row["Weekend"]),

            peak_hour=bool(row["Peak_Hour"])

        )

        db.add(energy)

    print("Saving data to database...")

    db.commit()

    db.close()

    print("Database Loaded Successfully!")


if __name__ == "__main__":
    load_data()