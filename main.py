from fastapi import FastAPI
from pydantic import BaseModel
import openai
from googletrans import Translator
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
translator = Translator()

BUSINESS_CONTEXT = '''
You are an AI assistant for a local coaching center in India.
You answer in simple, friendly language.

Sample FAQs:
Q: क्या क्लासेस ऑनलाइन हैं?
A: हां, हमारी क्लासेस ऑनलाइन और ऑफलाइन दोनों होती हैं।
Q: फीस कितनी है?
A: कोर्स के अनुसार फीस अलग-अलग होती है। कृपया कोर्स बताएं।
Q: डेमो क्लास मिलता है क्या?
A: हां, एक फ्री डेमो क्लास उपलब्ध है।
'''

class UserMessage(BaseModel):
    message: str
    language: str = "hi"

@app.post("/chat")
async def chat_with_bot(user_input: UserMessage):
    translated = translator.translate(user_input.message, src=user_input.language, dest='en')
    english_input = translated.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": BUSINESS_CONTEXT},
            {"role": "user", "content": english_input}
        ]
    )
    english_reply = response['choices'][0]['message']['content']
    final_reply = translator.translate(english_reply, src='en', dest=user_input.language).text

    return {
        "user_input": user_input.message,
        "bot_reply": final_reply
    }
