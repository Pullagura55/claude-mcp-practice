# Development Workflow

This document outlines the development workflow and processes for the Claude MCP Server project.

## Branch Strategy

### Main Branches

- **`main`**: Production-ready code. All releases are tagged from this branch.
- **`develop`**: Integration branch for features. All feature branches merge here first.

### Feature Branches

- **Naming**: `feature/description-of-feature`
- **Purpose**: Development of new features or enhancements
- **Lifecycle**: Created from `develop`, merged back to `develop`

### Bug Fix Branches

- **Naming**: `bugfix/description-of-bug`
- **Purpose**: Fix bugs in the current release
- **Lifecycle**: Created from `develop` or `main`, merged back to source branch

### Hotfix Branches

- **Naming**: `hotfix/critical-issue-description`
- **Purpose**: Critical fixes that need immediate deployment
- **Lifecycle**: Created from `main`, merged to both `main` and `develop`

## Development Process

### 1. Planning Phase

1. **Issue Creation**: Create GitHub issue with appropriate template
2. **Discussion**: Team discusses implementation approach
3. **Assignment**: Issue assigned to developer
4. **Branch Creation**: Create feature/bugfix branch from `develop`

### 2. Development Phase

1. **Local Setup**:
   ```bash
   git clone <repository>
   cd claude-mcp
   python scripts/setup.py --all --dev
   ```

2. **Development Cycle**:
   ```bash
   # Make changes
   python scripts/setup.py --format      # Format code
   python scripts/setup.py --type-check  # Type checking
   python scripts/setup.py --test        # Run tests
   git add .
   git commit -m "descriptive commit message"
   ```

3. **Regular Sync**:
   ```bash
   git fetch origin
   git rebase origin/develop
   ```

### 3. Testing Phase

#### Automated Testing

- **Unit Tests**: `pytest tests/`
- **Type Checking**: `mypy src/`
- **Integration Tests**: `python examples/client_example.py`
- **Server Tests**: `python scripts/setup.py --test-server`

#### Manual Testing

- Test with Claude Desktop integration
- Verify MCP protocol compliance
- Test error handling scenarios
- Performance testing for large operations

### 4. Review Phase

1. **Pre-PR Checklist**:
   - [ ] All tests pass
   - [ ] Code formatted and type-checked
   - [ ] Documentation updated
   - [ ] CHANGELOG.md updated (if applicable)

2. **Pull Request Creation**:
   - Use PR template
   - Link related issues
   - Add reviewers
   - Set appropriate labels

3. **Code Review Process**:
   - At least one approval required
   - Address all feedback
   - Re-run tests after changes
   - Squash commits if needed

### 5. Integration Phase

1. **Merge to Develop**:
   - Use "Squash and merge" for feature branches
   - Use "Merge commit" for release branches

2. **Integration Testing**:
   - Automated CI/CD pipeline runs
   - Integration tests with full MCP stack
   - Performance regression testing

### 6. Release Phase

#### Preparation

1. **Release Branch**: Create `release/vX.Y.Z` from `develop`
2. **Version Bump**: Update version numbers
3. **Documentation**: Update CHANGELOG.md and README.md
4. **Final Testing**: Complete regression testing

#### Release

1. **Merge to Main**: Merge release branch to `main`
2. **Tag Release**: Create git tag `vX.Y.Z`
3. **Merge Back**: Merge `main` back to `develop`
4. **Publish**: Deploy/publish the release

## Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Test additions or modifications
- **chore**: Build process or auxiliary tool changes

### Examples

```
feat(server): add file encryption tool

Add new MCP tool for encrypting/decrypting files using AES-256.
Includes comprehensive error handling and input validation.

Closes #123
```

```
fix(calculate): handle division by zero

The calculate tool now properly catches ZeroDivisionError and returns
a user-friendly error message instead of crashing.

Fixes #456
```

## CI/CD Pipeline

### Continuous Integration

**Triggers**: Push to any branch, PR creation/update

**Stages**:
1. **Setup**: Install dependencies
2. **Lint**: Code formatting and style checks
3. **Type Check**: mypy type checking
4. **Test**: Run unit and integration tests
5. **Security**: Security vulnerability scanning

### Continuous Deployment

**Triggers**: Push to `main` branch, release tag creation

**Stages**:
1. **Build**: Package the application
2. **Test**: Final integration tests
3. **Deploy**: Deploy to production/publish package
4. **Notify**: Send notifications to team

## Quality Gates

### Pre-Merge Requirements

- [ ] All CI checks pass
- [ ] Code coverage ≥ 80%
- [ ] No critical security vulnerabilities
- [ ] At least one code review approval
- [ ] Documentation updated
- [ ] Breaking changes documented

### Release Requirements

- [ ] All integration tests pass
- [ ] Performance benchmarks met
- [ ] Security audit completed
- [ ] Documentation complete
- [ ] Changelog updated

## Emergency Procedures

### Hotfix Process

1. **Assessment**: Evaluate severity and impact
2. **Branch**: Create hotfix branch from `main`
3. **Fix**: Implement minimal fix
4. **Test**: Quick but thorough testing
5. **Review**: Expedited code review
6. **Deploy**: Merge to `main` and deploy
7. **Backport**: Merge fix to `develop`

### Rollback Process

1. **Identify**: Confirm issue requires rollback
2. **Revert**: Revert problematic commits
3. **Test**: Verify rollback resolves issue
4. **Deploy**: Push rollback to production
5. **Communicate**: Notify stakeholders
6. **Post-Mortem**: Conduct retrospective

## Tools and Automation

### Development Tools

- **Code Formatting**: black, isort
- **Type Checking**: mypy
- **Testing**: pytest
- **Dependency Management**: pip, pip-tools
- **Documentation**: Sphinx (if applicable)

### Automation Scripts

- **Setup**: `python scripts/setup.py --all`
- **Testing**: `python scripts/setup.py --test`
- **Formatting**: `python scripts/setup.py --format`
- **Type Checking**: `python scripts/setup.py --type-check`

## Communication

### Channels

- **Issues**: GitHub issues for bug reports and feature requests
- **Pull Requests**: Code review and discussion
- **Releases**: GitHub releases with changelog
- **Documentation**: README.md and CLAUDE.md

### Notifications

- **PR Reviews**: Assign specific reviewers
- **Critical Issues**: Tag team members
- **Releases**: Announce in team channels
- **Security**: Private disclosure for vulnerabilities