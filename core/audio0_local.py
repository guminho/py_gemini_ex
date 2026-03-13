from pathlib import Path

from google import genai
from google.genai.types import Part

client = genai.Client()

data = Path("sample.wav").read_bytes()
au = Part.from_bytes(data=data, mime_type="audio/mp3")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["Describe this audio clip", au],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
