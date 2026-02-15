import requests


class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def generate_response(self, chat_history, document_chunks=None):

        # ---------------------------------
        # Get latest user question
        # ---------------------------------
        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        # ---------------------------------
        # Build prompt (RAG + Citation)
        # ---------------------------------
        source_info = ""

        if document_chunks:

            # Combine retrieved chunk texts
            context_text = "\n\n".join(
                [chunk["text"] for chunk in document_chunks]
            )

            # Collect unique sources
            sources = list(set(
                [chunk["source"] for chunk in document_chunks]
            ))

            source_info = ", ".join(sources)

            prompt = f"""
You are an AI assistant answering questions using document context.

Use ONLY the information from the provided context.
If the answer is not present, say:
"I could not find this information in the document."

Context:
{context_text}

Question: {latest_question}

Answer:
"""

        else:
            prompt = f"""
Answer the following question clearly and briefly.

Question: {latest_question}
Answer:
"""

        # ---------------------------------
        # Call Ollama
        # ---------------------------------
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

                # Add citation if document used
                if source_info:
                    reply += f"\n\n📄 Source: {source_info}"

                return reply

            return "⚠️ Ollama error."

        except Exception as e:
            print("Ollama Error:", e)
            return "⚠️ Ollama server not running."
