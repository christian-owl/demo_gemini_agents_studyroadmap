# ==========================================
# FUNZIONI DI SUPPORTO PER LA VALIDAZIONE DEL TESTO
# ==========================================

import requests
import json


class Validator:
    def __init__(self, text_to_validate: str):
        self.text_to_validate = text_to_validate
        self.problems = []

    def validate_length(self) -> bool:
        if len(self.text_to_validate.strip()) < 100:
            self.problems.append("Il testo è troppo corto")
            return False
        return True
    
    def validate_structure(self) -> bool:
        weird_sentences = ["non sono in grado", "non posso fornire", "come modello linguistico"]
        if any(f in self.text_to_validate.lower() for f in weird_sentences):
            self.problems.append("Il modello sembra aver rifiutato o evitato la domanda")
            return False
        return True

    def validate_ollama(self, wiki: str) -> dict:
        prompt = ("Confronta la spiegazione con le informazioni fornite in input " \
        "da Wikipedia se vanno in conflitto o contraddizione."
        "Rispondi SOLO in JSON con questo formato esatto: "
        '{"contraddizioni_trovate": true|false, "dettagli": "breve spiegazione"}\n\n'
        f"Testo 1 (spiegazione):\n{self.text_to_validate}\n\n"
        f"Testo 2 (fonte Wikipedia):\n{wiki}")

        try:
            response = requests.post(
            "http://localhost:11434/api/generate", #server locale dove gira Ollama
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "format": "json",  
            },
            timeout=60,
            )
            response.raise_for_status() #serve a sollevare un eventuale eccezione
            result = response.json()["response"] #estrae solo la risposta dal dizionario
            
            return json.loads(result) #converte la stringa JSON in un dizionario Python
        
        except requests.exceptions.RequestException as e:
            self.problems.append(f"Ollama non raggiungibile: {e}")
            return {"contraddizioni_trovate": None, "dettagli": "Validazione non eseguita (errore di rete/servizio)"}

        except (json.JSONDecodeError, KeyError) as e:
            self.problems.append(f"Risposta di Ollama non in formato JSON valido: {e}")
            return {"contraddizioni_trovate": None, "dettagli": "Validazione non eseguita (formato risposta inatteso)"}