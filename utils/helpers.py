# utils/helpers.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = "AIzaSyAbHFT87clVzIHF4DD900AaJRqehQ8uB50" #os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# You can switch models here centrally
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")


def get_gemini_response(prompt: str, model=model) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {str(e)}"

def get_gemini_embeddings(texts: list) -> list:
    """
    Uses Gemini to generate embeddings for a list of texts.
    Returns a list of embedding vectors.
    """
    try:
        embedding_model = genai.EmbeddingModel(model_name="models/embedding-001")
        response = embedding_model.embed_content(content=texts, task_type="retrieval_document")
        return [item.values for item in response.embeddings]
    except Exception as e:
        raise RuntimeError(f"Failed to get embeddings: {str(e)}")