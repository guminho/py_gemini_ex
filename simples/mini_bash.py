import os
import re
import subprocess

from google import genai

client = genai.Client()


def query_lm(messages: list[dict[str, str]]) -> str:
    contents = []
    for msg in messages:
        contents.append(
            {
                "role": msg["role"],
                "parts": [{"text": msg["content"]}],
            }
        )
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents,
    )
    return response.text


def parse_action(lm_output: str) -> str:
    """Take LM output, return action"""
    matches = re.findall(
        r"```bash-action\s*\n(.*?)\n```",
        lm_output,
        re.DOTALL,
    )
    return matches[0].strip() if matches else ""


def execute_action(command: str) -> str:
    """Execute action, return output"""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        env=os.environ,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    return result.stdout


# Main agent loop
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command.",
    },
    {
        "role": "user",
        "content": "List the files in the current directory",
    },
]

while True:
    lm_output = query_lm(messages)
    print(f"## LM output: {lm_output}")

    # remember what the LM said
    messages.append({"role": "assistant", "content": lm_output})

    # separate the action from output
    action = parse_action(lm_output)
    print(f"## Action: {action!r}")

    if not action or action == "exit":
        break
    output = execute_action(action)
    print(f"## Output: {output!r}")

    # send command output back
    messages.append({"role": "user", "content": output})
