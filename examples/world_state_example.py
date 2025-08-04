"""Example of tracking non-character entities with EntityMemory.

This script demonstrates how locations or other world elements can be stored
and queried just like character conversations. Each entity maintains its own
message history, letting you keep notes on the state of places, items, or
organizations in your game.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from memory import EntityMemory


def main() -> None:
    """Store and retrieve information about world entities."""

    mem = EntityMemory()

    # Track locations with arbitrary entity identifiers.
    mem.add_message("Coal Mine X", "status", "depleted")
    mem.add_message("Northwatch City", "status", "on high alert after raid")

    # Retrieve the latest notes for each entity.
    print("Mine:")
    print(mem.to_prompt("Coal Mine X"))
    print()
    print("City:")
    print(mem.to_prompt("Northwatch City"))


if __name__ == "__main__":
    main()
