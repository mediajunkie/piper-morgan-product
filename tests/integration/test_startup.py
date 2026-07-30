"""
Integration test for application startup
Verifies that main.py starts without hanging and serves basic endpoints
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests


class TestStartupIntegration:
    """Test that the application starts successfully"""

    def test_main_py_startup_no_hanging(self):
        """Test that python main.py starts without hanging"""
        # Start the application in a subprocess
        # sys.executable, not bare "python": hosts without a `python` shim on
        # PATH (e.g. Amber, homebrew python3 only) FileNotFoundError otherwise;
        # sys.executable is also the interpreter actually running the tests.
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent.parent.parent,  # Project root
        )

        try:
            # Wait for startup (max 30 seconds)
            startup_timeout = 30
            start_time = time.time()

            while time.time() - start_time < startup_timeout:
                # Check if process is still running
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    pytest.fail(f"Process exited unexpectedly. STDOUT: {stdout}, STDERR: {stderr}")

                # Try to connect to health endpoint
                try:
                    response = requests.get("http://localhost:8001/health", timeout=2)
                    if response.status_code == 200:
                        # Success! Application started
                        return
                except requests.exceptions.RequestException:
                    # Expected during startup, continue waiting
                    pass

                time.sleep(1)

            # If we get here, startup timed out
            stdout, stderr = process.communicate(timeout=5)
            pytest.fail(
                f"Startup timed out after {startup_timeout}s. STDOUT: {stdout}, STDERR: {stderr}"
            )

        finally:
            # Clean up: terminate the process
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

    def test_slack_health_endpoint_exists(self):
        """Test that /health/slack endpoint exists (may be in degraded state)"""
        # This test assumes the main application is running
        # In CI, this would be set up as a separate service
        try:
            response = requests.get("http://localhost:8001/health/slack", timeout=5)
            # Should return either 200 (working) or report degraded state
            assert response.status_code == 200
            data = response.json()
            # Should have status field
            assert "status" in data
        except requests.exceptions.RequestException:
            pytest.skip("Main application not running - this test requires a running instance")
