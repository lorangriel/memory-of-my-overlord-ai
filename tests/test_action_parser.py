import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from action_parser import parse_interaction


def test_parse_interaction_basic():
    text = "Alice (user): Hi\nBob (assistant): Hello"
    assert parse_interaction(text) == [
        ("Alice", "user", "Hi"),
        ("Bob", "assistant", "Hello"),
    ]
