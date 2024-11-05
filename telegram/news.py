import os
import requests
import asyncio
import schedule
import time
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Telegram bot token and chat ID
TELEGRAM_TOKEN = '7215307306:AAHmG0zVqNORgY1UXgfKESVBAr2NFzjHBHE'
CHAT_ID = '1958316281'

# NewsAPI token
NEWS_API_KEY = '57d9b7b034884cd7846407ff423f0379'  # Replace with your NewsAPI key
NEWS_URL = f'https://newsapi.org/v2/everything?q=visa+immigration&apiKey={NEWS_API_KEY}'

# File to store sent article URLs
SENT_ARTICLES_FILE = "sent_articles.txt"

# Keywords for filtering
keywords = ["visa", "immigration", "policy", "residency", "work permit", "golden visa", "citizenship", "green card"]

# Load sent articles from file
def load_sent_articles():
    if not os.path.exists(SENT_ARTICLES_FILE):
        return set()

    with open(SENT_ARTICLES_FILE, "r") as file:
        sent_articles = {line.strip() for line in file}
    return sent_articles

# Save sent articles to file
def save_sent_article(url):
    with open(SENT_ARTICLES_FILE, "a") as file:
        file.write(url + "\n")

# Reset the sent articles file at the start of each day
def reset_sent_articles():
    if os.path.exists(SENT_ARTICLES_FILE):
        os.remove(SENT_ARTICLES_FILE)
        print("Daily reset of sent articles.")

# Function to fetch news articles related to visa and immigration
def fetch_news():
    # Daily reset if it's a new day
    today = datetime.now().date()
    if today != load_last_reset_date():
        reset_sent_articles()
        save_last_reset_date(today)

    sent_articles = load_sent_articles()
    response = requests.get(NEWS_URL)
    if response.status_code != 200:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return []

    new_articles = []
    data = response.json()
    articles = data.get('articles', [])

    for article in articles:
        # Skip articles that were already sent
        if article['url'] in sent_articles:
            continue

        # Check if the article contains any general keyword
        if any(keyword.lower() in (article.get('title', '') + article.get('description', '')).lower() for keyword in keywords):
            # Format the article summary for sending
            date_published = article['publishedAt'].split("T")[0]
            summary = (
                f"<b>{article['title']}</b>\n\n"
                f"{article['description']}\n\n"
                f"Published on: {date_published}\n"
                f"<a href='{article['url']}'>Read more</a>")

            new_articles.append(summary)
            save_sent_article(article['url'])  # Mark article as sent

    if not new_articles:
        print("No new articles found matching the keywords.")

    return new_articles

# Asynchronous function to send news via Telegram
async def send_news_to_telegram():
    bot = Bot(token=TELEGRAM_TOKEN)
    news_articles = fetch_news()

    # Only send if there are new articles
    if news_articles:
        for article in news_articles:
            await bot.send_message(chat_id=CHAT_ID, text=article, parse_mode="HTML")
            await asyncio.sleep(1)  # Delay to avoid message flood
        print("Sent new articles to Telegram.")
    else:
        print("No new articles to send.")

# Track the last reset date in a file
RESET_DATE_FILE = "last_reset_date.txt"

def load_last_reset_date():
    if not os.path.exists(RESET_DATE_FILE):
        return None
    with open(RESET_DATE_FILE, "r") as file:
        return datetime.strptime(file.read().strip(), "%Y-%m-%d").date()

def save_last_reset_date(date):
    with open(RESET_DATE_FILE, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Welcome! I’ll be sending immigration and visa news updates here.")

    # Send news immediately to the user who sent /start
    news_articles = fetch_news()
    for article in news_articles:
        await context.bot.send_message(chat_id=chat_id, text=article, parse_mode="HTML")

def main():
    # Initialize the bot application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add /start command handler to the bot
    application.add_handler(CommandHandler("start", start))

    # Schedule the job to run at 7 am and 7 pm every day
    schedule.every().day.at("07:00").do(lambda: asyncio.run(send_news_to_telegram()))
    schedule.every().day.at("19:00").do(lambda: asyncio.run(send_news_to_telegram()))

    print("Scheduled bot to run at 7 am and 7 pm daily.")

    # Run both schedule and bot in parallel
    application.run_polling()  # Starts handling commands like /start

    # Schedule loop to run alongside bot polling
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check the schedule every 60 seconds
