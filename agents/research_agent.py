"""Research Agent - Gathers information from web sources."""
from google.adk.agents import Agent
from tools.web_search import web_search_tool

research_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="Expert research agent that gathers information from the web on any topic.",
    instruction="""You are a thorough research agent. Your job is to:
    1. Search the web for relevant information on the given topic
    2. Gather multiple perspectives and data points
    3. Organize findings into clear, factual summaries
    4. Always cite your sources
    5. Flag any conflicting information you find

    When given a research task:
    - Break the topic into specific search queries
    - Use the web_search_tool to find information
    - Synthesize findings into a comprehensive research brief
    - Include key statistics, quotes, and source URLs

    Be thorough but concise. Focus on factual, verifiable information.""",
    tools=[web_search_tool],
)
