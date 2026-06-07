"""State machine: WORKING -> ABSENT (countdown) -> SLOTHING (paused)."""

from enum import Enum, auto
import threading
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


class SlouchState(Enum):
    """States of the slouch mode system."""
    WORKING = auto()
    ABSENT = auto()
    SLOTHING = auto()


class SlouchStateMachine:
    """State machine managing slouch mode transitions."""
    
    def __init__(self, on_pause: Callable[[], None], on_resume: Callable[[], None], leave_seconds: float = 60.0):
        """Initialize state machine with callbacks."""
        self.state = SlouchState.WORKING
        self.leave_seconds = leave_seconds
        self._lock = threading.Lock()
        self._timer: Optional[threading.Timer] = None
        self._on_pause = on_pause
        self._on_resume = on_resume

    def update_presence(self, present: bool) -> None:
        """Update state based on whether user is present."""
        with self._lock:
            if present:
                if self.state == SlouchState.SLOTHING:
                    logger.info("User returned: resuming from SLOTHING")
                    try:
                        self._on_resume()
                    except Exception:
                        logger.exception("Error while resuming agent")
                    self.state = SlouchState.WORKING
                elif self.state == SlouchState.ABSENT:
                    logger.info("User returned before timeout: cancelling absence timer")
                    if self._timer is not None:
                        self._timer.cancel()
                        self._timer = None
                    self.state = SlouchState.WORKING
                else:
                    logger.debug("User present, state remains WORKING")
                return

            if self.state == SlouchState.WORKING:
                logger.info("User absent: starting leave timer")
                self.state = SlouchState.ABSENT
                self._timer = threading.Timer(self.leave_seconds, self._enter_sloth)
                self._timer.daemon = True
                self._timer.start()
            else:
                logger.debug("User absent and already in state %s", self.state.name)

    def reset(self) -> None:
        """Force reset to WORKING state, cancelling timer and resuming if needed."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            if self.state == SlouchState.SLOTHING:
                logger.info("Resetting from SLOTHING to WORKING")
                try:
                    self._on_resume()
                except Exception:
                    logger.exception("Error while resuming agent during reset")
            self.state = SlouchState.WORKING
            logger.debug("State machine reset to WORKING")

    def _enter_sloth(self) -> None:
        """Called by timer when timeout reached."""
        with self._lock:
            if self.state != SlouchState.ABSENT:
                logger.debug("Leave timer fired but state is %s", self.state.name)
                return
            logger.info("Absence timeout reached: entering SLOTHING")
            try:
                self._on_pause()
            except Exception:
                logger.exception("Error while pausing agent")
            self.state = SlouchState.SLOTHING
