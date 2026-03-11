import os
import requests
import time
from flask import Flask
from threading import Thread
from telegram import Bot

# ---------------- WEB SERVER ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "News Telegram Bot Running 🚀"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------------- BOT CONFIG ----------------
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API = os.getenv("NEWS_API")

bot = Bot(token=TOKEN)

# ---------------- NEWS FUNCTION ----------------
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API}"
    r = requests.get(url)
    data = r.json()

    articles = data["articles"][:5]

    news = "📰 *Today's Top News*\n\n"

    for a in articles:
        title = a["title"]
        link = a["url"]
        news += f"{title}\n{link}\n\n"

    return news

# ---------------- MAIN LOOP ----------------
def send_news():
    while True:
        try:
            news = get_news()
            bot.send_message(chat_id=CHAT_ID, text=news)
        except Exception as e:
            print(e)

        time.sleep(3600)

# ---------------- START ----------------
keep_alive()

thread = Thread(target=send_news)
thread.start()
