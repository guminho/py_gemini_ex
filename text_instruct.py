from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        system_instruction="Talk like Hermione Granger",
        thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disables thinking
    ),
    contents="What is Hogswart",
)
print(response.text)
