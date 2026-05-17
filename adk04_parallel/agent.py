"""
Parallel Research and Synthesis Pipeline.

This module orchestrates a parallel multi-agent research workflow followed by a
centralized synthesis agent:
1. RenewableEnergyResearcher: Researches latest advancements in renewable energy sources.
2. EVResearcher: Researches latest developments in electric vehicle technology.
3. CarbonCaptureResearcher: Researches current state of carbon capture methods.
4. SynthesisAgent: Merges and synthesizes research findings into a structured cited report.
5. ResearchAndSynthesisPipeline: Orchestrates the parallel execution of the researchers
   followed by the sequential execution of the synthesis agent.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import google_search

# --- Global Configurations ---
MODEL_NAME = "gemini-3-flash-preview"

# Output Keys (prevents spelling errors/typos when referencing keys)
KEY_RENEWABLE_ENERGY_RESULT = "renewable_energy_result"
KEY_EV_TECHNOLOGY_RESULT = "ev_technology_result"
KEY_CARBON_CAPTURE_RESULT = "carbon_capture_result"

# --- Prompt Templates ---

INSTRUCTION_RENEWABLE_ENERGY_RESEARCHER = """
    You are an AI Research Assistant specializing in energy.
    Research the latest advancements in 'renewable energy sources'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """

INSTRUCTION_EV_RESEARCHER = """
    You are an AI Research Assistant specializing in transportation.
    Research the latest developments in 'electric vehicle technology'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """

INSTRUCTION_CARBON_CAPTURE_RESEARCHER = """
    You are an AI Research Assistant specializing in climate solutions.
    Research the current state of 'carbon capture methods'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.
    """

INSTRUCTION_SYNTHESIS = f"""
    You are an AI Assistant responsible for combining research findings into a structured report.
    Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.

    **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

    **Input Summaries:**

    *   **Renewable Energy:**
        {{{KEY_RENEWABLE_ENERGY_RESULT}}}

    *   **Electric Vehicles:**
        {{{KEY_EV_TECHNOLOGY_RESULT}}}

    *   **Carbon Capture:**
        {{{KEY_CARBON_CAPTURE_RESULT}}}

    **Output Format:**

    ## Summary of Recent Sustainable Technology Advancements

    ### Renewable Energy Findings
    (Based on RenewableEnergyResearcher's findings)
    [Synthesize and elaborate *only* on the renewable energy input summary provided above.]

    ### Electric Vehicle Findings
    (Based on EVResearcher's findings)
    [Synthesize and elaborate *only* on the EV input summary provided above.]

    ### Carbon Capture Findings
    (Based on CarbonCaptureResearcher's findings)
    [Synthesize and elaborate *only* on the carbon capture input summary provided above.]

    ### Overall Conclusion
    [Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

    Output *only* the structured report following this format. Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
    """


# --- Sub-Agents Definition ---

researcher_agent_1 = LlmAgent(
    model=MODEL_NAME,
    name="RenewableEnergyResearcher",
    description="Researches renewable energy sources.",
    instruction=INSTRUCTION_RENEWABLE_ENERGY_RESEARCHER,
    tools=[google_search],
    output_key=KEY_RENEWABLE_ENERGY_RESULT,
)

researcher_agent_2 = LlmAgent(
    model=MODEL_NAME,
    name="EVResearcher",
    description="Researches electric vehicle technology.",
    instruction=INSTRUCTION_EV_RESEARCHER,
    tools=[google_search],
    output_key=KEY_EV_TECHNOLOGY_RESULT,
)

researcher_agent_3 = LlmAgent(
    model=MODEL_NAME,
    name="CarbonCaptureResearcher",
    description="Researches carbon capture methods.",
    instruction=INSTRUCTION_CARBON_CAPTURE_RESEARCHER,
    tools=[google_search],
    output_key=KEY_CARBON_CAPTURE_RESULT,
)

merger_agent = LlmAgent(
    model=MODEL_NAME,
    name="SynthesisAgent",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
    instruction=INSTRUCTION_SYNTHESIS,
)


# --- Parallel and Sequential Orchestration ---

root_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[
        ParallelAgent(
            name="ParallelWebResearchAgent",
            sub_agents=[
                researcher_agent_1,
                researcher_agent_2,
                researcher_agent_3,
            ],
        ),
        merger_agent,
    ],
)
