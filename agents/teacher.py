from agents.base_agent import BaseAgent
from tools.file_ops import edit

class TeacherAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Rispondi alle domande degli studenti e fornisci spiegazioni dettagliate sullo specifico argomento. "
                        "Quando hai finito di spiegare, usa il tool 'edit' per salvare la lezione in un file di testo. Il nome del file "
                        "è dato dall'input 'titolo', la domanda a cui devi rispondere è l'input 'domanda'.",
            tools = [edit],
            )
        
    def teach(self, titolo: str, domanda: str) -> str:
        contenuto = f"Titolo lezione: {titolo}\n\nDomanda dello studente: {domanda}"
        return self.run(contenuto)