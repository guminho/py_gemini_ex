from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client()
model_name = "gemini-3-flash-preview"

path = Path("1706.03762v7.pdf")
document = client.files.upload(file=path)

# Create a cached content object
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
        system_instruction="You are an expert analyzing research papers.",
        contents=[document],
    ),
)
print(f"{cache=}")

response = client.models.generate_content(
    model=model_name,
    contents="Please summarize this paper",
    config=types.GenerateContentConfig(
        cached_content=cache.name,
    ),
)
print("Answer:\n", response.text)
print(f"{response.usage_metadata=}")
