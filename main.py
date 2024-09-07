import telebot
import json
import schedule
import time
import threading

token = '7292028921:AAG_wBUrGbV62cP9SbXQ-nUSOOFMm6SXQ0k'
bot = telebot.TeleBot(token)

current_article_index = 0
user_chat_id = None

def load_articles():
    with open('result.json', 'r') as f:
        news = json.load(f)
    return news.get('articles', [])

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
        return

    if not articles or current_article_index >= len(articles):
        articles = load_articles()
        current_article_index = 0

    article = articles[current_article_index]

    author = article.get('author', 'Unknown Author')
    image_url = article.get('urlToImage', None)

    news_message = (
        f"*{article['title']}*\n\n"
        f"_{article['description']}_\n\n"
        f"**Author:** {author}\n\n"
        f"🔗 [Read More]({article['url']})\n"
    )

    if image_url:
        bot.send_photo(user_chat_id, image_url)

    bot.send_message(user_chat_id, news_message, parse_mode='Markdown')

    current_article_index += 1


schedule.every(5).minutes.do(send_next_article)

def run_scheduling():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    scheduling_thread = threading.Thread(target=run_scheduling)
    scheduling_thread.daemon = True
    scheduling_thread.start()

    run_bot()
