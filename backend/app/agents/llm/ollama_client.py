import ollama


from backend.app.agents.llm.system_prompt import SYSTEM_PROMPT

MODEL_NAME = "qwen2.5:7b"


def generate_response(user_question: str, tool_result: dict) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_question}

Tool Output:
{tool_result}

Generate a clear, concise, professional answer.
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
User Question:
{user_question}

Tool Output:
{tool_result}
"""
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"LLM Error: {e}"