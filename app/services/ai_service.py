import requests
import json


class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    # ---------------------------------------------------
    # NORMAL RESPONSE (used for non-stream fallback)
    # ---------------------------------------------------
    def generate_response(self, chat_history, document_chunks=None):

        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        source_info = ""

        if document_chunks:
            context_text = "\n\n".join(
                [chunk["text"] for chunk in document_chunks]
            )

            sources = list(set(
                [chunk["source"] for chunk in document_chunks]
            ))

            source_info = ", ".join(sources)

            prompt = f"""
You are an academic AI assistant.

Use ONLY the provided context to answer.
If answer not present, say you cannot find it.

Context:
{context_text}

Question: {latest_question}

Answer:
"""
        else:
            prompt = f"Question: {latest_question}\nAnswer:"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=payload)

        reply = response.json()["response"].strip()

        if source_info:
            reply += f"\n\n📄 Source: {source_info}"

        return reply

    # ---------------------------------------------------
    # STREAMING RESPONSE (NEW)
    # ---------------------------------------------------
    def stream_response(self, chat_history, document_chunks=None):

        latest_question = ""

        for msg in reversed(chat_history):
            if msg["role"] == "user":
                latest_question = msg["content"]
                break

        source_info = ""

        if document_chunks:
            context_text = "\n\n".join(
                [chunk["text"] for chunk in document_chunks]
            )

            sources = list(set(
                [chunk["source"] for chunk in document_chunks]
            ))

            source_info = ", ".join(sources)

            prompt = f"""
You are an academic AI assistant.

Use ONLY the provided context.

Context:
{context_text}

Question: {latest_question}

Answer:
"""
        else:
            prompt = f"Question: {latest_question}\nAnswer:"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        response = requests.post(
            self.url,
            json=payload,
            stream=True
        )

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    yield data.get("response", "")
                except:
                    continue

        if source_info:
            yield f"\n\n📄 Source: {source_info}"
