# backend/list_models.py

import google.generativeai as genai
from backend.gemini_service import api_key

genai.configure(api_key=api_key)

for model in genai.list_models():
    print(model.name)