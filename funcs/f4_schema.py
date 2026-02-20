from typing import Literal

from google.genai.types import FunctionDeclaration


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


fn_decl = FunctionDeclaration.from_callable_with_api_option(callable=set_light_values)
print(fn_decl.model_dump_json(exclude_none=True))
