from google import genai
from google.genai import types

client = genai.Client()

with open("dumbledore_pensieve.jpeg", "rb") as f:
    image = types.Part.from_bytes(data=f.read(), mime_type="image/jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe the image? Answer in one sentence."],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
