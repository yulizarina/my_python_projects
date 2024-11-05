import requests
import asyncio
import schedule
import time
from telegram import Bot

# Telegram bot token and chat ID
TELEGRAM_TOKEN = '7215307306:AAHmG0zVqNORgY1UXgfKESVBAr2NFzjHBHE'  # Replace with your bot token
CHAT_ID = 1958316281  # Replace with your chat ID

# NewsAPI token
NEWS_API_KEY = '57d9b7b034884cd7846407ff423f0379'  # Replace with your NewsAPI key
NEWS_URL = f'https://newsapi.org/v2/everything?q=visa+immigration&apiKey={NEWS_API_KEY}'

# Function to fetch news articles related to visa and immigration
def fetch_news():
    response = requests.get(NEWS_URL)
    articles_summary = []

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        # Define keywords for filtering relevant articles and country identification
        keywords = ["visa", "immigration", "policy", "residency", "work permit"]
        country_keywords = {
            "UK": ["UK", "United Kingdom", "Britain", "British"],
            "Australia": ["Australia", "Australian"],
            "USA": ["USA", "United States", "America", "American", "U.S.", "H-2A"],
            "Germany": ["Germany", "German"],
            "Canada": ["Canada", "Canadian"]
        }

        count = 0
        for article in articles:
            # Check if any keyword is in the title or description
            if any(keyword.lower() in (article['title'] + article['description']).lower() for keyword in keywords):

                # Determine the country based on keywords in the title or description
                country = "General"
                for key, values in country_keywords.items():
                    if any(val in article['title'] + article['description'] for val in values):
                        country = key
                        break

                # Format the published date (only date part)
                date_published = article['publishedAt'].split("T")[0]

                # Format the article summary
                summary = f"<b>{country}</b>\n\n" \
                          f"<b>{article['title']}</b>\n\n" \
                          f"{article['description']}\n\n" \
                          f"Published on: {date_published}\n" \
                          f"<a href='{article['url']}'>Read more</a>"

                articles_summary.append(summary)
                count += 1

            if count == 5:  # Limit to 5 articles
                break
    else:
        articles_summary.append("Failed to fetch news data.")

    return articles_summary

# Asynchronous function to send news via Telegram
async def send_news_to_telegram():
    bot = Bot(token=TELEGRAM_TOKEN)
    news_articles = fetch_news()

    # Check if there are articles to send
    if news_articles:
        for article in news_articles:
            await bot.send_message(chat_id=CHAT_ID, text=article, parse_mode="HTML")
            await asyncio.sleep(1)  # Small delay to avoid message flood

def job():  # <span style="color:pink">New wrapper function to integrate with schedule</span>
    asyncio.run(send_news_to_telegram())

# Schedule the job to run every 4 hours
schedule.every(4).hours.do(job)  # <span style="color:pink">Scheduling the job to run every 4 hours</span>

# Keep the script running
if __name__ == "__main__":
    print("Starting the news bot...")
    while True:  # <span style="color:pink">Keep the script running indefinitely</span>
        schedule.run_pending()  # <span style="color:pink">Check for any scheduled jobs</span>
        time.sleep(60)  # <span style="color:pink">Wait 60 seconds between checks</span>
