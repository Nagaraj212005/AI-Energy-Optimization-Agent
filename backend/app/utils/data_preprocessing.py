from pathlib import Path
import pandas as pd
import os

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DATA_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_PATH / "processed_energy_data.csv"

all_data = []

print("=" * 60)
print("Starting Data Preprocessing...")
print("=" * 60)

# ---------------------------------------------------
# Read every CSV
# ---------------------------------------------------

for file in os.listdir(RAW_DATA_PATH):

    # Ignore parquet files
    if not file.endswith(".csv"):
        print(f"Skipping {file}")
        continue

    file_path = RAW_DATA_PATH / file

    df = pd.read_csv(file_path)

    print(f"\nReading {file}")
    print(f"Columns : {len(df.columns)}")

    # Skip files that don't have exactly 2 columns
    if len(df.columns) != 2:
        print(f"Skipped {file} (Unexpected format)")
        continue

    region = file.replace("_hourly.csv", "").replace(".csv", "")

    df.columns = ["Datetime", "Consumption"]

    df["Region"] = region

    all_data.append(df)

# ---------------------------------------------------
# Merge
# ---------------------------------------------------

merged_df = pd.concat(all_data, ignore_index=True)

# Convert Datetime
merged_df["Datetime"] = pd.to_datetime(merged_df["Datetime"])

# Sort
merged_df = merged_df.sort_values("Datetime")

# Remove duplicates
merged_df = merged_df.drop_duplicates()

# Reset Index
merged_df.reset_index(drop=True, inplace=True)

# ---------------------------------------------------
# Feature Engineering
# ---------------------------------------------------

merged_df["Year"] = merged_df["Datetime"].dt.year
merged_df["Month"] = merged_df["Datetime"].dt.month
merged_df["Day"] = merged_df["Datetime"].dt.day
merged_df["Hour"] = merged_df["Datetime"].dt.hour
merged_df["Weekday"] = merged_df["Datetime"].dt.day_name()

merged_df["Weekend"] = merged_df["Weekday"].isin(
    ["Saturday", "Sunday"]
)

# Peak Hour
merged_df["Peak_Hour"] = merged_df["Hour"].between(17, 21)

# ---------------------------------------------------
# Save
# ---------------------------------------------------

merged_df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)

print(f"Rows : {len(merged_df)}")
print(f"Columns : {len(merged_df.columns)}")

print("\nColumns")

print(merged_df.columns.tolist())

print(f"\nSaved To : {OUTPUT_FILE}")