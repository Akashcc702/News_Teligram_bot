import requests
from telegram import Bot
import time

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
NEWS_API = "YOUR_NEWSAPI_KEY"

bot = Bot(token=TOKEN)

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API}"
    r = requests.get(url)
    data = r.json()

    articles = data["articles"][:5]

    news_text = "📰 Today's Top News\n\n"

    for a in articles:
        news_text += f"{a['title']}\n{a['url']}\n\n"

    return news_text

while True:
    news = get_news()
    bot.send_message(chat_id=CHAT_ID, text=news)
    
    time.sleep(3600)
