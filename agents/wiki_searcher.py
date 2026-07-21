from agents.base_agent import BaseAgent
from tools.file_ops import edit
from tools.wikipedia_api import search_wikipedia

class WikiSearcherAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Fai una ricerca su Wikipedia usando il tool 'search_wikipedia' per trovare informazioni "
                    "pertinenti alla domanda dello studente dell'input 'domanda'. ",
            tools = [search_wikipedia],
            )
        
    def search(self, domanda: str, titolo: str) -> str:
        contenuto = f"Domanda: {domanda}\nTitolo lezione: {titolo}"
        return self.run(contenuto)
    
    def submit(self, titolo: str, risposta: str):
        contenuto = f"\n\nFonte: Wikipedia\n\n{risposta}"
        edit(titolo, contenuto) #edit a parte per evitare che l'IA faccia errori di scrittura