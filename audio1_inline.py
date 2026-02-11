from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client()

path = Path("sample.wav")
data = path.read_bytes()
au = types.Part.from_bytes(data=data, mime_type="audio/mp3")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["Describe this audio clip", au],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
