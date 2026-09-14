from backend.app.agents.tools.dashboard_tool import run_dashboard
from backend.app.agents.tools.forecast_tool import run_forecast
from backend.app.agents.tools.history_tool import run_history
from backend.app.agents.tools.recommendation_tool import run_recommendation
from backend.app.agents.tools.anomaly_tool import run_anomaly



def execute_tool(intent):

    if intent == "dashboard":
        return run_dashboard()

    elif intent == "forecast":
        return run_forecast()

    elif intent == "anomaly":
        return run_anomaly()

    elif intent == "history":
        return run_history()

    elif intent == "report":
        return {"message": "Report generation coming soon"}

    elif intent == "optimization":
        return run_recommendation()

    elif intent == "comparison":
        return {"message": "Comparison feature coming soon"}

    elif intent == "summary":
        return {"message": "Summary feature coming soon"}

    elif intent == "system_health":
        return {"status": "Healthy"}

    else:
        return {"message": "Sorry, I don't understand."}