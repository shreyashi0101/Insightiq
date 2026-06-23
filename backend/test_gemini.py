from backend.gemini_service import model

response = model.generate_content(
    "Say hello in one sentence."
)

print(response.text)