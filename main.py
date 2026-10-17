import os
import threading
from flask import Flask
import telebot

# --- 1. خادم وهمي لإرضاء منصة Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- 2. كود بوت التيليجرام بـ telebot ---
TOKEN = "8791327289:AAHKEEWGKE8VL9WYUcrSI09QwVrKzsnoALM"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, f"أهلاً بك يا {user_name} في بوت التحليل الفني! 🚀\nأنا جاهز لمساعدتك في تحليل الأسواق.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"تم استلام طلبك: '{message.text}' 📊\nجاري معالجة التحليل الفني...")

if __name__ == '__main__':
    # تشغيل الخادم الوهمي في الخلفية
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("🤖 البوت يعمل الآن...")
    bot.infinity_polling()
