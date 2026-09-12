import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "anomalies.json")

def test_anomaly_api():
    client = app.test_client()
    response = client.get("/api/anomalies")

    assert response.status_code == 200

    data = response.get_json()

    assert "total_records" in data
    assert "total_anomalies" in data
    assert "anomalies" in data

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    assert os.path.exists(OUTPUT_FILE)