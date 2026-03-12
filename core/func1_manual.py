from decl_genai import fn_decl, set_light_values
from google import genai
from google.genai.types import Content, Part, Tool
from google.genai.types import GenerateContentConfig as GenConfig

client = genai.Client()
model = "gemini-3-flash-preview"
tools = [Tool(function_declarations=[fn_decl])]
contents = []


# Func call
prompt = "Turn the lights down to a romantic level"
contents.append(Content(role="user", parts=[Part(text=prompt)]))
response_1 = client.models.generate_content(
    model=model,
    contents=contents,
    config=GenConfig(tools=tools),
)
contents.append(response_1.candidates[0].content)
fc = response_1.function_calls[0]
print("Function call:", fc)


# Execute func
assert fc.name == set_light_values.__name__
result = set_light_values(**fc.args)
print("Function response:", result)


# Final Answer
contents.append(
    Content(
        role="user",
        parts=[Part.from_function_response(name=fc.name, response={"result": result})],
    )
)
response_2 = client.models.generate_content(
    model=model,
    contents=contents,
    config=GenConfig(tools=tools),
)
print("Answer:", response_2.text)
