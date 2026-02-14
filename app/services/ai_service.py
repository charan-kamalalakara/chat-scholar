import requests

class AIService:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "tinyllama"

    def generate_response(self, prompt):
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(self.url, json=payload)

            if response.status_code == 200:
                return response.json()["response"]

            return "⚠️ Ollama returned an error."

        except Exception as e:
            print("Ollama Error:", e)
            return "⚠️ Ollama server not running."
