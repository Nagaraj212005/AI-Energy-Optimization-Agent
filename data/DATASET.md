# Dataset

The AI Energy Optimization Agent uses hourly electricity consumption data to support forecasting, anomaly detection, and energy-saving recommendations for the Cognizant Smart Energy Consumption Optimization use case.

The source data contains time-series consumption records for multiple energy regions. The raw regional files are consolidated into a single feature-enriched dataset used by the backend services and machine learning pipelines.

## Dataset Source

- **Source:** [Hourly Energy Consumption Dataset on Kaggle](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)
- **Format:** CSV
- **Time granularity:** Hourly
- **Coverage:** Multiple regional energy consumption series

## Repository Location

```text
data/
├── raw/
│   ├── AEP_hourly.csv
│   ├── COMED_hourly.csv
│   ├── DAYTON_hourly.csv
│   ├── DEOK_hourly.csv
│   ├── DOM_hourly.csv
│   ├── DUQ_hourly.csv
│   ├── EKPC_hourly.csv
│   ├── FE_hourly.csv
│   ├── NI_hourly.csv
│   ├── PJM_Load_hourly.csv
│   ├── PJME_hourly.csv
│   └── PJMW_hourly.csv
└── processed/
    └── processed_energy_data.csv
```

The project stores the original region-level files in `data/raw/` and the merged, processed dataset in `data/processed/processed_energy_data.csv`.

## Dataset Overview

| Field | Details |
| --- | --- |
| **Dataset name** | Hourly Energy Consumption Dataset |
| **Source** | [Kaggle](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) |
| **Format** | CSV |
| **Number of records** | 1,090,167 records in the current processed dataset |
| **Time granularity** | Hourly |
| **Target variable** | `Consumption` |
| **Regions** | Multiple regional consumption series |
| **Processed file** | `data/processed/processed_energy_data.csv` |

## Feature Description

| Column | Description | Type |
| --- | --- | --- |
| `Datetime` | Timestamp for the energy consumption observation | Datetime |
| `Consumption` | Recorded energy consumption and primary modeling target | Numeric |
| `Region` | Region identifier derived from the source filename | Categorical |
| `Year` | Calendar year extracted from `Datetime` | Integer |
| `Month` | Calendar month extracted from `Datetime` | Integer |
| `Day` | Day of the month extracted from `Datetime` | Integer |
| `Hour` | Hour of the day extracted from `Datetime` | Integer |
| `Weekday` | Day name derived from `Datetime` | Categorical |
| `Weekend` | Indicates whether the observation falls on Saturday or Sunday | Boolean |
| `Peak_Hour` | Indicates whether the observation falls between 17:00 and 21:00 | Boolean |

## Sample Dataset Preview

The following rows are taken from the processed dataset:

| Datetime | Consumption | Region | Year | Month | Day | Hour | Weekday | Weekend | Peak_Hour |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1998-04-01 01:00:00 | 22259.0 | PJM_Load | 1998 | 4 | 1 | 1 | Wednesday | False | False |
| 1998-04-01 02:00:00 | 21244.0 | PJM_Load | 1998 | 4 | 1 | 2 | Wednesday | False | False |
| 1998-04-01 03:00:00 | 20651.0 | PJM_Load | 1998 | 4 | 1 | 3 | Wednesday | False | False |
| 1998-04-01 04:00:00 | 20421.0 | PJM_Load | 1998 | 4 | 1 | 4 | Wednesday | False | False |
| 1998-04-01 05:00:00 | 20713.0 | PJM_Load | 1998 | 4 | 1 | 5 | Wednesday | False | False |

## Data Preprocessing

The preprocessing workflow is implemented in `backend/app/utils/data_preprocessing.py`.

### Missing value handling

Each regional CSV is read and validated before merging. Records are consolidated, duplicate rows are removed, and the resulting dataset is written to the processed data directory. Model-specific services also remove or handle invalid feature rows where required.

### Datetime conversion

The source timestamp column is converted to a pandas datetime value. The processed data is sorted chronologically, and calendar fields are derived from the converted timestamp.

### Feature engineering

The preprocessing pipeline creates the following time-based features:

- `Year`
- `Month`
- `Day`
- `Hour`
- `Weekday`
- `Weekend`
- `Peak_Hour`

The `Region` field is derived from each source filename, allowing multiple regional time series to be analyzed together.

### Scaling and normalization

Scaling is applied where required by the model:

- The anomaly detection pipeline uses `StandardScaler` before Isolation Forest inference.
- The recommendation pipeline uses `StandardScaler` and a region encoder.
- The forecasting pipeline uses the engineered numeric features directly because its tree-based model does not require feature scaling.

### Train/test split

The forecasting pipeline uses an ordered 80/20 split to preserve the time-series sequence. The recommendation pipeline uses an 80/20 randomized train/test split. The anomaly detection pipeline trains on the available feature matrix because it is an unsupervised model.

## Project Data Flow

```text
Raw regional CSV files
          |
          v
Data validation and cleaning
          |
          v
Datetime conversion and deduplication
          |
          v
Feature engineering
(Region, calendar, weekend, peak-hour features)
          |
          v
Processed dataset
(data/processed/processed_energy_data.csv)
          |
          v
Machine learning models
(forecasting, anomaly detection, recommendations)
          |
          v
FastAPI services and agent routes
          |
          v
React dashboard and AI assistant
```

## Processed Data Storage

Processed datasets are stored in:

```text
data/processed/
```

The primary generated file is:

```text
data/processed/processed_energy_data.csv
```

The backend loader uses this file to populate the local SQLite database, `energy.db`, which is then queried by the API services.

## Replacing the Dataset

The source data can be replaced with any compatible hourly energy consumption CSV. A replacement dataset should provide a timestamp column and a numeric consumption column for each regional series. If the column names or file layout differ, update the preprocessing mapping in `backend/app/utils/data_preprocessing.py` before rebuilding the processed dataset and retraining the models.
