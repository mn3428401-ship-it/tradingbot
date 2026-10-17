import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_message = (
        f"أهلاً بك يا {user_name} في بوت التحليل الفني! 🚀\n\n"
        "أنا جاهز لمساعدتك في تحليل الأسواق والمؤشرات الفنية.\n"
        "أرسل لي أي رسالة أو أمر لنبدأ."
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"تم استلام طلبك: '{text}' 📊\nجاري معالجة التحليل الفني...")

def main():
    token = "8791327289:AAHKEEWGKE8VL9WYUcrSI09QwVrKzsnoALM"

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
