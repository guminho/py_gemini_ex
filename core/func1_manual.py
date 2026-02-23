from typing import Literal

from google import genai
from google.genai.types import Content, FunctionDeclaration, Part, Tool
from google.genai.types import GenerateContentConfig as GenConfig


# 1. Define func
def set_light_values(
    brightness: int,
    color_temp: Literal["daylight", "cool", "warm"],
) -> dict[str, int | str]:
    """Set the brightness and color temperature of a room light. (mock API).

    Args:
        brightness: Light level from 0 to 100. Zero is off and 100 is full brightness
        color_temp: Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.

    Returns:
        A dictionary containing the set brightness and color temperature.
    """
    return {"brightness": brightness, "colorTemperature": color_temp}


client = genai.Client()
fn_decl = FunctionDeclaration.from_callable_with_api_option(callable=set_light_values)
tools = [Tool(function_declarations=[fn_decl])]
contents = []


# 2. Func call
prompt = "Turn the lights down to a romantic level"
contents.append(Content(role="user", parts=[Part(text=prompt)]))
response_1 = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=GenConfig(tools=tools),
)
fc = response_1.function_calls[0]
print("Function call:", fc)


# 3. Execute func
if fc.name == set_light_values.__name__:
    result = set_light_values(**fc.args)
    print("Function response:", result)


# 4. Final Answer
contents.append(response_1.candidates[0].content)
contents.append(
    Content(
        role="user",
        parts=[Part.from_function_response(name=fc.name, response={"result": result})],
    )
)
response_2 = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=contents,
    config=GenConfig(tools=tools),
)
print("Answer:", response_2.text)
