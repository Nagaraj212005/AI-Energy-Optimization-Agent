from fastapi import APIRouter
from backend.app.services.forecast_service import get_next_24_hour_forecast

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

@router.get("/")
def forecast():
    return get_next_24_hour_forecast()