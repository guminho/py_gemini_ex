from google import genai

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="What is Hogswart",
)
for chunk in response:
    print(chunk.text, end="")
print()
