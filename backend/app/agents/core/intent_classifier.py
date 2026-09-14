from typing import Dict


INTENT_KEYWORDS = {
    "dashboard": [
        "dashboard",
        "summary",
        "overview",
        "status",
        "statistics",
        "stats"
    ],

    "forecast": [
        "forecast",
        "predict",
        "prediction",
        "future",
        "tomorrow",
        "next"
    ],

    "anomaly": [
        "anomaly",
        "abnormal",
        "issue",
        "problem",
        "spike",
        "outlier"
    ],


    "history": [
        "history",
        "previous",
        "past",
        "yesterday",
        "last week",
        "last month",
        "last year"
    ],

    "report": [
        "report",
        "generate report",
        "analysis"
    ],

    "optimization": [
    "optimize",
    "optimization",
    "recommend",
    "recommendation",
    "suggest",
    "advice",
    "tip",
    "save energy",
    "reduce energy",
    "reduce cost",
    "electricity bill",
    "cost"
],

    "comparison": [
        "compare",
        "difference",
        "versus",
        "vs"
    ],

    "summary": [
        "summarize",
        "summary of today",
        "today summary"
    ],

    "system_health": [
        "health",
        "healthy",
        "system status"
    ]
}


def classify_intent(question: str) -> Dict:

    question = question.lower()

    for intent, keywords in INTENT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in question:

                return {
                    "intent": intent,
                    "confidence": 0.95
                }

    return {
        "intent": "unknown",
        "confidence": 0.20
    }