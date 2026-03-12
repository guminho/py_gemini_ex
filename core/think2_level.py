from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the sum of the first 30 prime numbers?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="minimal",
            # thinking_budget=0,
        )
    ),
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
