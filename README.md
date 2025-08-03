# Memory of My Overlord AI

An experiment in building memory tools for local large language models.

## Conversation memory

The `memory.py` module introduces `ConversationMemory`, a minimal class for
tracking chat messages. It can:

- append new messages with a role and content
- retrieve recent history for inclusion in prompts
- save/load the conversation to a JSONL file

This is only a starting point for richer context handling.

## Integrating with a local LLM

The `examples/local_llm_example.py` script demonstrates pairing
`ConversationMemory` with a small language model from the
[Hugging Face Transformers](https://github.com/huggingface/transformers)
library. To try it out:

1. Install dependencies:
   ```bash
   pip install transformers torch
   ```
2. Run the example:
   ```bash
   python examples/local_llm_example.py
   ```

The script maintains conversation state and feeds the recent history to the
local model on every turn, allowing the model to respond with awareness of the
previous messages.
