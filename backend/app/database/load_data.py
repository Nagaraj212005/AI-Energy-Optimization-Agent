import sys
import pandas as pd
from pathlib import Path

# Project Root — must match parents[3] in database.py
BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal, engine, DB_PATH
from backend.app.database.models import EnergyConsumption
from backend.app.database.database import Base

# Processed CSV Path
CSV_PATH = BASE_DIR / "data" / "processed" / "processed_energy_data.csv"

CHUNK_SIZE = 10_000  # rows per bulk insert batch


def load_data():

    # ------------------------------------------------------------------
    # 1. Confirm which DB file we are writing to
    # ------------------------------------------------------------------
    print(f"Target database: {DB_PATH}")

    # ------------------------------------------------------------------
    # 2. Ensure the table exists (idempotent)
    # ------------------------------------------------------------------
    Base.metadata.create_all(bind=engine)
    print("Tables verified / created.")

    # ------------------------------------------------------------------
    # 3. Read CSV
    # ------------------------------------------------------------------
    print(f"Reading CSV from: {CSV_PATH}")
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    print(f"Loaded {len(df)} rows from CSV")

    # ------------------------------------------------------------------
    # 4. Bulk insert in chunks
    # ------------------------------------------------------------------
    print("Saving data to database...")

    db: Session = SessionLocal()
    try:
        total_inserted = 0
        for start in range(0, len(df), CHUNK_SIZE):
            chunk = df.iloc[start : start + CHUNK_SIZE]
            mappings = [
                {
                    "datetime":    row["Datetime"].to_pydatetime(),
                    "consumption": float(row["Consumption"]),
                    "region":      str(row["Region"]),
                    "year":        int(row["Year"]),
                    "month":       int(row["Month"]),
                    "day":         int(row["Day"]),
                    "hour":        int(row["Hour"]),
                    "weekday":     str(row["Weekday"]),
                    "weekend":     bool(row["Weekend"]),
                    "peak_hour":   bool(row["Peak_Hour"]),
                }
                for _, row in chunk.iterrows()
            ]
            db.bulk_insert_mappings(EnergyConsumption, mappings)
            db.commit()
            total_inserted += len(mappings)
            print(f"  Inserted {total_inserted}/{len(df)} rows...")

        print(f"Database Loaded Successfully! Total rows inserted: {total_inserted}")

    except Exception as e:
        db.rollback()
        print(f"ERROR during insert: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_data()