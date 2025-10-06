"""Hilfsskript zum Auffinden von AGENTS.md-Anweisungen im Repository."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Iterator

IGNORED_DIRECTORIES = {".git", "node_modules", "__pycache__"}


def find_agents(root: Path) -> Iterator[Path]:
    """Yield all AGENTS.md files below ``root`` sorted by their relative path."""
    for path in sorted(root.iterdir() if root.is_dir() else []):
        if path.name in IGNORED_DIRECTORIES:
            continue
        if path.is_file() and path.name == "AGENTS.md":
            yield path
        elif path.is_dir():
            yield from find_agents(path)


def print_agent_instructions(agent_paths: Iterable[Path], root: Path) -> None:
    """Druckt die Inhalte der gefundenen AGENTS.md-Dateien."""
    printed_any = False
    for path in sorted(agent_paths, key=lambda p: p.relative_to(root).as_posix()):
        printed_any = True
        relative = path.relative_to(root)
        print(f"# {relative}")
        print(path.read_text(encoding="utf-8").strip())
        print()

    if not printed_any:
        print("Keine AGENTS.md-Dateien gefunden. Es liegen keine zusätzlichen Agentenhinweise vor.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository-Wurzel, in der nach AGENTS.md-Dateien gesucht wird.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    print_agent_instructions(find_agents(root), root)


if __name__ == "__main__":
    main()
