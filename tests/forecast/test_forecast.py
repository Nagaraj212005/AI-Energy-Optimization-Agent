from datetime import datetime

from backend.app.services.forecast_service import get_next_24_hour_forecast


def test_get_next_24_hour_forecast_returns_24_records():
    result = get_next_24_hour_forecast()

    assert len(result["forecast"]) == 24
    assert all(
        {"datetime", "predicted_consumption"} <= record.keys()
        for record in result["forecast"]
    )
    assert all(
        isinstance(datetime.strptime(record["datetime"], "%Y-%m-%d %H:%M:%S"), datetime)
        for record in result["forecast"]
    )
    assert all(
        isinstance(record["predicted_consumption"], float)
        for record in result["forecast"]
    )
