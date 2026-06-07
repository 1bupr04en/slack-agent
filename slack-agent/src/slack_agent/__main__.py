"""Entry point: assemble components and run MCP server."""

import sys
import logging
import cv2
import importlib
from slouch_mode.config import settings
from slouch_mode.utils.logging import configure_logging
from slouch_mode.core.workflow import WorkflowController
from slouch_mode.core.state_machine import SlouchStateMachine
from slouch_mode.monitoring.camera import CameraMonitor
from slouch_mode.monitoring.health import HealthChecker
from slouch_mode.mcp.tools import set_controller, mcp

logger = logging.getLogger(__name__)


def self_test() -> None:
    """Verify camera and dependencies before starting."""
    try:
        cap = cv2.VideoCapture(settings.camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Camera index {settings.camera_index} is not available")
        cap.release()
    except Exception as exc:
        logger.error("Self-test failed: %s", exc)
        raise RuntimeError("Camera not available") from exc

    for module_name in ("structlog", "tenacity", "desktop_api"):
        try:
            importlib.import_module(module_name)
        except ImportError:
            logger.warning("Optional dependency %s is not installed", module_name)

    logger.info("Self-test completed successfully")


def main() -> None:
    """Main entry point for the slouch mode plugin."""
    configure_logging(settings.log_level)
    logger.info("Starting Agent Slouch Mode")
    
    self_test()
    
    # Assemble components
    workflow = WorkflowController()
    state_machine = SlouchStateMachine(
        on_pause=workflow.pause,
        on_resume=workflow.resume,
        leave_seconds=settings.leave_seconds,
    )
    monitor = CameraMonitor(state_machine)
    health = HealthChecker(monitor, state_machine, settings.health_check_interval)
    set_controller(workflow)
    
    # Start background threads
    logger.info("Starting background monitoring threads")
    monitor.start()
    health.start()
    
    logger.info("Slouch mode ready - waiting for connections")
    
    try:
        mcp.run(transport="stdio")
    except Exception:
        logger.exception("MCP server failed")
        raise


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
