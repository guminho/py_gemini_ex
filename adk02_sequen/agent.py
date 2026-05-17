"""
Sequential Code Generation & Refactoring Pipeline.

This module orchestrates a sequential multi-agent workflow to generate, review,
and refactor Python code based on user specifications:
1. CodeWriterAgent: Generates the initial Python code.
2. CodeReviewerAgent: Reviews the generated code and provides feedback.
3. CodeRefactorerAgent: Applies the reviewer's feedback to refactor and optimize the code.
4. CodePipelineAgent: Coordinates the sequence of execution for all sub-agents.
"""

from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent

# --- Global Configurations ---
MODEL_NAME = "gemini-3-flash-preview"

# Output Keys (prevents spelling errors/typos when referencing keys)
KEY_GENERATED_CODE = "generated_code"
KEY_REVIEW_COMMENTS = "review_comments"
KEY_REFACTORED_CODE = "refactored_code"

# --- Prompt Templates ---

INSTRUCTION_CODE_WRITER = """
    You are a Python Code Generator.
    Based *only* on the user's request, write Python code that fulfills the requirement.
    Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```).
    Do not add any other text before or after the code block.
    """

INSTRUCTION_CODE_REVIEWER = f"""
    You are an expert Python Code Reviewer.
    Your task is to provide constructive feedback on the provided code.

    **Code to Review:**
    ```python
    {{{KEY_GENERATED_CODE}}}
    ```

    **Review Criteria:**
    1.  **Correctness:** Does the code work as intended? Are there logic errors?
    2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
    3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
    4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    5.  **Best Practices:** Does the code follow common Python best practices?

    **Output:**
    Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    If the code is excellent and requires no changes, simply state: "No major issues found."
    Output *only* the review comments or the "No major issues" statement.
    """

INSTRUCTION_CODE_REFACTORER = f"""
    You are a Python Code Refactoring AI.
    Your goal is to improve the given Python code based on the provided review comments.

    **Original Code:**
    ```python
    {{{KEY_GENERATED_CODE}}}
    ```

    **Review Comments:**
    {{{KEY_REVIEW_COMMENTS}}}

    **Task:**
    Carefully apply the suggestions from the review comments to refactor the original code.
    If the review comments state "No major issues found," return the original code unchanged.
    Ensure the final code is complete, functional, and includes necessary imports and docstrings.

    **Output:**
    Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```).
    Do not add any other text before or after the code block.
    """


# --- Sub-Agents Definition ---

code_writer_agent = LlmAgent(
    model=MODEL_NAME,
    name="CodeWriterAgent",
    description="Writes initial Python code based on a specification.",
    instruction=INSTRUCTION_CODE_WRITER,
    output_key=KEY_GENERATED_CODE,
)

code_reviewer_agent = LlmAgent(
    model=MODEL_NAME,
    name="CodeReviewerAgent",
    description="Reviews code and provides feedback.",
    instruction=INSTRUCTION_CODE_REVIEWER,
    output_key=KEY_REVIEW_COMMENTS,
)

code_refactorer_agent = LlmAgent(
    model=MODEL_NAME,
    name="CodeRefactorerAgent",
    description="Refactors code based on review comments.",
    instruction=INSTRUCTION_CODE_REFACTORER,
    output_key=KEY_REFACTORED_CODE,
)


# --- Sequential Orchestration ---

code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[
        code_writer_agent,
        code_reviewer_agent,
        code_refactorer_agent,
    ],
)

root_agent = code_pipeline_agent
