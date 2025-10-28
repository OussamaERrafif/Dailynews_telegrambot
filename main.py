import telebot
import json
import schedule
import time
import threading
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    raise ValueError("Please set TELEGRAM_BOT_TOKEN in .env file or environment variables")

bot = telebot.TeleBot(token)

# Configuration
NEWS_UPDATE_INTERVAL = int(os.getenv('NEWS_UPDATE_INTERVAL', 5))
NEWS_FILE = 'result.json'

current_article_index = 0
user_chat_id = None

def load_articles():
    """
    Load articles from the JSON file.
    
    Returns:
        list: A list of article dictionaries, or empty list if file not found/invalid.
    """
    try:
        with open(NEWS_FILE, 'r', encoding='utf-8') as f:
            news = json.load(f)
        articles = news.get('articles', [])
        logger.info(f"Loaded {len(articles)} articles from {NEWS_FILE}")
        return articles
    except FileNotFoundError:
        logger.error(f"{NEWS_FILE} not found. Please create it with news articles.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing {NEWS_FILE}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading articles: {e}")
        return []

articles = load_articles()

@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Handle the 'start' command and send a welcome message to the user.

    Args:
        message (telegram.Message): The message object representing the user's message.

    Returns:
        None
    """
    global user_chat_id
    user_chat_id = message.chat.id
    logger.info(f"New user started bot: {user_chat_id}")
    
    try:
        bot.send_message(user_chat_id, """
**Welcome to the News Bot!** 📰🤖

This bot was created by *Oussama Errafif* to keep you updated with the latest news, delivered directly to you every 5 minutes. Whether it's breaking news, updates, or trending stories, you'll stay informed!

**Features:**
- News updates every 5 minutes
- Personalized notifications based on your preferences
- Easy and simple to use

If you have any questions or feedback, feel free to reach out to me through the following links:

🔗 **LinkedIn:** [Oussama Errafif](https://www.linkedin.com/in/oussama-errafif-5155b5247/)  
🔗 **GitHub:** [OussamaERrafif](https://github.com/OussamaERrafif)

Enjoy your news updates!
    """, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")


@bot.message_handler(commands=['help'])
def help_message(message):
    """
    Handle the 'help' command and send help information to the user.

    Args:
        message (telegram.Message): The message object representing the user's message.

    Returns:
        None
    """
    try:
        bot.send_message(message.chat.id, """
**Available Commands:**

/start - Start receiving news updates
/help - Show this help message
/stop - Stop receiving news updates
/status - Check bot status and subscription info

**How it works:**
Once you start the bot, you'll receive news articles every 5 minutes automatically.
    """, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error sending help message: {e}")


@bot.message_handler(commands=['stop'])
def stop_message(message):
    """
    Handle the 'stop' command to pause news updates.

    Args:
        message (telegram.Message): The message object representing the user's message.

    Returns:
        None
    """
    global user_chat_id
    if user_chat_id == message.chat.id:
        user_chat_id = None
        logger.info(f"User stopped bot: {message.chat.id}")
        try:
            bot.send_message(message.chat.id, "You have unsubscribed from news updates. Send /start to subscribe again.")
        except Exception as e:
            logger.error(f"Error sending stop confirmation: {e}")
    else:
        try:
            bot.send_message(message.chat.id, "You are not currently subscribed. Send /start to begin receiving updates.")
        except Exception as e:
            logger.error(f"Error sending stop message: {e}")


@bot.message_handler(commands=['status'])
def status_message(message):
    """
    Handle the 'status' command to show bot status.

    Args:
        message (telegram.Message): The message object representing the user's message.

    Returns:
        None
    """
    try:
        status_text = f"""
**Bot Status** 📊

**Articles loaded:** {len(articles)}
**Current article:** {current_article_index + 1} of {len(articles) if articles else 0}
**Update interval:** {NEWS_UPDATE_INTERVAL} minutes
**Subscribed:** {'Yes' if user_chat_id == message.chat.id else 'No'}

Send /start to subscribe to updates.
        """
        bot.send_message(message.chat.id, status_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error sending status message: {e}")


def send_next_article():
    """
    Sends the next article to the user.

    This function retrieves the next article from the list of articles and sends it to the user.
    If there are no more articles or the user chat ID is not set, nothing is sent.

    Args:
        None

    Returns:
        None
    """
    global current_article_index, articles, user_chat_id

    if not user_chat_id:
        logger.debug("No active user, skipping article send")
        return

    if not articles:
        logger.warning("No articles available to send")
        return

    if current_article_index >= len(articles):
        logger.info("Reloading articles, reached end of list")
        articles = load_articles()
        current_article_index = 0
        
        if not articles:
            logger.error("No articles available after reload")
            return

    try:
        article = articles[current_article_index]
        
        # Validate article has required fields
        if 'title' not in article or 'description' not in article or 'url' not in article:
            logger.error(f"Article {current_article_index} missing required fields")
            current_article_index += 1
            return

        author = article.get('author', 'Unknown Author')
        image_url = article.get('urlToImage', None)

        news_message = (
            f"*{article['title']}*\n\n"
            f"_{article['description']}_\n\n"
            f"**Author:** {author}\n\n"
            f"🔗 [Read More]({article['url']})\n"
        )

        if image_url:
            try:
                bot.send_photo(user_chat_id, image_url)
            except Exception as e:
                logger.warning(f"Failed to send image: {e}")

        bot.send_message(user_chat_id, news_message, parse_mode='Markdown')
        logger.info(f"Sent article {current_article_index + 1}/{len(articles)} to user {user_chat_id}")
        
        current_article_index += 1
    except Exception as e:
        logger.error(f"Error sending article: {e}")
        current_article_index += 1


schedule.every(NEWS_UPDATE_INTERVAL).minutes.do(send_next_article)

def run_scheduling():
    """
    Run the scheduling loop to send periodic news updates.
    
    Returns:
        None
    """
    logger.info(f"Starting scheduler with {NEWS_UPDATE_INTERVAL} minute interval")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error in scheduling loop: {e}")
            time.sleep(1)

def run_bot():
    """
    Start the Telegram bot polling loop.
    
    Returns:
        None
    """
    logger.info("Starting bot polling...")
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
        raise

if __name__ == '__main__':
    logger.info("Starting Telegram News Bot...")
    
    if not articles:
        logger.warning(f"No articles loaded. Please create {NEWS_FILE} with news articles.")
    
    scheduling_thread = threading.Thread(target=run_scheduling)
    scheduling_thread.daemon = True
    scheduling_thread.start()

    run_bot()
