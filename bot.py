from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ChatAction
import os
import asyncio
from ai_service import chat_ai, generate_image
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv("/home/Nasro77/ai_telegram_bot/.env")  # ضع المسار الكامل إذا لزم الأمر

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # هذا يستخدم في ai_service

# التأكد من تحميل المفاتيح
print("TELEGRAM_BOT_TOKEN =", "✔ موجود" if TELEGRAM_BOT_TOKEN else "❌ غير موجود")
print("OPENAI_API_KEY =", "✔ موجود" if OPENAI_API_KEY else "❌ غير موجود")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً! اسقسي أي سؤال.\n"
        "🖼️ لتوليد صورة استعمل:\n"
        "/img وصف الصورة"
    )

# التعامل مع النصوص
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.chat.send_action(ChatAction.TYPING)
    loop = asyncio.get_event_loop()
    reply = await loop.run_in_executor(None, chat_ai, msg)
    await update.message.reply_text(reply)

# توليد الصور
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✍️ اكتب وصف الصورة بعد /img")
        return
    prompt = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    loop = asyncio.get_event_loop()
    img_url = await loop.run_in_executor(None, generate_image, prompt)
    await update.message.reply_photo(img_url)

# نقطة البداية
def main():
    if not TELEGRAM_BOT_TOKEN:
        print("❌ خطأ: TELEGRAM_BOT_TOKEN غير موجود. تحقق من .env")
        return
    if not OPENAI_API_KEY:
        print("❌ خطأ: OPENAI_API_KEY غير موجود. تحقق من .env")
        return

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
