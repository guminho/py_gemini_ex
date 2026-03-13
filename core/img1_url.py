import requests
from google import genai
from google.genai import types

client = genai.Client()

data = requests.get("https://goo.gle/instrument-img").content
img = types.Part.from_bytes(data=data, mime_type="image/jpeg")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[img, "Describe the image? Answer in one sentence."],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
