import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجل (Logs)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# جلب توكن البوت من المتغيرات البيئية
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# قاموس بسيط لتخزين حالة إيداعات المستخدمين (مؤقت لحين ربط قاعدة بيانات)
# المفتاح هو معرف المستخدم (User ID)، والقيمة هي المبلغ المودع
user_deposits = {}

# رابط منصة التداول أو الإيداع (يمكنك استبداله برابط إحالتك أو رابط المنصة)
DEPOSIT_URL = "https://pocketoption.com/"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # جلب إيداعات المستخدم (الافتراضي 0)
    current_deposit = user_deposits.get(user_id, 0)
    
    text = (
        f"🚀 **الخطوة 1 - تفعيل بوت التداول**\n\n"
        f"بقي القليل فقط. للحصول على الوصول، قم بتعبئة رصيدك بمبلغ لا يقل عن 5$[span_1](start_span)[span_1](end_span).\n\n"
        f"إجمالي إيداعاتك الحالية: **${current_deposit}**[span_2](start_span)[span_2](end_span)\n\n"
        f"بعد التعبئة اضغط تحقق وسنقوم بتحديث وصولك[span_3](start_span)[span_3](end_span)."
    )
    
    keyboard = [
        [InlineKeyboardButton("↗️ إيداع", url=DEPOSIT_URL)],
        [InlineKeyboardButton("✅ تحقق", callback_data='check_deposit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# التعامل مع الأزرار (مثل زر تحقق)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    current_deposit = user_deposits.get(user_id, 0)
    
    if query.data == 'check_deposit':
        if current_deposit >= 5:
            # إذا كان الرصيد كافياً
            success_text = (
                f"🎉 **تم التحقق بنجاح!**\n\n"
                f"إجمالي إيداعاتك: ${current_deposit}\n"
                f"حسابك مفعل الآن وجاهز لاستقبال الإشارات وتنفيذ الصفقات تلقائياً من السحابة 🚀"
            )
            keyboard = [[InlineKeyboardButton("📈 فتح لوحة التداول", callback_data='trading_menu')]]
            await query.edit_message_text(success_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        else:
            # إذا لم يتم الإيداع بعد أو أقل من 5$
            alert_text = (
                f"⚠️ **لم يتم تأكيد الإيداع بعد**\n\n"
                f"إجمالي إيداعاتك الحالية: ${current_deposit}[span_4](start_span)[span_4](end_span)\n"
                f"الرجاء إيداع مبلغ لا يقل عن 5$ عبر زر (إيداع) ثم المحاولة مرة أخرى[span_5](start_span)[span_5](end_span)."
            )
            keyboard = [
                [InlineKeyboardButton("↗️ إيداع", url=DEPOSIT_URL)],
                [InlineKeyboardButton("🔄 إعادة التحقق", callback_data='check_deposit')]
            ]
            await query.edit_message_text(alert_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
            
    elif query.data == 'trading_menu':
        await query.edit_message_text("📊 أهلاً بك في لوحة التداول السحابية. جارٍ ربط الأوامر بالحساب...")

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running with deposit & verification system...")
    app.run_polling()

if __name__ == "__main__":
    main()


