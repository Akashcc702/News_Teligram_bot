import os
import requests
import feedparser
import pytz
from flask import Flask
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API = os.getenv("NEWS_API")
CHAT_ID = os.getenv("CHAT_ID")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# ---------------- NEWS FUNCTION ----------------
def get_news(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={NEWS_API}"
    data = requests.get(url).json()
    articles = data["articles"][:5]

    msg = ""
    for a in articles:
        msg += f"📰 {a['title']}\n{a['url']}\n\n"
    return msg

# ---------------- COMMANDS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 ULTRA India Info Bot Ready")

async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news("technology"))

async def sports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news("sports"))

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API}"
    data = requests.get(url).json()

    msg = "💰 Crypto News\n\n"
    for a in data["articles"][:5]:
        msg += f"{a['title']}\n{a['url']}\n\n"

    await update.message.reply_text(msg)

# ---------------- TRENDING ----------------
async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://newsapi.org/v2/everything?q=india&sortBy=popularity&apiKey={NEWS_API}"
    data = requests.get(url).json()

    msg = "🔥 Trending India News\n\n"
    for a in data["articles"][:5]:
        msg += f"{a['title']}\n{a['url']}\n\n"

    await update.message.reply_text(msg)

# ---------------- GOVT JOB ----------------
async def govtjobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse("https://www.freejobalert.com/rss.xml")

    msg = "🇮🇳 Govt Jobs\n\n"
    for e in feed.entries[:5]:
        msg += f"{e.title}\n{e.link}\n\n"

    await update.message.reply_text(msg)

# ---------------- SCHOLARSHIP ----------------
async def scholarship(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse("https://www.scholarships.gov.in/rss")

    msg = "🎓 Govt Scholarships\n\n"
    for e in feed.entries[:5]:
        msg += f"{e.title}\n{e.link}\n\n"

    await update.message.reply_text(msg)

# ---------------- BTC PRICE ----------------
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json").json()
    price = data["bpi"]["USD"]["rate"]

    await update.message.reply_text(f"💰 BTC Price: ${price}")

# ---------------- AI REPLY ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"🤖 AI: {text}")

# ---------------- AUTO NEWS ----------------
def auto_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API}"
    data = requests.get(url).json()

    msg = "🔥 Auto Tech News\n\n"
    for a in data["articles"][:5]:
        msg += f"{a['title']}\n{a['url']}\n\n"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(auto_news, "interval", minutes=30)
scheduler.start()

# ---------------- HANDLERS ----------------
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tech", tech))
app.add_handler(CommandHandler("sports", sports))
app.add_handler(CommandHandler("crypto", crypto))
app.add_handler(CommandHandler("trending", trending))
app.add_handler(CommandHandler("govtjobs", govtjobs))
app.add_handler(CommandHandler("scholarship", scholarship))
app.add_handler(CommandHandler("btc", btc))

app.add_handler(MessageHandler(filters.TEXT, chat))

# ---------------- WEB SERVER ----------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "ULTRA Telegram Bot Running 🚀"

def run():
    flask_app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

app.run_polling()
def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
updater.start_polling()
updater.idle()
