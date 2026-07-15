from core.coordinator import Coordinator
from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
import os

if __name__ == "__main__":
    if not os.path.exists("SRlessons"):
        os.makedirs("SRlessons")

    client = genai.Client(api_key=GEMINI_API_KEY)
    coordinator = Coordinator(client=client, model=MODEL_NAME)
    domanda = "Parlami del teorema di Pitagora"
    risultato = coordinator.coordinate(domanda)
    
    print(risultato)