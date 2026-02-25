from pathlib import Path

from google import genai
from google.genai.types import Part

client = genai.Client()

EXT = {
    ".html": "text/html",
    ".css": "text/css",
    ".txt": "text/plain",
    ".xml": "text/xml",
    ".csv": "text/csv",
    ".rtf": "text/rtf",
    ".js": "text/javascript",
    ".md": "text/markdown",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".bmp": "image/bmp",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def count(path: Path) -> int:
    mime = EXT[path.suffix.lower()]
    file = Part.from_bytes(data=path.read_bytes(), mime_type=mime)

    return client.models.count_tokens(
        model="gemini-3-flash-preview",
        contents=[file, "Tell me about this file."],
    )


path = Path("potter_snitch.jpeg")
tokens = count(path)
print(f"{tokens.total_tokens:<8}:{path.name}")
