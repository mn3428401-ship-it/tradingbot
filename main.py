import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك يا محمد! البوت يعمل بنجاح من السحابة 🚀")

if __name__ == '__main__':
    TOKEN = "8888506170:AAGjzExojxoGdJc0TvUQzySovije562X30I"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
