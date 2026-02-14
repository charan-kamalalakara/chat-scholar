import requests


class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def generate_response(self, chat_history, document_chunks=None):

        # -----------------------------
        # Get latest user question
        # -----------------------------
        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        # -----------------------------
        # Build prompt
        # -----------------------------
        if document_chunks:

            context = "\n\n".join(document_chunks)

            prompt = f"""
You are an AI assistant answering questions using document context.

Use ONLY the information from the context.
If the answer is not present, say:
"I could not find this information in the document."

Context:
{context}

Question: {latest_question}

Answer:
"""

        else:
            prompt = f"""
Answer the following question clearly and briefly.

Question: {latest_question}
Answer:
"""

        # -----------------------------
        # Call Ollama
        # -----------------------------
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 180
                }
            }

            response = requests.post(self.url, json=payload)

            if response.status_code == 200:
                reply = response.json()["response"].strip()

                if not reply:
                    return "I couldn't find an answer."

                return reply

            return "⚠️ Ollama error."

        except Exception as e:
            print("Ollama Error:", e)
            return "⚠️ Ollama server not running."
