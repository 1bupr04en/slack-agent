# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-05

### Added

- Initial release of Agent Slouch Mode
- Real-time face detection using Haar Cascade classifier
- 3-state finite state machine (WORKING ? ABSENT ? SLOTHING)
- Automatic pause/resume workflow control
- MCP (Model Context Protocol) integration
- Four MCP tools: `get_status()`, `manual_pause()`, `manual_resume()`, `set_leave_timeout()`
- Background camera monitoring thread with auto-recovery
- Health checking thread for monitoring thread liveness
- Structured logging with structlog
- Cross-platform notifications (Windows, macOS, Linux)
- Configuration management with pydantic-settings
- Environment variable support
- Comprehensive test suite (14 tests, 100% passing)
- Claude Desktop integration guide
- Continue IDE compatibility

### Features

- **Face Detection**: Haar Cascade-based real-time detection
- **State Machine**: 3-state slouch mode lifecycle
- **MCP Tools**: Remote control via Model Context Protocol
- **Health Monitoring**: Auto-restart on thread failure
- **Graceful Fallbacks**: Continues operation with missing optional dependencies
- **Structured Logging**: JSON-capable logging with structlog
- **Cross-Platform**: Windows, macOS, Linux support

### Documentation

- README.md: Project overview and quick start
- QUICKSTART.md: Setup and installation guide
- DEVELOPMENT.md: Development and architecture guide
- MCP_CONFIG.md: Detailed MCP configuration
- DEPLOY_CLAUDE.md: Claude Desktop integration steps
- CONTRIBUTING.md: Contribution guidelines
- CHANGELOG.md: Version history

### Testing

- 5 basic functionality tests
- 3 advanced monitoring tests
- 5 MCP integration tests
- 1 server startup test
- Test coverage for all core modules

### Dependencies

- opencv-python 4.13.0+
- pydantic-settings 2.14.0+
- tenacity 9.1.0+
- structlog 25.5.0+
- mcp 1.27.2+

### Optional Dependencies

- desktop-api: Advanced window control
- win10toast: Windows native notifications
- mediapipe: Alternative face detection backend

---

## [Unreleased]

### Planned Features

- Eye closure detection for improved slouch detection
- Multiple window support
- Web UI dashboard
- Advanced face tracking (position, gaze direction)
- IDE-specific plugins (VSCode, JetBrains)
- Custom notification sounds
- Data visualization and analytics
- Integration with more code editors

---

## Notes

### Version 1.0.0 Status

- ? Production ready
- ? All tests passing (14/14)
- ? Comprehensive documentation
- ? MCP fully integrated
- ? Zero known issues

### Backward Compatibility

Version 1.0.0 is the initial release. Future releases will maintain backward compatibility for the MCP tool API and configuration format where possible.

---

For more information, see:
- [README.md](README.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [LICENSE](LICENSE)
