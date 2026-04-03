"""Tests for the MCP server."""

import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from claude_mcp_server.server import handle_call_tool, handle_list_tools


class TestMCPServer:
    """Test suite for MCP server functionality."""

    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test that tools are listed correctly."""
        tools = await handle_list_tools()
        tool_names = [tool.name for tool in tools]

        expected_tools = [
            "read_file",
            "write_file",
            "list_directory",
            "get_system_info",
            "calculate",
            "get_timestamp"
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names

    @pytest.mark.asyncio
    async def test_calculate_tool(self):
        """Test the calculate tool."""
        # Test basic calculation
        result = await handle_call_tool("calculate", {"expression": "2 + 2"})
        assert len(result) == 1
        assert "2 + 2 = 4" in result[0].text

        # Test invalid expression
        result = await handle_call_tool("calculate", {"expression": "import os"})
        assert len(result) == 1
        assert "invalid characters" in result[0].text

    @pytest.mark.asyncio
    async def test_get_timestamp(self):
        """Test timestamp generation."""
        # Test ISO format (default)
        result = await handle_call_tool("get_timestamp", {})
        assert len(result) == 1
        assert "Current timestamp (iso):" in result[0].text

        # Test epoch format
        result = await handle_call_tool("get_timestamp", {"format": "epoch"})
        assert len(result) == 1
        assert "Current timestamp (epoch):" in result[0].text

    @pytest.mark.asyncio
    async def test_file_operations(self):
        """Test file read/write operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.txt"
            test_content = "Hello, MCP Server!"

            # Test write file
            result = await handle_call_tool("write_file", {
                "path": str(test_file),
                "content": test_content
            })
            assert len(result) == 1
            assert "Successfully wrote" in result[0].text

            # Test read file
            result = await handle_call_tool("read_file", {
                "path": str(test_file)
            })
            assert len(result) == 1
            assert test_content in result[0].text

    @pytest.mark.asyncio
    async def test_list_directory(self):
        """Test directory listing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            (Path(temp_dir) / "test.txt").write_text("test")
            (Path(temp_dir) / "subdir").mkdir()

            result = await handle_call_tool("list_directory", {"path": temp_dir})
            assert len(result) == 1
            assert "📁 subdir/" in result[0].text
            assert "📄 test.txt" in result[0].text

    @pytest.mark.asyncio
    async def test_get_system_info(self):
        """Test system info retrieval."""
        result = await handle_call_tool("get_system_info", {})
        assert len(result) == 1
        assert "System Information:" in result[0].text
        assert "platform:" in result[0].text
        assert "python_version:" in result[0].text

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test unknown tool
        result = await handle_call_tool("unknown_tool", {})
        assert len(result) == 1
        assert "Unknown tool" in result[0].text

        # Test read non-existent file
        result = await handle_call_tool("read_file", {"path": "/nonexistent/file.txt"})
        assert len(result) == 1
        assert "not found" in result[0].text