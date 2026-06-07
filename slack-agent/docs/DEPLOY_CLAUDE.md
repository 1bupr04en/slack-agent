# Deploy Slouch Mode to Claude Desktop

## Step 1: Verify Installation

```bash
# Check Python
python --version  # Should be 3.9 or later

# Check MCP
pip show mcp  # Should show version 1.27.2

# Check slouch-mode
python -c "from slouch_mode import __version__; print(f'Slouch Mode installed')"
```

## Step 2: Locate Claude Desktop Config

### Windows
```
C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json
```

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

## Step 3: Create/Edit Config File

### Option A: Basic Configuration

Open the config file and add:

```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "python",
      "args": ["-m", "slouch_mode"]
    }
  }
}
```

### Option B: With Configuration

```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "python",
      "args": ["-m", "slouch_mode"],
      "env": {
        "SLOTH_AGENT_WINDOW_TITLE": "Claude",
        "SLOTH_LEAVE_SECONDS": "60",
        "SLOTH_CAMERA_INDEX": "0",
        "SLOTH_DETECTION_FPS": "20",
        "SLOTH_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Option C: From Project Directory

```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "python",
      "args": ["-m", "slouch_mode"],
      "env": {
        "SLOTH_AGENT_WINDOW_TITLE": "Claude",
        "SLOTH_LEAVE_SECONDS": "60",
        "PYTHONPATH": "d:\\??\\agent-slouch-mode\\src"
      }
    }
  }
}
```

## Step 4: Test Configuration

Restart Claude Desktop and check:

1. **Open Developer Tools** (Ctrl+Shift+I)
2. **Look for Slouch Mode** in the Tools panel
3. **Should see:** get_status, manual_pause, manual_resume, set_leave_timeout

## Step 5: Try Commands

### Test 1: Check Status
```
What's my current work status?
```
Claude will call `get_status()` and report.

### Test 2: Pause Agent
```
Pause my work session
```
Claude will call `manual_pause()`.

### Test 3: Resume Work
```
Resume my session
```
Claude will call `manual_resume()`.

### Test 4: Change Timeout
```
Change my away timeout to 45 seconds
```
Claude will call `set_leave_timeout(45)`.

## Troubleshooting

### Tools Don't Appear

**Check 1: Claude Version**
- Requires Claude 3.x or later
- Update Claude: Settings ? Check for Updates

**Check 2: Config Syntax**
- Use JSON validator: `python -m json.tool` to verify syntax
- Ensure paths use correct slashes (Windows: `\\` or `/`)

**Check 3: Python Path**
```bash
which python  # Unix/Mac
where python  # Windows
```
Use absolute path if needed:
```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "C:\\Users\\<Username>\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
      "args": ["-m", "slouch_mode"]
    }
  }
}
```

### Connection Error

**Error:** "Failed to connect to slouch-mode"

**Solution:**
```bash
# Test MCP server directly
python -m slouch_mode

# Should output: "Listening for MCP connections on stdio..."
# Press Ctrl+C to stop
```

### Camera Permission Issues (Windows)

If camera doesn't work:

1. **Check Camera in Settings:**
   - Settings ? Privacy ? Camera
   - Ensure Python has permission

2. **Grant App Permission:**
   - Settings ? Privacy ? Camera
   - Toggle Python.exe on

### Missing Dependencies

```bash
# Reinstall with dependencies
pip install --upgrade mcp

# Verify
python -m slouch_mode --version
```

## Advanced Configuration

### Multiple MCP Servers

```json
{
  "mcpServers": {
    "slouch-mode": {
      "command": "python",
      "args": ["-m", "slouch_mode"],
      "env": {"SLOTH_AGENT_WINDOW_TITLE": "Claude"}
    },
    "other-server": {
      "command": "python",
      "args": ["-m", "other_mcp_server"]
    }
  }
}
```

### Custom Camera Index

If you have multiple cameras:

```json
{
  "env": {
    "SLOTH_CAMERA_INDEX": "1"  // Use camera 1 instead of 0
  }
}
```

### Debug Logging

```json
{
  "env": {
    "SLOTH_LOG_LEVEL": "DEBUG"
  }
}
```

Then check Claude's logs:
- **Windows:** `%APPDATA%\Claude\logs`
- **macOS:** `~/Library/Logs/Claude`
- **Linux:** `~/.cache/Claude/logs`

## Alternative: Continue IDE

For Continue IDE (VS Code extension):

1. Install Continue extension
2. Add to `.continue/config.json`:

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

## Alternative: Direct Python

Run directly without Claude:

```bash
# Start server
python -m slouch_mode

# In another terminal, test
python -c "
from slouch_mode.mcp.tools import get_status, set_controller
from slouch_mode.core.workflow import WorkflowController

set_controller(WorkflowController())
print(get_status())
"
```

## Performance Optimization

If experiencing lag:

1. **Lower detection FPS:**
   ```json
   {
     "env": {
       "SLOTH_DETECTION_FPS": "10"
     }
   }
   ```

2. **Increase health check interval:**
   ```json
   {
     "env": {
       "SLOTH_HEALTH_CHECK_INTERVAL": "60"
     }
   }
   ```

3. **Monitor resources:**
   - Open Task Manager (Windows)
   - Search for "Python" or "slouch-mode"
   - Check CPU/Memory usage

## Security Best Practices

1. **Keep camera pointed away** from sensitive information
2. **Disable logging** in production:
   ```json
   {
     "env": {
       "SLOTH_LOG_LEVEL": "ERROR"
     }
   }
   ```
3. **Run in isolated environment** if needed
4. **Review face detection** accuracy before deploying

## Next Steps

1. ? Configure Claude Desktop (you are here)
2. Test with various prompts
3. Adjust timeouts based on your preferences
4. Optional: Install desktop-api for better window control
5. Optional: Switch to MediaPipe for better face detection

## Getting Help

- **View logs:** Check Claude's developer console (F12)
- **Test directly:** `python -m slouch_mode`
- **Check config:** `python -m json.tool < claude_desktop_config.json`
- **Report issues:** Include logs and Python version

---

**Deployment Status:** Ready ?  
**MCP Version:** 1.27.2  
**Estimated Setup Time:** 5 minutes
