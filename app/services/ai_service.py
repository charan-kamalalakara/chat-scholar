import requests

class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def generate_response(self, chat_history):

        # Get latest user message only
        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        # SIMPLE prompt (best for tiny models)
        prompt = f"""
Answer the following question clearly and briefly.

Question: {latest_question}
Answer:
"""

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 120
                }
            }

            response = requests.post(self.url, json=payload)

            if response.status_code == 200:
                reply = response.json()["response"].strip()

                if not reply:
                    return "Please ask your question again."

                return reply

            return "⚠️ Ollama error."

        except Exception as e:
            print("Ollama Error:", e)
            return "⚠️ Ollama server not running."
