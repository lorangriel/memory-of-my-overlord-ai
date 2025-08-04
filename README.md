# Memory of My Overlord AI (aka Jason)

Memory of My Overlord AI (aka Jason) is an experiment in building memory tools for local large language models.

## Conversation memory

The `memory.py` module introduces `ConversationMemory`, a minimal class for
tracking chat messages. It can:

- append new messages with a role and content
- retrieve recent history for inclusion in prompts
- save/load the conversation to a JSONL file

 This is only a starting point for richer context handling.

## Entity memory

The `EntityMemory` class manages a separate `ConversationMemory` for each
entity identifier, making it straightforward to track multiple characters or
participants simultaneously. Each entity's messages are stored and retrieved
independently.

```python
from memory import EntityMemory

mem = EntityMemory()
mem.add_message("wizard", "user", "Greetings")
mem.add_message("dragon", "user", "Roar")
print(mem.to_prompt("wizard"))  # -> "user: Greetings"
```

To track locations or other non-character entities, use descriptive identifiers:

```python
mem.add_message("Coal Mine X", "status", "depleted")
mem.add_message("Northwatch City", "status", "on high alert after raid")
print(mem.to_prompt("Northwatch City"))
```

See `examples/world_state_example.py` for a complete demonstration.

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
