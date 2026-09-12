from sqlalchemy.orm import Session

from backend.app.services.dashboard_service import get_dashboard_summary
from backend.app.services.forecast_service import get_next_24_hour_forecast
from backend.app.services.anomaly_service import detect_anomalies
from backend.app.services.recommendation_service import detect_recommendations
from backend.app.services.report_service import generate_report
from backend.app.services.history_service import get_history


def ask_agent(question: str, db: Session):

    question = question.lower().strip()

    # Dashboard
    if "dashboard" in question or "summary" in question:
        return {
            "module": "Dashboard",
            "data": get_dashboard_summary(db)
        }

    # Forecast
    elif "forecast" in question or "predict" in question:
        return {
            "module": "Forecast",
            "data": get_next_24_hour_forecast()
        }

    # Anomaly Detection
    elif "anomaly" in question or "outlier" in question:
        return {
            "module": "Anomaly Detection",
            "data": detect_anomalies()
        }

    # Recommendation
    elif (
        "recommend" in question
        or "optimization" in question
        or "save energy" in question
    ):
        return {
            "module": "Recommendation",
            "data": detect_recommendations(db)
        }

    # Report
    elif "report" in question:
        return {
            "module": "Report",
            "data": generate_report(db)
        }

    # History
    elif "history" in question:
        return {
            "module": "History",
            "data": get_history(db)
        }

    # Help
    else:
        return {
            "message": "AI Energy Optimization Assistant",
            "supported_queries": [
                "dashboard",
                "forecast",
                "anomaly",
                "recommendation",
                "report",
                "history"
            ],
            "example_questions": [
                "Show dashboard summary",
                "Forecast next 24 hours",
                "Detect anomalies",
                "Give recommendations",
                "Generate report",
                "Show history"
            ]
        }