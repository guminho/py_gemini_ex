from google import genai
from google.genai.types import GenerateContentConfig, Tool

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Who won the euro 2024? Answer in one sentence.",
    config=GenerateContentConfig(
        tools=[Tool(google_search={})],
    ),
)
cand = response.candidates[0]
print(cand.content.parts[0].text)
print(f"{cand.grounding_metadata.web_search_queries=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
