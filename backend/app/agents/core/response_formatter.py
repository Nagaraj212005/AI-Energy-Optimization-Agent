def format_response(intent, results):

    # ---------------- Dashboard ----------------
    if intent == "dashboard":

        dashboard = results.get("dashboard", {})

        return {
            "type": "dashboard",
            "message": "Here is the latest dashboard summary.",
            "data": dashboard
        }

    # ---------------- Forecast ----------------
    elif intent == "forecast":

        forecast = results.get("forecast", {})

        return {
            "type": "forecast",
            "message": "Forecast generated successfully.",
            "data": forecast
        }

    # ---------------- History ----------------
    elif intent == "history":

        history = results.get("history", {})

        return {
            "type": "history",
            "message": "Here is the recent energy consumption history.",
            "data": history
        }

    # ---------------- Optimization ----------------
    elif intent == "optimization":

        dashboard = results.get("dashboard", {})
        forecast = results.get("forecast", {})

        recommendations = [
            "Turn off unused electrical equipment.",
            "Shift heavy loads to off-peak hours.",
            "Use energy-efficient appliances.",
            "Monitor daily consumption."
        ]

        return {
            "type": "optimization",
            "message": "Optimization analysis completed.",
            "dashboard": dashboard,
            "forecast": forecast,
            "recommendations": recommendations
        }

    # ---------------- Recommendation ----------------
    elif intent == "recommendation":

        recommendations = results.get("recommendation", {})

        return {
            "type": "recommendation",
            "message": "Here are your energy-saving recommendations.",
            "data": recommendations
        }

    # ---------------- Anomaly ----------------
    elif intent == "anomaly":

        anomalies = results.get("anomaly", {})

        return {
            "type": "anomaly",
            "message": "Anomaly detection completed.",
            "data": anomalies
        }

    # ---------------- Report ----------------
    elif intent == "report":

        report = results.get("report", {})

        return {
            "type": "report",
            "message": "Report generated successfully.",
            "data": report
        }

    # ---------------- System Health ----------------
    elif intent == "system_health":

        health = results.get("system_health", {})

        return {
            "type": "system",
            "message": "System is healthy.",
            "data": health
        }

    # ---------------- Unknown ----------------
    return {
        "type": "unknown",
        "message": "Sorry, I couldn't understand your request.",
        "data": {}
    }