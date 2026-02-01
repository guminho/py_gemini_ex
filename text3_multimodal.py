from google import genai
from PIL import Image

client = genai.Client()

image = Image.open("dumbledore_pensieve.jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe the image? Answer in one sentence."],
)
print(response.text)
print(response.usage_metadata)
