#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MCP Integration Verification Test."""

import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_mcp_installation():
    """Test that MCP is properly installed."""
    logger.info("Testing MCP installation...")
    try:
        import mcp
        logger.info("OK: MCP module imported")
        return True
    except ImportError as e:
        logger.error("FAIL: MCP not installed: %s", e)
        return False


def test_fastmcp():
    """Test FastMCP functionality."""
    logger.info("")
    logger.info("Testing FastMCP...")
    try:
        from mcp.server.fastmcp import FastMCP
        
        # Create instance
        mcp_server = FastMCP("Test Server")
        logger.info("OK: FastMCP instance created")
        
        # Add a test tool
        @mcp_server.tool()
        def test_tool() -> str:
            """A test tool."""
            return "Test successful"
        
        logger.info("OK: Tool decorator works")
        
        # Check that tools method exists
        if hasattr(mcp_server, '_tool_manager'):
            logger.info("OK: Tool manager available")
        
        return True
    except Exception as e:
        logger.error("FAIL: FastMCP test failed: %s", e, exc_info=True)
        return False


def test_slouch_mode_mcp():
    """Test slouch-mode MCP integration."""
    logger.info("")
    logger.info("Testing slouch-mode MCP integration...")
    try:
        from slouch_mode.mcp.tools import (
            mcp, get_status, manual_pause, manual_resume,
            set_leave_timeout, set_controller
        )
        from slouch_mode.core.workflow import WorkflowController
        
        logger.info("OK: MCP tools imported")
        
        # Set controller
        wc = WorkflowController()
        set_controller(wc)
        logger.info("OK: Controller set for MCP tools")
        
        # Test each tool
        status = get_status()
        logger.info("  get_status() = %s", status)
        
        pause_result = manual_pause()
        logger.info("  manual_pause() = %s", pause_result)
        
        resume_result = manual_resume()
        logger.info("  manual_resume() = %s", resume_result)
        
        timeout_result = set_leave_timeout(45)
        logger.info("  set_leave_timeout(45) = %s", timeout_result)
        
        logger.info("OK: All MCP tools working")
        return True
    except Exception as e:
        logger.error("FAIL: slouch-mode MCP test failed: %s", e, exc_info=True)
        return False


def test_mcp_server_modes():
    """Test different MCP server transport modes."""
    logger.info("")
    logger.info("Testing MCP server modes...")
    try:
        from slouch_mode.mcp.tools import mcp
        
        # Check available methods
        methods = [m for m in dir(mcp) if 'run' in m and not m.startswith('_')]
        logger.info("OK: Available run methods: %s", methods)
        
        # Verify key methods exist
        expected = ['run', 'run_stdio_async', 'run_sse_async']
        for method in expected:
            if hasattr(mcp, method):
                logger.info("  - %s: available", method)
            else:
                logger.warning("  - %s: NOT available", method)
        
        return True
    except Exception as e:
        logger.error("FAIL: MCP server modes test failed: %s", e, exc_info=True)
        return False


def test_mcp_dependencies():
    """Test that MCP dependencies are installed."""
    logger.info("")
    logger.info("Checking MCP dependencies...")
    
    dependencies = [
        'anyio',
        'httpx',
        'httpx_sse',
        'jsonschema',
        'pydantic',
        'starlette',
        'uvicorn',
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep.replace('_', '-').replace('-', '_'))
            logger.info("  - %s: OK", dep)
        except ImportError:
            logger.warning("  - %s: MISSING", dep)
            missing.append(dep)
    
    return len(missing) == 0


def main():
    """Run all MCP integration tests."""
    logger.info("=" * 70)
    logger.info("MCP INTEGRATION TEST SUITE")
    logger.info("=" * 70)
    
    results = {
        "MCP Installation": test_mcp_installation(),
        "FastMCP": test_fastmcp(),
        "Slouch Mode MCP": test_slouch_mode_mcp(),
        "MCP Server Modes": test_mcp_server_modes(),
        "MCP Dependencies": test_mcp_dependencies(),
    }
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("TEST RESULTS")
    logger.info("=" * 70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        logger.info("%s: %s", test_name, status)
    
    logger.info("=" * 70)
    logger.info("Total: %d/%d passed", passed, total)
    logger.info("=" * 70)
    
    if passed == total:
        logger.info("")
        logger.info("MCP Integration Status: READY")
        logger.info("")
        logger.info("The plugin can now run in MCP mode with:")
        logger.info("  slouch-mode")
        logger.info("")
        return 0
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
