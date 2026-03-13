from google import genai
from google.genai.types import Part

client = genai.Client()

url = "https://arxiv.org/pdf/1706.03762"
doc = Part.from_uri(file_uri=url, mime_type="application/pdf")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
