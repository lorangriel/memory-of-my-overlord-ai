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
    entity: str | None = None
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
    def add_message(
        self, role: str, content: str, entity: str | None = None
    ) -> None:
        """Append a message to the conversation history.

        Parameters
        ----------
        role:
            The speaker's role in the conversation, e.g. ``"user"``.
        content:
            The textual content of the message.
        entity:
            Optional identifier for the entity associated with the message.
        """

        self._messages.append(
            ChatMessage(role=role, content=content, entity=entity)
        )

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


class EntityMemory:
    """Manage separate conversation memories for multiple entities.

    Each entity identifier maps to its own :class:`ConversationMemory` instance.
    Messages are recorded per entity and can be saved/loaded from disk with the
    entity information preserved.
    """

    def __init__(self) -> None:
        self._entities: dict[str, ConversationMemory] = {}

    # ------------------------------------------------------------------
    # mutation
    def add_message(self, entity: str, role: str, content: str) -> None:
        """Append a message for ``entity``.

        A :class:`ConversationMemory` is created automatically for unknown
        entities.
        """

        self._entities.setdefault(entity, ConversationMemory()).add_message(
            role, content, entity=entity
        )

    # ------------------------------------------------------------------
    # access
    def get_recent(self, entity: str, limit: int = 5) -> List[ChatMessage]:
        """Return recent messages for ``entity``."""

        mem = self._entities.get(entity)
        if not mem:
            return []
        return mem.get_recent(limit)

    def to_prompt(self, entity: str, limit: int = 5) -> str:
        """Format ``entity``'s recent messages as a prompt string."""

        mem = self._entities.get(entity)
        if not mem:
            return ""
        return mem.to_prompt(limit)

    # ------------------------------------------------------------------
    # persistence helpers
    def save(self, path: str | Path) -> None:
        """Persist all entity memories to ``path`` as JSON lines."""

        p = Path(path)
        with p.open("w", encoding="utf-8") as fh:
            for entity, mem in self._entities.items():
                for msg in mem:
                    json.dump({"entity": entity, **msg.__dict__}, fh)
                    fh.write("\n")

    @classmethod
    def load(cls, path: str | Path) -> "EntityMemory":
        """Load entity memories from ``path`` if it exists."""

        mem = cls()
        p = Path(path)
        if not p.exists():
            return mem
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                data = json.loads(line)
                entity = data.pop("entity")
                msg = ChatMessage(**data)
                mem._entities.setdefault(entity, ConversationMemory())._messages.append(
                    msg
                )
        return mem

