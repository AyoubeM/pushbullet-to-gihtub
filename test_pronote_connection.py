import requests

# Met ici l'URL exacte de base (sans /eleve.html) fournie par l'ENT
BASE_URL = "https://0930834b.index-education.net/pronote"

# Colle ici les cookies récupérés depuis Playwright
cookies_dict = {
    "AUTH_SESSION_ID": "632a2b0c-0283-4746-aec4-83a5c5d2cd52",
    "KEYCLOAK_IDENTITY": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjMT...",
    "TGC": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImVlNDQwNGY...",
    "CASTJU_902BA3CDA1883801594B6E1B452790CC53948FDA": "akzKK2qT9qMkr6E2",
    "DISSESSIONAuthnDelegation": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjM0...",
    # Tu peux ajouter les autres cookies si besoin
}

def get_headers(cookies):
    cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    return {
        "Cookie": cookies_str,
        "User-Agent": "Mozilla/5.0"
    }

def test_url(path):
    url = f"{BASE_URL}/eleve.html#{path}"
    print(f"🔍 Test de l'accès à : {url}")
    try:
        response = requests.get(url, headers=get_headers(cookies_dict))
        print(f"✅ Statut HTTP : {response.status_code}")
        print(response.text[:500])  # Juste un aperçu
    except Exception as e:
        print(f"❌ Erreur lors de l'accès : {e}")

if __name__ == "__main__":
    print("🔎 Tentative d'accès à Pronote...")

    test_url("/notes")
    test_url("/emploi-du-temps")
    test_url("/travail-a-faire")
    test_url("/absences")
