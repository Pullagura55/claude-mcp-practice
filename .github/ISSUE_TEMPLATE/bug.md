---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Reproduction Steps

Steps to reproduce the behavior:

1. Set up environment with '...'
2. Run command '...'
3. Call MCP tool '...'
4. See error

## Error Messages

If applicable, paste the complete error message and stack trace:

```
[Paste error message here]
```

## Environment Information

**System Details:**
- OS: [e.g., Windows 11, macOS 14.0, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- Claude MCP Server Version: [e.g., 1.0.0]

**MCP Configuration:**
```json
{
  "mcpServers": {
    // Paste relevant MCP server config (remove sensitive tokens)
  }
}
```

**Dependency Versions:**
```bash
# Output of: pip list | grep -E "(mcp|claude|anthropic)"
[Paste output here]
```

## MCP Tool Information

**Tool Name:** [e.g., read_file, calculate, get_system_info]

**Tool Input:**
```json
{
  // Paste the tool input parameters that caused the issue
}
```

**Tool Output/Error:**
```json
{
  // Paste the tool response or error
}
```

## Additional Context

### Screenshots

If applicable, add screenshots to help explain your problem.

### Log Output

If available, include relevant log output:

```
[Paste log output here]
```

### Related Issues

- Link to any related issues or discussions
- Reference any similar bugs or feature requests

### Workarounds

- Describe any temporary workarounds you've found
- Note if the workaround is sufficient for your use case

## Impact Assessment

**Severity:** [Low/Medium/High/Critical]

**Frequency:** [Always/Often/Sometimes/Rarely]

**User Impact:** [Describe how this affects users]

## Proposed Solution

If you have ideas for fixing this bug, please describe them here:

- Potential root cause
- Suggested implementation approach
- Any code pointers or references

## Checklist

- [ ] I have searched existing issues for duplicates
- [ ] I have provided all requested information
- [ ] I have tested with the latest version
- [ ] I have included reproduction steps
- [ ] I have removed any sensitive information from logs/config