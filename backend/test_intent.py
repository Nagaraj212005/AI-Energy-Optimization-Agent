from backend.app.agents.core.intent_classifier import classify_intent

questions = [

    "Show dashboard",

    "Predict tomorrow",

    "Any anomalies?",

    "Generate report",

    "Reduce electricity bill",

    "Compare today with yesterday",

    "Is system healthy?",

    "Hello"
]

for q in questions:

    print(q)

    print(classify_intent(q))

    print("-" * 40)