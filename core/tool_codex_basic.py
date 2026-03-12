from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the sum of the first 30 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 30.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})],
    ),
)
PANEL = "*" * 10
for idx, part in enumerate(response.candidates[0].content.parts):
    if out := part.text:
        print(f"{PANEL} #{idx}. Answer {PANEL}\n{out}\n")
    if out := part.executable_code:
        print(f"{PANEL} #{idx}. Code {PANEL}\n{out.code}\n")
    if out := part.code_execution_result:
        print(f"{PANEL} #{idx}. Output {PANEL}\n{out.output}\n")
print(f"{response.usage_metadata=}")
