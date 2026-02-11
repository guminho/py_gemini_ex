import requests
from google import genai
from google.genai import types

client = genai.Client()

url = "https://goo.gle/instrument-img"
data = requests.get(url).content
img = types.Part.from_bytes(data=data, mime_type="image/jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[img, "Describe the image? Answer in one sentence."],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
