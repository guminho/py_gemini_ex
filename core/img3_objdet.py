import json

from google import genai
from google.genai import types
from PIL import Image, ImageDraw

client = genai.Client()

img = Image.open("potter_snitch.jpeg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[img, "Detect Snitch in this image."],
    config=types.GenerateContentConfig(response_mime_type="application/json"),
)

width, height = img.size
bounding_boxes = json.loads(response.text)
# box_2d: [ymin, xmin, ymax, xmax] normalized to 0-1000

draw = ImageDraw.Draw(img)
for box in bounding_boxes:
    abs_y1 = int(box["box_2d"][0] / 1000 * height)
    abs_x1 = int(box["box_2d"][1] / 1000 * width)
    abs_y2 = int(box["box_2d"][2] / 1000 * height)
    abs_x2 = int(box["box_2d"][3] / 1000 * width)
    origin_box = [abs_x1, abs_y1, abs_x2, abs_y2]
    draw.rectangle(origin_box, outline="red")

print(f"{bounding_boxes=}")
img.show()
