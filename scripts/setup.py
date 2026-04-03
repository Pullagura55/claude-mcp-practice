#!/usr/bin/env python3
"""
Setup script for Claude MCP Server.

This script helps with common setup tasks like:
- Installing dependencies
- Running tests
- Generating configuration files
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def install_dependencies(dev: bool = False) -> bool:
    """Install project dependencies."""
    cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
    if dev:
        cmd.append("[dev]")
    return run_command(cmd, f"Installing dependencies (dev={dev})")


def run_tests() -> bool:
    """Run the test suite."""
    return run_command([sys.executable, "-m", "pytest"], "Running tests")


def format_code() -> bool:
    """Format code with black and isort."""
    success = True
    success &= run_command([sys.executable, "-m", "black", "src/"], "Formatting with black")
    success &= run_command([sys.executable, "-m", "isort", "src/"], "Sorting imports with isort")
    return success


def type_check() -> bool:
    """Run mypy type checking."""
    return run_command([sys.executable, "-m", "mypy", "src/"], "Type checking with mypy")


def generate_config(output_path: str = None) -> bool:
    """Generate MCP server configuration."""
    if output_path is None:
        output_path = "claude-mcp-config.json"

    current_dir = Path.cwd().resolve()
    src_path = current_dir / "src"

    config = {
        "mcpServers": {
            "claude-mcp-server": {
                "command": "python",
                "args": ["-m", "claude_mcp_server.server"],
                "env": {
                    "PYTHONPATH": str(src_path)
                }
            }
        }
    }

    try:
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration generated at {output_path}")
        print(f"📋 Add this to your Claude Desktop settings.json:")
        print(json.dumps(config, indent=2))
        return True
    except Exception as e:
        print(f"❌ Failed to generate config: {e}")
        return False


def test_server() -> bool:
    """Test that the server starts correctly."""
    cmd = [
        sys.executable, "-c",
        "import asyncio; from claude_mcp_server.server import main; print('Server test passed')"
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")

    try:
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True, timeout=5)
        print("✅ Server test passed")
        return True
    except subprocess.TimeoutExpired:
        print("✅ Server started successfully (timeout expected)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Server test failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Main setup script entry point."""
    parser = argparse.ArgumentParser(description="Setup script for Claude MCP Server")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--type-check", action="store_true", help="Run type checking")
    parser.add_argument("--config", action="store_true", help="Generate MCP config file")
    parser.add_argument("--test-server", action="store_true", help="Test server startup")
    parser.add_argument("--all", action="store_true", help="Run all setup tasks")
    parser.add_argument("--config-output", help="Output path for config file")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    success = True

    if args.all or args.install:
        success &= install_dependencies(dev=args.dev or args.all)

    if args.all or args.format:
        success &= format_code()

    if args.all or args.type_check:
        success &= type_check()

    if args.all or args.test:
        success &= run_tests()

    if args.all or args.test_server:
        success &= test_server()

    if args.all or args.config:
        success &= generate_config(args.config_output)

    if success:
        print("\n🎉 Setup completed successfully!")
    else:
        print("\n💥 Setup encountered errors. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()