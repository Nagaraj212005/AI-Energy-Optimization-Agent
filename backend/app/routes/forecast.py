from fastapi import APIRouter

from app.services.forecast_service import get_next_24_hour_forecast

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.get("/next24hours")
def forecast():

    return get_next_24_hour_forecast()