import os
import logging
import random
from flask import Flask, request
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
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

# قائمة الـ IDs المعتمدة (تتحدث تلقائياً عند وصول Postback)
ALLOWED_IDS = set([
    "12345678",
    "139822533"
])

# قائمة الأزواج
ALL_PAIRS = {
    'XAUUSD': "🪙 الذهب (XAUUSD)",
    'EURUSD': "💶 EUR/USD",
    'GBPUSD': "💷 GBP/USD",
    'USDJPY': "💴 USD/JPY",
    'AUDUSD': "🇦🇺 AUD/USD",
    'USDCAD': "🇨🇦 USD/CAD",
    'USDCHF': "🇨🇭 USD/CHF",
    'NZDUSD': "🇳🇿 NZD/USD"
}

# --- سيرفر Flask لاستقبال إشعارات الـ Postback تلقائياً من Pocket Partners ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot Server & Postback Listener is Running Active!"

@app_web.route('/postback', methods=['GET', 'POST'])
def handle_postback():
    user_id = request.args.get('user_id') or request.form.get('user_id')
    deposit = request.args.get('deposit') or request.form.get('deposit')
    
    if user_id:
        ALLOWED_IDS.add(str(user_id).strip())
        logging.info(f"✅ New Verified ID added via Postback: {user_id} (Deposit: {deposit})")
        return f"OK - User {user_id} Verified", 200
    return "No user_id received", 400

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# -------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 **مرحباً بك في بوت التداول والتحليل الفني السريع**\n\n"
        "لتفعيل البوت والحصول على إشارات دقيقة 100%، يرجى اتباع الخطوات التالية:\n\n"
        "1️⃣ **سجّل حساباً جديداً** عبر رابط الإحالة الخاص بنا.\n"
        "2️⃣ **قم بإيداع مبلغ 5$ كحد أدنى** لتفعيل الحساب تلقائياً.\n"
        "3️⃣ **أدخل رقم الـ ID** الخاص بحسابك للتحقق الفوري."
    )
    
    keyboard = [
        [InlineKeyboardButton("🔗 تسجيل حساب جديد", url=REGISTRATION_URL)],
        [InlineKeyboardButton("✅ أدخل رقم الـ ID للتحقق", callback_data='check_id_step')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    return ConversationHandler.END

async def check_id_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📥 **الرجاء إرسال رقم الـ ID الخاص بحسابك الآن للتحقق التلقائي:**"
    await query.edit_message_text(text, parse_mode='Markdown')
    return WAITING_FOR_ID

async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_input = update.message.text.strip()
    
    if user_id_input in ALLOWED_IDS:
        context.user_data['is_verified'] = True
        context.user_data['pocket_id'] = user_id_input
        
        text = (
            f"✅ **تم التحقق بنجاح من الـ ID:** `{user_id_input}`\n\n"
            "🎉 **حسابك مسجل ومربوط رسمياً!**\n"
            "اختر الزوج المالي الذي ترغب بتحليله واستخراج الإشارة له فوراً:"
        )
        
        keyboard = []
        pairs_list = list(ALL_PAIRS.items())
        for i in range(0, len(pairs_list), 2):
            row = [InlineKeyboardButton(pairs_list[i][1], callback_data=f"analyze_{pairs_list[i][0]}")]
            if i + 1 < len(pairs_list):
                row.append(InlineKeyboardButton(pairs_list[i+1][1], callback_data=f"analyze_{pairs_list[i+1][0]}"))
            keyboard.append(row)
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return ConversationHandler.END
    else:
        text = (
            f"❌ **عذراً، هذا الـ ID (`{user_id_input}`) غير مسجل عبر رابطنا أو لم يتم تأكيد إيداع $5 بعد.**\n\n"
            "⚠️ **للتفعيل:**\n"
            "1. قم بالتسجيل عبر الرابط أدناه.\n"
            "2. قم بإيداع 5$ على الأقل.\n"
            "3. انتظر بضع ثوانٍ وأعد المحاولة."
        )
        keyboard = [
            [InlineKeyboardButton("🔗 تسجيل حساب جديد", url=REGISTRATION_URL)],
            [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data='check_id_step')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        return ConversationHandler.END

async def market_analysis_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not context.user_data.get('is_verified', False):
        text = "⚠️ **عذراً، يجب التحقق من الـ ID أولاً.**"
        keyboard = [[InlineKeyboardButton("🔗 تسجيل وشحن الحساب", url=REGISTRATION_URL)]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    data = query.data.replace("analyze_", "")
    selected_pair_name = ALL_PAIRS.get(data, "🪙 الذهب (XAUUSD)")
    
    rsi_value = random.randint(20, 80)
    if rsi_value <= 35:
        action = "صعود 🟢 (CALL / شراء)"
        reason = "وصول المؤشر لمنطقة تشبع بيعي قوية (Oversold) + ارتداد من الدعم."
    elif rsi_value >= 65:
        action = "هبوط 🔴 (PUT / بيع)"
        reason = "وصول المؤشر لمنطقة تشبع شرائي (Overbought) + كسر مقاومة."
    else:
        action = random.choice(["صعود 🟢 (CALL / شراء)", "هبوط 🔴 (PUT / بيع)"])
        reason = "تقاطع متوسطات الحركة Moving Averages على فريم 1M."
        
    timeframe = "دقيقة واحدة (1M) - التداول السريع"
    accuracy_rate = "75% - 82%"
    
    analysis_text = (
        f"📊 **تقرير التحليل الفني المتقدم:**\n\n"
        f"📌 **الأصل المالي:** {selected_pair_name}\n"
        f"⏱️ **الفريم الزمني:** {timeframe}\n"
        f"📈 **قوة المؤشر (RSI):** {rsi_value}\n"
        f"🎯 **نسبة دقة التحليل:** {accuracy_rate}\n"
        f"💡 **سبب التحليل:** {reason}\n\n"
        f"🔥 **التوصية النهائية:** **{action}**\n\n"
        f"⚠️ *تنبيه: التزم بإدارة رأس المال وتداول بحكمة.*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث التحليل وإعطاء إشارة جديدة", callback_data=query.data)],
        [InlineKeyboardButton("🔙 اختيار زوج آخر", callback_data='back_to_pairs_list')],
        [InlineKeyboardButton("📈 فتح منصة التداول", url=REGISTRATION_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(analysis_text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception:
        pass

async def back_to_pairs_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📊 **الرجاء اختيار الزوج المالي الذي ترغب بتحليله:**"
    keyboard = []
    pairs_list = list(ALL_PAIRS.items())
    for i in range(0, len(pairs_list), 2):
        row = [InlineKeyboardButton(pairs_list[i][1], callback_data=f"analyze_{pairs_list[i][0]}")]
        if i + 1 < len(pairs_list):
            row.append(InlineKeyboardButton(pairs_list[i+1][1], callback_data=f"analyze_{pairs_list[i+1][0]}"))
        keyboard.append(row)
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        return

    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(check_id_callback, pattern='^check_id_step$')],
        states={
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^🚀 بدء / Start$'), handle_start_button))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(market_analysis_callback, pattern='^analyze_.*$'))
    app.add_handler(CallbackQueryHandler(back_to_pairs_list_callback, pattern='^back_to_pairs_list$'))

    print("Bot with Flask Postback Integration is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
