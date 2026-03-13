from google import genai

client = genai.Client()

au = client.files.upload(file="sample.wav")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["Describe this audio clip", au],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
