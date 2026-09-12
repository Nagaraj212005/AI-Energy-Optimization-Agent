from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database.models import EnergyConsumption


def generate_report(db: Session):

    total_records = db.query(EnergyConsumption).count()

    avg_consumption = db.query(
        func.avg(EnergyConsumption.consumption)
    ).scalar()

    max_consumption = db.query(
        func.max(EnergyConsumption.consumption)
    ).scalar()

    min_consumption = db.query(
        func.min(EnergyConsumption.consumption)
    ).scalar()

    total_regions = db.query(
        EnergyConsumption.region
    ).distinct().count()

    peak_hour_records = db.query(
        EnergyConsumption
    ).filter(
        EnergyConsumption.peak_hour == True
    ).count()

    weekend_records = db.query(
        EnergyConsumption
    ).filter(
        EnergyConsumption.weekend == True
    ).count()

    latest_record = db.query(
        EnergyConsumption
    ).order_by(
        EnergyConsumption.datetime.desc()
    ).first()

    return {
        "report": {
            "total_records": total_records,
            "total_regions": total_regions,
            "average_consumption": round(avg_consumption, 2),
            "maximum_consumption": max_consumption,
            "minimum_consumption": min_consumption,
            "peak_hour_records": peak_hour_records,
            "weekend_records": weekend_records,
            "latest_datetime": str(latest_record.datetime) if latest_record else None,
            "generated_by": "AI Energy Optimization Agent",
            "status": "Success"
        }
    }