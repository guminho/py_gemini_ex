from pathlib import Path

from google import genai
from google.genai.types import Part

client = genai.Client()

data = Path("potter_snitch.jpeg").read_bytes()
img = Part.from_bytes(data=data, mime_type="image/jpeg")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[img, "Describe the image? Answer in one sentence."],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
