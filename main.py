import threading
import time
import requests
from flask import Flask
import telebot

# --- FLASK SUNUCUSU ---
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

# --- TELEGRAM BOT ---
API_TOKEN = '8844560364:AAGk0G9VPwsdTxhxDdlJbHieHtKxG29tq8g'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! TikTok, Instagram veya YouTube video linkini at, hemen videosunu göndereyim.")

@bot.message_handler(func=lambda message: message.text and ("tiktok.com" in message.text or "instagram.com" in message.text or "youtu" in message.text))
def download_social_video(message):
    url = message.text.strip()
    msg = bot.reply_to(message, "Video indiriliyor, lütfen bekleyin...")
    
    try:
        # Cobalt API kullanarak videoyu çekiyoruz
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": url}
        
        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()
        
        if data.get("status") in ["stream", "redirect"]:
            video_direct_url = data.get("url")
            bot.send_video(message.chat.id, video_direct_url, caption="İşte videon!")
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("Video indirilemedi. Lütfen bağlantının doğru ve herkese açık olduğunu kontrol edin.", message.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"İndirme sırasında bir hata oluştu: {e}", message.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Lütfen indirmek istediğin videonun bağlantısını (TikTok/Instagram/YouTube) gönder.")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    bot.infinity_polling()


