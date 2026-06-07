# Agent Slouch Mode

[![Tests](https://github.com/yourusername/agent-slouch-mode/workflows/Tests/badge.svg)](https://github.com/yourusername/agent-slouch-mode/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)

MCP (Model Context Protocol) plugin that automatically pauses your AI agent when it detects you've stepped away from the computer.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [MCP Tools](#mcp-tools)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Development](#development)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-time Face Detection**: Uses camera to detect your presence
- **Smart Pause/Resume**: Automatically pauses when you step away
- **MCP Integration**: Full Model Context Protocol support with 4 tools
- **Health Monitoring**: Background thread monitoring with auto-recovery
- **Graceful Fallbacks**: Continues working even with missing optional dependencies
- **Structured Logging**: Comprehensive logging for debugging
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Configurable**: Extensive environment variable configuration
- **Production Ready**: Fully tested (14/14 tests passing)

## Quick Start

### Installation

```bash
pip install agent-slouch-mode
```

### Claude Desktop Integration

1. Edit `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "python",
      "args": ["-m", "slouch_mode"],
      "env": {
        "SLOTH_AGENT_WINDOW_TITLE": "Claude",
        "SLOTH_LEAVE_SECONDS": "60"
      }
    }
  }
}
```

2. Restart Claude Desktop

3. Ask Claude: "Is my agent paused?"

See [DEPLOY_CLAUDE.md](docs/DEPLOY_CLAUDE.md) for detailed setup instructions.

### Run Standalone

```bash
slouch-mode
```

## Installation

### From PyPI (Recommended)

```bash
pip install agent-slouch-mode
```

### From Source

```bash
git clone https://github.com/yourusername/agent-slouch-mode.git
cd agent-slouch-mode
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

Configuration can be set via environment variables or `.env` file:

### Environment Variables

```env
# Agent window title (default: "YourAgentName")
SLOTH_AGENT_WINDOW_TITLE=Claude

# Absence timeout in seconds (default: 60.0)
SLOTH_LEAVE_SECONDS=60

# Camera device index (default: 0)
SLOTH_CAMERA_INDEX=0

# Face detection FPS (default: 20)
SLOTH_DETECTION_FPS=20

# Face detector backend: "haar" or "mediapipe" (default: "haar")
SLOTH_FACE_DETECTOR_BACKEND=haar

# Health check interval in seconds (default: 30)
SLOTH_HEALTH_CHECK_INTERVAL=30

# Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
SLOTH_LOG_LEVEL=INFO
```

Create `.env` file in your project root:

```env
SLOTH_AGENT_WINDOW_TITLE=Claude
SLOTH_LEAVE_SECONDS=60
```

For full configuration options, see [docs/MCP_CONFIG.md](docs/MCP_CONFIG.md).

## Usage

### As MCP Server

```bash
slouch-mode
```

The server will start listening for MCP connections on stdio.

### With Claude Desktop

See [docs/DEPLOY_CLAUDE.md](docs/DEPLOY_CLAUDE.md) for step-by-step integration guide.

### With Continue IDE

Add to `.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "slouch-mode",
      "command": "python",
      "args": ["-m", "slouch_mode"]
    }
  ]
}
```

## MCP Tools

Once connected to the MCP server, the following tools are available:

### `get_status()`

Returns the current agent state.

**Returns**: `"working"` or `"paused"`

```
User: Is my agent paused?
Claude: Your agent is currently working
```

### `manual_pause()`

Manually pause the agent.

**Returns**: Confirmation message

### `manual_resume()`

Manually resume the agent.

**Returns**: Confirmation message

### `set_leave_timeout(seconds: float)`

Change the absence timeout.

**Parameters**:
- `seconds`: New timeout in seconds (e.g., 45.0)

**Returns**: Confirmation message

```
User: Change my away timeout to 45 seconds
Claude: Timeout changed from 60.0 to 45 seconds
```

## Claude Desktop Integration

For detailed Claude Desktop setup instructions, see [docs/DEPLOY_CLAUDE.md](docs/DEPLOY_CLAUDE.md).

### Quick Setup

1. Edit your Claude config file
2. Add slouch-mode MCP server configuration
3. Restart Claude Desktop
4. Use natural language to control

Example usage in Claude:

```
"Check if I'm paused"           ?ú calls get_status()
"Pause my work"                 ?ú calls manual_pause()
"Resume working"                ?ú calls manual_resume()
"Set timeout to 2 minutes"      ?ú calls set_leave_timeout(120)
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/agent-slouch-mode.git
cd agent-slouch-mode
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/slouch_mode

# Run specific test
pytest tests/test_mcp_integration.py
```

### Code Style

```bash
# Format with Black
black src/ tests/

# Check with Ruff
ruff check src/ tests/

# Type checking
mypy src/
```

For full development guide, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [MCP Configuration](docs/MCP_CONFIG.md)
- [Claude Desktop Integration](docs/DEPLOY_CLAUDE.md)
- [Full Status Report](docs/FINAL_STATUS_REPORT.md)

## Project Status

- ? Production Ready
- ? All Tests Passing (14/14)
- ? MCP 1.27.2 Integrated
- ? Claude Desktop Compatible
- ? Comprehensive Documentation

## Performance

- Memory: ~150-200MB
- CPU (idle): 2-5%
- Face Detection: 20 FPS
- MCP Tool Latency: <50ms

## Troubleshooting

### MCP Tools Not Appearing

1. Check Claude version (3.x required)
2. Verify config syntax using JSON validator
3. Restart Claude Desktop
4. See [docs/DEPLOY_CLAUDE.md](docs/DEPLOY_CLAUDE.md) ?ú Troubleshooting

### Camera Not Working

1. Check Windows Settings ?ú Privacy ?ú Camera
2. Enable Python in camera permissions
3. Test: `python -c "import cv2; cv2.VideoCapture(0)"`

### Face Detection Issues

- Ensure good lighting
- Check camera is not blocked
- Try adjusting `SLOTH_DETECTION_FPS`
- See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for debug logging

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)
- [Continue IDE](https://continue.dev/)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and recent changes.

## Acknowledgments

Built with:
- [OpenCV](https://opencv.org/) for face detection
- [Pydantic](https://docs.pydantic.dev/) for configuration
- [Structlog](https://www.structlog.org/) for structured logging
- [Tenacity](https://tenacity.readthedocs.io/) for retry logic
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) for protocol support

---

**Questions or Issues?**

- Check the [documentation](docs/)
- Review [existing issues](https://github.com/yourusername/agent-slouch-mode/issues)
- Start a [discussion](https://github.com/yourusername/agent-slouch-mode/discussions)
- Open an [issue](https://github.com/yourusername/agent-slouch-mode/issues/new)
