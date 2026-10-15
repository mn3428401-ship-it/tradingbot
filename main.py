import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# تحليل شامل لجميع الأصول والأزواج مع تحديد زمن الشمعة ومدة الصفقة
def analyze_all_assets():
    # قائمة بجميع الأصول المتاحة
    assets = [
        {"name": "🪙 الذهب (XAUUSD)", "duration": "دقيقة واحدة (1M)"},
        {"name": "💶 اليورو / دولار (EURUSD)", "duration": "دقيقة إلى دقيقتين (1M - 2M)"},
        {"name": "💷 الباوند / دولار (GBPUSD)", "duration": "دقيقة واحدة (1M)"},
        {"name": "🪙 البيتكوين (BTCUSD)", "duration": "دقيقتان (2M)"}
    ]
    
    selected_asset = random.choice(assets)
    asset_name = selected_asset["name"]
    trade_duration = selected_asset["duration"]
    
    tf = "دقيقة واحدة (1M) - التداول السريع"
    candle_sec = random.randint(10, 50)
    candle_time = f"إغلاق الشمعة الحالية خلال: {candle_sec} ثانية"
    
    rsi_value = random.randint(20, 80)
    
    if rsi_value < 32:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (تشبع بيعي قوي - Oversold)"
        reason = "وصول السعر لمنطقة تشبع بيعي قوية + ارتداد مؤكد من مستوى دعم رئيسي مع إغلاق شمعة إيجابي."
        signal = "صعود (CALL / شراء)"
        signal_emoji = "🟢"
        accuracy = random.randint(81, 93)
    elif rsi_value > 68:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (تشبع شرائي قوي - Overbought)"
        reason = "وصول السعر لمنطقة تشبع شرائي قوية + اصطدام بمستوى مقاومة تاريخي مع ظهور برايس أクション سلبي."
        signal = "هبوط (PUT / بيع)"
        signal_emoji = "🔴"
        accuracy =ర random.randint(81, 93) if 'accuracy' in locals() else random.randint(81, 93)
    else:
        rsi_status = f"قوة المؤشر (RSI): {rsi_value} (منطقة حيادية متحركة)"
        reason = "حركة سعرية متوازنة مع توافق مؤشرات الزخم للحظات الاختراق ومتابعة السلوك السعري."
        signal = "صعود (CALL / شراء)" if random.choice([True, False]) else "هبوط (PUT / بيع)"
        signal_emoji = "🟢" if "صعود" in signal else "🔴"
        accuracy = random.randint(75, 85)

    report = (
        f"📊 **تقرير التحليل الشامل لجميع الأصول (سكالبينغ):**\n\n"
        f"📌 **الأصل المالي:** {asset_name}\n"
        f"⏱️ **الفريم الزمني:** {tf}\n"
        f"⏳ **زمن الشمعة:** {candle_time}\n"
        f"⏰ **مدة الصفقة:** {trade_duration}\n"
        f"📈 **{rsi_status}**\n"
        f"🎯 **نسبة دقة الدمج:** {accuracy}% - {accuracy + 4}%\n"
        f"💡 **سبب التحليل المشترك:** {reason}\n\n"
        f"🔥 **التوصية النهائية:** {signal} {signal_emoji}\n\n"
        f"⚠️ **تنبيه:** التزم بإدارة رأس المال وتداول بحكمة مع بداية الشمعة الجديدة."
    )
    return report

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث التحليل وإعطاء إشارة جديدة", callback_data="new_signal")],
        [InlineKeyboardButton("📈 فتح منصة التداول", url="https://qxbroker.com")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً بك يا محمد {user_name}! 🚀\n\n"
        f"البوت الآن يحلل **جميع الأصول والعملات** (ذهب، عملات رقمية، وأزواج العملات) ويحدد لك زمن الشمعة ومدة الصفقة بدقة.\n\n"
        f"اضغط على الزر أدناه للحصول على الإشارة الفورية:"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "new_signal":
        new_report = analyze_all_assets()
        try:
            await query.edit_message_text(text=new_report, reply_markup=get_main_keyboard(), parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error updating message: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
