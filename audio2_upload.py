from pathlib import Path

from google import genai

client = genai.Client()

path = Path("sample.wav")
au = client.files.upload(file=path)
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=["Describe this audio clip", au],
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
