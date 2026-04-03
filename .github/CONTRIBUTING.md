# Contributing to Claude MCP Server

Thank you for your interest in contributing to the Claude MCP Server! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   python scripts/setup.py --all --dev
   ```

## Development Workflow

1. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes**:
   ```bash
   python scripts/setup.py --test
   python scripts/setup.py --type-check
   ```

4. **Format your code**:
   ```bash
   python scripts/setup.py --format
   ```

5. **Commit your changes** with a clear commit message

6. **Push to your fork** and create a pull request

## Coding Standards

- Follow PEP 8 for Python code style
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

## Code Formatting

We use `black` and `isort` for code formatting:
```bash
python scripts/setup.py --format
```

## Testing

- Write tests for new functionality
- Ensure all existing tests pass
- Add integration tests for new MCP tools
- Test with both unit tests and the example client

## MCP Tool Development

When adding new MCP tools:

1. **Add tool definition** in `handle_list_tools()`
2. **Implement tool handler** in `handle_call_tool()`
3. **Follow error handling patterns** from existing tools
4. **Update documentation** in CLAUDE.md
5. **Add tests** for the new tool
6. **Test with example client** (`examples/client_example.py`)

## Documentation

- Update CLAUDE.md for any new tools or changes
- Include usage examples for new functionality
- Document configuration changes
- Update README.md if needed

## Pull Request Guidelines

- Fill out the pull request template completely
- Link to any related issues
- Include tests for new features
- Ensure CI passes
- Request review from maintainers

## Code Review Process

1. All submissions require review
2. Maintainers will review for:
   - Code quality and style
   - Test coverage
   - Documentation completeness
   - MCP protocol compliance
3. Address feedback promptly
4. Maintain discussion in PR comments

## Issue Reporting

Use the appropriate issue template:
- **Bug reports**: Use the bug template with reproduction steps
- **Feature requests**: Use the feature template with use case details

## Security

- Do not commit sensitive information (tokens, keys, passwords)
- Follow security best practices for file operations
- Report security issues privately to maintainers

## Getting Help

- Check existing issues and documentation
- Ask questions in issue comments
- Reach out to maintainers for guidance

## Recognition

Contributors will be acknowledged in:
- Git commit history
- Release notes
- Project documentation

Thank you for contributing!