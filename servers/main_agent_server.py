"""
Main Agent OS Server - MCP Meetup Demo (Improved)

Following Agno cookbook patterns from:
- https://docs.agno.com/examples/agent-os/mcp/enable_mcp_example
- https://docs.agno.com/concepts/tools/mcp/multiple-servers

Architecture:
- Consumes: GitHub MCP, Agno Docs MCP, Brave Search MCP
- Exposes: AgentOS MCP server at /mcp endpoint
"""

from os import getenv
from typing import List

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded .env file\n")
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables.\n")

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# ==========================================
# Database Setup
# ==========================================
db = SqliteDb(db_file="tmp/mcp_meetup_demo.db")

# ==========================================
# MCP Servers Configuration
# ==========================================

def setup_mcp_tools() -> List[MCPTools]:
    """Setup MCP tools based on available API keys"""
    tools = []
    
    # 1. Agno Docs MCP (always available - no API key needed)
    try:
        agno_docs_mcp = MCPTools(
            transport="streamable-http",
            url="https://docs.agno.com/mcp",
            timeout_seconds=60,
        )
        tools.append(agno_docs_mcp)
        print("Agno Docs MCP enabled")
    except Exception as e:
        print(f"Warning: Agno Docs MCP failed: {e}")
    
    # 2. GitHub MCP (optional - needs GITHUB_PERSONAL_ACCESS_TOKEN)
    github_token = getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if github_token and github_token != "your_github_token_here":
        try:
            github_mcp = MCPTools(
                command="npx -y @modelcontextprotocol/server-github",
                env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token},
                timeout_seconds=60,
            )
            tools.append(github_mcp)
            print("GitHub MCP enabled")
        except Exception as e:
            print(f"Warning: GitHub MCP failed: {e}")
    else:
        print("Warning: GitHub MCP disabled (GITHUB_PERSONAL_ACCESS_TOKEN not set)")
    
    # 3. Brave Search MCP (optional - needs BRAVE_API_KEY)
    brave_api_key = getenv("BRAVE_API_KEY")
    if brave_api_key and brave_api_key != "your_brave_api_key_here":
        try:
            brave_search_mcp = MCPTools(
                command="npx -y @modelcontextprotocol/server-brave-search",
                env={"BRAVE_API_KEY": brave_api_key},
                timeout_seconds=60,
            )
            tools.append(brave_search_mcp)
            print("Brave Search MCP enabled")
        except Exception as e:
            print(f"Warning: Brave Search MCP failed: {e}")
    else:
        print("Warning: Brave Search MCP disabled (BRAVE_API_KEY not set)")
    
    print()
    return tools

# ==========================================
# Community Support Agent
# ==========================================

def create_community_agent(tools: List[MCPTools]) -> Agent:
    """Create the main community support agent"""
    
    # Build instructions based on available tools
    instructions = [
        "You are a helpful Community Support Agent for the Agno AI framework.",
        "You have access to:",
    ]
    
    # Add tool-specific instructions
    tool_names = []
    if any("docs.agno.com" in str(t) for t in tools):
        instructions.append("- Agno documentation for technical questions")
        tool_names.append("Agno Docs")
    if any("github" in str(t) for t in tools):
        instructions.append("- GitHub repositories for issues, PRs, and community activity")
        tool_names.append("GitHub")
    if any("brave" in str(t) for t in tools):
        instructions.append("- Web search for current information")
        tool_names.append("Brave Search")
    
    instructions.extend([
        "",
        "Your role is to help answer community questions comprehensively.",
        "Use the appropriate MCP server for each query:",
        "- For Agno features/docs → Agno Docs MCP",
        "- For repository issues → GitHub MCP", 
        "- For current web info → Brave Search MCP",
    ])
    
    return Agent(
        id="community-support-agent",
        name="Community Support Agent",
        model=Claude(id="claude-sonnet-4-5"),
        db=db,
        tools=tools,
        instructions=instructions,
        add_history_to_context=True,
        num_history_runs=3,
        add_datetime_to_context=True,
        enable_session_summaries=True,
        markdown=True,
    )

# ==========================================
# Agent OS Setup
# ==========================================

# Setup tools and agent
tools = setup_mcp_tools()
community_support_agent = create_community_agent(tools)

# Create Agent OS with MCP server enabled
# Following cookbook pattern: enable_mcp_server=True
agent_os = AgentOS(
    description="Community Support Agent OS - Exposed as MCP for teams",
    agents=[community_support_agent],
    enable_mcp_server=True,  # Exposes /mcp endpoint for other teams
)

app = agent_os.get_app()

# ==========================================
# Server Entry Point
# ==========================================

if __name__ == "__main__":
    """
    Run the main Agent OS server.
    
    The MCP server will be available at:
    - MCP endpoint: http://localhost:7777/mcp
    - API docs: http://localhost:7777/docs
    - Health check: http://localhost:7777/health
    
    This server can be consumed by:
    - PM team agents
    - DevRel team agents  
    - Sales team agents
    - Engineering team agents
    """
    print("=" * 60)
    print("Starting Community Support Agent OS")
    print("=" * 60)
    print(f"Active MCP servers: {len(tools)}")
    print(f"Registered agents: {[agent.id for agent in agent_os.agents]}")
    print("MCP Server: http://localhost:7777/mcp")
    print("API Docs: http://localhost:7777/docs")
    print("=" * 60)
    print()
    
    # Following cookbook pattern: agent_os.serve()
    agent_os.serve(app="main_agent_server_improved:app")
