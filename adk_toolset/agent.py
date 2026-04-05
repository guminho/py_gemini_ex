import asyncio
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool, FunctionTool, ToolContext
from google.adk.tools.base_toolset import BaseToolset, ReadonlyContext


# Define the individual tool functions
def add_numbers(a: int, b: int, tool_context: ToolContext) -> dict[str, Any]:
    """Adds two integer numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        A dictionary with the sum, e.g., {'status': 'success', 'result': 5}
    """
    print(f"Tool: add_numbers called with a={a}, b={b}")
    result = a + b
    # Example: Storing something in tool_context state
    tool_context.state["last_math_operation"] = "addition"
    return {"status": "success", "result": result}


def subtract_numbers(a: int, b: int) -> dict[str, Any]:
    """Subtracts the second number from the first.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        A dictionary with the difference, e.g., {'status': 'success', 'result': 1}
    """
    print(f"Tool: subtract_numbers called with a={a}, b={b}")
    return {"status": "success", "result": a - b}


# Create the Toolset by implementing BaseToolset
class SimpleMathToolset(BaseToolset):
    def __init__(self, prefix: str = "math"):
        self._add_tool = FunctionTool(func=add_numbers)
        self._subtract_tool = FunctionTool(func=subtract_numbers)
        super().__init__(tool_name_prefix=prefix)

    async def get_tools(
        self, readonly_context: ReadonlyContext | None = None
    ) -> list[BaseTool]:
        print("SimpleMathToolset.get_tools() called.")
        # Example of dynamic behavior:
        # Could use readonly_context.state to decide which tools to return

        # For this simple example, always return both tools
        return [self._add_tool, self._subtract_tool]

    async def close(self) -> None:
        # No resources to clean up in this simple example
        await asyncio.sleep(0)  # Placeholder for async cleanup if needed


# Define an individual tool (not part of the toolset)
def greet_user(name: str = "User", tool_context: ToolContext = None) -> dict[str, str]:
    """Greets the user."""
    tool_context.actions.skip_summarization = True
    return {"greeting": f"Hello, {name}!"}


greet_tool = FunctionTool(greet_user)
math_toolset_instance = SimpleMathToolset(prefix="calculator")

# Define an agent that uses both the individual tool and the toolset
calculator_agent = LlmAgent(
    name="CalculatorAgent",
    model="gemini-3-flash-preview",  # Replace with your desired model
    instruction="You are a helpful calculator and greeter. "
    "Use 'greet_user' for greetings. "
    "Use 'calculator_add_numbers' to add and 'calculator_subtract_numbers' to subtract. "
    "Announce the state of 'last_math_operation' if it's set.",
    tools=[greet_tool, math_toolset_instance],  # Individual tool  # Toolset instance
)

root_agent = calculator_agent
