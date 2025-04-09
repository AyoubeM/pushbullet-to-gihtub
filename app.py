import requests
import time

PUSHBULLET_TOKEN = "o.z3B8iKoU0WlHUjMQVNMYSuhDhGzxNxIz"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1359585519918387242/t36r1WFh2Ik5ipxWtOW4f7Wxb2QXdv5CmqYX5MyG4v3mB6GTrqwCkSkMX6c1WdTPZ-fM"

headers = {
    "Access-Token": PUSHBULLET_TOKEN
}

def get_pushes():
    try:
        response = requests.get("https://api.pushbullet.com/v2/pushes?active=true", headers=headers)
        response.raise_for_status()
        return response.json().get("pushes", [])
    except Exception as e:
        print(f"Erreur lors de la récupération des pushes: {e}")
        return []

def send_to_discord(message):
    try:
        data = {
            "content": f"📲 Nouvelle notification Pushbullet: {message} <@825674203029962753>"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Erreur lors de l'envoi à Discord: {e}")

latest_time = 0

while True:
    pushes = get_pushes()
    for push in pushes:
        if push.get("created", 0) > latest_time:
            latest_time = push["created"]
            send_to_discord(push.get("body", "Pas de contenu"))
    time.sleep(10)
