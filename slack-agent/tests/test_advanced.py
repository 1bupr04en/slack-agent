#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advanced tests for camera and detection functions."""

import sys
import logging
import cv2

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_camera_availability():
    """Test if camera is available."""
    logger.info("Testing camera availability...")
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.warning("SKIP: Camera not available on index 0")
            return None
        
        ret, frame = cap.read()
        cap.release()
        
        if ret and frame is not None:
            logger.info("OK: Camera is working. Frame shape: %s", frame.shape)
            return True
        else:
            logger.warning("SKIP: Could not read frame from camera")
            return None
    except Exception as e:
        logger.warning("SKIP: Camera test error: %s", e)
        return None


def test_camera_monitor():
    """Test camera monitor (if camera available)."""
    logger.info("")
    logger.info("Testing camera monitor...")
    
    # First check if camera is available
    if test_camera_availability() is None:
        logger.warning("SKIP: Camera monitor test (no camera)")
        return None
    
    try:
        from slouch_mode.core.state_machine import SlouchStateMachine
        from slouch_mode.monitoring.camera import CameraMonitor
        
        call_log = []
        
        def on_pause():
            call_log.append("pause")
        
        def on_resume():
            call_log.append("resume")
        
        sm = SlouchStateMachine(on_pause, on_resume, leave_seconds=10)
        monitor = CameraMonitor(sm)
        
        # Start monitor briefly
        logger.info("Starting camera monitor...")
        monitor.start()
        
        import time
        time.sleep(3)
        
        monitor.stop()
        logger.info("OK: Camera monitor ran successfully")
        return True
    except Exception as e:
        logger.error("FAIL: Camera monitor test failed: %s", e, exc_info=True)
        return False


def test_health_checker():
    """Test health checker."""
    logger.info("")
    logger.info("Testing health checker...")
    
    if test_camera_availability() is None:
        logger.warning("SKIP: Health checker test (no camera)")
        return None
    
    try:
        from slouch_mode.core.state_machine import SlouchStateMachine
        from slouch_mode.monitoring.camera import CameraMonitor
        from slouch_mode.monitoring.health import HealthChecker
        
        def on_pause():
            pass
        
        def on_resume():
            pass
        
        sm = SlouchStateMachine(on_pause, on_resume, leave_seconds=10)
        monitor = CameraMonitor(sm)
        health = HealthChecker(monitor, sm, check_interval=1.0)
        
        monitor.start()
        health.start()
        
        import time
        time.sleep(2)
        
        health.stop()
        monitor.stop()
        logger.info("OK: Health checker ran successfully")
        return True
    except Exception as e:
        logger.error("FAIL: Health checker test failed: %s", e, exc_info=True)
        return False


def test_mcp_tools():
    """Test MCP tool functions."""
    logger.info("")
    logger.info("Testing MCP tools...")
    try:
        from slouch_mode.mcp.tools import (
            get_status, manual_pause, manual_resume, 
            set_leave_timeout, set_controller
        )
        from slouch_mode.core.workflow import WorkflowController
        
        # Set up controller
        wc = WorkflowController()
        set_controller(wc)
        
        # Test get_status
        status = get_status()
        logger.info("get_status: %s", status)
        assert status in ("working", "paused"), f"Invalid status: {status}"
        
        # Test manual_pause
        result = manual_pause()
        logger.info("manual_pause: %s", result)
        
        # Test manual_resume
        result = manual_resume()
        logger.info("manual_resume: %s", result)
        
        # Test set_leave_timeout
        result = set_leave_timeout(45.0)
        logger.info("set_leave_timeout: %s", result)
        
        logger.info("OK: MCP tools work correctly")
        return True
    except Exception as e:
        logger.error("FAIL: MCP tools test failed: %s", e, exc_info=True)
        return False


def main():
    """Run advanced tests."""
    logger.info("=" * 60)
    logger.info("Agent Slouch Mode - Advanced Test Suite")
    logger.info("=" * 60)
    
    results = {
        "Camera Monitor": test_camera_monitor(),
        "Health Checker": test_health_checker(),
        "MCP Tools": test_mcp_tools(),
    }
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Results:")
    logger.info("=" * 60)
    
    passed = sum(1 for r in results.values() if r is True)
    skipped = sum(1 for r in results.values() if r is None)
    failed = sum(1 for r in results.values() if r is False)
    total = len(results)
    
    for test_name, result in results.items():
        if result is True:
            status = "PASS"
        elif result is None:
            status = "SKIP"
        else:
            status = "FAIL"
        logger.info("%s: %s", test_name, status)
    
    logger.info("=" * 60)
    logger.info("Total: %d passed, %d skipped, %d failed", passed, skipped, failed)
    logger.info("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
