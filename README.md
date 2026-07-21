# SRlessons — Multi-Agent Learning Assistant

> ⚠️ **Work in progress.** Questo è un progetto personale sviluppato per esplorare pattern di orchestrazione multi-agente con LLM. È in fase attiva di sviluppo: architettura, funzionalità e documentazione possono cambiare frequentemente.

## Cosa fa

SRlessons è un sistema multi-agente che, a partire da una domanda in linguaggio naturale, genera automaticamente una lezione completa:

1. **Normalizza** l'argomento della domanda in un titolo pulito e utilizzabile come nome file (agente "Normalizer")
2. **Spiega** l'argomento in modo chiaro e dettagliato (agente "Teacher")
3. **Arricchisce** la lezione con informazioni verificate da Wikipedia (agente "Searcher")
4. **Genera un quiz** di verifica con 5 domande a risposta multipla (agente "Quiz Generator")
5. Salva tutto in un file di testo strutturato, pronto per essere riletto o riutilizzato

### Esempio

```
Input:  "Spiegami cos'è la ricorsione in programmazione"

Output: SRlessons/ricorsione_programmazione.txt
  ├── Spiegazione dettagliata dell'argomento
  ├── Approfondimento da Wikipedia (con fonte citata)
  └── Quiz di 5 domande a risposta multipla con soluzioni

```
### Perché questa struttura

- **Tool = funzioni pure**: `read`, `edit`, ricerca Wikipedia (usa le API ufficiali di Wikipedia)
- **Agenti = classi**: condividono comportamento comune tramite `BaseAgent`, ma ognuno personalizza prompt e tool disponibili
- **Coordinator = classe con stato**: mantiene le istanze degli agenti configurati e uno storico delle interazioni

## Stack tecnico

- **Python 3.x**
- **Google Gemini API** `gemini-2.5-flash` — free tier
- **Wikipedia REST API** chiamate dirette via `requests`

## Limiti noti

- Nessuna interfaccia utente: al momento è eseguibile solo da riga di comando
- Nessuna persistenza strutturata (le lezioni sono file `.txt`, non un database)
- Copertura di test parziale
- Gestione errori di rete verso Wikipedia ancora minimale
- Nessun controllo sulla qualità/pertinenza del quiz generato (nessun ciclo di revisione automatica)
