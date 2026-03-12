from google import genai

# export GOOGLE_API_KEY=
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is the only Slytherin Headmaster known for his lifelong unrequited love for a Muggle-born Gryffindor?",
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
