"""
Complete Demo Runner - MCP Meetup Demo

This script demonstrates the full architecture:
1. Main Agent OS with multiple MCP servers (GitHub, Docs, Brave)
2. Agent OS exposed as MCP server
3. Multiple team clients connecting to the Agent OS MCP

Run this after starting main_agent_server.py
"""

import asyncio

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning:  python-dotenv not installed. Install with: pip install python-dotenv")

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.mcp import MCPTools

# MCP server URL of the main Community Support Agent OS
COMMUNITY_SUPPORT_MCP_URL = "http://localhost:7777/mcp"


async def run_all_teams_demo():
    """Run a complete demo showing all teams using the Agent OS MCP"""
    
    print("\n" + "=" * 80)
    print(" MCP MEETUP DEMO - AGNO AGENT OS WITH MULTIPLE MCP SERVERS")
    print("=" * 80)
    print("\nArchitecture:")
    print("  [User on Discord/Slack]")
    print("           ↓")
    print("  [Agent OS MCP Infrastructure]")
    print("    ├─ GitHub MCP (repo data)")
    print("    ├─ Agno Docs MCP (documentation)")
    print("    └─ Brave Search MCP (web search)")
    print("           ↓")
    print("  Multiple Teams Connect:")
    print("    ├─ PM Team")
    print("    ├─ DevRel Team")
    print("    ├─ Sales Team")
    print("    └─ Engineers Team")
    print("=" * 80 + "\n")
    
    # Connect to the Agent OS MCP
    async with MCPTools(
        transport="streamable-http",
        url=COMMUNITY_SUPPORT_MCP_URL,
        timeout_seconds=90,
    ) as community_mcp:
        
        # ==========================================
        # 1. PM Team Demo
        # ==========================================
        print("\n" + "🔹" * 40)
        print("1️⃣  PM TEAM - Community Insights")
        print("🔹" * 40)
        
        pm_agent = Agent(
            name="PM Insights Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=["You help PM team understand community needs via the Community Support Agent."],
            markdown=True,
        )
        
        await pm_agent.aprint_response(
            input="What are the last 5 issues from the community? What features are they requesting?",
            stream=True,
            markdown=True,
        )
        
        await asyncio.sleep(2)
        
        # ==========================================
        # 2. DevRel Team Demo
        # ==========================================
        print("\n" + "🔹" * 40)
        print("2️⃣  DEVREL TEAM - Documentation Needs")
        print("🔹" * 40)
        
        devrel_agent = Agent(
            name="DevRel Content Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=["You help DevRel identify documentation gaps via the Community Support Agent."],
            markdown=True,
        )
        
        await devrel_agent.aprint_response(
            input="Based on community questions, what tutorials should we create? Give me top 3 priorities.",
            stream=True,
            markdown=True,
        )
        
        await asyncio.sleep(2)
        
        # ==========================================
        # 3. Engineers Team Demo
        # ==========================================
        print("\n" + "🔹" * 40)
        print("3️⃣  ENGINEERS TEAM - Bug Prioritization")
        print("🔹" * 40)
        
        engineers_agent = Agent(
            name="Engineering Insights Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=["You help Engineers prioritize bugs via the Community Support Agent."],
            markdown=True,
        )
        
        await engineers_agent.aprint_response(
            input="What are the most critical bugs reported? Which should we fix first?",
            stream=True,
            markdown=True,
        )
        
        await asyncio.sleep(2)
        
        # ==========================================
        # 4. Sales Team Demo
        # ==========================================
        print("\n" + "🔹" * 40)
        print("4️⃣  SALES TEAM - Adoption Analysis")
        print("🔹" * 40)
        
        sales_agent = Agent(
            name="Sales Intelligence Agent",
            model=Claude(id="claude-sonnet-4-5"),
            tools=[community_mcp],
            instructions=["You help Sales understand adoption trends via the Community Support Agent."],
            markdown=True,
        )
        
        await sales_agent.aprint_response(
            input="Who are the most active users and organizations? Any enterprise adoption signals?",
            stream=True,
            markdown=True,
        )
    
    print("\n" + "=" * 80)
    print(" DEMO COMPLETE!")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("   One Agent OS with multiple MCP servers (GitHub, Docs, Brave)")
    print("   Agent OS exposed as MCP server for other teams")
    print("   Multiple specialized team agents connecting to one MCP infrastructure")
    print("   Each team gets tailored insights from the same data sources")
    print("\n")


if __name__ == "__main__":
    """
    Run the complete demo.
    
    Prerequisites:
    1. Start main_agent_server.py first
    2. Set environment variables in .env file (ANTHROPIC_API_KEY required)
    3. Run this script
    """
    print("\nWarning:  Make sure main_agent_server.py is running at http://localhost:7777")
    print("Warning:  Press Ctrl+C to stop\n")
    
    try:
        asyncio.run(run_all_teams_demo())
    except KeyboardInterrupt:
        print("\n\nDemo stopped by user")
    except Exception as e:
        print(f"\n\nError: Error: {e}")
        print("Make sure the main_agent_server.py is running!")
