"""
Test Client - Following Agno Cookbook Patterns

Based on: https://docs.agno.com/examples/agent-os/mcp/enable_mcp_example

This client demonstrates how to:
1. Connect to an Agent OS MCP server
2. Use async context manager for proper cleanup
3. Handle streaming responses
"""

import asyncio
from uuid import uuid4

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

# MCP server URL
MCP_SERVER_URL = "http://localhost:7777/mcp"


async def test_mcp_connection():
    """
    Test MCP connection following cookbook patterns.
    
    Key patterns:
    - Use async with for MCPTools (automatic connection management)
    - Use await agent.aprint_response() for streaming
    - Include timeout_seconds for reliability
    """
    
    print("\n" + "=" * 60)
    print("Testing MCP Connection - Documentation Query")
    print("=" * 60 + "\n")
    
    # Following cookbook pattern: async with MCPTools(...)
    async with MCPTools(
        transport="streamable-http",
        url=MCP_SERVER_URL,
        timeout_seconds=60,
    ) as mcp_tools:
        
        # Create agent with MCP tools
        test_agent = Agent(
            name="Test Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[mcp_tools],
            instructions=[
                "You help users learn about Agno by querying the Community Support Agent.",
                "Use the MCP tools to get information from the Agent OS.",
            ],
            markdown=True,
        )
        
        # Following cookbook pattern: await agent.aprint_response()
        await test_agent.aprint_response(
            input="How do I use MCP with Agno? Give me a simple code example.",
            stream=True,
            markdown=True,
        )
        
        print("\n" + "=" * 60)
        print("Test Complete!")
        print("=" * 60 + "\n")


async def test_multiple_queries():
    """Test multiple queries in the same session"""
    
    session_id = f"test-session-{uuid4()}"
    
    print("\n" + "=" * 60)
    print("Testing Multiple Queries in Same Session")
    print("=" * 60 + "\n")
    
    async with MCPTools(
        transport="streamable-http",
        url=MCP_SERVER_URL,
        timeout_seconds=60,
    ) as mcp_tools:
        
        agent = Agent(
            name="Multi-Query Test Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[mcp_tools],
            session_id=session_id,
            add_history_to_context=True,
            instructions=[
                "You help users test MCP functionality.",
                "Use the Community Support Agent for information.",
            ],
            markdown=True,
        )
        
        # Query 1
        print("\n📝 Query 1: Basic MCP Usage")
        print("-" * 60)
        await agent.aprint_response(
            input="What is MCP?",
            stream=True,
            markdown=True,
        )
        
        await asyncio.sleep(2)
        
        # Query 2 (should have context from Query 1)
        print("\n📝 Query 2: With Context")
        print("-" * 60)
        await agent.aprint_response(
            input="Give me a code example of what we just discussed.",
            stream=True,
            markdown=True,
        )
    
    print("\n" + "=" * 60)
    print("Multi-Query Test Complete!")
    print("=" * 60 + "\n")


async def main():
    """Main entry point with error handling"""
    
    print("\nWarning: Make sure main_agent_server.py is running at http://localhost:7777\n")
    
    try:
        # Run basic test
        await test_mcp_connection()
        
        # Uncomment to test multiple queries
        # await test_multiple_queries()
        
    except ConnectionError as e:
        print(f"\nError: Connection Error: {e}")
        print("Make sure the server is running at http://localhost:7777")
    except Exception as e:
        print(f"\nError: Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    Run the test client.
    
    Prerequisites:
    1. Start main_agent_server.py first
    2. Set ANTHROPIC_API_KEY in .env file
    3. Run this script
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
