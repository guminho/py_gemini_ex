from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who won the euro 2024? Answer in one sentence.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})],
    ),
)
part = response.candidates[0]
print(part.grounding_metadata.web_search_queries)
print(part.content.parts[0].text)
