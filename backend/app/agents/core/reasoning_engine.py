"""
Reasoning Engine

This module decides:

1. Which tools are required
2. Whether multiple tools are needed
3. In what order they should run
"""

from backend.app.agents.core.tool_router import execute_tool


def reason(intent, question):
    """
    Returns execution plan and collected results.
    """

    # ---------- Dashboard ----------
    if intent == "dashboard":
        dashboard = execute_tool("dashboard")

        return {
            "plan": ["dashboard"],
            "results": {
                "dashboard": dashboard
            }
        }

    # ---------- Forecast ----------
    elif intent == "forecast":
        forecast = execute_tool("forecast")

        return {
            "plan": ["forecast"],
            "results": {
                "forecast": forecast
            }
        }

    # ---------- History ----------
    elif intent == "history":
        history = execute_tool("history")

        return {
            "plan": ["history"],
            "results": {
                "history": history
            }
        }

    # ---------- Optimization ----------
    elif intent == "optimization":

        dashboard = execute_tool("dashboard")
        forecast = execute_tool("forecast")

        return {
            "plan": [
                "dashboard",
                "forecast"
            ],
            "results": {
                "dashboard": dashboard,
                "forecast": forecast
            }
        }

    # ---------- System ----------
    elif intent == "system_health":

        health = execute_tool("system_health")

        return {
            "plan": ["system_health"],
            "results": {
                "system_health": health
            }
        }


    elif intent == "anomaly":

        anomaly = execute_tool("anomaly")

        return {
            "plan": ["anomaly"],
            "results": {
                "anomaly": anomaly
            }
    }

    # ---------- Unknown ----------
    return {
        "plan": [],
        "results": {}
    }