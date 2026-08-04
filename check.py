import os
import requests
import json

API_URL = "https://api.voyalcine.net/films/5875/tree/3250"

TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]

STATE = "state.json"

data = requests.get(API_URL, timeout=20).json()

functions = []

for date, cinemas in data.get("days", {}).items():
    for cinema in cinemas:
        if "IMAX" in cinema.get("name", ""):
            for fmt in cinema.get("formats", []):
                if "IMAX" in fmt.get("formatDescription", ""):
                    for performance in fmt.get("performances", []):
                        functions.append(
                            {
                                "date": date,
                                "time": performance["showTime"]
                            }
                        )

functions = sorted(functions, key=lambda x: (x["date"], x["time"]))

try:
    with open(STATE, "r") as f:
        old = json.load(f)
except:
    old = []

if functions != old:

    msg = "🎬 LA ODISEA - IMAX NORCENTER\n\n"

    if functions:
        msg += "✅ Funciones disponibles:\n\n"

        for f in functions:
            msg += f"📅 {f['date']}  🕒 {f['time']}\n"

    else:
        msg += "❌ No hay funciones disponibles."

    msg += "\n\n🔗 https://entradas.todoshowcase.com/showcase/pelicula?filmid=5875&house_id=3250"

    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={
            "chat_id": CHAT,
            "text": msg
        }
    )

with open(STATE, "w") as f:
    json.dump(functions, f)
