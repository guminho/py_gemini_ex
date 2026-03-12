from google import genai
from google.genai import types

client = genai.Client()

url1 = "https://openai.com/index/hello-gpt-4o/"
url2 = "https://openai.com/index/introducing-o3-and-o4-mini/"

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=f"Compare these models at {url1} and {url2}",
    config=types.GenerateContentConfig(
        tools=[types.Tool(url_context={})],
    ),
)
cand = response.candidates[0]
print(cand.content.parts[0].text)
if metas := cand.url_context_metadata.url_metadata:
    for meta in metas:
        print(meta.url_retrieval_status.value, meta.retrieved_url)
print(f"{response.usage_metadata=}")
