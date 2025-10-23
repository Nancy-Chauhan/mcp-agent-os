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

**Key MCP Concepts Demonstrated:**
1. **Agent as MCP Client** - Agent OS connects to multiple upstream MCP servers
2. **Agent as MCP Server** - Same Agent OS exposes MCP endpoint downstream
3. **MCP Chaining** - Clients → Agent → External MCPs (multi-hop architecture)
4. **Specialized Contexts** - Each client gets tailored responses from shared infrastructure

## What You'll Learn

### MCP Architecture Patterns
- How to configure Agent OS with multiple MCP servers
- Setting up both HTTP-based (`streamable-http`) and command-based MCP servers
- Exposing Agent OS as an MCP server with `enable_mcp_server=True`
- Building MCP clients that connect to Agent OS endpoints
- Managing sessions and state across MCP connections

### Real-World Application
- Processing unstructured community feedback
- Routing different insights to different stakeholders
- Building domain-specific AI agents for teams
- Scaling intelligence across an organization

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js (for GitHub and Brave Search MCP servers)
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

### Installation

```bash
# Install dependencies
pip install -U agno anthropic fastapi uvicorn sqlalchemy python-dotenv

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the Demo

**Terminal 1: Start the Agent OS Server**
```bash
# Simple version (Agno Docs MCP only)
python3 servers/simple_server.py

# OR Full version (GitHub + Docs + Search MCPs)
python3 servers/main_agent_server.py
```

Wait for: `Uvicorn running on http://localhost:7777`

**Terminal 2: Run a Team Client**
```bash
# Test the connection
python3 clients/test_client.py

# Or run team-specific clients
python3 clients/pm_team_client.py           # Product insights
python3 clients/devrel_team_client.py       # Documentation gaps
python3 clients/sales_team_client.py        # Sales intelligence
python3 clients/engineers_team_client.py    # Bug prioritization
```

## Project Structure

```
mcp-meetup-demo/
├── servers/
│   ├── main_agent_server.py      # Full Agent OS (all MCP servers)
│   └── simple_server.py           # Simplified Agent OS (docs only)
│
├── clients/
│   ├── test_client.py             # Basic MCP client test
│   ├── pm_team_client.py          # Product management client
│   ├── devrel_team_client.py      # Developer relations client
│   ├── sales_team_client.py       # Sales team client
│   └── engineers_team_client.py   # Engineering team client
│
├── scripts/
│   ├── demo_runner.py             # Run all team demos
│   └── test_setup.py              # Verify environment setup
│
└── .env                           # API keys (create from .env.example)
```

## How Each Component Works

### Agent OS Server (`main_agent_server.py`)

**Consumes MCP Servers:**
```python
# HTTP-based MCP
MCPTools(
    transport="streamable-http",
    url="https://docs.agno.com/mcp"
)

# Command-based MCP
MCPTools(
    command="npx -y @modelcontextprotocol/server-github",
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
)
```

**Exposes as MCP Server:**
```python
agent_os = AgentOS(
    agents=[community_agent],
    enable_mcp_server=True  # Exposes /mcp endpoint
)
```

### Team Clients

Each client connects to the Agent OS MCP endpoint:

```python
async with MCPTools(
    transport="streamable-http",
    url="http://localhost:7777/mcp"
) as mcp_tools:
    agent = Agent(tools=[mcp_tools])
    await agent.aprint_response("Analyze community issues...")
```

## Real Output Examples

### PM Team Client
```
Top 3 Feature Requests:
1. Custom session_state Support (Issue #5139) - 12 requests
2. LLM Model Response Caching (Issue #5138) - 8 requests  
3. Multi VectorDB Support (Issue #5142) - 5 requests

Critical Bugs:
[URGENT] JWTMiddleware Dependencies (Issue #5143)
- Blocks production deployments
- Affects authentication for 40% of users
- Fix immediately

Recommendation: Prioritize JWT bug first, then session_state feature.
```

### DevRel Team Client
```
Documentation Gaps Identified:
1. "How to setup MCP servers?" - 18 questions
2. "Agent vs Agent OS differences" - 12 questions
3. "Error handling best practices" - 9 questions

Suggested Tutorials:
1. "MCP Setup: Complete Beginner's Guide" (HIGH PRIORITY)
2. "Agent Architecture: When to use what"
3. "Error Handling Patterns in Agno"
```


## Configuration

### Required Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...        # Get from console.anthropic.com
```

### Optional (for Full Features)
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...  # Get from github.com/settings/tokens
BRAVE_API_KEY=...                     # Get from brave.com/search/api
```

## Key Features Demonstrated

### MCP Architecture
- Multiple upstream MCP server integration
- HTTP and command-based MCP transports
- Agent OS acting as both client and server
- Session management across MCP connections
- Error handling and graceful degradation

### Real-World Intelligence
- Natural language query processing
- Context-aware responses per team
- Automatic pattern detection in feedback
- Priority and impact analysis
- Actionable recommendations


## Why This Matters

### For the MCP Meetup
- **Reference Implementation**: Shows production-ready MCP patterns
- **Chaining Architecture**: Demonstrates multi-hop MCP connections
- **Best Practices**: Error handling, session management, configuration
- **Real Use Case**: Not just a "hello world" - solves actual problems

### For Your Organization
- **Scales Intelligence**: One AI system serves multiple teams
- **Reduces Manual Work**: Automates feedback analysis
- **Data-Driven Decisions**: From opinions to ranked priorities
- **Shared Infrastructure**: One Agent OS, many use cases

## Resources

- [Agno Documentation](https://docs.agno.com)
- [MCP Concepts](https://docs.agno.com/concepts/tools/mcp)
- [Agent OS Guide](https://docs.agno.com/examples/agent-os)
- [MCP Cookbook Examples](https://docs.agno.com/examples/agent-os/mcp)


**Built for the MCP Meetup** - Demonstrating practical MCP architecture patterns with real-world value.
