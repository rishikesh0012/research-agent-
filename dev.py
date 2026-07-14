"""Makefile-like targets for common tasks."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests."""
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=Path(__file__).parent)
    return result.returncode


def run_coverage():
    """Run tests with coverage."""
    print("Running tests with coverage...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--cov=app", "--cov-report=html"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def run_server():
    """Run development server."""
    print("Starting development server...")
    result = subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def run_demo():
    """Run demonstration."""
    print("Running demonstration...")
    result = subprocess.run(
        [sys.executable, "sample_data/demo.py"],
        cwd=Path(__file__).parent
    )
    return result.returncode


def run_quickstart():
    """Run quickstart example."""
    print("Running quickstart...")
    result = subprocess.run(
        [sys.executable, "quickstart.py"],
        cwd=Path(__file__).parent
    )
    return result.returncode


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Development utilities")
    parser.add_argument(
        "command",
        choices=["test", "coverage", "server", "demo", "quickstart"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    commands = {
        "test": run_tests,
        "coverage": run_coverage,
        "server": run_server,
        "demo": run_demo,
        "quickstart": run_quickstart,
    }
    
    sys.exit(commands[args.command]())
