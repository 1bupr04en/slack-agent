"""Abstract face detector and implementations (Haar, MediaPipe)."""

from abc import ABC, abstractmethod
import cv2
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FaceDetector(ABC):
    """Abstract base class for face detection."""
    
    @abstractmethod
    def detect(self, frame: np.ndarray) -> bool:
        """Return True if at least one face is present in the frame."""
        pass


class HaarCascadeDetector(FaceDetector):
    """Face detector using OpenCV Haar Cascades."""
    
    def __init__(self):
        """Initialize Haar cascade detector."""
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        if self.cascade.empty():
            logger.error("Failed to load Haar cascade from %s", cascade_path)
            raise RuntimeError(f"Unable to load Haar cascade: {cascade_path}")
        logger.info("Loaded Haar cascade from %s", cascade_path)
    
    def detect(self, frame: np.ndarray) -> bool:
        """Detect faces in frame using Haar cascade."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        found = len(faces) > 0
        logger.debug("Haar cascade detected %d faces", len(faces))
        return found


class MediaPipeDetector(FaceDetector):
    """Face detector using MediaPipe (optional dependency)."""
    
    def __init__(self):
        """Initialize MediaPipe face detector."""
        try:
            import mediapipe as mp
        except ImportError as exc:
            logger.error("MediaPipe is not installed: %s", exc)
            raise RuntimeError("MediaPipe backend requested but mediapipe is not installed") from exc

        self.mp = mp
        self.detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5,
        )
        logger.info("Initialized MediaPipe face detector")
    
    def detect(self, frame: np.ndarray) -> bool:
        """Detect faces in frame using MediaPipe."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.detector.process(rgb_frame)
        found = bool(results.detections)
        logger.debug("MediaPipe detected faces: %s", found)
        return found


def get_face_detector(backend: str = "haar") -> FaceDetector:
    """Factory that returns detector based on backend name."""
    backend_name = backend.lower().strip()
    if backend_name == "haar":
        return HaarCascadeDetector()
    if backend_name == "mediapipe":
        return MediaPipeDetector()
    raise ValueError(f"Unknown backend: {backend}")
