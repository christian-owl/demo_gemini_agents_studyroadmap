import requests

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
