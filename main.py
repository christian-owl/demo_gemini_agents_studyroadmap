import os
import re
from google import genai
from google.genai import types
import requests

# ==========================================
# 1. CREATE A CLIENT
# ==========================================
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model = "gemini-2.5-flash"

import time
from google.genai import errors

def generate_with_retry(max_retries=3, **kwargs):
    """
    This function attempts to generate content using the client, retrying up to max_retries times if a RESOURCE_EXHAUSTED error occurs.
    """
    for tentativo in range(max_retries):
        try:
            return client.models.generate_content(**kwargs)
        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) and tentativo < max_retries - 1:
                attesa = 60
                print(f"Quota esaurita, attendo {attesa}s (tentativo {tentativo + 1})...")
                time.sleep(attesa)
            else:
                raise

# ==========================================
# 2. PYTHON FUNCTION TO CALL
# ==========================================

def edit(titolo: str, contenuto: str):
    """
    This function edits the lesson content
    """
    contenuto = f"\n\n{contenuto}"
    with open(f"SRlessons/{titolo}.txt", "a") as file:
        file.write(contenuto)

def read(titolo: str):
    """
    This function reads the lesson content
    """
    with open(f"SRlessons/{titolo}.txt", "r") as file:
        return file.read()
    
def normalize(testo: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", testo.lower())[:50]

def search_wikipedia(argomento: str) -> str:
    """
    This function searches for information on Wikipedia
    This function uses the Wikipedia API
    """
    headers = {"User-Agent": "SRlessons-agent/1.0"} #evita blocco di Wikipedia (policy)

    search_url = "https://it.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": argomento,
        "format": "json",
        "srlimit": 1,
    }

    try:
        search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=10)
        search_resp.raise_for_status()
        risultati = search_resp.json().get("query", {}).get("search", [])

        if not risultati:
            return f"Nessuna pagina Wikipedia trovata per '{argomento}'"

        titolo_pagina = risultati[0]["title"]

        summary_url = f"https://it.wikipedia.org/api/rest_v1/page/summary/{titolo_pagina}"
        summary_resp = requests.get(summary_url, headers=headers, timeout=10)
        summary_resp.raise_for_status()
        dati = summary_resp.json()

        return dati.get("extract", "Nessun contenuto disponibile.")

    except requests.exceptions.RequestException as e:
        return f"Errore di rete durante la ricerca Wikipedia: {e}"

# ==========================================
# 3. AGENTS
# ==========================================

def teacherAgent(titolo: str, domanda: str) -> str:
    prompt= ("Rispondi alle domande degli studenti e fornisci spiegazioni dettagliate sullo specifico argomento. "
    "Quando hai finito di spiegare, usa il tool 'edit' per salvare la lezione in un file di testo. Il nome del file "
    "è dato dall'input 'titolo', la domanda a cui devi rispondere è l'input 'domanda'.")

    contenuto = f"Titolo lezione: {titolo}\n\nDomanda dello studente: {domanda}"
    
    response = generate_with_retry(
        model=model,
        contents=contenuto,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            tools=[edit],
        ),
    )
    return response.text

def quizGeneratorAgent(titolo: str) -> str:
    prompt = ("Apri il file della lezione con il tool 'read' e genera un quiz con 5 domande a risposta multipla sull'argomento trattato. " \
    "Assicurati che le domande siano pertinenti e coprano i punti chiave della lezione. Fornisci le risposte corrette per ogni domanda "
    "e salva il quiz nel file di testo con il nome dell'argomento della lezione. Usa il tool 'edit' per salvare il quiz. Il file deve essere"
    "lo stesso della lezione, quindi il nome del file è dato dall'input 'titolo'.")

    response = generate_with_retry(
        model=model,
        contents=titolo,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            tools=[read, edit],
        ),
    )
    return response.text
    
def searcherAgent(titolo: str, domanda: str) -> str:
    prompt = ("Fai una ricerca su Wikipedia usando il tool 'search_wikipedia' per trovare informazioni "
    "pertinenti alla domanda dello studente dell'input 'domanda'. Aggiungi le informazioni alla lezione usando il tool 'edit'."
    " Il nome del file della lezione è dato dall'input 'titolo'. Prima di inserire le informazioni trovate"
    "scrivi 'Fonte: Wikipedia' all'inizio del contenuto.")

    contenuto = f"Titolo lezione: {titolo}\n\nDomanda originale: {domanda}"

    response = generate_with_retry(
        model=model,
        contents=contenuto,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            tools=[search_wikipedia, edit],
        ),
    )
    return response.text

def normalizerAgent(domanda: str) -> str:
    prompt = ("Trasforma la domanda in un argomento di studio valido. Usa al massimo 3 parole.")
    response = generate_with_retry(
        model=model,
        contents=domanda,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
        ),
    )
    return normalize(response.text.strip())

# ==========================================
# 4. COORDINATOR
# ==========================================

def coordinator(domanda: str):
    # Create a folder named "SRlessons" if it doesn't exist
    if not os.path.exists("SRlessons"):
        os.makedirs("SRlessons")
    
    print(f"[Student] {domanda}\n")

    titolo = normalizerAgent(domanda)
    with open(f"SRlessons/{titolo}.txt", "w") as file:
        file.write(f"Lezione: {titolo}\n")

    time.sleep(15)
    spiegazione = teacherAgent(titolo, domanda)
    print(f"[Teacher] {spiegazione}\n")

    time.sleep(15)
    quiz = quizGeneratorAgent(titolo)
    print(f"[Quiz Generator] {quiz}\n")

    time.sleep(15)
    wiki = searcherAgent(titolo, domanda)
    print(f"[Searcher] {wiki}\n")


if __name__ == "__main__":
    coordinator("Spiegami cos'è la ricorsione in programmazione")