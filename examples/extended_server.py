#!/usr/bin/env python3
"""
Example of extending the basic MCP server with additional tools.

This demonstrates how to add custom tools to the server for specific use cases.
"""

import asyncio
import json
import os
import requests
from typing import Any, Dict, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl

# Import the base server functionality
from claude_mcp_server.server import (
    handle_call_tool as base_call_tool,
    handle_list_tools as base_list_tools
)

# Create extended server
server = Server("extended-claude-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools (base tools + extended tools)."""
    # Get base tools
    base_tools = await base_list_tools()

    # Add extended tools
    extended_tools = [
        types.Tool(
            name="fetch_url",
            description="Fetch content from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to fetch"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds",
                        "default": 10
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="json_format",
            description="Format and validate JSON content",
            inputSchema={
                "type": "object",
                "properties": {
                    "json_string": {
                        "type": "string",
                        "description": "JSON string to format"
                    },
                    "indent": {
                        "type": "integer",
                        "description": "Indentation level",
                        "default": 2
                    }
                },
                "required": ["json_string"]
            }
        ),
        types.Tool(
            name="environment_info",
            description="Get environment variables and system path information",
            inputSchema={
                "type": "object",
                "properties": {
                    "show_sensitive": {
                        "type": "boolean",
                        "description": "Whether to show potentially sensitive environment variables",
                        "default": False
                    }
                }
            }
        ),
        types.Tool(
            name="word_count",
            description="Count words, lines, and characters in text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    }
                },
                "required": ["text"]
            }
        )
    ]

    return base_tools + extended_tools


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[types.TextContent]:
    """Handle tool calls (base tools + extended tools)."""
    if arguments is None:
        arguments = {}

    # Handle extended tools
    try:
        if name == "fetch_url":
            url = arguments.get("url", "")
            timeout = arguments.get("timeout", 10)

            if not url:
                return [types.TextContent(type="text", text="Error: No URL provided")]

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()

                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    try:
                        formatted_content = json.dumps(response.json(), indent=2)
                    except json.JSONDecodeError:
                        formatted_content = response.text
                else:
                    formatted_content = response.text

                result = f"URL: {url}\nStatus: {response.status_code}\nContent-Type: {content_type}\nContent-Length: {len(formatted_content)} characters\n\nContent:\n{formatted_content[:2000]}{'...' if len(formatted_content) > 2000 else ''}"

                return [types.TextContent(type="text", text=result)]

            except requests.RequestException as e:
                return [types.TextContent(type="text", text=f"Error fetching URL: {str(e)}")]

        elif name == "json_format":
            json_string = arguments.get("json_string", "")
            indent = arguments.get("indent", 2)

            if not json_string:
                return [types.TextContent(type="text", text="Error: No JSON string provided")]

            try:
                parsed = json.loads(json_string)
                formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
                return [types.TextContent(type="text", text=f"Formatted JSON:\n\n{formatted}")]
            except json.JSONDecodeError as e:
                return [types.TextContent(type="text", text=f"Error: Invalid JSON - {str(e)}")]

        elif name == "environment_info":
            show_sensitive = arguments.get("show_sensitive", False)

            # Potentially sensitive env var patterns
            sensitive_patterns = ['key', 'secret', 'token', 'password', 'auth', 'api']

            env_vars = {}
            for key, value in os.environ.items():
                if show_sensitive:
                    env_vars[key] = value
                else:
                    # Check if the env var might be sensitive
                    is_sensitive = any(pattern.lower() in key.lower() for pattern in sensitive_patterns)
                    if is_sensitive:
                        env_vars[key] = "[HIDDEN - use show_sensitive=true to view]"
                    else:
                        env_vars[key] = value

            path_info = {
                "PATH": os.environ.get("PATH", "").split(os.pathsep),
                "PYTHONPATH": os.environ.get("PYTHONPATH", "").split(os.pathsep) if os.environ.get("PYTHONPATH") else [],
                "Current Working Directory": os.getcwd(),
                "User Home": os.path.expanduser("~")
            }

            result = "Environment Variables:\n"
            for key in sorted(env_vars.keys()):
                result += f"  {key}={env_vars[key]}\n"

            result += "\nPath Information:\n"
            for key, value in path_info.items():
                if isinstance(value, list):
                    result += f"  {key}:\n"
                    for item in value:
                        if item:  # Skip empty strings
                            result += f"    - {item}\n"
                else:
                    result += f"  {key}: {value}\n"

            return [types.TextContent(type="text", text=result)]

        elif name == "word_count":
            text = arguments.get("text", "")

            if not text:
                return [types.TextContent(type="text", text="Error: No text provided")]

            lines = text.split('\n')
            words = text.split()
            characters = len(text)
            characters_no_spaces = len(text.replace(' ', ''))

            stats = {
                "Characters (with spaces)": characters,
                "Characters (without spaces)": characters_no_spaces,
                "Words": len(words),
                "Lines": len(lines),
                "Paragraphs": len([line for line in lines if line.strip()]),
                "Average words per line": len(words) / len(lines) if lines else 0,
            }

            result = "Text Statistics:\n"
            for key, value in stats.items():
                if isinstance(value, float):
                    result += f"  {key}: {value:.1f}\n"
                else:
                    result += f"  {key}: {value}\n"

            return [types.TextContent(type="text", text=result)]

        else:
            # Delegate to base tools
            return await base_call_tool(name, arguments)

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool '{name}': {str(e)}")]


async def main() -> None:
    """Main entry point for the extended MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            NotificationOptions()
        )


if __name__ == "__main__":
    asyncio.run(main())