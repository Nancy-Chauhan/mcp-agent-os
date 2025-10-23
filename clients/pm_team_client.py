"""
PM Team Client - Following Agno Cookbook Patterns

This demonstrates how different teams can connect to the same Agent OS MCP
and get specialized insights for their needs.

PM Team Use Cases:
- Track community issues and feature requests
- Understand user pain points
- Prioritize product roadmap based on feedback
"""

import asyncio
from typing import Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

# MCP server URL of the main Community Support Agent OS
COMMUNITY_SUPPORT_MCP_URL = "http://localhost:7777/mcp"


async def run_pm_analysis(query: Optional[str] = None):
    """
    Run PM team analysis using the Community Support Agent OS.
    
    Following cookbook patterns:
    - async with for connection management
    - await agent.aprint_response() for streaming
    - Clear instructions for specialized use case
    """
    
    print("\n" + "=" * 60)
    print("PM TEAM - Community Insights Analysis")
    print("=" * 60 + "\n")
    
    # Following cookbook pattern: async with MCPTools(...)
    async with MCPTools(
        transport="streamable-http",
        url=COMMUNITY_SUPPORT_MCP_URL,
        timeout_seconds=90,  # Higher timeout for complex queries
    ) as community_mcp:
        
        # Create PM-specialized agent
        pm_agent = Agent(
            name="PM Insights Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=[
                "You are a PM team assistant analyzing community feedback.",
                "Your goal: Help PMs understand user needs and prioritize features.",
                "",
                "When answering:",
                "1. Query the Community Support Agent for data",
                "2. Summarize key themes and patterns",
                "3. Highlight urgent issues or popular requests",
                "4. Provide actionable recommendations",
                "",
                "Focus on: Feature requests, pain points, adoption blockers",
            ],
            markdown=True,
        )
        
        # Use provided query or default
        default_query = (
            "Analyze the last 10 community issues. "
            "What are the top 3 feature requests? "
            "Any critical bugs we should prioritize?"
        )
        
        query_to_use = query or default_query
        
        print(f"Query: {query_to_use}\n")
        print("-" * 60 + "\n")
        
        # Following cookbook pattern: await agent.aprint_response()
        await pm_agent.aprint_response(
            input=query_to_use,
            stream=True,
            markdown=True,
        )
    
    print("\n" + "=" * 60)
    print("PM Analysis Complete!")
    print("=" * 60 + "\n")


async def run_feature_prioritization():
    """Example: Feature prioritization analysis"""
    
    query = (
        "Based on community feedback, what features should we prioritize "
        "for the next sprint? Consider: frequency of requests, user impact, "
        "and technical complexity indicators."
    )
    
    await run_pm_analysis(query)


async def run_user_sentiment_analysis():
    """Example: User sentiment analysis"""
    
    query = (
        "Analyze user sentiment in recent issues and discussions. "
        "Are users happy? Any major frustrations? "
        "What's the overall community health?"
    )
    
    await run_pm_analysis(query)


async def main():
    """Main entry point with menu"""
    
    print("\nWarning: Make sure main_agent_server.py is running at http://localhost:7777\n")
    
    try:
        # Run default analysis
        await run_pm_analysis()
        
        # Uncomment to run specific analyses:
        # await run_feature_prioritization()
        # await run_user_sentiment_analysis()
        
    except ConnectionError as e:
        print(f"\nError: Connection Error: {e}")
        print("Make sure the server is running!")
    except Exception as e:
        print(f"\nError: Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    Run the PM team client.
    
    Prerequisites:
    1. Start main_agent_server.py first
    2. Set ANTHROPIC_API_KEY in .env file
    3. Run this script
    
    The PM agent will connect to the Community Support Agent OS
    and get specialized insights for product management.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nAnalysis stopped by user")
