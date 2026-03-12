import io

import requests
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

image_path = "https://goo.gle/instrument-img"
image_bytes = requests.get(image_path).content
image = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        image,
        "Zoom into the expression pedals and tell me how many pedals are there?",
    ],
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
    if out := part.as_image():
        print(f"{PANEL} #{idx}. Image {PANEL}\n")
        img = Image.open(io.BytesIO(out.image_bytes))
        img.show()  # Opens in a standalone window
print(f"{response.usage_metadata=}")
