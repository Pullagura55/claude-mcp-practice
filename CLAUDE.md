# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python MCP (Model Context Protocol) server that provides essential tools for Claude to interact with local systems. The server is designed to be reusable across multiple projects and serves as a foundation for building more sophisticated MCP integrations.

## Architecture

### Core Components

- **`src/claude_mcp_server/server.py`**: Main MCP server implementation with tool handlers
- **`src/claude_mcp_server/__init__.py`**: Package initialization
- **`config/mcp-server-config.json`**: Example MCP server configuration
- **`pyproject.toml`**: Project configuration with dependencies and build settings
- **`scripts/setup.py`**: Comprehensive setup script for all development tasks
- **`examples/`**: Contains extension patterns and testing utilities

### Examples and Extensions

- **`examples/extended_server.py`**: Demonstrates how to extend the base server with additional tools (web requests, JSON formatting, environment info, text analysis). Shows the composition pattern for building specialized servers.
- **`examples/client_example.py`**: Test client that demonstrates programmatic interaction with the MCP server using JSON-RPC protocol. Useful for integration testing and understanding the MCP communication flow.

### Key Design Patterns

- **Tool-based Architecture**: Each functionality is exposed as a discrete MCP tool
- **Async/Await Pattern**: All MCP handlers use async/await for non-blocking operations
- **Error Handling**: Comprehensive error handling with user-friendly error messages
- **Type Safety**: Uses Pydantic for schema validation and type hints throughout
- **Extensibility**: Server can be extended by importing base functions and adding new tools
- **Composition over Inheritance**: Examples show how to compose servers rather than inherit

## Development Commands

### Quick Setup (Recommended)
```bash
# Complete setup: install, format, test, and generate config
python scripts/setup.py --all

# Setup with development dependencies
python scripts/setup.py --all --dev
```

### Manual Setup and Installation
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]

# Alternative: install via setup script
python scripts/setup.py --install --dev
```

### Running the Server
```bash
# Run standalone (for testing)
python -m claude_mcp_server.server

# Run with specific Python path
PYTHONPATH=./src python -m claude_mcp_server.server
```

### Development Tools
```bash
# Format code (or use setup script: --format)
black src/
isort src/

# Type checking (or use setup script: --type-check)
mypy src/

# Run all tests (or use setup script: --test)
pytest

# Run tests with coverage
pytest --cov=claude_mcp_server

# Run specific test file
pytest tests/test_server.py

# Run specific test function
pytest tests/test_server.py::TestMCPServer::test_calculate_tool
```

### Setup Script Capabilities
The `scripts/setup.py` provides a comprehensive development workflow:

```bash
# Individual tasks
python scripts/setup.py --install          # Install dependencies
python scripts/setup.py --dev              # Install dev dependencies  
python scripts/setup.py --format           # Format code (black + isort)
python scripts/setup.py --type-check       # Run mypy
python scripts/setup.py --test             # Run pytest
python scripts/setup.py --test-server      # Test server startup
python scripts/setup.py --config           # Generate MCP config

# Combined workflows
python scripts/setup.py --all              # Run everything
python scripts/setup.py --all --dev        # Run everything with dev deps

# Custom config output
python scripts/setup.py --config --config-output my-config.json
```

### Testing MCP Integration
```bash
# Test server startup (or use setup script: --test-server)
python -c "import asyncio; from claude_mcp_server.server import main; asyncio.run(main())"

# Run the example client to test full integration
PYTHONPATH=./src python examples/client_example.py
```

## MCP Server Configuration

### For Claude Desktop

Add to Claude Desktop's settings.json:
```json
{
  "mcpServers": {
    "claude-mcp-server": {
      "command": "python",
      "args": ["-m", "claude_mcp_server.server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/claude-mcp/src"
      }
    }
  }
}
```

### For Other Projects

1. Install the package: `pip install /path/to/claude-mcp`
2. Configure MCP client to use `claude_mcp_server.server` as the command

## Available MCP Tools

The server provides these tools for Claude to use:

- **`read_file`**: Read file contents (handles encoding and error cases)
- **`write_file`**: Write content to files (creates directories as needed)
- **`list_directory`**: List directory contents with file/folder indicators
- **`get_system_info`**: Retrieve system platform and environment information
- **`calculate`**: Perform basic mathematical calculations (with safety checks)
- **`get_timestamp`**: Generate timestamps in ISO, epoch, or readable formats

## Adding New Tools

### Method 1: Direct Extension (Simple)
To add a new tool to the existing server:

1. Add the tool definition in `handle_list_tools()`
2. Add the tool handler logic in `handle_call_tool()`
3. Follow the existing pattern for error handling and return types
4. Update this documentation

### Method 2: Server Composition (Recommended for Complex Extensions)
For more complex additions, use the pattern shown in `examples/extended_server.py`:

1. Import base functions from the main server
2. Create a new server instance
3. Combine base tools with new tools in `handle_list_tools()`
4. Delegate base tool calls to the imported `base_call_tool()` function

Example (Method 1):
```python
# In handle_list_tools():
types.Tool(
    name="my_new_tool",
    description="Description of what the tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)

# In handle_call_tool():
elif name == "my_new_tool":
    param1 = arguments.get("param1", "")
    # Tool logic here
    return [types.TextContent(type="text", text=result)]
```

Example (Method 2 - Composition):
```python
from claude_mcp_server.server import (
    handle_call_tool as base_call_tool,
    handle_list_tools as base_list_tools
)

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    base_tools = await base_list_tools()
    new_tools = [/* your tools */]
    return base_tools + new_tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None):
    if name == "my_new_tool":
        # Handle new tool
        pass
    else:
        # Delegate to base server
        return await base_call_tool(name, arguments)
```

## Testing Strategy

- **Unit Tests**: Test individual tool functions (`pytest tests/test_server.py`)
- **Integration Tests**: Test MCP protocol compliance using `examples/client_example.py`
- **Server Startup Tests**: Use `python scripts/setup.py --test-server` to verify server initialization
- **Manual Testing**: Use Claude Desktop or MCP client for end-to-end testing
- **Extension Testing**: Use `examples/extended_server.py` to test server composition patterns

## Security Considerations

- File operations are restricted to the current working directory context
- Mathematical calculations use basic eval() with character filtering
- No network operations are performed by default tools
- All file paths should be validated before use

## Cross-Project Usage

This server is designed to be portable:

1. **As a Package**: Install and import in other Python projects
2. **As a Standalone Service**: Run as a separate process that other applications can connect to
3. **As a Template**: Copy and modify for project-specific needs

## Configuration Management

- Use environment variables for paths and settings that change between deployments
- The `PYTHONPATH` environment variable is crucial for proper module loading
- Consider using `.env` files for local development configurations