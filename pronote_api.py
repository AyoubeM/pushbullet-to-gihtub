# pronote_api.py
import requests
import json

# Exemple simple pour parser les données depuis Pronote avec les cookies
# (en supposant que tu es déjà loggé avec Playwright et que les cookies sont valides)

def get_headers(cookies_dict):
    cookies = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    return {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://0930834b.index-education.net",
        "Referer": "https://0930834b.index-education.net/pronote/eleve.html"
    }

def call_polling(base_url, cookies):
    url = f"{base_url}/pronote/appelpolling/3/6947323/4ded5eb9e758f395ec16d3e5712b2708"
    headers = get_headers(cookies)
    data = {
        "session": 6947323,
        "numeroOrdre": "4ded5eb9e758f395ec16d3e5712b2708",
        "nom": "polling",
        "donneesSec": {}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.text

def get_notes(base_url, cookies):
    url = f"{base_url}/eleve.html#/notes"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_edt(base_url, cookies):
    url = f"{base_url}/eleve.html#/emploi-du-temps"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_devoirs(base_url, cookies):
    url = f"{base_url}/eleve.html#/travail-a-faire"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_absents(base_url, cookies):
    url = f"{base_url}/eleve.html#/absences"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_bulletin(base_url, cookies):
    url = f"{base_url}/eleve.html#/bulletin"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_messages(base_url, cookies):
    url = f"{base_url}/eleve.html#/messagerie"
    headers = get_headers(cookies)
    response = requests.get(url, headers=headers)
    return response.text[:500]

def get_polling(base_url, cookies):
    status_code, response_text = call_polling(base_url, cookies)
    return f"Statut: {status_code}\nRéponse:\n{response_text[:500]}"

def get_resume_semaine(base_url, cookies):
    notes = get_notes(base_url, cookies)
    edt = get_edt(base_url, cookies)
    devoirs = get_devoirs(base_url, cookies)
    absents = get_absents(base_url, cookies)
    return f"📌 Résumé de la semaine :\n\n📝 Notes :\n{notes[:200]}\n\n📅 Emploi du temps :\n{edt[:200]}\n\n📚 Devoirs :\n{devoirs[:200]}\n\n🚫 Absences :\n{absents[:200]}"

def get_all(base_url, cookies):
    return {
        "notes": get_notes(base_url, cookies),
        "edt": get_edt(base_url, cookies),
        "devoirs": get_devoirs(base_url, cookies),
        "absences": get_absents(base_url, cookies),
        "bulletin": get_bulletin(base_url, cookies),
        "messages": get_messages(base_url, cookies),
        "polling": get_polling(base_url, cookies),
        "resume": get_resume_semaine(base_url, cookies)
    }
