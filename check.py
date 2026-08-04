import os
import requests
import json
from datetime import datetime

API_URL = "https://api.voyalcine.net/films/5875/tree/3250"

TOKEN = os.environ["BOT_TOKEN"]
CHATS = [
    os.environ["CHAT_ID"],
    os.environ["CHAT_ID_FRUBI"]
]
STATE = "state.json"


def format_date(date):
    days = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]

    months = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]

    d = datetime.strptime(date, "%Y-%m-%d")

    return f"{days[d.weekday()].capitalize()} {d.day} de {months[d.month-1]}"


data = requests.get(API_URL, timeout=20).json()

# Obtener solamente fechas con IMAX Norcenter
dates = []

for date, cinemas in data.get("days", {}).items():
    for cinema in cinemas:
        if "IMAX" in cinema.get("name", ""):
            dates.append(date)
            break

dates = sorted(set(dates))


try:
    with open(STATE, "r") as f:
        old_dates = json.load(f)

except:
    old_dates = dates

    with open(STATE, "w") as f:
        json.dump(dates, f)

    exit()


new_dates = [d for d in dates if d not in old_dates]
new_dates = ["2026-08-21"]
if new_dates:

    msg = "🎬 LA ODISEA - IMAX NORCENTER\n\n"
    msg += "🚨 NUEVAS FECHAS HABILITADAS\n\n"

    for d in new_dates:
        msg += f"📅 {format_date(d)}\n"

    msg += "\n🔗 https://entradas.todoshowcase.com/showcase/pelicula?filmid=5875&house_id=3250"

    for chat in CHATS:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": chat,
                "text": msg
            }
        )


with open(STATE, "w") as f:
    json.dump(dates, f)
