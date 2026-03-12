from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client()

path = Path("1706.03762v7.pdf")
data = path.read_bytes()
doc = types.Part.from_bytes(data=data, mime_type="application/pdf")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
