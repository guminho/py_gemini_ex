from google import genai
from google.genai.types import Content, Part

client = genai.Client()
model = "gemini-3-flash-preview"

chat = client.chats.create(
    model=model,
    history=[
        Content(role="user", parts=[Part(text="Hi my name is Bob")]),
        Content(role="model", parts=[Part(text="Hi Bob!")]),
    ],
)

extra = [Part(text="In one sentence, who is Albus Dumbledore?")]
tokens = client.models.count_tokens(model=model, contents=[*chat.get_history(), extra])
print(f"{tokens=}")

response = chat.send_message(message=extra)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
