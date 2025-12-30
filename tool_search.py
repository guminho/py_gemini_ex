from google import genai
from google.genai import types

client = genai.Client()
tools = types.Tool(google_search=types.GoogleSearch())
config = types.GenerateContentConfig(tools=[tools])


response = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Who won the euro 2024?",
    config=config,
)
answer = ""
for chunk in response:
    print(chunk.text, end="")
    answer += chunk.text
print()
meta = chunk.candidates[0].grounding_metadata


def add_citations(answer: str, meta: types.GroundingMetadata):
    text = answer.encode()  # as indices measured in bytes
    chunks = meta.grounding_chunks
    supports = meta.grounding_supports
    # Sort end_index in descending to avoid shifting issues when inserting.
    sorted_supports: list[types.GroundingSupport] = sorted(
        supports, key=lambda sp: sp.segment.end_index, reverse=True
    )
    for sp in sorted_supports:
        end_index = sp.segment.end_index
        links = []
        for i in sp.grounding_chunk_indices[:2]:
            links.append(f"[{chunks[i].web.title}]({chunks[i].web.uri})".encode())
        text = text[:end_index] + b",".join(links) + text[end_index:]
    return text.decode()


print("\n\n@inline_citations\n")
print(add_citations(answer, meta))
