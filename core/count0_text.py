from google import genai

client = genai.Client()
model = "gemini-3-flash-preview"
prompt = "The quick brown fox jumps over the lazy dog."

tokens = client.models.count_tokens(model=model, contents=prompt)
print(f"{tokens=}")

response = client.models.generate_content(model=model, contents=prompt)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
