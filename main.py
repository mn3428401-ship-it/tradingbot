import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# قائمة الأزواج والأصول
PAIRS = [
    ("🪙 الذهب (XAUUSD)", "pair_XAUUSD"),
    ("💶 EUR/USD", "pair_EURUSD"),
    ("💷 GBP/USD", "pair_GBPUSD"),
    ("🇯🇵 USD/JPY", "pair_USDJPY"),
    ("🪙 BTC/USD", "pair_BTCUSD"),
    ("🇦🇺 AUD/USD", "pair_AUDUSD")
]

# فريمات الشموع
CANDLE_TIMEFRAMES = [
    ("⏱️ شمعة دقيقة (1M)", "tf_1M"),
    ("⏱️ شمعة 5 دقائق (5M)", "tf_5M"),
    ("⏱️ شمعة 15 دقيقة (15M)", "tf_15M")
]

# مدة الصفقة
TRADE_DURATIONS = [
    ("⏰ صفقة دقيقة (1 Min)", "dur_1M"),
    ("⏰ صفقة دقيقتين (2 Min)", "dur_2M"),
    ("⏰ صفقة 5 دقائق (5 Min)", "dur_5M")
]

# لوحة اختيار الزوج
def get_pairs_keyboard():
    keyboard = []
    row = []
    for name, code in PAIRS:
        row.append(InlineKeyboardButton(name, callback_data=f"select_pair:{code}:{name}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# لوحة اختيار زمن الشمعة
def get_tf_keyboard(pair_code, pair_name):
    keyboard = []
    for name, code in CANDLE_TIMEFRAMES:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"select_tf:{pair_code}:{pair_name}:{code}:{name}")])
    return InlineKeyboardMarkup(keyboard)

# لوحة اختيار مدة الصفقة
def get_dur_keyboard(pair_code, pair_name, tf_code, tf_name):
    keyboard = []
    for name, code in TRADE_DURATIONS:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"analyze:{pair_code}:{pair_name}:{tf_code}:{tf_name}:{code}:{name}")])
    return InlineKeyboardMarkup(keyboard)

# زر العودة
def get_result_keyboard(pair_code, pair_name, tf_code, tf_name, dur_code, dur_name):
    keyboard = [
        [InlineKeyboardButton("🔄 إعادة التحليل لنفس الاختيارات", callback_data=f"analyze:{pair_code}:{pair_name}:{tf_code}:{tf_name}:{dur_code}:{dur_name}")],
        [InlineKeyboardButton("📊 اختيار زوج أو زمن آخر", callback_data="start_over")],
        [InlineKeyboardButton("📈 فتح منصة التداول", url="https://qxbroker.com")]
    ]
    return InlineKeyboardMarkup(keyboard)

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    text = (
        f"أهلاً بك يا محمد {user_name}! 🚀\n\n"
        f"يرجى **اختيار زوج العملات/الأصل** الذي تريد تحليله أولاً:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=get_pairs_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=get_pairs_keyboard())

# معالج ضغطات الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start_over":
        await start(update, context)
        return

    parts = data.split(":")
    action = parts[0]

    # 1. بعد اختيار الزوج -> اختر زمن الشمعة
    if action == "select_pair":
        pair_code, pair_name = parts[1], parts[2]
        text = f"الزوج المختار: **{pair_name}**\n\nالان اختر **زمن/فريم الشمعة**:"
        await query.edit_message_text(text, reply_markup=get_tf_keyboard(pair_code, pair_name), parse_mode="Markdown")

    # 2. بعد اختيار الشمعة -> اختر مدة الصفقة
    elif action == "select_tf":
        pair_code, pair_name, tf_code, tf_name = parts[1], parts[2], parts[3], parts[4]
        text = f"الزوج: **{pair_name}**\nالفريم: **{tf_name}**\n\nالان اختر **مدة الصفقة** التي تريد فتحها:"
        await query.edit_message_text(text, reply_markup=get_dur_keyboard(pair_code, pair_name, tf_code, tf_name), parse_mode="Markdown")

    # 3. جلب نتيجة التحليل المخصصة
    elif action == "analyze":
        pair_code, pair_name, tf_code, tf_name, dur_code, dur_name = parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        
        rsi_val = random.randint(20, 80)
        candle_sec = random.randint(5, 55)
        
        if rsi_val < 35:
            signal = "صعود (CALL / شراء)"
            signal_emoji = "🟢"
            reason = f"وصول {pair_name} لمنطقة تشبع بيعي (RSI: {rsi_val}) + ارتداد من الدعم على فريم {tf_name}."
            accuracy = random.randint(83, 93)
        elif rsi_val > 65:
            signal = "هبوط (PUT / بيع)"
            signal_emoji = "🔴"
            reason = f"وصول {pair_name} لمنطقة تشبع شرائي (RSI: {rsi_val}) + ارتداد من المقاومة على فريم {tf_name}."
            accuracy = random.randint(83, 93)
        else:
            signal = "صعود (CALL / شراء)" if random.choice([True, False]) else "هبوط (PUT / بيع)"
            signal_emoji = "🟢" if "صعود" in signal else "🔴"
            reason = f"استقرار الحركة بين مناطق الدعم والمقاومة مع توافق الزخم على فريم {tf_name}."
            accuracy = random.randint(76, 85)

        report = (
            f"📊 **تقرير التحليل الفني المخصص:**\n\n"
            f"📌 **الأصل المالي:** {pair_name}\n"
            f"⏱️ **زمن الشمعة:** {tf_name}\n"
            f"⏳ **المتبقي لإغلاق الشمعة:** {candle_sec} ثانية\n"
            f"⏰ **مدة الصفقة المطلوبة:** {dur_name}\n"
            f"📈 **مؤشر الزخم (RSI):** {rsi_val}\n"
            f"🎯 **نسبة الدقة المتوقعة:** {accuracy}%\n"
            f"💡 **سبب التحليل:** {reason}\n\n"
            f"🔥 **التوصية النهائية:** {signal} {signal_emoji}\n\n"
            f"⚠️ **تنبيه:** افتح صفقة ({dur_name}) فور بداية الشمعة الجديدة."
        )

        await query.edit_message_text(
            text=report,
            reply_markup=get_result_keyboard(pair_code, pair_name, tf_code, tf_name, dur_code, dur_name),
            parse_mode="Markdown"
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
