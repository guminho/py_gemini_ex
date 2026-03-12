from google import genai
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    winner: str = Field(description="The name of the winner.")
    final_match_score: str = Field(description="The final match score.")
    scorers: list[str] = Field(description="The name of the scorer.")


client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Search for all details for the latest Euro.",
    config={
        "tools": [
            {"google_search": {}},
            {"url_context": {}},
        ],
        "response_mime_type": "application/json",
        "response_json_schema": MatchResult.model_json_schema(),
    },
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
