# MCP Meetup Demo

**An MCP Architecture Reference Implementation with a Real-World Use Case**

This project demonstrates the Model Context Protocol (MCP) architecture by building a practical community intelligence system. It shows how to create an Agent OS that both consumes multiple MCP servers AND exposes itself as an MCP server for other clients.

## What We're Building

**MCP Chaining Architecture:** An Agent OS that consumes multiple MCP servers (GitHub, Agno Docs, Brave Search) and exposes itself as an MCP server for team clients to query.

**Real-World Use Case:** Community intelligence system that analyzes GitHub issues at scale and routes actionable insights to different teams:
- **PM Team:** Feature requests prioritized by demand and business impact
- **DevRel Team:** Documentation gaps identified from user confusion patterns  
- **Sales Team:** Common objections blocking enterprise deals
- **Engineers:** Critical bugs affecting production deployments

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         External MCP Servers (Data Sources)         │
│                                                     │
│  GitHub MCP    Agno Docs MCP    Brave Search MCP   │
└─────────────────────┬───────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────┐
│         Community Support Agent OS (Port 7777)      │
│                                                     │
│  • Consumes: GitHub, Docs, Search MCPs             │
│  • Processes: Analyzes with Claude AI              │
│  • Exposes: MCP endpoint for team clients          │
│                                                     │
│  Endpoint: http://localhost:7777/mcp               │
└─────────────────────┬───────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────┐
│           Team Clients (Specialized Queries)        │
│                                                     │
│  PM Team     DevRel Team    Sales Team    Engineers│
└─────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Install dependencies
pip install -U agno anthropic fastapi uvicorn sqlalchemy python-dotenv

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Terminal 1: Start the Agent OS Server
python3 servers/simple_server.py          # Simple (Agno Docs only)
# OR
python3 servers/main_agent_server.py      # Full (GitHub + Docs + Search)

# Terminal 2: Run a client
python3 clients/test_client.py            # Test connection
python3 clients/pm_team_client.py         # Product insights
python3 clients/devrel_team_client.py     # Documentation gaps
python3 clients/sales_team_client.py      # Sales intelligence
python3 clients/engineers_team_client.py  # Bug prioritization
```

## How It Works

### Server: Consuming MCP Servers

```python
from agno.tools.mcp import MCPTools

# HTTP-based MCP
tools.append(MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp"
))

# Command-based MCP
tools.append(MCPTools(
    command="npx -y @modelcontextprotocol/server-github",
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
))
```

### Server: Exposing as MCP Server

```python
from agno.os import AgentOS

agent_os = AgentOS(
    agents=[community_agent],
    enable_mcp_server=True  # Exposes /mcp endpoint at port 7777
)
```

### Client: Connecting to Agent OS

```python
from agno.tools.mcp import MCPTools
from agno import Agent

async with MCPTools(
    transport="streamable-http",
    url="http://localhost:7777/mcp"
) as mcp_tools:
    agent = Agent(tools=[mcp_tools])
    await agent.aprint_response("Analyze community feedback...")
```

## Configuration

### Required
```bash
ANTHROPIC_API_KEY=sk-ant-...        # Get from console.anthropic.com
```

### Optional (for full features)
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...  # Get from github.com/settings/tokens
BRAVE_API_KEY=...                     # Get from brave.com/search/api
```

## Resources

- [Agno Documentation](https://docs.agno.com)
- [MCP Concepts](https://docs.agno.com/concepts/tools/mcp)
- [Agent OS Guide](https://docs.agno.com/examples/agent-os)
- [MCP Cookbook Examples](https://docs.agno.com/examples/agent-os/mcp)

---

**Built for the MCP Meetup** - Demonstrating practical MCP architecture patterns with real-world value.
