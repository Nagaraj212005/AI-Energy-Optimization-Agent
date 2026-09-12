from sqlalchemy.orm import Session
from app.database.models import EnergyConsumption


def detect_anomalies(db: Session):

    THRESHOLD = 50000

    anomalies = (
        db.query(EnergyConsumption)
        .filter(EnergyConsumption.consumption > THRESHOLD)
        .all()
    )

    results = []

    for row in anomalies[:100]:
        results.append({
            "datetime": row.datetime,
            "region": row.region,
            "consumption": row.consumption
        })

    return {
        "threshold": THRESHOLD,
        "total_anomalies": len(anomalies),
        "anomalies": results
    }