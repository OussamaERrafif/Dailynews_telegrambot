# Telegram News Bot 📰🤖

This project is a simple Telegram bot that provides periodic news updates directly to users. The bot fetches news articles from a JSON file and sends them to the user every 5 minutes. The bot also responds to the `/start` command with a welcome message and a brief overview of the features.

## Features
- **Automated News Delivery**: The bot sends a new article to the user every 5 minutes.
- **Personalized Notifications**: Updates are delivered to the user's chat ID after they initiate communication with the bot.
- **Simple & Lightweight**: Built using the `telebot` library, the bot is lightweight and easy to set up.

## Requirements

Before running the Telegram News Bot, ensure that you have the following:

1. **Python 3.7+** installed on your machine.
2. A valid **Telegram Bot API token** (get one from [BotFather](https://core.telegram.org/bots#botfather)).
3. A file called `result.json` containing the news articles in the following format:

    ```json
    {
        "articles": [
            {
                "title": "Sample Article Title",
                "description": "Brief description of the article.",
                "author": "Author Name",
                "url": "https://example.com",
                "urlToImage": "https://example.com/image.jpg"
            },
            ...
        ]
    }
    ```

### Libraries

The required libraries for this project are listed below:

- `pyTelegramBotAPI`
- `schedule`

You can install these using pip, as described in the installation instructions below.

## Installation & Setup

Follow the steps below to run the bot locally on your machine:

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/telegram-news-bot.git
cd telegram-news-bot
```

### Step 2: Set up a Virtual Environment

To avoid conflicts with other Python projects, it's a good idea to use a virtual environment.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment active, install the necessary libraries:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, manually install the required libraries:

```bash
pip install pyTelegramBotAPI schedule
```

### Step 4: Set Up Your Telegram Bot Token

You'll need to replace the placeholder API token with your actual token in the code. Find the following line:

```python
token = 'your-telegram-bot-token-here'
```

Replace `'your-telegram-bot-token-here'` with the token you received from BotFather.

### Step 5: Run the Bot

Once everything is set up, you can run the bot using:

```bash
python bot.py
```

### Step 6: Interact with the Bot

1. Open Telegram and search for your bot.
2. Send `/start` to initiate the conversation and start receiving news updates every 5 minutes.

## How it Works

1. **Start Command**: When the user sends the `/start` command, the bot replies with a welcome message and stores the user's chat ID.
2. **Periodic News Delivery**: Every 5 minutes, the bot sends the next article from the `result.json` file to the user.
3. **Article Cycling**: Once all articles are sent, the bot reloads the list and starts sending from the beginning.

## Notes
- Ensure the `result.json` file is in the same directory as the bot script.
- Make sure the Telegram Bot token is valid, or the bot will fail to start.

---

Created by **[Oussama Errafif](https://www.linkedin.com/in/oussama-errafif-5155b5247/)**