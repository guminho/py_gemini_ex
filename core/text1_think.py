from google import genai
from google.genai import types

# export GOOGLE_API_KEY=
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who is the only Slytherin Headmaster known for his lifelong unrequited love for a Muggle-born Gryffindor?",
    config=types.GenerateContentConfig(
        system_instruction="Talk like Hermione Granger",
        temperature=1.0,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
