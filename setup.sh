#!/bin/bash

# Setup script for MCP Meetup Demo

echo "=========================================="
echo "MCP Meetup Demo - Setup Script"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js for MCP servers"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -U agno anthropic fastapi uvicorn sqlalchemy python-dotenv
echo "✅ Dependencies installed"

# Check for required environment variables
echo ""
echo "Checking environment variables..."

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set"
    echo "   Get one at: https://console.anthropic.com/"
else
    echo "✅ ANTHROPIC_API_KEY is set"
fi

if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "⚠️  GITHUB_PERSONAL_ACCESS_TOKEN not set (optional but recommended)"
    echo "   Get one at: https://github.com/settings/tokens"
else
    echo "✅ GITHUB_PERSONAL_ACCESS_TOKEN is set"
fi

if [ -z "$BRAVE_API_KEY" ]; then
    echo "⚠️  BRAVE_API_KEY not set (optional)"
    echo "   Get one at: https://brave.com/search/api/"
else
    echo "✅ BRAVE_API_KEY is set"
fi

# Test MCP servers
echo ""
echo "Testing MCP servers..."

# Test if we can run npx
if command -v npx &> /dev/null; then
    echo "✅ NPX available for MCP servers"
else
    echo "❌ NPX not found. Install Node.js to use MCP servers"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Set your API keys:"
echo "   export ANTHROPIC_API_KEY='your_key'"
echo "   export GITHUB_PERSONAL_ACCESS_TOKEN='your_token'"
echo "   export BRAVE_API_KEY='your_key'  # optional"
echo ""
echo "2. Start the server:"
echo "   python main_agent_server_improved.py"
echo ""
echo "3. In another terminal, run the demo:"
echo "   python demo_runner.py"
echo ""
echo "See README.md for more details!"
