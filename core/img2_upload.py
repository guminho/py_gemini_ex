from google import genai

client = genai.Client()

image = client.files.upload(file="dumbledore_pensieve.jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe the image? Answer in one sentence."],
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
