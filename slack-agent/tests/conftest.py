"""Pytest fixtures: mock camera, mock face detector, mock workflow."""

import pytest
from unittest.mock import MagicMock, patch
import numpy as np


@pytest.fixture
def mock_camera():
    """Mock camera that simulates frame reading."""
    # TODO:
    # - Create MagicMock that behaves like cv2.VideoCapture
    # - set isOpened() to return True
    # - set read() to return (True, fake_frame)
    # - fake_frame should be numpy array (480, 640, 3)
    pass


@pytest.fixture
def mock_face_detector():
    """Mock face detector with controllable detection."""
    # TODO:
    # - Create MagicMock that behaves like FaceDetector
    # - Add detect() method that returns True/False
    # - Make it settable so tests can control return value
    pass


@pytest.fixture
def mock_workflow():
    """Mock workflow controller."""
    # TODO:
    # - Create MagicMock with pause() and resume() methods
    # - Both should return True
    # - Add is_paused property that toggles
    pass


@pytest.fixture
def state_machine(mock_workflow):
    """Real state machine with mock callbacks."""
    from slouch_mode.core.state_machine import SlouchStateMachine
    
    # TODO:
    # - Create SlouchStateMachine with mock callbacks
    # - Return for use in tests
    pass
