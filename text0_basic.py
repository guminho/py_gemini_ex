from google import genai

# export GOOGLE_API_KEY=
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is Albus Dumbledore? Answer in one sentence.",
)
print(response.text)
print(response.usage_metadata)
