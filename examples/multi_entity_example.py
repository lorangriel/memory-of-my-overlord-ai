"""Example of parsing a multi-entity interaction script."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repository root is on the import path when running directly.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from action_parser import parse_interaction
from memory import EntityMemory


def main() -> None:
    """Parse a script and store messages for each entity."""

    script = """
    Alice (user): Hello Bob
    Bob (assistant): Hi Alice
    Narrator (system): The room is quiet.
    """
    interactions = parse_interaction(script)
    mem = EntityMemory()
    mem.add_messages(interactions)

    for entity in ["Alice", "Bob", "Narrator"]:
        print(f"{entity}:")
        print(mem.to_prompt(entity))
        print()


if __name__ == "__main__":
    main()
