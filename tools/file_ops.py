import re

# ==========================================
# FUNZIONI DI SUPPORTO PER LA GESTIONE DEI FILE
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
