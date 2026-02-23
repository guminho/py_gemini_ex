from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})],
    ),
)

response = chat.send_message("I have a math question for you.")
print(response.text)

response = chat.send_message(
    "What is the sum of the first 50 prime numbers? "
    "Generate and run code for the calculation, and make sure you get all 50."
)
PANEL = "*" * 10
for idx, part in enumerate(response.candidates[0].content.parts):
    if out := part.text:
        print(f"{PANEL} #{idx}. Answer {PANEL}\n{out}\n")
    if out := part.executable_code:
        print(f"{PANEL} #{idx}. Code {PANEL}\n{out.code}\n")
    if out := part.code_execution_result:
        print(f"{PANEL} #{idx}. Output {PANEL}\n{out.output}\n")
