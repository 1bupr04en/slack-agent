# Agent Slouch Mode - Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Install Dependencies
```bash
cd d:\??\agent-slouch-mode
pip install -e .
```

### 2. Create Configuration
```bash
copy .env.example .env
```

Edit `.env` with your settings:
```env
SLOTH_AGENT_WINDOW_TITLE=Cursor
SLOTH_LEAVE_SECONDS=60
SLOTH_CAMERA_INDEX=0
SLOTH_FACE_DETECTOR_BACKEND=haar
```

### 3. Verify Installation
```bash
python test_basic.py
```

Expected output: **Total: 5/5 passed**

## Running the Plugin

### Option A: Direct Command
```bash
slouch-mode
```

This starts the MCP server on stdio.

### Option B: Debug Mode
```bash
python -m slouch_mode
```

## Test Suites

### Basic Tests (Core Functionality)
```bash
python test_basic.py
```
Tests: Imports, State Machine, Face Detector, Workflow, Logging

### Advanced Tests (Camera & Threading)
```bash
python test_advanced.py
```
Tests: Camera Monitor, Health Checker, MCP Tools

### Summary Report
```bash
python test_report.py
```
Comprehensive project status check

## Configuration Options

```env
# Required
SLOTH_AGENT_WINDOW_TITLE=Cursor        # Window title to pause/resume

# Timing
SLOTH_LEAVE_SECONDS=60                 # Seconds before auto-pause
SLOTH_DETECTION_FPS=20                 # Detection frequency
SLOTH_HEALTH_CHECK_INTERVAL=30         # Health check frequency

# Detection
SLOTH_CAMERA_INDEX=0                   # Camera device (0=default)
SLOTH_FACE_DETECTOR_BACKEND=haar       # haar or mediapipe
SLOTH_ABSENT_FRAME_THRESHOLD=30        # Frames to confirm absence

# Other
SLOTH_LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
SLOTH_CAMERA_REOPEN_RETRIES=3          # Retry count on failure
```

## Troubleshooting

### Camera Issues
```bash
# Check if camera is accessible
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"

# Try different camera index
SLOTH_CAMERA_INDEX=1 python test_basic.py
```

### Import Errors
```bash
# Verify installation
pip show agent-slouch-mode

# Reinstall
pip uninstall agent-slouch-mode
pip install -e .
```

### Face Detection Issues
- Ensure good lighting
- Try different SLOTH_DETECTION_FPS (lower = slower but more accurate)
- Try MediaPipe backend: `pip install mediapipe`

## Architecture Overview

```
???????????????????????????????????????????
?     Camera Monitor (Background Thread)   ?
?  - Captures frames @ 20 FPS             ?
?  - Detects faces with Haar Cascade      ?
?  - Sends presence updates               ?
???????????????????????????????????????????
               ?
               v
        State Machine
    (WORKING ? ABSENT ? SLOTHING)
               ?
               v
    Workflow Controller
    - pause() : Save + Minimize
    - resume() : Restore Window
               ?
               v
          Target Agent
         (Cursor/Claude)
```

## MCP Tool Usage (When Connected)

Once connected to your agent (Claude Desktop, etc.):

```javascript
// Get current status
get_status()  // Returns: "working" or "paused"

// Manually pause
manual_pause()  // Returns: "Agent paused"

// Manually resume
manual_resume()  // Returns: "Agent resumed"

// Change timeout dynamically
set_leave_timeout(45)  // 45 seconds
```

## Next Steps

1. **Run basic tests:** `python test_basic.py`
2. **Start the plugin:** `slouch-mode`
3. **Connect to your agent** (if using MCP mode)
4. **Adjust settings** via .env file as needed

## Support

All core functionality is tested and working. For issues:

1. Check `TEST_RESULTS.md` for detailed test output
2. Review `.env` configuration
3. Check logs with `SLOTH_LOG_LEVEL=DEBUG`
4. Run diagnostic tests

---

**Status:** Production Ready ?  
**Last Updated:** 2026-06-05
