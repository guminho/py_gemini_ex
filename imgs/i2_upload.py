from google import genai

client = genai.Client()

image = client.files.upload(file="dumbledore_pensieve.jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe the image? Answer in one sentence."],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
