"""Main entry point for the Google ADK Multi-Agent Workflow System.

This system demonstrates a multi-agent architecture where specialized
agents collaborate to research, analyze, and produce content on any topic.

Architecture:
    Orchestrator Agent
    ├── Research Agent (web search, data gathering)
    ├── Analysis Agent (text analysis, keyword extraction, sentiment)
    └── Writer Agent (report generation, email drafting, summarization)

Usage:
    # Interactive mode
    python main.py

    # With ADK dev server
    adk web
"""
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

from agents.orchestrator import orchestrator_agent


async def run_interactive():
    """Run the multi-agent system in interactive mode."""
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService

    session_service = InMemorySessionService()
    runner = Runner(
        agent=orchestrator_agent,
        app_name="multi_agent_workflow",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="multi_agent_workflow",
        user_id="user_1",
    )

    print("=" * 60)
    print("  Google ADK Multi-Agent Workflow System")
    print("  Research → Analyze → Write")
    print("=" * 60)
    print()
    print("Commands:")
    print("  Type your request to start the workflow")
    print("  Type 'quit' or 'exit' to stop")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("\n🔄 Processing your request...\n")

        from google.genai import types

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        response_text = ""
        async for event in runner.run_async(
            user_id="user_1",
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text

        if response_text:
            print(f"Agent: {response_text}\n")
        else:
            print("Agent: (No response generated)\n")


# ADK entrypoint - expose the root agent for `adk web`
root_agent = orchestrator_agent


if __name__ == "__main__":
    asyncio.run(run_interactive())
