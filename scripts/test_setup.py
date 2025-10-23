#!/usr/bin/env python3
"""
Test script to verify your environment setup is correct.

Run this before starting the demo to check everything is configured properly.
"""

import sys

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"[OK] Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[Error] Python 3.8+ required!")
        return False
    return True

def check_imports():
    """Check required packages are installed"""
    packages = {
        'agno': 'agno',
        'anthropic': 'anthropic',
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'dotenv': 'python-dotenv',
    }
    
    all_good = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"[OK] {package} installed")
        except ImportError:
            print(f"[Error] {package} not installed - run: pip install {package}")
            all_good = False
    
    return all_good

def check_env_variables():
    """Check environment variables"""
    import os
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("[OK] Loaded .env file")
    except Exception as e:
        print(f"[Warning]  Could not load .env file: {e}")
    
    print("\nEnvironment Variables:")
    
    # Check Anthropic (required)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print("[OK] ANTHROPIC_API_KEY is set")
    else:
        print("[Error] ANTHROPIC_API_KEY not set (REQUIRED)")
        print("   Get one at: https://console.anthropic.com/")
        return False
    
    # Check GitHub (optional)
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if github_token and github_token != "your_github_token_here":
        print("[OK] GITHUB_PERSONAL_ACCESS_TOKEN is set")
    else:
        print("[Warning]  GITHUB_PERSONAL_ACCESS_TOKEN not set (optional)")
    
    # Check Brave (optional)
    brave_key = os.getenv("BRAVE_API_KEY")
    if brave_key and brave_key != "your_brave_api_key_here":
        print("[OK] BRAVE_API_KEY is set")
    else:
        print("[Warning]  BRAVE_API_KEY not set (optional)")
    
    return True

def check_node():
    """Check if Node.js is available for MCP servers"""
    import subprocess
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"\n[OK] Node.js installed: {result.stdout.strip()}")
            return True
    except Exception:
        pass
    
    print("\n[Warning]  Node.js not found (optional - needed for GitHub/Brave MCP)")
    print("   Install from: https://nodejs.org/")
    return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("MCP Meetup Demo - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version()),
        ("Required Packages", check_imports()),
        ("Environment Variables", check_env_variables()),
        ("Node.js (optional)", check_node()),
    ]
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in checks[:3])  # Only check required items
    
    if all_passed:
        print("\n[Success] Setup looks good! You're ready to run the demo.")
        print("\nNext steps:")
        print("  1. Run: python main_agent_server_improved.py")
        print("  2. In another terminal: python demo_runner.py")
        print("\nOr for a simpler test:")
        print("  1. Run: python simple_server.py")
        print("  2. In another terminal: python test_client_improved.py")
    else:
        print("\n[Error] Setup incomplete. Please fix the issues above.")
        print("\nSee ENV_SETUP.md for detailed setup instructions.")
        sys.exit(1)

if __name__ == "__main__":
    main()
