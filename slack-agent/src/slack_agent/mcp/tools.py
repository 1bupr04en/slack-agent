"""MCP tool definitions (FastMCP)."""

import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from slouch_mode.config import settings

logger = logging.getLogger(__name__)

mcp = FastMCP("Sloth Mode")

# Will be set from __main__
_controller: Optional[object] = None


def set_controller(ctrl) -> None:
    """Set the workflow controller for MCP tools."""
    global _controller
    _controller = ctrl
    logger.info("WorkflowController set for MCP tools")


@mcp.tool()
def get_status() -> str:
    """Return 'working' or 'paused'."""
    if _controller is None:
        logger.warning("get_status called before _controller initialized")
        return "error: controller not initialized"
    return "paused" if _controller.is_paused else "working"


@mcp.tool()
def manual_pause() -> str:
    """Manually trigger sloth mode."""
    if _controller is None:
        return "error: controller not initialized"
    if _controller.is_paused:
        return "Already paused"
    result = _controller.pause()
    return "Agent paused" if result else "Failed to pause"


@mcp.tool()
def manual_resume() -> str:
    """Manually resume work."""
    if _controller is None:
        return "error: controller not initialized"
    if not _controller.is_paused:
        return "Already working"
    result = _controller.resume()
    return "Agent resumed" if result else "Failed to resume"


@mcp.tool()
def set_leave_timeout(seconds: float) -> str:
    """Dynamically change leave timeout."""
    old_value = settings.leave_seconds
    settings.leave_seconds = seconds
    logger.info("Leave timeout changed from %s to %s", old_value, seconds)
    return f"Timeout changed from {old_value} to {seconds} seconds"
