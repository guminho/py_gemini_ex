from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the sum of the first 30 prime numbers?",
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
