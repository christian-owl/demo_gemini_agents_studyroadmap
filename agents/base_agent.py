import time
from google import genai
from google.genai import types
from google.genai import errors

class BaseAgent:

    def __init__(self, client: genai.Client, model: str, prompt: str, tools: list = None):
        self.client = client
        self.model = model
        self.prompt = prompt
        self.tools = tools

    def run(self, content: str, max_retries: int = 3):
        # Try-Except usato per gestire eventuali errori di quota esaurita (RESOURCE_EXHAUSTED) durante la generazione del contenuto
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model = self.model,
                    contents = content,
                    config = types.GenerateContentConfig(
                        system_instruction = self.prompt,
                        tools = self.tools,
                    )
                )
                return response.text
            except errors.ClientError as e:
                if "RESOURCE_EXHAUSTED" in str(e) and attempt < max_retries - 1:
                    attesa = 60
                    print(f"Quota esaurita, attendo {attesa}s (tentativo {attempt + 1})...")
                    time.sleep(attesa)
                else:
                    raise #rilancia comunque l'errore 