import requests
from google import genai
from google.genai.types import Part

client = genai.Client()

url = "https://arxiv.org/pdf/1706.03762"
data = requests.get(url).content
doc = Part.from_bytes(data=data, mime_type="application/pdf")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
