#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic test script for slouch-mode components."""

import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing module imports...")
    try:
        from slouch_mode.config import settings
        logger.info("OK: Config loaded: leave_seconds=%s", settings.leave_seconds)
        
        from slouch_mode.exceptions import CameraError, WorkflowError
        logger.info("OK: Exceptions imported")
        
        from slouch_mode.core.face_detector import get_face_detector
        logger.info("OK: Face detector factory imported")
        
        from slouch_mode.core.state_machine import SlouchStateMachine, SlouchState
        logger.info("OK: State machine imported")
        
        from slouch_mode.core.workflow import WorkflowController
        logger.info("OK: Workflow controller imported")
        
        from slouch_mode.monitoring.camera import CameraMonitor
        logger.info("OK: Camera monitor imported")
        
        from slouch_mode.monitoring.health import HealthChecker
        logger.info("OK: Health checker imported")
        
        from slouch_mode.utils.notifications import send_notification
        logger.info("OK: Notifications imported")
        
        from slouch_mode.utils.logging import configure_logging
        logger.info("OK: Logging configured")
        
        return True
    except Exception as e:
        logger.error("FAIL: Import failed: %s", e, exc_info=True)
        return False


def test_state_machine():
    """Test state machine transitions."""
    logger.info("")
    logger.info("Testing state machine...")
    try:
        from slouch_mode.core.state_machine import SlouchStateMachine, SlouchState
        import time
        
        pause_called = False
        resume_called = False
        
        def on_pause():
            nonlocal pause_called
            pause_called = True
            logger.info("  on_pause called")
        
        def on_resume():
            nonlocal resume_called
            resume_called = True
            logger.info("  on_resume called")
        
        sm = SlouchStateMachine(on_pause, on_resume, leave_seconds=0.5)
        logger.info("Initial state: %s", sm.state.name)
        assert sm.state == SlouchState.WORKING, "Should start in WORKING"
        
        # Test absence
        sm.update_presence(False)
        logger.info("After absence: %s", sm.state.name)
        assert sm.state == SlouchState.ABSENT, "Should enter ABSENT"
        
        logger.info("Waiting for timeout...")
        time.sleep(1.0)
        
        assert sm.state == SlouchState.SLOTHING, "Should enter SLOTHING after timeout"
        assert pause_called, "on_pause should be called"
        logger.info("OK: State machine works correctly")
        
        # Test resume
        sm.update_presence(True)
        assert sm.state == SlouchState.WORKING, "Should return to WORKING"
        assert resume_called, "on_resume should be called"
        logger.info("OK: Resume works correctly")
        
        return True
    except Exception as e:
        logger.error("FAIL: State machine test failed: %s", e, exc_info=True)
        return False


def test_face_detector():
    """Test face detector initialization."""
    logger.info("")
    logger.info("Testing face detector...")
    try:
        from slouch_mode.core.face_detector import get_face_detector
        import numpy as np
        
        detector = get_face_detector("haar")
        logger.info("OK: Haar detector initialized: %s", type(detector).__name__)
        
        # Test with dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = detector.detect(dummy_frame)
        logger.info("OK: Detector can process frames: no faces detected=%s", not result)
        
        return True
    except Exception as e:
        logger.error("FAIL: Face detector test failed: %s", e, exc_info=True)
        return False


def test_workflow_controller():
    """Test workflow controller."""
    logger.info("")
    logger.info("Testing workflow controller...")
    try:
        from slouch_mode.core.workflow import WorkflowController
        
        wc = WorkflowController()
        logger.info("OK: WorkflowController initialized")
        logger.info("  is_paused: %s", wc.is_paused)
        
        # Test pause/resume (will not actually minimize windows)
        result = wc.pause()
        logger.info("  pause result: %s", result)
        
        result = wc.resume()
        logger.info("  resume result: %s", result)
        
        return True
    except Exception as e:
        logger.error("FAIL: Workflow controller test failed: %s", e, exc_info=True)
        return False


def test_logging():
    """Test logging configuration."""
    logger.info("")
    logger.info("Testing logging...")
    try:
        from slouch_mode.utils.logging import configure_logging
        
        configure_logging("DEBUG")
        logger.info("OK: Logging configured successfully")
        
        return True
    except Exception as e:
        logger.error("FAIL: Logging test failed: %s", e, exc_info=True)
        return False


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Agent Slouch Mode - Basic Test Suite")
    logger.info("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "State Machine": test_state_machine(),
        "Face Detector": test_face_detector(),
        "Workflow Controller": test_workflow_controller(),
        "Logging": test_logging(),
    }
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Results:")
    logger.info("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        logger.info("%s: %s", test_name, status)
    
    logger.info("=" * 60)
    logger.info("Total: %d/%d passed", passed, total)
    logger.info("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
