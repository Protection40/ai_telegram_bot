from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
import os
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
from ai_service import chat_ai, generate_image

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً! اسقسي أي سؤال.\n"
        "🖼️ لتوليد صورة استعمل:\n"
        "/img وصف الصورة"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.chat.send_action("typing")
    reply = chat_ai(msg)
    await update.message.reply_text(reply)

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✍️ اكتب وصف الصورة بعد /img")
        return

    prompt = " ".join(context.args)
    await update.message.chat.send_action("upload_photo")
    img_url = generate_image(prompt)
    await update.message.reply_photo(img_url)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
