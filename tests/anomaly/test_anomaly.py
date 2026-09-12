from types import SimpleNamespace

from backend.app.services.anomaly_service import detect_anomalies


class Query:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, condition):
        return self

    def all(self):
        return self.rows


class Session:
    def __init__(self, rows):
        self.rows = rows

    def query(self, model):
        return Query(self.rows)


def test_detect_anomalies_returns_threshold_and_matching_rows():
    rows = [
        SimpleNamespace(
            datetime="2026-09-12 01:00:00",
            region="North",
            consumption=60000,
        )
    ]

    result = detect_anomalies(Session(rows))

    assert result == {
        "threshold": 50000,
        "total_anomalies": 1,
        "anomalies": [
            {
                "datetime": "2026-09-12 01:00:00",
                "region": "North",
                "consumption": 60000,
            }
        ],
    }
