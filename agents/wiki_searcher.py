from agents.base_agent import BaseAgent
from tools.file_ops import edit
from tools.wikipedia_api import search_wikipedia

class WikiSearcherAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Fai una ricerca su Wikipedia usando il tool 'search_wikipedia' per trovare informazioni "
                    "pertinenti alla domanda dello studente dell'input 'domanda'. Aggiungi le informazioni alla lezione usando il tool 'edit'."
                    " Il nome del file della lezione è dato dall'input 'titolo'. Prima di inserire le informazioni trovate"
                    "scrivi 'Fonte: Wikipedia' all'inizio del contenuto.",
            tools = [edit, search_wikipedia],
            )
        
    def search(self, domanda: str, titolo: str) -> str:
        contenuto = f"Domanda: {domanda}\nTitolo lezione: {titolo}"
        return self.run(contenuto)