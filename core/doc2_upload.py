from pathlib import Path

from google import genai

client = genai.Client()

path = Path("1706.03762v7.pdf")
doc = client.files.upload(file=path)
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
