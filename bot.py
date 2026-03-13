import telebot
import time
import threading
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

messages = []

@bot.channel_post_handler(content_types=[
    'text','photo','video','document','audio','voice',
    'sticker','animation','video_note'
])
def handle_post(message):

    delete_time = datetime.now() + timedelta(hours=72)

    messages.append({
        "chat_id": message.chat.id,
        "message_id": message.message_id,
        "delete_time": delete_time.timestamp()
    })

def delete_worker():
    while True:
        now = datetime.now().timestamp()

        for msg in messages[:]:
            if now >= msg["delete_time"]:
                try:
                    bot.delete_message(msg["chat_id"], msg["message_id"])
                    messages.remove(msg)
                except:
                    pass

        time.sleep(5)

threading.Thread(target=delete_worker).start()

bot.infinity_polling()

