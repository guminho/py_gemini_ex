import asyncio
from functools import partial

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from basic_team.agent import weather_agent


async def call_agent(runner: Runner, user_id: str, session_id: str, query: str):
    final_response_text = "Agent did not produce a final response."  # Default
    content = Content(role="user", parts=[Part(text=query)])

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            break

    print(f"Agent:{final_response_text}")


async def main():
    session_service = InMemorySessionService()

    APP_NAME = "weather_tutorial_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    runner = Runner(
        agent=weather_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    run_agent = partial(call_agent, runner, USER_ID, SESSION_ID)

    await run_agent("What is the weather like in London?")
    await run_agent("How about Paris?")
    await run_agent("Tell me the weather in New York")


if __name__ == "__main__":
    asyncio.run(main())
