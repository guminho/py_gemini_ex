from pathlib import Path

from google import genai

client = genai.Client()

path = Path("1706.03762v7.pdf")
doc = client.files.upload(file=path)
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
