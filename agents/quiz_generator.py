from agents.base_agent import BaseAgent
from tools.file_ops import edit, read

class QuizGeneratorAgent(BaseAgent):
    def __init__(self, client, model):
        super().__init__(
            client, model, 
            prompt = "Apri il file della lezione con il tool 'read' e genera un quiz con 5 domande a risposta multipla sull'argomento trattato. " \
                    "Assicurati che le domande siano pertinenti e coprano i punti chiave della lezione. Fornisci le risposte corrette per ogni domanda "
                    "e salva il quiz nel file di testo con il nome dell'argomento della lezione. Usa il tool 'edit' per salvare il quiz. Il file deve essere"
                    "lo stesso della lezione, quindi il nome del file è dato dall'input 'titolo'.",
            tools = [read, edit],
            )
        
    def generate_quiz(self, titolo: str) -> str:
        return self.run(titolo)