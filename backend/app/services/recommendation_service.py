from sqlalchemy import desc

from backend.app.database.models import EnergyConsumption


def get_recommendations(db):

    latest = (
        db.query(EnergyConsumption)
        .order_by(desc(EnergyConsumption.datetime))
        .first()
    )

    if latest is None:
        return {
            "status": "error",
            "message": "No energy data found."
        }

    recommendations = []

    if latest.consumption > 15000:
        recommendations.append(
            "High energy consumption detected. Reduce usage during peak hours."
        )

    recommendations.append(
        "Turn off unused electrical equipment."
    )

    recommendations.append(
        "Use energy-efficient appliances."
    )

    recommendations.append(
        "Schedule heavy loads during off-peak hours."
    )

    recommendations.append(
        "Monitor daily consumption through the dashboard."
    )

    return {
        "status": "success",
        "recommendations": recommendations
    }