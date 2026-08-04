import os,requests,json
from bs4 import BeautifulSoup

URL="https://entradas.todoshowcase.com/showcase/pelicula?filmid=5875&house_id=3250"
TOKEN=os.environ["BOT_TOKEN"]
CHAT=os.environ["CHAT_ID"]
STATE="state.json"

html=requests.get(URL,timeout=20).text
soup=BeautifulSoup(html,"html.parser")
text=" ".join(soup.stripped_strings)
# Simple extraction fallback
current=sorted(set([t for t in text.split() if ":" in t or "/" in t]))
try:
    old=json.load(open(STATE))
except:
    old=[]
new=[x for x in current if x not in old]
if new:
    msg="🎬 Posibles nuevas funciones detectadas:\\n"+"\\n".join(new[:30])
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",params={"chat_id":CHAT,"text":msg})
json.dump(current,open(STATE,"w"))
