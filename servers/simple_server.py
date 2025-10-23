"""
Simplified Demo Server - No External API Keys Required

This is a simplified version that only uses the Agno Docs MCP server
which doesn't require any API keys. Perfect for quick testing!

Architecture:
- Consumes: Agno Docs MCP only (no API key needed)
- Exposes: AgentOS MCP server at /mcp endpoint
"""

from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not required for simple server

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

# Setup the database
db_path = Path(__file__).parent / "tmp" / "mcp_meetup_demo_simple.db"
db = SqliteDb(db_file=str(db_path))

# ==========================================
# Single MCP Server (no API keys required)
# ==========================================

# Agno Docs MCP Server - for documentation
agno_docs_mcp = MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp",
    timeout_seconds=60,
)

# ==========================================
# Documentation Support Agent
# ==========================================

doc_support_agent = Agent(
    id="doc_support_agent",
    name="Documentation Support Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    tools=[agno_docs_mcp],  # Only Agno Docs MCP
    instructions=[
        "You are a helpful Documentation Support Agent for the Agno AI framework.",
        "You have access to Agno documentation to answer technical questions.",
        "Help users understand how to use Agno features and capabilities.",
    ],
    add_history_to_context=True,
    num_history_runs=1,  # Reduced to save tokens
    add_datetime_to_context=True,
    enable_session_summaries=False,  # Disabled to save tokens
    markdown=True,
)

# ==========================================
# AgentOS with MCP Server Enabled
# ==========================================

agent_os = AgentOS(
    description="Documentation Support Agent OS - Simplified Demo",
    agents=[doc_support_agent],
    enable_mcp_server=True,  # This exposes /mcp endpoint
)

app = agent_os.get_app()

if __name__ == "__main__":
    """
    Run the simplified Agent OS server (no external API keys needed).
    
    The MCP server will be available at:
    http://localhost:7777/mcp
    
    This is perfect for testing the MCP architecture without needing
    GitHub or Brave API keys!
    """
    print("=" * 60)
    print("Starting Documentation Support Agent OS (Simplified)")
    print("=" * 60)
    print("No external API keys required!")
    print("Using Agno Docs MCP only")
    print("=" * 60)
    print("MCP Server available at: http://localhost:7777/mcp")
    print("API Docs available at: http://localhost:7777/docs")
    print("=" * 60)
    
    agent_os.serve(app="simple_server:app")
