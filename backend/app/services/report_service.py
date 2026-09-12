from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import EnergyConsumption


def generate_report(db: Session):

    total_records = db.query(EnergyConsumption).count()

    avg_consumption = (
        db.query(func.avg(EnergyConsumption.consumption))
        .scalar()
    )

    max_consumption = (
        db.query(func.max(EnergyConsumption.consumption))
        .scalar()
    )

    min_consumption = (
        db.query(func.min(EnergyConsumption.consumption))
        .scalar()
    )

    total_regions = (
        db.query(EnergyConsumption.region)
        .distinct()
        .count()
    )

    return {
        "report": {
            "total_records": total_records,
            "total_regions": total_regions,
            "average_consumption": round(avg_consumption, 2),
            "maximum_consumption": max_consumption,
            "minimum_consumption": min_consumption
        }
    }