"""
DevRel Team Client - Connects to Community Support Agent OS via MCP

The DevRel team wants to:
- Identify major issues that need tutorials
- Understand what documentation gaps exist
- Create content based on community needs
"""

import asyncio
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # Will use system environment variables

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

# MCP server URL of the main Community Support Agent OS
COMMUNITY_SUPPORT_MCP_URL = "http://localhost:7777/mcp"


async def devrel_agent_example():
    """DevRel team agent that identifies documentation needs"""
    
    async with MCPTools(
        transport="streamable-http",
        url=COMMUNITY_SUPPORT_MCP_URL,
        timeout_seconds=60,
    ) as community_mcp:
        devrel_agent = Agent(
            name="DevRel Content Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=[
                "You are a DevRel team assistant.",
                "You help identify documentation gaps and tutorial opportunities.",
                "Use the Community Support Agent to analyze GitHub issues and find patterns in user questions.",
                "Suggest tutorials and guides based on community needs.",
            ],
            markdown=True,
        )
        
        print("\n" + "=" * 60)
        print("DevRel Team Agent - Identifying Tutorial Opportunities")
        print("=" * 60)
        
        # Example query from DevRel team
        await devrel_agent.aprint_response(
            input="What are the major issues or confusion points from the community? What tutorials or guides should we create?",
            stream=True,
            markdown=True,
        )


if __name__ == "__main__":
    """
    Run the DevRel team client.
    Make sure the main_agent_server.py is running first!
    """
    asyncio.run(devrel_agent_example())
