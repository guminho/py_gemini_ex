from google import genai

client = genai.Client()

doc = client.files.upload(file="1706.03762v7.pdf")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[doc, "Summarize this document"],
)
print(f"{response.text=}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
