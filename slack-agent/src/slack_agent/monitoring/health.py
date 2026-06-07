"""Health checker to restart dead threads and verify camera."""

import threading
import logging
import time
from typing import Optional
from slouch_mode.config import settings

logger = logging.getLogger(__name__)


class HealthChecker:
    """Monitors health of camera monitor and restarts if needed."""
    
    def __init__(self, monitor, state_machine, check_interval: float):
        """Initialize health checker."""
        self.monitor = monitor
        self.state_machine = state_machine
        self.interval = check_interval
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        logger.info(f"Initialized HealthChecker with interval: {check_interval}s")

    def start(self) -> None:
        """Start background health check thread."""
        self._stop.clear()
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()
        logger.info("HealthChecker started")

    def stop(self) -> None:
        """Stop health checker."""
        self._stop.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        logger.info("HealthChecker stopped")

    def _check_loop(self) -> None:
        """Periodically check monitor thread liveness and camera status."""
        while not self._stop.is_set():
            time.sleep(self.interval)
            try:
                if self.monitor._thread is None or not self.monitor._thread.is_alive():
                    logger.warning("Camera monitor thread is not alive; restarting")
                    self.monitor.stop()
                    self.monitor.start()
                    continue

                if self.monitor.cap is not None:
                    ret, frame = self.monitor.cap.read()
                    if not ret or frame is None:
                        logger.warning("Camera health check failed; restarting monitor")
                        self.monitor.stop()
                        self.monitor.start()
            except Exception:
                logger.exception("Unexpected error in health checker")
