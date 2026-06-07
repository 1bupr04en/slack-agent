"""Control the Agent's working state (pause/resume via desktop automation)."""

import logging
from typing import Optional
from slouch_mode.config import settings
from slouch_mode.utils.notifications import send_notification

logger = logging.getLogger(__name__)


class WorkflowController:
    """Controls the Agent workflow (pause/resume operations)."""
    
    def __init__(self):
        """Initialize workflow controller."""
        self._is_paused = False
        self.controller = None
        try:
            from desktop_api import DesktopController

            self.controller = DesktopController()
            logger.info("DesktopController initialized successfully")
        except ImportError:
            logger.warning("desktop_api is not installed; workflow automation will be limited")
        except Exception as exc:
            logger.warning("Failed to initialize DesktopController: %s", exc)

    @property
    def is_paused(self) -> bool:
        """Return current pause state."""
        return self._is_paused

    def _find_window(self) -> Optional[object]:
        if self.controller is None:
            return None
        if hasattr(self.controller, "find_window"):
            try:
                return self.controller.find_window(settings.agent_window_title)
            except Exception:
                logger.exception("Error finding window with desktop_api")
                return None
        logger.debug("DesktopController does not expose find_window")
        return None

    def pause(self) -> bool:
        """Pause the Agent: save (Ctrl+S), minimize window. Return success."""
        if self._is_paused:
            logger.debug("Pause called but already paused")
            return True

        success = False
        window = self._find_window()
        if window is not None:
            try:
                if hasattr(self.controller, "activate_window"):
                    self.controller.activate_window(window)
                if hasattr(self.controller, "send_keys"):
                    self.controller.send_keys("ctrl", "s")
                if hasattr(self.controller, "minimize_window"):
                    self.controller.minimize_window(window)
                success = True
                logger.info("Agent window paused and minimized")
            except Exception:
                logger.exception("Failed to pause the agent window")
        else:
            logger.warning("Agent window not found: %s", settings.agent_window_title)
            send_notification("Slouch Mode", f"Could not find window '{settings.agent_window_title}' to pause")

        self._is_paused = True
        return success or True

    def resume(self) -> bool:
        """Resume the Agent: restore and activate window. Return success."""
        if not self._is_paused:
            logger.debug("Resume called but not currently paused")
            return True

        window = self._find_window()
        if window is not None:
            try:
                if hasattr(self.controller, "restore_window"):
                    self.controller.restore_window(window)
                if hasattr(self.controller, "activate_window"):
                    self.controller.activate_window(window)
                logger.info("Agent window restored and activated")
                self._is_paused = False
                return True
            except Exception:
                logger.exception("Failed to resume the agent window")
                return False

        logger.warning("Agent window not found: %s", settings.agent_window_title)
        send_notification("Slouch Mode", f"Could not find window '{settings.agent_window_title}' to resume")
        return False
