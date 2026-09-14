from backend.app.services.forecast_service import get_next_24_hour_forecast


def run_forecast():
    """
    Forecast Tool

    Returns the next 24-hour energy consumption forecast.
    """

    try:
        result = get_next_24_hour_forecast()

        return {
            "status": "success",
            "forecast": result["forecast"]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }