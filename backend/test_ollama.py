from backend.app.agents.llm.ollama_client import generate_response

tool_result = {
    "status": "success",
    "recommendations": [
        "Turn off unused lights",
        "Run heavy appliances during off-peak hours"
    ]
}

response = generate_response(
    "Give me optimization suggestions",
    tool_result
)

print(response)