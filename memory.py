"""Basic conversation memory for local LLM contexts.

This module defines simple data structures to store chat messages and
retrieve recent context for prompting local language models. It is intended
as a starting point for more sophisticated memory mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import List, Iterable


@dataclass
class ChatMessage:
    """A single message in a conversation."""

    role: str
    content: str
    timestamp: float = field(
        default_factory=lambda: datetime.now(timezone.utc).timestamp()
    )


class ConversationMemory:
    """Store and retrieve conversation history.

    Messages are kept in memory and can optionally be persisted to a JSONL file.
    """

    def __init__(self) -> None:
        self._messages: List[ChatMessage] = []

    # ------------------------------------------------------------------
    # mutation
    def add_message(self, role: str, content: str) -> None:
        """Append a message to the conversation history."""

        self._messages.append(ChatMessage(role=role, content=content))

    # ------------------------------------------------------------------
    # access
    def get_recent(self, limit: int = 5) -> List[ChatMessage]:
        """Return the most recent ``limit`` messages."""

        if limit <= 0:
            return []
        return self._messages[-limit:]

    def to_prompt(self, limit: int = 5) -> str:
        """Format recent messages as a prompt string.

        Each line is formatted as ``"role: content"``.
        """

        return "\n".join(f"{m.role}: {m.content}" for m in self.get_recent(limit))

    # ------------------------------------------------------------------
    # persistence helpers
    def save(self, path: str | Path) -> None:
        """Persist memory to ``path`` as JSON lines."""

        p = Path(path)
        with p.open("w", encoding="utf-8") as fh:
            for msg in self._messages:
                json.dump(msg.__dict__, fh)
                fh.write("\n")

    @classmethod
    def load(cls, path: str | Path) -> "ConversationMemory":
        """Load memory from ``path`` if it exists.

        Missing files result in an empty memory instance.
        """

        mem = cls()
        p = Path(path)
        if not p.exists():
            return mem
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                data = json.loads(line)
                mem._messages.append(ChatMessage(**data))
        return mem

    # ------------------------------------------------------------------
    # utility
    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._messages)

    def __iter__(self) -> Iterable[ChatMessage]:  # pragma: no cover - trivial
        return iter(self._messages)
