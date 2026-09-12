from sqlalchemy.orm import Session
from app.database.models import EnergyConsumption


def generate_recommendations(db: Session):

    rows = db.query(EnergyConsumption).limit(10).all()

    print("\n========== SAMPLE DATA ==========")
    for row in rows:
        print(f"Region: {row.region} | Consumption: {row.consumption}")
    print("=================================\n")

    recommendations = []

    rows = db.query(EnergyConsumption).all()

    for row in rows:

        if row.consumption > 50000:
            recommendations.append({
                "priority": "High",
                "region": row.region,
                "issue": "Very high energy consumption",
                "recommendation": "Reduce industrial load during peak hours."
            })

        elif row.consumption > 45000:
            recommendations.append({
                "priority": "Medium",
                "region": row.region,
                "issue": "High energy demand",
                "recommendation": "Shift non-critical loads to off-peak hours."
            })

        elif row.consumption < 15000:
            recommendations.append({
                "priority": "Low",
                "region": row.region,
                "issue": "Low energy utilization",
                "recommendation": "Store excess energy or charge batteries."
            })

    return {
        "total_recommendations": len(recommendations),
        "recommendations": recommendations[:100]
    }