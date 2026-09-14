"""
Simple Conversation Manager

Stores recent conversation context so the AI Agent
can understand follow-up questions.
"""


class ConversationMemory:

    def __init__(self):
        self.last_intent = None
        self.last_question = None
        self.history = []

    def update(self, question, intent):
        self.last_question = question
        self.last_intent = intent

        self.history.append({
            "question": question,
            "intent": intent
        })

        # Keep only last 10 interactions
        if len(self.history) > 10:
            self.history.pop(0)

    def get_last_intent(self):
        return self.last_intent

    def get_history(self):
        return self.history

    def clear(self):
        self.last_question = None
        self.last_intent = None
        self.history.clear()


conversation = ConversationMemory()