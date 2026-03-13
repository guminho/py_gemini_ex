from google import genai

client = genai.Client()

img = client.files.upload(file="dumbledore_pensieve.jpeg")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[img, "Describe the image? Answer in one sentence."],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
