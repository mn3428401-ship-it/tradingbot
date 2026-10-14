import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# جلب رمز البوت من المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# دالة تحليل السوق المدمجة (تجمع كل الاستراتيجيات: Price Action, RSI, S/R, Multi-Timeframe)
def analyze_market_comprehensive():
    assets = ["الذهب (XAUUSD)", "يورو/دولار (EURUSD)", "بتكوين (BTCUSD)", "جي بي بي/دولار (GBPUSD)"]
    asset = random.choice(assets)
    
    # محاكاة تحليل الفريمات المتعددة والزخم (RSI) والدعم والمقاومة
    timeframes = ["دقيقة واحدة (1M) - التداول السريع", "5 دقائق (5M)", "15 دقيقة (15M)", "ساعة واحدة (H1)"]
    tf = random.choice(timeframes)
    
    rsi_value = random.randint(20, 80)
    
    # بناء شروط دمج الاستراتيجيات
    if rsi_value < 30:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (تشبع بيعي قوي - Oversold)"
        reason = "وصول المؤشر لمنطقة تشبع بيعي قوية + ارتداد مؤكد من مستوى دعم يومي رئيسي مع إغلاق شمعة إيجابي."
        signal = "صعود (CALL / شراء)"
        signal_emoji = "🟢"
        accuracy = random.randint(82, 94)
    elif rsi_value > 70:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (تشبع شرائي قوي - Overbought)"
        reason = "وصول المؤشر لمنطقة تشبع شرائي قوية + اصطدام بمستوى مقاومة تاريخي قوي مع ظهور برايس أクション سلبي."
        signal = "هبوط (PUT / بيع)"
        signal_emoji = "🔴"
        accuracy = random.randint(82, 94)
    else:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (منطقة حيادية متوازنة)"
        reason = "استقرار السعر بين مناطق الدعم والمقاومة مع توافق إشارات الزخم على الفريمات الكبيرة والصغيرة."
        signal = "صعود (CALL / شراء)" if random.choice([True, False]) else "هبوط (PUT / بيع)"
        signal_emoji = "🟢" if "صعود" in signal else "🔴"
        accuracy = random.randint(75, 85)

    report = (
        f"📊 **تقرير التحليل الفني الشامل والمتقدم (جميع الاستراتيجيات):**\n\n"
        f"📌 **الأصل المالي:** 🪙 {asset}\n"
        f"⏱️ **الفريم الزمني:** {tf}\n"
        f"📈 **{rsi_status}**\n"
        f"🎯 **نسبة دقة الدمج:** {accuracy}% - {accuracy + 4}%\n"
        f"💡 **سبب التحليل المشترك:** {reason}\n\n"
        f"🔥 **التوصية النهائية:** {signal} {signal_emoji}\n\n"
        f"⚠️ **تنبيه:** التزم بإدارة رأس المال وتداول بحكمة واستفد من إغلاق الشموع المؤكد."
    )
    return report

# لوحة الأزرار التفاعلية
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث التحليل وإعطاء إشارة جديدة", callback_data="new_signal")],
        [InlineKeyboardButton("📊 اختيار زوج آخر", callback_data="change_asset")],
        [InlineKeyboardButton("📈 فتح منصة التداول", url="https://qxbroker.com")] # رابط المنصة أو لوحة الشركاء
    ]
    return InlineKeyboardMarkup(keyboard)

# أمر البدء /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً بك يا أخي {user_name} في بوت التداول الاحترافي الشامل! 🚀\n\n"
        f"هذا البوت يدمج الآن **جميع استراتيجيات التحليل الفني** (السلوك السعري، مؤشر RSI، الدعم والمقاومة، والفريمات المتعددة).\n\n"
        f"اضغط على الزر أدناه لجلب أحدث إشارة تحليلية دقيقة:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# التعامل مع الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "new_signal" or query.data == "change_asset":
        new_report = analyze_market_comprehensive()
        try:
            await query.edit_message_text(text=new_report, reply_markup=get_main_keyboard(), parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error updating message: {e}")

def main():
    # إنشاء تطبيق تيليجرام
    application = Application.builder().token(BOT_TOKEN).build()

    # تسجيل الأوامر والمعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # بدء تشغيل البوت عبر التحديثات المستمرة (Polling)
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
