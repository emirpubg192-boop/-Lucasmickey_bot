import threading
import time
import requests
from flask import Flask
import telebot

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        time.sleep(240)
        try:
            requests.get("http://127.0.0.1:8080")
        except Exception:
            pass

API_TOKEN = '8844560364:AAGk0G9VPwsdTxhxDdlJbHieHtKxG29tq8g'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Bot 7/24 aktif olarak hizmetinizde.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    bot.infinity_polling()

