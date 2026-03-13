from pathlib import Path

from google import genai
from google.genai.types import Part

client = genai.Client()

data = Path("1706.03762v7.pdf").read_bytes()
doc = Part.from_bytes(data=data, mime_type="application/pdf")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
