"""Hilfsskript zum Ausführen der Node.js- und Python-Test-Suites ohne zusätzliche Argumente."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_node_tests() -> None:
    subprocess.run(["node", "--test", "tests/test_ws_demo_server_js.js"], check=True, cwd=ROOT)


def run_py_tests() -> None:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    pythonpath_parts = [str(ROOT)]
    if existing:
        pythonpath_parts.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    subprocess.run([sys.executable, "-m", "pytest"], check=True, cwd=ROOT, env=env)


def main() -> None:
    run_node_tests()
    run_py_tests()


if __name__ == "__main__":
    main()
