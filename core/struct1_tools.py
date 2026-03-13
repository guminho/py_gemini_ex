from typing import Annotated

from google import genai
from google.genai.types import GenerateContentConfig, Tool
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    winner: Annotated[str, Field(description="The name of the winner.")]
    final_match_score: Annotated[str, Field(description="The final match score.")]
    scorers: Annotated[list[str], Field(description="The name of the scorer.")]


client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Search for all details for the latest Euro.",
    config=GenerateContentConfig(
        tools=[
            Tool(google_search={}),
            Tool(url_context={}),
        ],
        response_mime_type="application/json",
        response_json_schema=MatchResult.model_json_schema(),
    ),
)
print(f"{response.text}")
print(f"{response.usage_metadata.model_dump_json(exclude_none=True, indent=2)}")
