#!/usr/bin/env python3
"""
Kappa Starter Script
Launches Kappa FastAPI server locally for development

Usage:
    python tools/kappa-cli/start_kappa.py
    python tools/kappa-cli/start_kappa.py --debug
    python tools/kappa-cli/start_kappa.py --port 8001
"""

import sys
import os
from pathlib import Path
import subprocess

# Add kappa to path
REPO_ROOT = Path(__file__).parent.parent.parent
KAPPA_DIR = REPO_ROOT / "kappa"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(KAPPA_DIR))

import argparse

def main():
    parser = argparse.ArgumentParser(description="Start Kappa FastAPI Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--mock", action="store_true", help="Enable mock mode (no API keys required)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on file changes")

    args = parser.parse_args()

    # Set environment variables
    env = os.environ.copy()
    env["KAPPA_DEBUG"] = "true" if args.debug else "false"
    env["KAPPA_PORT"] = str(args.port)
    env["KAPPA_HOST"] = args.host
    env["KAPPA_MOCK_MODE"] = "true" if args.mock else "false"
    env["PYTHONUNBUFFERED"] = "1"  # Unbuffered output

    print(f"Starting Kappa FastAPI Server")
    print(f"  Host: {args.host}")
    print(f"  Port: {args.port}")
    print(f"  Debug: {args.debug}")
    print(f"  Mock Mode: {args.mock}")
    print(f"  Auto-reload: {args.reload or args.debug}")
    print("")
    print("Kappa will be available at:")
    print(f"  Health: http://{args.host}:{args.port}/api/kappa/health")
    print(f"  API Docs: http://{args.host}:{args.port}/docs")
    print("")
    print("Ctrl+C to stop")
    print("")

    # Start uvicorn
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        f"--host={args.host}",
        f"--port={args.port}",
        f"--log-level={'debug' if args.debug else 'info'}",
    ]

    if args.reload or args.debug:
        cmd.append("--reload")

    # Change to kappa directory
    os.chdir(KAPPA_DIR)

    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\n\nKappa server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
