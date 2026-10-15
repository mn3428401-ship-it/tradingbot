import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد التسجيل لرؤية الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# جلب التوكن من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⏱ دقيقة واحدة (1M)", callback_data='frame_1m')],
        [InlineKeyboardButton("⏱ 5 دقائق (5M)", callback_data='frame_5m')],
        [InlineKeyboardButton("⏱ 15 دقيقة (15M)", callback_data='frame_15m')],
        [InlineKeyboardButton("⏱ ساعة (1H)", callback_data='frame_1h')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    msg_text = "📌 **الأصل المختار:** EUR/USD 💶💵\n\nاختر زمن/فريم الشمعة:"
    
    if update.message:
        await update.message.reply_text(msg_text, reply_markup=reply_markup, parse_mode='Markdown')
    elif update.callback_query:
        await update.callback_query.edit_message_text(msg_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # أهم خطوة: إجابة التيليجرام لإلغاء جاري التحميل على الزر
    await query.answer()
    
    data = query.data
    
    if data.startswith('frame_'):
        frame_name = data.split('_')[1].upper()
        
        # إعداد أزرار التحليل بعد اختيار الفريم
        keyboard = [
            [InlineKeyboardButton("📊 تحليل الاتجاه (Trend)", callback_data=f'analyze_{frame_name}')],
            [InlineKeyboardButton("🔙 رجوع لاختيار الفريم", callback_data='back_to_frames')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"✅ **تم اختيار فريم:** {frame_name}\n\nاختر نوع التحليل المطلوب:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    elif data == 'back_to_frames' or data == 'back_main':
        await start(update, context)
        
    elif data.startswith('analyze_'):
        frame = data.split('_')[1]
        await query.edit_message_text(
            f"📈 **جاري تحليل السوق على فريم {frame}...**\n\nالسوق حالياً في اتجاه متوازن مع مستويات دعم قوية.",
            parse_mode='Markdown'
        )

def main():
    if not TOKEN:
        print("خطأ: BOT_TOKEN غير موجود!")
        return

    app = Application.builder().token(TOKEN).build()

    # الأوامر والمعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
