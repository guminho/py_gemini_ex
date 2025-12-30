from google import genai

# export GOOGLE_API_KEY=
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is the author of Lord of the Ring",
)
print(response.text)
