import json

from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

image = Image.open("dumbledore_pensieve.jpeg")
prompt = "Detect the wand in this image."
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, prompt],
    config=types.GenerateContentConfig(response_mime_type="application/json"),
)

width, height = image.size
bounding_boxes = json.loads(response.text)
# box_2d: [ymin, xmin, ymax, xmax] normalized to 0-1000

origin_boxes = []
for box in bounding_boxes:
    abs_y1 = int(box["box_2d"][0] / 1000 * height)
    abs_x1 = int(box["box_2d"][1] / 1000 * width)
    abs_y2 = int(box["box_2d"][2] / 1000 * height)
    abs_x2 = int(box["box_2d"][3] / 1000 * width)
    origin_boxes.append([abs_x1, abs_y1, abs_x2, abs_y2])

print("Image size: ", width, height)
print("Boxes scaled:", bounding_boxes)
print("Boxes origin:", origin_boxes)
