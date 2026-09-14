from backend.app.database.database import SessionLocal
from backend.app.database.models import EnergyConsumption


def run_history(limit=10):
    db = SessionLocal()

    try:
        records = (
            db.query(EnergyConsumption)
            .order_by(EnergyConsumption.datetime.desc())
            .limit(limit)
            .all()
        )

        history = []

        for record in records:
            history.append({
                "datetime": record.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "consumption": round(record.consumption, 2),
                "region": record.region
            })

        return {
            "status": "success",
            "history": history
        }

    finally:
        db.close()