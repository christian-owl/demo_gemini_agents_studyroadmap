from agents.base_agent import BaseAgent
from tools.file_ops import edit

class TeacherAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Rispondi alla domanda e fornisci spiegazioni dettagliate sullo specifico argomento. "
                        "Comportati come un insegnante esperto e dai per scontato che lo studente non abbia" \
                        "conoscenze pregresse sull'argomento. ",
            tools = [],
            )
        
    def teach(self, titolo: str, domanda: str) -> str:
        contenuto = f"Titolo lezione: {titolo}\n\nDomanda dello studente: {domanda}"
        response = self.run(contenuto)
        
        return response
    
    def submit(self, titolo: str, risposta: str):
        edit(titolo, risposta) #edit a parte per evitare che l'IA faccia errori di scrittura