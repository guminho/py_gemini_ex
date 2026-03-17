import asyncio
from functools import partial

from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

from basic_weather.agent import app


async def call_agent(runner: InMemoryRunner, user_id: str, session_id: str, query: str):
    final_response_text = "Agent did not produce a final response."  # Default
    content = Content(role="user", parts=[Part(text=query)])

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response():
            # dont break, it exhaust the generator
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )

    print(f"Agent:{final_response_text}")


async def main():
    async with InMemoryRunner(app=app) as runner:
        USER_ID = "user_1"
        SESSION_ID = "session_001"

        await runner.session_service.create_session(
            app_name=runner.app_name, user_id=USER_ID, session_id=SESSION_ID
        )
        run_agent = partial(call_agent, runner, USER_ID, SESSION_ID)

        await run_agent("What is the weather like in London?")
        await run_agent("How about Paris?")
        await run_agent("Tell me the weather in New York")


if __name__ == "__main__":
    asyncio.run(main())
