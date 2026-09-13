from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database.models import EnergyConsumption

ELECTRICITY_RATE = 8.0


def get_dashboard_summary(db: Session):

    total_consumption = db.query(
        func.sum(EnergyConsumption.consumption)
    ).scalar()

    average_consumption = db.query(
        func.avg(EnergyConsumption.consumption)
    ).scalar()

    peak_consumption = db.query(
        func.max(EnergyConsumption.consumption)
    ).scalar()

    total_records = db.query(
        EnergyConsumption
    ).count()

    estimated_cost = (total_consumption or 0) * ELECTRICITY_RATE

    return {
        "total_consumption": round(total_consumption or 0, 2),
        "average_consumption": round(average_consumption or 0, 2),
        "peak_consumption": round(peak_consumption or 0, 2),
        "total_records": total_records,
        "estimated_cost": round(estimated_cost, 2)
    }


def get_dashboard(db: Session):
    return get_dashboard_summary(db)