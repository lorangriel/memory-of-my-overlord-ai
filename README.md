# Memory of My Overlord AI

An experiment in building memory tools for local large language models.

## Conversation memory

The `memory.py` module introduces `ConversationMemory`, a minimal class for
tracking chat messages. It can:

- append new messages with a role and content
- retrieve recent history for inclusion in prompts
- save/load the conversation to a JSONL file

This is only a starting point for richer context handling.
