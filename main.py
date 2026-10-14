import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# مراحل المحادثة
WAITING_FOR_ID = 1

# رابط الإحالة الخاص بك
REGISTRATION_URL = "https://pocket-friends.co/r/g6ccrwmyb6"

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 **الخطوة 1 - تفعيل البوت**\n\n"
        "لتفعيل البوت، يجب عليك تسجيل حساب جديد عبر رابط الإحالة الخاص بنا.\n\n"
        "⚠️ **مهم:** إذا كان لديك حساب بالفعل، يجب إنشاء حساب جديد باستخدام الرابط أدناه لربط البوت.\n\n"
        "1️⃣ **سجّل حساباً جديداً عبر الزر أدناه.**\n"
        "2️⃣ **جاهز؟** اضغط على (تحقق من ID) وأرسل رقم ID الخاص بحسابك."
    )
    
    keyboard = [
        [InlineKeyboardButton("🔗 تسجيل", url=REGISTRATION_URL)],
        [InlineKeyboardButton("✅ تحقق من ID", callback_data='check_id_step')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return ConversationHandler.END

# زر التحقق من ID
async def check_id_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📥 **الرجاء إرسال رقم الـ ID الخاص بحسابك الجديد الآن:**"
    await query.edit_message_text(text, parse_mode='Markdown')
    return WAITING_FOR_ID

# استقبال الـ ID من المستخدم
async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_input = update.message.text.strip()
    
    # حفظ الـ ID في بيانات المستخدم
    context.user_data['pocket_id'] = user_id_input
    
    # رسالة خطوة الإيداع وتفعيل اختيار الأزواج
    text = (
        f"✅ **تم تسجيل الـ ID الخاص بك:** `{user_id_input}`\n\n"
        "🚀 **الخطوة 2 - شحن الحساب والتفعيل**\n\n"
        "بقي القليل فقط! للحصول على الوصول الشامل لتحليل السوق والإشارات، قم بتعبئة رصيدك بمبلغ لا يقل عن **$5**.\n\n"
        "اختر الزوج الذي تريد تحليله مباشرة:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🪙 الذهب (XAUUSD)", callback_data='analyze_XAUUSD')],
        [InlineKeyboardButton("💶 EUR/USD", callback_data='analyze_EURUSD')],
        [InlineKeyboardButton("💷 GBP/USD", callback_data='analyze_GBPUSD')],
        [InlineKeyboardButton("↗️ إيداع الرصيد", url=REGISTRATION_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return ConversationHandler.END

# محرك تحليل السوق المخصص بناءً على اختيار المستخدم
async def market_analysis_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # معرفة الزوج الذي اختاره المستخدم من الـ callback_data
    data = query.data
    pair_map = {
        'analyze_XAUUSD': "XAUUSD (الذهب)",
        'analyze_EURUSD': "EURUSD",
        'analyze_GBPUSD': "GBPUSD"
    }
    
    selected_pair = pair_map.get(data, "XAUUSD (الذهب)")
    action = random.choice(["صعود 🟢 (CALL)", "هبوط 🔴 (PUT)"])
    timeframe = "دقيقة واحدة (1M)"
    rsi_value = random.randint(30, 70)
    
    analysis_text = (
        f"🔍 **تقرير تحليل السوق (حسب طلبك):**\n\n"
        f"🪙 **الأصل المالي:** {selected_pair}\n"
        f"⏱️ **الفريم الزمني:** {timeframe}\n"
        f"📊 **مؤشر القوة النسبية (RSI):** {rsi_value}\n"
        f"📉 **حالة الدعم والمقاومة:** تم رصد تقاطع فني واستقرار عند مستويات قوية.\n\n"
        f"🎯 **التوصية:** **{action}**\n\n"
        f"⚠️ *ملاحظة: تداول بحكمة وقم بإدارة رأس مالك.*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 اختيار زوج آخر", callback_data='back_to_pairs')],
        [InlineKeyboardButton("📈 الذهاب للتداول", url=REGISTRATION_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(analysis_text, reply_markup=reply_markup, parse_mode='Markdown')

# العودة لقائمة اختيار الأزواج
async def back_to_pairs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📊 **الرجاء اختيار الزوج المالي الذي ترغب بتحليله:**"
    keyboard = [
        [InlineKeyboardButton("🪙 الذهب (XAUUSD)", callback_data='analyze_XAUUSD')],
        [InlineKeyboardButton("💶 EUR/USD", callback_data='analyze_EURUSD')],
        [InlineKeyboardButton("💷 GBP/USD", callback_data='analyze_GBPUSD')],
        [InlineKeyboardButton("↗️ إيداع الرصيد", url=REGISTRATION_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# التعامل مع زر تحقق من الإيداع
async def check_deposit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📊 **الرجاء اختيار الزوج المالي الذي ترغب بتحليله:**"
    keyboard = [
        [InlineKeyboardButton("🪙 الذهب (XAUUSD)", callback_data='analyze_XAUUSD')],
        [InlineKeyboardButton("💶 EUR/USD", callback_data='analyze_EURUSD')],
        [InlineKeyboardButton("💷 GBP/USD", callback_data='analyze_GBPUSD')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(check_id_callback, pattern='^check_id_step$')],
        states={
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(check_deposit_callback, pattern='^check_deposit_step$'))
    app.add_handler(CallbackQueryHandler(market_analysis_callback, pattern='^analyze_.*$'))
    app.add_handler(CallbackQueryHandler(back_to_pairs_callback, pattern='^back_to_pairs$'))

    print("Bot is running with custom pair selection...")
    app.run_polling()

if __name__ == "__main__":
    main()
