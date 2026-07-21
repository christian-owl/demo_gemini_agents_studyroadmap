# SRlessons — Multi-Agent Learning Assistant

> ⚠️ **Work in progress.** Questo è un progetto personale sviluppato per esplorare pattern di orchestrazione multi-agente con LLM. È in fase attiva di sviluppo: architettura, funzionalità e documentazione possono cambiare.

## Cosa fa

SRlessons è un sistema multi-agente che, a partire da una domanda in linguaggio naturale, genera automaticamente una lezione completa:

1. **Normalizza** l'argomento della domanda in un titolo pulito e utilizzabile come nome file (agente "Normalizer")
2. **Spiega** l'argomento in modo chiaro e dettagliato (agente "Teacher")
3. **Arricchisce** la lezione con informazioni verificate da Wikipedia (agente "Searcher")
4. **Valida** il contenuto confrontandolo con una fonte sicura (classe 'Validator')
5. **Genera un quiz** di verifica con 5 domande a risposta multipla (agente "Quiz Generator")
6. Salva tutto in un file di testo strutturato, pronto per essere riletto o riutilizzato

### Esempio

```
Input:  "Spiegami cos'è la ricorsione in programmazione"

Output: SRlessons/ricorsione_programmazione.txt
  ├── Spiegazione dettagliata dell'argomento
  ├── Approfondimento da Wikipedia
  └── Quiz di 5 domande a risposta multipla con soluzioni

```
### Perché questa struttura

- **Tool = funzioni pure**: `read`, `edit`, ricerca Wikipedia (usa le API ufficiali di Wikipedia)
- **Agenti = classi**: condividono comportamento comune tramite `BaseAgent`, ma ognuno personalizza prompt e tool disponibili
- **Validator = classe con stato dei problemi**: funzioni di validazione della struttura e dei contenuti del testo generato
- **Coordinator = classe con stato**: mantiene le istanze degli agenti configurati e uno storico delle interazioni

## Stack tecnico

- **Python 3.x**
- **Google Gemini API** `gemini-2.5-flash` — free tier
- **llama3.2** locale
- **Wikipedia REST API**

## Validazione
Le lezioni generate dal Teacher passano attraverso un livello di validazione prima di essere salvate. L'obiettivo non è certificare la "verità assoluta" del contenuto ma applicare controlli complementari che aumentano la fiducia nel risultato:

- Validazione strutturale: controlli deterministici e istantanei — lunghezza minima del testo, rilevamento di risposte in cui il modello ha rifiutato o evitato la domanda.
- Validazione di coerenza con fonte esterna (ollama): la spiegazione generata viene confrontata con l'estratto Wikipedia, per rilevare eventuali contraddizioni evidenti tra le due fonti. Non verifica "la verità", ma la coerenza tra fonti indipendenti.

## Perché Ollama?
- **Separazione dei ruoli**: usare un modello diverso da quello che ha generato il contenuto riduce il rischio che lo stesso modello sia "sistematicamente sicuro" dei propri errori nel validare se stesso.
- **Nessun costo o rate limit aggiuntivo**: Ollama gira interamente in locale, senza API key né limiti di quota.

## Limiti noti

- Nessuna interfaccia utente: al momento è eseguibile solo da riga di comando
- Nessuna persistenza strutturata (le lezioni sono file `.txt`, non un database)
- Copertura di test parziale
- Gestione errori di rete verso Wikipedia ancora minimale
