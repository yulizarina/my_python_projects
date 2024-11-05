Telegram News Bot for Immigration and Visa Updates
This Python project creates a Telegram bot that periodically sends news updates related to immigration and visa policies from various countries. The bot uses the NewsAPI to fetch the latest articles, filters them based on relevant keywords, and sends formatted news summaries to a specified Telegram chat.

Features
Fetches immigration and visa news articles every 4 hours.
Filters articles based on keywords (e.g., "visa," "immigration," "policy").
Sends formatted article summaries with links directly to a Telegram chat.
Responds to the /start command to send an initial news update.
Setup
Prerequisites
Python 3.7+

Install dependencies by running:

bash
Copy code
pip install requests python-telegram-bot schedule
API Keys
Telegram Bot Token:

Create a Telegram bot by chatting with BotFather on Telegram.
Replace TELEGRAM_TOKEN in the code with your bot's token.
NewsAPI Key:

Sign up at NewsAPI and obtain an API key.
Replace NEWS_API_KEY in the code with your NewsAPI key.
Configuration
Replace CHAT_ID in the code with the chat ID where the bot should send messages. To get your chat ID, you can use the bot in a group or direct chat and retrieve it from the Telegram Bot API.
Usage
Running the Bot:

To start the bot, run the following command:

bash
Copy code
python <your_script_name>.py
Bot Commands:

/start - Initializes the bot and sends the latest immigration news immediately.
Scheduled News Updates:

The bot fetches and sends immigration news updates to the specified chat every 4 hours.
Code Overview
fetch_news(): Fetches news articles from NewsAPI, filters them based on keywords, and formats them with country-specific labels.
send_news_to_telegram(): Sends the formatted news articles to the specified Telegram chat.
start(): Handles the /start command, welcoming the user and sending an initial set of news articles.
job(): Triggers the send_news_to_telegram() function every 4 hours using the schedule library.
main(): Runs the bot, initializes the /start command handler, and starts the scheduling loop.
Important Notes
Message Limit: The bot sends up to 5 articles per update to avoid message overload.
Error Handling: If fetching news fails, an error message is sent instead of the news update.
Scheduling: The schedule checks for updates every 60 seconds and sends updates every 4 hours.
Dependencies
requests: To fetch news articles from NewsAPI.
asyncio: For handling asynchronous tasks in Python.
schedule: For scheduling news updates every 4 hours.
python-telegram-bot: For interacting with the Telegram Bot API.
License
This project is licensed under the MIT License.
