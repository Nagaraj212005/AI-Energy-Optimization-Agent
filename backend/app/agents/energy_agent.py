from backend.app.agents.core.intent_classifier import classify_intent
from backend.app.agents.core.reasoning_engine import reason
from backend.app.agents.core.response_formatter import format_response
from backend.app.agents.core.conversation_memory import conversation
from backend.app.agents.llm.ollama_client import generate_response

class EnergyAgent:

    def run(self, question):

        # Step 1: Intent Classification
        intent_data = classify_intent(question)
        intent = intent_data["intent"]
        confidence = intent_data["confidence"]

        # Step 2: Save Conversation
        conversation.update(question, intent)

        # Step 3: Build Execution Plan
        reasoning = reason(intent, question)

        plan = reasoning["plan"]
        results = reasoning["results"]

        # Step 4: Format Response
        response = format_response(intent, results)


        ai_response = generate_response(
            question,
            response
    )
        # Step 5: Final Output
        return {
            "question": question,
            "intent": intent,
            "confidence": confidence,
            "plan": plan,
            "response": response,
            "ai_response": ai_response
        }


# Global Agent Instance
agent = EnergyAgent()


# Compatibility Function
def ask_agent(question):
    return agent.run(question)