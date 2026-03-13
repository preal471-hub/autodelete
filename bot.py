import telebot
import time
import threading
from datetime import datetime, timedelta

TOKEN = "8589017588:AAGcwhyXK0vMOl0zT5zX8kX_Na7r2GdxooY"

bot = telebot.TeleBot(TOKEN)

messages = []

@bot.channel_post_handler(content_types=[
    'text','photo','video','document','audio','voice',
    'sticker','animation','video_note','contact','location'
])
def handle_post(message):

    delete_time = datetime.now() + timedelta(seconds=15)   # test mode

    messages.append({
        "chat_id": message.chat.id,
        "message_id": message.message_id,
        "delete_time": delete_time.timestamp()
    })

    print("Saved message:", message.message_id)


def delete_worker():
    while True:
        now = datetime.now().timestamp()

        for msg in messages[:]:
            if now >= msg["delete_time"]:
                try:
                    bot.delete_message(msg["chat_id"], msg["message_id"])
                    print("Deleted:", msg["message_id"])
                    messages.remove(msg)
                except Exception as e:
                    print("Delete error:", e)

        time.sleep(5)


threading.Thread(target=delete_worker).start()

bot.infinity_polling()