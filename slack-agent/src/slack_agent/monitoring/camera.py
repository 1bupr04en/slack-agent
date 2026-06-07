"""Camera capture with retry and frame reading."""

import cv2
import threading
import logging
import time
from typing import Optional, Generator
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from slouch_mode.config import settings
from slouch_mode.exceptions import CameraError
from slouch_mode.core.face_detector import get_face_detector

logger = logging.getLogger(__name__)


class CameraMonitor:
    """Monitors camera and detects user presence."""
    
    def __init__(self, state_machine):
        """Initialize camera monitor."""
        self.state_machine = state_machine
        self.cap: Optional[cv2.VideoCapture] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.face_detector = get_face_detector(settings.face_detector_backend)
        self._absent_frames = 0
        logger.info(f"Initialized CameraMonitor with backend: {settings.face_detector_backend}")

    def start(self) -> None:
        """Open camera and start background monitoring thread."""
        try:
            self._open_camera()
        except CameraError as exc:
            logger.error("Camera open failed during start: %s", exc)
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("CameraMonitor started")

    def stop(self) -> None:
        """Stop monitoring and release camera."""
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        logger.info("CameraMonitor stopped")

    @retry(stop=stop_after_attempt(settings.camera_reopen_retries),
           retry=retry_if_exception_type(CameraError),
           wait=wait_fixed(2))
    def _open_camera(self) -> None:
        """Open camera with retry; raise CameraError on failure."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        cap = cv2.VideoCapture(settings.camera_index)
        if not cap.isOpened():
            raise CameraError(f"Unable to open camera index {settings.camera_index}")
        self.cap = cap
        logger.info("Camera opened on index %s", settings.camera_index)

    def _run(self) -> None:
        """Main loop: read frames, detect faces, update state machine."""
        while not self._stop_event.is_set():
            if self.cap is None:
                logger.debug("Camera capture missing, attempting reopen")
                try:
                    self._open_camera()
                except CameraError:
                    logger.exception("Failed to reopen camera")
                    time.sleep(2.0)
                    continue

            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.warning("Failed to read frame from camera")
                try:
                    self._open_camera()
                except CameraError:
                    logger.exception("Failed to reopen camera after read failure")
                    time.sleep(2.0)
                continue

            try:
                present = self.face_detector.detect(frame)
            except Exception:
                logger.exception("Face detector failed; assuming user absent")
                present = False

            if present:
                self._absent_frames = 0
                self.state_machine.update_presence(True)
            else:
                self._absent_frames += 1
                if self._absent_frames >= settings.absent_frame_threshold:
                    self.state_machine.update_presence(False)
                else:
                    self.state_machine.update_presence(True)

            time.sleep(settings.detection_interval)
