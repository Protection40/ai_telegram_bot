import os
from openai import OpenAI
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY غير موجود في متغيرات البيئة")

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_ai(message: str) -> str:
    """
    ترجع الرد من نموذج GPT-4.1-mini
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي، تجيب بدقة وبأسلوب واضح وبسيط."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7
        )
        # التحقق من وجود الرد
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        return "❌ لم أتمكن من توليد الرد."
    except Exception as e:
        return f"❌ خطأ: {e}"

def generate_image(prompt: str) -> str:
    """
    توليد صورة من وصف
    """
    try:
        image = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        if image.data and len(image.data) > 0:
            return image.data[0].url
        return ""
    except Exception as e:
        return f"❌ خطأ في توليد الصورة: {e}"
