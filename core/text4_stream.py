from google import genai

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Who is Albus Dumbledore? Give me 3 essential bullet points.",
)
for chunk in response:
    print(chunk.text, end="")
print()
print(f"{chunk.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
