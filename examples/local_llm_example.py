"""Example of integrating ConversationMemory with a local Hugging Face model.

This script shows how to pair the ConversationMemory utility with a small
language model that runs locally via the `transformers` library. The example
uses the `distilgpt2` model for convenience, but any causal language model
from the Hugging Face Hub (or a local path) can be substituted.
"""

from __future__ import annotations

from memory import ConversationMemory

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def main() -> None:
    """Run an interactive chat using ConversationMemory and a local model."""

    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    memory = ConversationMemory()

    while True:
        user_input = input("you: ")
        if not user_input:
            break
        memory.add_message("user", user_input)

        prompt = memory.to_prompt(limit=10) + "\nassistant:"
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            output_ids = model.generate(input_ids, max_new_tokens=50)
        reply = tokenizer.decode(
            output_ids[0][input_ids.shape[1]:], skip_special_tokens=True
        ).strip()
        print(f"assistant: {reply}")
        memory.add_message("assistant", reply)


if __name__ == "__main__":
    main()
