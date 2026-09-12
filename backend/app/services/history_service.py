from sqlalchemy.orm import Session
from backend.app.database.models import EnergyConsumption

def get_history(db: Session):

    rows = (
        db.query(EnergyConsumption)
        .order_by(EnergyConsumption.datetime.desc())
        .limit(100)
        .all()
    )

    data = []

    for row in rows:
        data.append({
            "datetime": row.datetime,
            "region": row.region,
            "consumption": row.consumption
        })

    return {
        "count": len(data),
        "history": data
    }