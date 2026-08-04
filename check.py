import os
import requests
from bs4 import BeautifulSoup

URL="https://entradas.todoshowcase.com/showcase/pelicula?filmid=5875&house_id=3250"

TOKEN=os.environ["BOT_TOKEN"]
CHAT=os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

text = " ".join(soup.stripped_strings)

msg = "🔎 TEXTO ENCONTRADO:\n\n" + text[:3000]

requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    params={
        "chat_id": CHAT,
        "text": msg
    }
)
