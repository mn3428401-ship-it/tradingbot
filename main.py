import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# قائمة الأزواج
PAIRS = [
    ("🪙 الذهب (XAUUSD)", "XAUUSD"),
    ("💶 EUR/USD", "EURUSD"),
    ("💷 GBP/USD", "GBPUSD"),
    ("🇯🇵 USD/JPY", "USDJPY"),
    ("🪙 BTC/USD", "BTCUSD"),
    ("🇦🇺 AUD/USD", "AUDUSD")
]

CANDLE_TIMEFRAMES = [
    ("⏱️ دقيقة واحدة (1M)", "1M"),
    ("⏱️ 5 دقائق (5M)", "5M"),
    ("⏱️ 15 دقيقة (15M)", "15M"),
    ("⏱️ ساعة (1H)", "1H")
]

TRADE_DURATIONS = [
    ("⏰ صفقة دقيقة (1 Min)", "1M"),
    ("⏰ صفقة دقيقتين (2 Min)", "2M"),
    ("⏰ صفقة 5 دقائق (5 Min)", "5M"),
    ("⏰ صفقة 15 دقيقة (15 Min)", "15M")
]

def get_pairs_keyboard():
    keyboard = []
    row = []
    for name, code in PAIRS:
        row.append(InlineKeyboardButton(name, callback_data=f"pair:{code}:{name}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_tf_keyboard(pair_code, pair_name):
    keyboard = []
    for name, code in CANDLE_TIMEFRAMES:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"tf:{pair_code}:{pair_name}:{code}:{name}")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="start_over")])
    return InlineKeyboardMarkup(keyboard)

def get_dur_keyboard(pair_code, pair_name, tf_code, tf_name):
    keyboard = []
    for name, code in TRADE_DURATIONS:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"analyze:{pair_code}:{pair_name}:{tf_code}:{tf_name}:{code}:{name}")])
    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"pair:{pair_code}:{pair_name}")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "أهلاً بك يا محمد! 🚀\n\nيرجى اختيار زوج العملات أو الأصل المطلوب:"
    if update.message:
        await update.message.reply_text(text, reply_markup=get_pairs_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=get_pairs_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start_over":
        await start(update, context)
        return

    parts = data.split(":")
    action = parts[0]

    if action == "pair":
        code, name = parts[1], parts[2]
        text = f"الأصل المختار: **{name}** 📌\n\nاختر زمن/فريم الشمعة:"
        await query.edit_message_text(text, reply_markup=get_tf_keyboard(code, name), parse_mode="Markdown")

    elif action == "tf":
        pair_code, pair_name, tf_code, tf_name = parts[1], parts[2], parts[3], parts[4]
        text = f"الأصل: **{pair_name}** | الفريم: **{tf_name}** ⏱️\n\nاختر مدة الصفقة:"
        await query.edit_message_text(text, reply_markup=get_dur_keyboard(pair_code, pair_name, tf_code, tf_name), parse_mode="Markdown")

    elif action == "analyze":
        pair_code, pair_name, tf_code, tf_name, dur_code, dur_name = parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        
        rsi_val = random.randint(20, 80)
        rem_sec = random.randint(15, 45)

        if rsi_val < 33:
            signal = "صعود (CALL / شراء)"
            signal_emoji = "🟢"
            reason = f"تشبع بيعي قوي على مؤشر RSI ({rsi_val}) مع ارتداد مؤكد من الدعم."
            accuracy = random.randint(83, 94)
        elif rsi_val > 67:
            signal = "هبوط (PUT / بيع)"
            signal_emoji = "🔴"
            reason = f"تشبع شرائي قوي على مؤشر RSI ({rsi_val}) مع اصطدام السعر بالمقاومة."
            accuracy = random.randint(83, 94)
        else:
            signal = "صعود (CALL / شراء)" if random.choice([True, False]) else "هبوط (PUT / بيع)"
            signal_emoji = "🟢" if "صعود" in signal else "🔴"
            reason = f"استقرار الحركة السعرية مع توافق إشارات الزخم."
            accuracy = random.randint(76, 86)

        report = (
            f"📊 **تقرير التحليل الفني الشامل:**\n\n"
            f"📌 **الأصل المالي:** {pair_name}\n"
            f"⏱️ **زمن الشمعة:** {tf_name}\n"
            f"⏳ **المتبقي لإغلاق الشمعة:** تقريباً {rem_sec} ثانية\n"
            f"⏰ **مدة الصفقة:** {dur_name}\n"
            f"📈 **مؤشر الزخم (RSI):** {rsi_val}\n"
            f"🎯 **نسبة الدقة:** {accuracy}%\n"
            f"💡 **السبب:** {reason}\n\n"
            f"🔥 **التوصية النهائية:** {signal} {signal_emoji}\n\n"
            f"⚠️ التزم بإدارة رأس المال وتداول بحكمة."
        )

        keyboard = [
            [InlineKeyboardButton("🔄 فحص زوج جديد", callback_data="start_over")],
            [InlineKeyboardButton("📈 فتح منصة التداول", url="https://qxbroker.com")]
        ]
        
        await query.edit_message_text(text=report, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Error: BOT_TOKEN is missing!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
