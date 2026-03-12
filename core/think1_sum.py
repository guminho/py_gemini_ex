from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the sum of the first 30 prime numbers?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    ),
)
for part in response.candidates[0].content.parts:
    if not part.text:
        continue
    if part.thought:
        print(f"Thought summary:\n{part.text}\n")
    else:
        print(f"Answer:\n{part.text}\n")
print(f"{response.usage_metadata=}")
