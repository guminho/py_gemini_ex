from typing import Literal

from google import genai
from pydantic import BaseModel, Field

TYPE_SPAM = Literal["phishing", "scam", "unsolicited promotion", "other"]


class SpamDetails(BaseModel):
    reason: str = Field(description="The reason why the content is considered spam.")
    spam_type: TYPE_SPAM = Field(description="The type of spam.")


class NotSpamDetails(BaseModel):
    summary: str = Field(description="A brief summary of the content.")
    is_safe: bool = Field(description="Whether the content is safe for all audiences.")


class ModerationResult(BaseModel):
    decision: SpamDetails | NotSpamDetails


client = genai.Client()

prompt = """
Please moderate the following content and provide a decision.
Content: 'Congratulations! You''ve won a free cruise to the Bahamas. Click here to claim your prize: www.definitely-not-a-scam.com'
"""
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": ModerationResult.model_json_schema(),
    },
)
print(f"{response.text=}")
print(f"{response.usage_metadata=}")
