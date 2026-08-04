import os
import requests
import json

API_URL = "https://api.voyalcine.net/films/5875/tree/3250"

TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]

STATE = "state.json"

data = requests.get(API_URL, timeout=20).json()

# Guardamos todo lo que tenga horarios disponibles
content = json.dumps(data, ensure_ascii=False)

try:
    with open(STATE, "r") as f:
        old = json.load(f)
except:
    old = ""

if content != old:

    msg = (
        "🎬 IMAX ALERT - NUEVAS FUNCIONES\n\n"
        "La Odisea podría tener cambios en cartelera.\n\n"
        "🔗 https://entradas.todoshowcase.com/showcase/pelicula?filmid=5875&house_id=3250"
    )

    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={
            "chat_id": CHAT,
            "text": msg
        }
    )

with open(STATE, "w") as f:
    json.dump(content, f)
