#!/usr/bin/env python3
"""
Basic MCP Server implementation with example tools.

This server provides basic functionality that can be extended for various use cases:
- File operations (read, write, list)
- System information
- Custom calculations
- Data processing utilities
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl


# Initialize the MCP server
server = Server("claude-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools for Claude to use."""
    return [
        types.Tool(
            name="read_file",
            description="Read the contents of a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["path"]
            }
        ),
        types.Tool(
            name="write_file",
            description="Write content to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["path", "content"]
            }
        ),
        types.Tool(
            name="list_directory",
            description="List contents of a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the directory to list",
                        "default": "."
                    }
                }
            }
        ),
        types.Tool(
            name="get_system_info",
            description="Get basic system information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="calculate",
            description="Perform basic mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                    }
                },
                "required": ["expression"]
            }
        ),
        types.Tool(
            name="get_timestamp",
            description="Get current timestamp in various formats",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "Format for the timestamp: 'iso', 'epoch', or 'readable'",
                        "default": "iso"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent]:
    """Handle tool calls from Claude."""
    if arguments is None:
        arguments = {}

    try:
        if name == "read_file":
            path = arguments.get("path", "")
            if not path:
                return [types.TextContent(type="text", text="Error: No path provided")]

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return [types.TextContent(type="text", text=f"File content:\n\n{content}")]
            except FileNotFoundError:
                return [types.TextContent(type="text", text=f"Error: File '{path}' not found")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]

        elif name == "write_file":
            path = arguments.get("path", "")
            content = arguments.get("content", "")

            if not path:
                return [types.TextContent(type="text", text="Error: No path provided")]

            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return [types.TextContent(type="text", text=f"Successfully wrote {len(content)} characters to '{path}'")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error writing file: {str(e)}")]

        elif name == "list_directory":
            path = arguments.get("path", ".")

            try:
                items = []
                for item in sorted(os.listdir(path)):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        items.append(f"📁 {item}/")
                    else:
                        size = os.path.getsize(item_path)
                        items.append(f"📄 {item} ({size} bytes)")

                result = f"Contents of '{path}':\n" + "\n".join(items)
                return [types.TextContent(type="text", text=result)]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error listing directory: {str(e)}")]

        elif name == "get_system_info":
            import platform
            info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "current_working_directory": os.getcwd(),
                "user": os.getenv("USER", os.getenv("USERNAME", "unknown"))
            }

            result = "System Information:\n" + "\n".join([f"- {k}: {v}" for k, v in info.items()])
            return [types.TextContent(type="text", text=result)]

        elif name == "calculate":
            expression = arguments.get("expression", "")
            if not expression:
                return [types.TextContent(type="text", text="Error: No expression provided")]

            try:
                # Basic safety check - only allow basic math operations
                allowed_chars = set("0123456789+-*/()., ")
                if not all(c in allowed_chars for c in expression):
                    return [types.TextContent(type="text", text="Error: Expression contains invalid characters")]

                result = eval(expression)
                return [types.TextContent(type="text", text=f"{expression} = {result}")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Error evaluating expression: {str(e)}")]

        elif name == "get_timestamp":
            format_type = arguments.get("format", "iso")
            now = datetime.now()

            if format_type == "epoch":
                result = str(int(now.timestamp()))
            elif format_type == "readable":
                result = now.strftime("%Y-%m-%d %H:%M:%S")
            else:  # iso
                result = now.isoformat()

            return [types.TextContent(type="text", text=f"Current timestamp ({format_type}): {result}")]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool '{name}': {str(e)}")]


@server.list_resources()
async def handle_list_resources() -> List[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri=AnyUrl("file://server-info"),
            name="Server Information",
            description="Information about this MCP server",
            mimeType="text/plain"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Handle resource read requests."""
    if str(uri) == "file://server-info":
        info = {
            "name": "Claude MCP Server",
            "version": "0.1.0",
            "description": "A basic Python MCP server for Claude integration",
            "tools": len(await handle_list_tools()),
            "capabilities": [
                "File operations (read, write, list)",
                "System information",
                "Basic calculations",
                "Timestamp generation"
            ]
        }
        return json.dumps(info, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")


async def main() -> None:
    """Main entry point for the MCP server."""
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            NotificationOptions()
        )


if __name__ == "__main__":
    asyncio.run(main())