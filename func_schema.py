from google import genai
from google.genai import types


def multiply(a: float, b: float):
    """Returns a * b."""
    return a * b


client = genai.Client()
fn_decl = types.FunctionDeclaration.from_callable(callable=multiply, client=client)
print(fn_decl.to_json_dict())
