from google import genai
from google.genai import types

client = genai.Client()

url = "https://www.klook.com/vi/blog/dia-diem-du-lich-da-lat/"
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=f"Give me three day events schedule based on {url}. Also let me know what needs to taken care of considering weather and commute.",
    config=types.GenerateContentConfig(
        tools=[
            types.Tool(url_context={}),
            types.Tool(google_search={}),
        ],
    ),
)
cand = response.candidates[0]
print(cand.content.parts[0].text)
if x := cand.grounding_metadata:
    print(x.web_search_queries)
if x := cand.url_context_metadata:
    print(x.url_metadata)
print(f"{response.usage_metadata=}")
