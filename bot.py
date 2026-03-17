import telebot
import time
import threading
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

FILE = "messages.json"

# ---------- LOAD OLD DATA ----------
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        messages = json.load(f)
else:
    messages = []

# ---------- SAVE FUNCTION ----------
def save_messages():
    with open(FILE, "w") as f:
        json.dump(messages, f)

# ---------- STORE CHANNEL POSTS ----------
@bot.channel_post_handler(content_types=[
    'text','photo','video','document','audio','voice',
    'sticker','animation','video_note'
])
def handle_post(message):
    delete_time = datetime.now() + timedelta(hours=72)

    msg_data = {
        "chat_id": message.chat.id,
        "message_id": message.message_id,
        "delete_time": delete_time.timestamp()
    }

    messages.append(msg_data)
    save_messages()

    print(f"Saved message {message.message_id} for deletion")

# ---------- DELETE WORKER ----------
def delete_worker():
    while True:
        try:
            now = datetime.now().timestamp()

            for msg in messages[:]:
                if now >= msg["delete_time"]:
                    try:
                        bot.delete_message(msg["chat_id"], msg["message_id"])
                        messages.remove(msg)
                        save_messages()
                        print(f"Deleted message {msg['message_id']}")
                    except Exception as e:
                        print("Delete error:", e)

            time.sleep(5)

        except Exception as e:
            print("Worker error:", e)
            time.sleep(5)

# ---------- START THREAD ----------
threading.Thread(target=delete_worker, daemon=True).start()

# ---------- AUTO RECONNECT POLLING ----------
while True:
    try:
        print("Bot running...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
