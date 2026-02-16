from google import genai
from google.genai import types

client = genai.Client()

youtube_url = "https://www.youtube.com/watch?v=ku-N-eS1lgM"
prompt = """
  Process the audio file and generate a detailed transcription.

  Requirements:
  1. Identify distinct speakers (e.g., Speaker 1, Speaker 2, or names if context allows).
  2. Provide accurate timestamps for each segment (Format: MM:SS).
  3. Detect the primary language of each segment.
  4. If the segment is in a language different than English, also provide the English translation.
  5. Identify the primary emotion of the speaker in this segment. You MUST choose exactly one of the following: Happy, Sad, Angry, Neutral.
  6. Provide a brief summary of the entire audio at the beginning.
"""
schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "summary": types.Schema(
            type=types.Type.STRING,
            description="A concise summary of the audio content.",
        ),
        "segments": types.Schema(
            type=types.Type.ARRAY,
            description="List of transcribed segments with speaker and timestamp.",
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "speaker": types.Schema(type=types.Type.STRING),
                    "timestamp": types.Schema(type=types.Type.STRING),
                    "content": types.Schema(type=types.Type.STRING),
                    "language": types.Schema(type=types.Type.STRING),
                    "language_code": types.Schema(type=types.Type.STRING),
                    "translation": types.Schema(type=types.Type.STRING),
                    "emotion": types.Schema(
                        type=types.Type.STRING,
                        enum=["happy", "sad", "angry", "neutral"],
                    ),
                },
                required=[
                    "speaker",
                    "timestamp",
                    "content",
                    "language",
                    "language_code",
                    "emotion",
                ],
            ),
        ),
    },
    required=["summary", "segments"],
)


response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part(file_data=types.FileData(file_uri=youtube_url)),
        types.Part(text=prompt),
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema,
    ),
)
print(response.text)
print(response.usage_metadata.model_dump_json(indent=2))
