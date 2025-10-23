"""
Engineers Team Client - Connects to Community Support Agent OS via MCP

The Engineers team wants to:
- Track bug reports
- Understand technical issues users are facing
- Prioritize engineering work based on community feedback
"""

import asyncio

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Will use system environment variables

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

# MCP server URL of the main Community Support Agent OS
COMMUNITY_SUPPORT_MCP_URL = "http://localhost:7777/mcp"


async def engineers_agent_example():
    """Engineers team agent that tracks bugs and technical issues"""
    
    async with MCPTools(
        transport="streamable-http",
        url=COMMUNITY_SUPPORT_MCP_URL,
        timeout_seconds=60,
    ) as community_mcp:
        engineers_agent = Agent(
            name="Engineering Insights Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=[
                "You are an Engineering team assistant.",
                "You help prioritize bug fixes and technical improvements.",
                "Use the Community Support Agent to analyze bug reports and technical issues from the community.",
                "Focus on critical bugs and frequently reported issues.",
            ],
            markdown=True,
        )
        
        print("\n" + "=" * 60)
        print("Engineers Team Agent - Analyzing Bug Reports")
        print("=" * 60)
        
        # Example query from Engineers team
        await engineers_agent.aprint_response(
            input="What are the most critical bugs and technical issues reported by users? Which should we prioritize?",
            stream=True,
            markdown=True,
        )


if __name__ == "__main__":
    """
    Run the Engineers team client.
    Make sure the main_agent_server.py is running first!
    """
    asyncio.run(engineers_agent_example())
