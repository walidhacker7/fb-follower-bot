from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
import subprocess

# مراحل المحادثة
LINK, COUNT = range(2)

# توكن البوت
TOKEN = "7664125256:AAEI6wi3dvbe4M-fZqhl5D33LpZj-AplG2U"

# (اختياري) تحديد مستخدم واحد فقط يسمح له باستخدام البوت
ALLOWED_USER_ID = 7074806886

# تخزين البيانات مؤقتًا
user_data_store = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("❌ غير مسموح لك باستخدام هذا البوت.")
        return ConversationHandler.END

    await update.message.reply_text("👋 أهلا بيك! ابعتلي رابط صفحة فيسبوك:")
    return LINK

# المرحلة الأولى: استلام الرابط
async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_store[update.effective_user.id] = {"link": update.message.text}
    await update.message.reply_text("✅ تمام، ابعتلي عدد الحسابات اللي تتابع:")
    return COUNT

# المرحلة الثانية: عدد الحسابات
async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data_store:
        await update.message.reply_text("❌ حصل خطأ داخلي.")
        return ConversationHandler.END

    link = user_data_store[user_id]["link"]
    count = update.message.text.strip()

    await update.message.reply_text(f"🚀 جاري تنفيذ المتابعة من {count} حساب...")

    try:
        # تشغيل السكربت الخارجي
        subprocess.run(["python", "follow_script.py", link, count])
        await update.message.reply_text("✅ تمت المتابعة بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"❌ حصل خطأ أثناء التنفيذ: {str(e)}")

    return ConversationHandler.END

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم الإلغاء.")
    return ConversationHandler.END

# تشغيل البوت
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link)],
            COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("🤖 البوت شغال... انتظر الرسائل في تليجرام.")
    app.run_polling()
