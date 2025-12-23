import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_ai(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "أنت مساعد ذكي، تجيب بدقة وبأسلوب واضح وبأسلوب مفهوم."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def generate_image(prompt: str) -> str:
    image = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return image.data[0].url

