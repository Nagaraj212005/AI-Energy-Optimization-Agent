from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database.models import EnergyConsumption


def ai_agent_summary(db: Session):

    total_records = db.query(EnergyConsumption).count()

    avg_consumption = (
        db.query(func.avg(EnergyConsumption.consumption))
        .scalar()
    )

    max_consumption = (
        db.query(func.max(EnergyConsumption.consumption))
        .scalar()
    )

    recommendations = []

    if avg_consumption > 45000:
        recommendations.append(
            "Average energy consumption is high. Shift loads to off-peak hours."
        )

    if max_consumption > 50000:
        recommendations.append(
            "Peak demand detected. Enable demand response strategy."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Energy usage appears normal."
        )

    return {
        "agent": "AI Energy Optimization Agent",
        "total_records": total_records,
        "average_consumption": round(avg_consumption, 2),
        "maximum_consumption": max_consumption,
        "recommendations": recommendations
    }