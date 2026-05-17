"""
Iterative Refinement and Writing Loop Pipeline.

This module orchestrates a streamlined iterative refinement loop using a single 
LoopAgent. It combines initial writing and refinement into a single Creative 
Writing Agent, and uses a Critic Agent to evaluate and optionally exit the loop:
1. WriterAgent: Generates the initial draft if none exists, or refines the 
   existing draft based on the critic's feedback.
2. CriticAgent: Evaluates the draft against quality criteria. If satisfied, it 
   calls the `exit_loop` tool to terminate; otherwise, it outputs critique.
3. RefinementLoop: The root LoopAgent executing the writer and critic iteratively.
"""

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext

# --- Global Configurations ---
MODEL_NAME = "gemini-3-flash-preview"

# Output Keys (prevents spelling errors/typos when referencing keys)
KEY_INITIAL_TOPIC = "initial_topic"
KEY_CURRENT_DOCUMENT = "current_document"
KEY_CRITICISM = "criticism"

# --- Prompt Templates ---

INSTRUCTION_WRITER = f"""
    You are a Creative Writing Assistant.
    Your task is to write or refine a short story based on the topic: {{{KEY_INITIAL_TOPIC}}}.

    **Current Draft (if any):**
    {{{KEY_CURRENT_DOCUMENT}}}

    **Feedback to address (if any):**
    {{{KEY_CRITICISM}}}

    **Task:**
    - If the Current Draft is empty, write a basic first draft of a short story (just 1-2 simple sentences) about the topic. Keep it plain and minimal - do NOT add descriptive language yet.
    - If there is a Current Draft and Feedback, carefully apply the feedback suggestions to refine and improve the Current Draft.

    Output *only* the story/document text. Do not add introductions, explanations, or formatting.
    """

INSTRUCTION_CRITIC = f"""
    You are a Constructive Critic AI reviewing a short story draft.

    **Document to Review:**
    ```
    {{{KEY_CURRENT_DOCUMENT}}}
    ```

    **Completion Criteria (ALL must be met):**
    1. At least 4 sentences long
    2. Has a clear beginning, middle, and end
    3. Includes at least one descriptive detail (sensory or emotional)

    **Task:**
    Check the document against the criteria above.

    IF any criteria is NOT met:
    Provide specific feedback on what to add or improve. Output *only* the critique text. Do not call the 'exit_loop' function.

    IF ALL criteria are met:
    You MUST call the 'exit_loop' function to signal completion. Do not output any text.
    """


# --- Tool Definitions ---

def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the document meets all criteria, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    return {}


# --- Sub-Agents Definition ---

writer_agent = LlmAgent(
    model=MODEL_NAME,
    name="WriterAgent",
    include_contents="none",
    description="Generates the initial story draft or refines it based on criticism.",
    instruction=INSTRUCTION_WRITER,
    output_key=KEY_CURRENT_DOCUMENT,
)

critic_agent = LlmAgent(
    model=MODEL_NAME,
    name="CriticAgent",
    include_contents="none",
    description="Reviews the draft against criteria and calls exit_loop if successful.",
    instruction=INSTRUCTION_CRITIC,
    tools=[exit_loop],
    output_key=KEY_CRITICISM,
)


# --- Iterative Orchestration ---

def initialize_state(callback_context: CallbackContext):
    """Ensure all state keys are initialized to avoid formatting/placeholder errors on the first run."""
    callback_context.state[KEY_INITIAL_TOPIC] = callback_context.state.get(
        KEY_INITIAL_TOPIC, "a robot developing unexpected emotions"
    )
    callback_context.state[KEY_CURRENT_DOCUMENT] = callback_context.state.get(
        KEY_CURRENT_DOCUMENT, ""
    )
    callback_context.state[KEY_CRITICISM] = callback_context.state.get(
        KEY_CRITICISM, ""
    )


# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        writer_agent,
        critic_agent,
    ],
    max_iterations=5,
    before_agent_callback=initialize_state,
)
