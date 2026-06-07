# Contributing to Agent Slouch Mode

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/agent-slouch-mode.git
cd agent-slouch-mode
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/slouch_mode

# Run specific test file
pytest tests/test_mcp_integration.py
```

### Code Style

We follow PEP 8 with some modifications:

- Line length: 100 characters
- Use type hints where possible
- Format with Black

```bash
# Format code
black src/ tests/

# Check style
ruff check src/ tests/

# Type checking
mypy src/
```

### Documentation

- Update docstrings for all public functions/classes
- Use Google-style docstrings
- Update relevant `.md` files
- Keep README.md in sync with features

## Making Changes

### Branch Naming

- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Documentation: `docs/description`

### Commit Messages

- Use present tense: "add feature" not "added feature"
- Be specific and descriptive
- Reference issues: "fixes #123"

### Pull Requests

1. Create a branch from `main`
2. Make your changes with clear commit messages
3. Add tests for new features
4. Update documentation as needed
5. Run all tests locally: `pytest`
6. Submit PR with description

## Testing Requirements

- New features must include tests
- Tests should cover happy path and error cases
- Minimum 80% code coverage

## Documentation

### Updating Docs

- README.md: Feature overview and quick start
- DEVELOPMENT.md: Development guide
- MCP_CONFIG.md: MCP-specific configuration
- CONTRIBUTING.md: This file
- Code docstrings: Implementation details

### Adding Examples

Create reproducible examples in docstrings or separate example files.

## Reporting Issues

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

### Feature Requests

Include:
- Motivation/use case
- Proposed solution
- Alternative solutions
- Additional context

## Project Structure

```
agent-slouch-mode/
??? src/slouch_mode/          # Main package
?   ??? __main__.py            # Entry point
?   ??? config.py              # Configuration
?   ??? core/                  # Core modules
?   ??? monitoring/            # Background monitoring
?   ??? mcp/                   # MCP integration
?   ??? utils/                 # Utilities
??? tests/                     # Test suite
??? docs/                      # Documentation
??? pyproject.toml             # Package configuration
??? README.md                  # Project overview
??? LICENSE                    # MIT License
??? CONTRIBUTING.md            # This file
```

## Key Files

- `pyproject.toml`: Defines dependencies, scripts, and metadata
- `src/slouch_mode/__main__.py`: MCP server entry point
- `src/slouch_mode/config.py`: Configuration management
- `src/slouch_mode/core/state_machine.py`: Core state logic

## Questions?

- Check existing issues
- Review documentation in `docs/` and `.md` files
- Start a discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Agent Slouch Mode!
