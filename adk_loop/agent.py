from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext

# --- State Keys ---
KEY_CURRENT_DOCUMENT = "current_document"
KEY_CRITICISM = "criticism"
# Define the exact phrase the Critic should use to signal completion
COMPLETION_PHRASE = "No major issues found."


# --- Agent Definitions ---
# initial_writer_agent >> [critic_agent_in_loop >> refiner_agent_in_loop(exit_loop)]

# Agent 1: Initial Writer Agent (Runs ONCE at the beginning)
initial_writer_agent = LlmAgent(
    model="gemini-3-flash-preview",
    name="InitialWriterAgent",
    include_contents="none",
    description="Writes the initial document draft based on the topic, aiming for some initial substance.",
    instruction="""
    You are a Creative Writing Assistant tasked with starting a story.
    Write a *very basic* first draft of a short story (just 1-2 simple sentences).
    Keep it plain and minimal - do NOT add descriptive language yet.
    Topic: {initial_topic}

    Output *only* the story/document text. Do not add introductions or explanations.
    """,  # this is not f-string, hence single curly braces for placeholders
    output_key=KEY_CURRENT_DOCUMENT,
)

# Agent 2a: Critic Agent (Inside the Refinement Loop)
critic_agent_in_loop = LlmAgent(
    model="gemini-3-flash-preview",
    name="CriticAgent",
    include_contents="none",
    description="Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
    instruction=f"""
    You are a Constructive Critic AI reviewing a short story draft.

    **Document to Review:**
    ```
    {{current_document}}
    ```

    **Completion Criteria (ALL must be met):**
    1. At least 4 sentences long
    2. Has a clear beginning, middle, and end
    3. Includes at least one descriptive detail (sensory or emotional)

    **Task:**
    Check the document against the criteria above.

    IF any criteria is NOT met, provide specific feedback on what to add or improve.
    Output *only* the critique text.

    IF ALL criteria are met, respond *exactly* with: "{COMPLETION_PHRASE}"
    """,
    output_key=KEY_CRITICISM,
)


# Agent 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
# Tool definition
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}


refiner_agent_in_loop = LlmAgent(
    model="gemini-3-flash-preview",
    name="RefinerAgent",
    # Relies solely on state via placeholders
    include_contents="none",
    description="Refines the document based on critique, or calls exit_loop if critique indicates completion.",
    instruction=f"""
    You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    **Current Document:**
    ```
    {{current_document}}
    ```
    **Critique/Suggestions:**
    {{criticism}}

    **Task:**
    Analyze the 'Critique/Suggestions'.
    IF the critique is *exactly* "{COMPLETION_PHRASE}":
    You MUST call the 'exit_loop' function. Do not output any text.
    ELSE (the critique contains actionable feedback):
    Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.

    Do not add explanations. Either output the refined document OR call the exit_loop function.
    """,
    tools=[exit_loop],
    output_key=KEY_CURRENT_DOCUMENT,  # Overwrites state. NOTE: is blank after exit_loop is called
)


# --- Overall Sequential Pipeline ---
# Before agent callback
def update_initial_topic_state(callback_context: CallbackContext):
    """Ensure 'initial_topic' is set in state before pipeline starts."""
    callback_context.state["initial_topic"] = callback_context.state.get(
        "initial_topic", "a robot developing unexpected emotions"
    )


# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
    name="IterativeWritingPipeline",
    sub_agents=[
        initial_writer_agent,  # Agent 1
        LoopAgent(
            name="RefinementLoop",
            sub_agents=[
                critic_agent_in_loop,  # Agent 2a
                refiner_agent_in_loop,  # Agent 2b with exit tool
            ],
            max_iterations=5,
        ),
    ],
    before_agent_callback=update_initial_topic_state,  # set initial topic in state
)
