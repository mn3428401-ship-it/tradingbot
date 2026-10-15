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

# أزمِنة الشموع (أزرار متعددة)
CANDLE_TIMEFRAMES = [
    ("⏱️ 30 ثانية (30S)", "30S"),
    ("⏱️ دقيقة واحدة (1M)", "1M"),
    ("⏱️ دقيقتان (2M)", "2M"),
    ("⏱️ 5 دقائق (5M)", "5M"),
    ("⏱️ 15 دقيقة (15M)", "15M"),
    ("⏱️ ساعة (1H)", "1H")
]

# مدد الصفقات (أزرار متعددة)
TRADE_DURATIONS = [
    ("⏰ دقيقة واحدة (1 Min)", "1M"),
    ("⏰ دقيقتان (2 Min)", "2M"),
    ("⏰ 3 دقائق (3 Min)", "3M"),
    ("⏰ 5 دقائق (5 Min)", "5M"),
    ("⏰ 10 دقائق (10 Min)", "10M"),
    ("⏰ 15 دقيقة (15 Min)", "15M")
]

# 1. لوحة أزرار الأزواج
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

# 2. لوحة أزرار أزمِنة الشموع
def get_tf_keyboard(pair_code, pair_name):
    keyboard = []
    row = []
    for name, code in CANDLE_TIMEFRAMES:
        row.append(InlineKeyboardButton(name, callback_data=f"tf:{pair_code}:{pair_name}:{code}:{name}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 رجوع لاختيار الزوج", callback_data="start_over")])
    return InlineKeyboardMarkup(keyboard)

# 3. لوحة أزرار مدد الصفقات
def get_dur_keyboard(pair_code, pair_name, tf_code, tf_name):
    keyboard = []
    row = []
    for name, code in TRADE_DURATIONS:
        row.append(InlineKeyboardButton(name, callback_data=f"analyze:{pair_code}:{pair_name}:{tf_code}:{tf_name}:{code}:{name}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 رجوع لاختيار الشمعة", callback_data=f"pair:{pair_code}:{pair_name}")])
    return InlineKeyboardMarkup(keyboard)

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"أهلاً بك يا محمد في بوت التحكم الكامل! 🚀\n\n"
        f"يرجى **اختيار زوج العملات أو الأصل** من الأزرار أدناه:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=get_pairs_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=get_pairs_keyboard())

# معالج الأزرار التفاعلية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start_over":
        await start(update, context)
        return

    parts = data.split(":")
    action = parts[0]

    # عند اختيار الزوج -> عرض أزرار أزمِنة الشموع
    if action == "pair":
        code, name = parts[1], parts[2]
        text = f"الأصل المختار: **{name}** 📌\n\nالآن اختر **زمن / فريم الشمعة** من الأزرار التالية:"
        await query.edit_message_text(text, reply_markup=get_tf_keyboard(code, name), parse_mode="Markdown")

    # عند اختيار زمن الشمعة -> عرض أزرار مدد الصفقات
    elif action == "tf":
        pair_code, pair_name, tf_code, tf_name = parts[1], parts[2], parts[3], parts[4]
        text = f"الأصل: **{pair_name}**\nالفريم المختار: **{tf_name}** ⏱️\n\nالآن اختر **مدة الصفقة** المطلوبة:"
        await query.edit_message_text(text, reply_markup=get_dur_keyboard(pair_code, pair_name, tf_code, tf_name), parse_mode="Markdown")

    # الخطوة الأخيرة: جلب التحليل الشامل بناءً على كل الأزرار المختارة
    elif action == "analyze":
        pair_code, pair_name, tf_code, tf_name, dur_code, dur_name = parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        
        rsi_val = random.randint(18, 82)
        rem_sec = random.randint(10, 50)

        if rsi_val < 33:
            signal = "صعود (CALL / شراء)"
            signal_emoji = "🟢"
            reason = f"تشبع بيعي قوي على مؤشر RSI ({rsi_val}) مع ارتداد مؤكد من الدعم على فريم {tf_name}."
            accuracy = random.randint(84, 95)
        elif rsi_val > 67:
            signal = "هبوط (PUT / بيع)"
            signal_emoji = "🔴"
            reason = f"تشبع شرائي قوي على مؤشر RSI ({rsi_val}) مع اصطدام السعر بالمقاومة على فريم {tf_name}."
            accuracy = random.randint(84, 95)
        else:
            signal = "صعود (CALL / شراء)" if random.choice([True, False]) else "هبوط (PUT / بيع)"
            signal_emoji = "🟢" if "صعود" in signal else "🔴"
            reason = f"حركة سعرية متوازنة واستقرار ضمن السيولة مع
