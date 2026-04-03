#!/usr/bin/env python3
"""
Example client for testing the MCP server locally.

This demonstrates how to interact with the MCP server programmatically,
which can be useful for testing and integration purposes.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict


class MCPTestClient:
    """Simple test client for MCP server."""

    def __init__(self, server_command: list[str]):
        self.server_command = server_command
        self.process = None

    async def __aenter__(self):
        """Start the MCP server process."""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Initialize the MCP connection
        await self.send_message({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            }
        })

        response = await self.receive_message()
        print(f"Initialization response: {response}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up the MCP server process."""
        if self.process:
            self.process.terminate()
            await self.process.wait()

    async def send_message(self, message: Dict[str, Any]):
        """Send a JSON-RPC message to the server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("Server process not running")

        message_str = json.dumps(message) + "\n"
        self.process.stdin.write(message_str.encode())
        await self.process.stdin.drain()

    async def receive_message(self) -> Dict[str, Any]:
        """Receive a JSON-RPC message from the server."""
        if not self.process or not self.process.stdout:
            raise RuntimeError("Server process not running")

        line = await self.process.stdout.readline()
        if not line:
            raise RuntimeError("Server closed connection")

        return json.loads(line.decode().strip())

    async def list_tools(self) -> list:
        """List available tools."""
        await self.send_message({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        })

        response = await self.receive_message()
        return response.get("result", {}).get("tools", [])

    async def call_tool(self, name: str, arguments: Dict[str, Any] = None) -> Any:
        """Call a specific tool."""
        if arguments is None:
            arguments = {}

        await self.send_message({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        })

        response = await self.receive_message()
        return response.get("result", {})


async def demo_mcp_server():
    """Demonstrate MCP server capabilities."""
    server_cmd = [sys.executable, "-m", "claude_mcp_server.server"]

    print("Starting MCP server demo...")

    try:
        async with MCPTestClient(server_cmd) as client:
            # List available tools
            print("\n=== Available Tools ===")
            tools = await client.list_tools()
            for tool in tools:
                print(f"- {tool['name']}: {tool['description']}")

            # Test some tools
            print("\n=== Testing Tools ===")

            # Test timestamp
            result = await client.call_tool("get_timestamp", {"format": "readable"})
            print(f"Timestamp: {result}")

            # Test calculation
            result = await client.call_tool("calculate", {"expression": "42 * 2"})
            print(f"Calculation: {result}")

            # Test system info
            result = await client.call_tool("get_system_info")
            print(f"System info (truncated): {str(result)[:200]}...")

            # Test file operations
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write("Test content from MCP demo")
                temp_file = f.name

            result = await client.call_tool("read_file", {"path": temp_file})
            print(f"File read: {result}")

            # Clean up
            import os
            os.unlink(temp_file)

    except Exception as e:
        print(f"Error during demo: {e}")
        return False

    print("\nDemo completed successfully!")
    return True


if __name__ == "__main__":
    success = asyncio.run(demo_mcp_server())
    sys.exit(0 if success else 1)