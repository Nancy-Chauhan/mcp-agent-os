"""
Sales Team Client - Connects to Community Support Agent OS via MCP

The Sales team wants to:
- Understand who is using the framework
- Identify potential enterprise customers
- Track adoption trends
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


async def sales_agent_example():
    """Sales team agent that analyzes adoption and potential customers"""
    
    async with MCPTools(
        transport="streamable-http",
        url=COMMUNITY_SUPPORT_MCP_URL,
        timeout_seconds=60,
    ) as community_mcp:
        sales_agent = Agent(
            name="Sales Intelligence Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=[
                "You are a Sales team assistant.",
                "You help identify adoption trends and potential enterprise customers.",
                "Use the Community Support Agent to analyze community engagement and user profiles.",
            ],
            markdown=True,
        )
        
        print("\n" + "=" * 60)
        print("Sales Team Agent - Analyzing Adoption Trends")
        print("=" * 60)
        
        # Example query from Sales team
        await sales_agent.aprint_response(
            input="Based on recent GitHub activity, who are the most active contributors and organizations using agno? Any enterprise adoption signals?",
            stream=True,
            markdown=True,
        )


if __name__ == "__main__":
    """
    Run the Sales team client.
    Make sure the main_agent_server.py is running first!
    """
    asyncio.run(sales_agent_example())
