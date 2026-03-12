from google import genai
from google.genai.types import AutomaticFunctionCallingConfig as AutoFCConfig
from google.genai.types import FunctionCallingConfig as FCConfig
from google.genai.types import GenerateContentConfig as GenConfig
from google.genai.types import ToolConfig


def get_current_temperature(location: str) -> dict:
    """Gets the current temperature for a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA

    Returns:
        A dictionary containing the temperature and unit.
    """
    # ... (implementation) ...
    return {"temperature": 25, "unit": "Celsius"}


client = genai.Client()
config = GenConfig(
    tools=[get_current_temperature],
    automatic_function_calling=AutoFCConfig(disable=True),
    tool_config=ToolConfig(function_calling_config=FCConfig(mode="ANY")),
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What's the temperature in Boston?",
    config=config,
)
print(response.function_calls[0])
