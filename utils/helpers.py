# utils/helpers.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = 'AIzaSyA96QHffl93JFQwOs2sMc8EsV4wBLOkTNs'       #os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# You can switch models here centrally
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")


def get_gemini_response(prompt: str, model=model) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {str(e)}"
