from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is Albus Dumbledore? Answer in one sentence.",
    config=types.GenerateContentConfig(
        system_instruction="Talk like Hermione Granger",
        temperature=0.3,
    ),
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
