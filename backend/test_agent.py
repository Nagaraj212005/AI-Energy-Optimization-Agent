from backend.app.agents.energy_agent import agent

print("=" * 60)
print("        AI Energy Optimization Agent")
print("=" * 60)
print("Type 'exit' to quit.\n")

while True:

    question = input("You : ")

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    result = agent(question)

    print("\nAI :")
    print(result["ai_response"])
    print("-" * 60)