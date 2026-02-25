from google import genai

client = genai.Client()
model = "gemini-3-flash-preview"
prompt = "In one sentence, tell me about this image"
img = client.files.upload(file="potter_snitch.jpeg")

tokens = client.models.count_tokens(model=model, contents=[prompt, img])
print(f"{tokens=}")

response = client.models.generate_content(model=model, contents=[prompt, img])
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
