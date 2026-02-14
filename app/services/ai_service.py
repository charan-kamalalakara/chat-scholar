import requests

class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def generate_response(self, chat_history, document_text=None):

        # get latest user question
        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        # limit document size (tiny models can't handle huge text)
        if document_text:
            document_text = document_text[:3000]

            prompt = f"""
Use the following document to answer the question.

Document:
{document_text}

Question: {latest_question}
Answer using only the document information:
"""
        else:
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
                    "num_predict": 150
                }
            }

            response = requests.post(self.url, json=payload)

            if response.status_code == 200:
                reply = response.json()["response"].strip()

                if not reply:
                    return "I couldn't find an answer in the document."

                return reply

            return "⚠️ Ollama error."

        except Exception as e:
            print("Ollama Error:", e)
            return "⚠️ Ollama server not running."
