import os
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ChatAction

from openai import OpenAI

# =============================
# تحميل المتغيرات من .env
# =============================
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN غير موجود")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY غير موجود")

# =============================
# OpenAI Client
# =============================
client = OpenAI(api_key=OPENAI_API_KEY)

# =============================
# AI Chat Function
# =============================
def chat_ai(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي، واضح، مختصر، ومفيد."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ OpenAI: {e}"

# =============================
# AI Image Function
# =============================
def generate_image(prompt: str) -> str:
    try:
        image = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        return image.data[0].url
    except Exception as e:
        return f"❌ خطأ توليد صورة: {e}"

# =============================
# Telegram Handlers
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً!\n"
        "اسقسي أي سؤال ✨\n\n"
        "🖼️ توليد صورة:\n"
        "/img وصف الصورة"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action(ChatAction.TYPING)
    msg = update.message.text
    loop = asyncio.get_event_loop()
    reply = await loop.run_in_executor(None, chat_ai, msg)
    await update.message.reply_text(reply)

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("✍️ اكتب وصف الصورة بعد /img")
        return

    prompt = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    loop = asyncio.get_event_loop()
    img_url = await loop.run_in_executor(None, generate_image, prompt)

    if img_url.startswith("http"):
        await update.message.reply_photo(img_url)
    else:
        await update.message.reply_text(img_url)

# =============================
# Main
# =============================
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("img", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
