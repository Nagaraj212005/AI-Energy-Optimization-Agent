from datetime import datetime, timedelta
import random


def get_next_24_hour_forecast():

    forecast = []

    current_time = datetime.now()

    for i in range(24):

        forecast.append({
            "datetime": (current_time + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "predicted_consumption": round(random.uniform(18000, 35000), 2)
        })

    return {
        "forecast": forecast
    }