# Claude MCP Server

A basic Python MCP (Model Context Protocol) server that provides essential tools for Claude to interact with the local system. This server can be used across multiple projects and provides a foundation for building more sophisticated MCP integrations.

## Features

- **File Operations**: Read, write, and list files and directories
- **System Information**: Get platform and environment details
- **Calculations**: Perform basic mathematical operations
- **Timestamps**: Generate timestamps in various formats
- **Extensible**: Easy to add new tools and capabilities

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. For development:
```bash
pip install -e .[dev]
```

## Usage

### Running the Server Standalone

```bash
python -m claude_mcp_server.server
```

### Using with Claude Desktop

Add the server configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "claude-mcp-server": {
      "command": "python",
      "args": ["-m", "claude_mcp_server.server"],
      "env": {
        "PYTHONPATH": "/path/to/claude-mcp/src"
      }
    }
  }
}
```

### Using in Other Projects

1. Install the package in your project:
```bash
pip install /path/to/claude-mcp
```

2. Configure your MCP client to connect to the server.

## Available Tools

- `read_file`: Read file contents
- `write_file`: Write content to files
- `list_directory`: List directory contents
- `get_system_info`: Get system information
- `calculate`: Perform mathematical calculations
- `get_timestamp`: Generate timestamps

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black src/
isort src/
```

Type checking:
```bash
mypy src/
```