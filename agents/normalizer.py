from agents.base_agent import BaseAgent
from tools.file_ops import normalize

class NormalizerAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Trasforma la domanda in un argomento di studio valido. Usa al massimo 3 parole.",
            tools = [],
            )
        
    def normalize_content(self, domanda: str) -> str:
        response = self.run(domanda)
        return normalize(response.strip())