import os
import requests
import feedparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from threading import Thread

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API = os.getenv("NEWS_API")
CHAT_ID = os.getenv("CHAT_ID")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# ---------- NEWS ----------
def get_news(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={NEWS_API}"
    data = requests.get(url).json()
    articles = data["articles"][:5]

    msg = ""
    for a in articles:
        msg += f"📰 {a['title']}\n{a['url']}\n\n"
    return msg

# ---------- COMMANDS ----------
def start(update, context):
    update.message.reply_text("🇮🇳 Ultimate India Info Bot Ready 🚀")

def tech(update, context):
    update.message.reply_text(get_news("technology"))

def sports(update, context):
    update.message.reply_text(get_news("sports"))

def crypto(update, context):
    url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API}"
    data = requests.get(url).json()
    msg = "💰 Crypto News\n\n"
    for a in data["articles"][:5]:
        msg += f"{a['title']}\n{a['url']}\n\n"
    update.message.reply_text(msg)

# ---------- TRENDING ----------
def trending(update, context):
    url = f"https://newsapi.org/v2/everything?q=india&sortBy=popularity&apiKey={NEWS_API}"
    data = requests.get(url).json()
    msg = "🔥 Trending India News\n\n"
    for a in data["articles"][:5]:
        msg += f"{a['title']}\n{a['url']}\n\n"
    update.message.reply_text(msg)

# ---------- GOVT JOB ----------
def govtjobs(update, context):
    feed = feedparser.parse("https://www.freejobalert.com/rss.xml")
    msg = "🇮🇳 Latest Govt Jobs\n\n"
    for e in feed.entries[:5]:
        msg += f"{e.title}\n{e.link}\n\n"
    update.message.reply_text(msg)

# ---------- SCHOLARSHIP ----------
def scholarship(update, context):
    feed = feedparser.parse("https://www.scholarships.gov.in/rss")
    msg = "🎓 Govt Scholarships\n\n"
    for e in feed.entries[:5]:
        msg += f"{e.title}\n{e.link}\n\n"
    update.message.reply_text(msg)

# ---------- CRYPTO PRICE ----------
def btc(update, context):
    data = requests.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json").json()
    price = data["bpi"]["USD"]["rate"]
    update.message.reply_text(f"💰 BTC Price: ${price}")

# ---------- AUTO NEWS ----------
def auto_news():
    msg = get_news("technology")
    updater.bot.send_message(chat_id=CHAT_ID, text="🔥 Auto Tech News\n\n"+msg)

scheduler = BackgroundScheduler()
scheduler.add_job(auto_news, "interval", minutes=30)
scheduler.start()

# ---------- AI REPLY ----------
def chat(update, context):
    text = update.message.text
    update.message.reply_text("🤖 AI: " + text)

# ---------- HANDLERS ----------
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tech", tech))
dp.add_handler(CommandHandler("sports", sports))
dp.add_handler(CommandHandler("crypto", crypto))
dp.add_handler(CommandHandler("trending", trending))
dp.add_handler(CommandHandler("govtjobs", govtjobs))
dp.add_handler(CommandHandler("scholarship", scholarship))
dp.add_handler(CommandHandler("btc", btc))

dp.add_handler(MessageHandler(Filters.text, chat))

# ---------- SERVER ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "India Info Bot Running 🚀"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
updater.start_polling()
updater.idle()
