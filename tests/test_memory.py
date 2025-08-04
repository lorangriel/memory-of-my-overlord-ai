import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from memory import ConversationMemory, EntityMemory


def test_add_and_retrieve():
    mem = ConversationMemory()
    mem.add_message("user", "Hi")
    mem.add_message("assistant", "Hello")
    assert len(mem.get_recent()) == 2
    assert mem.to_prompt() == "user: Hi\nassistant: Hello"


def test_persistence(tmp_path):
    path = tmp_path / "mem.jsonl"
    mem = ConversationMemory()
    mem.add_message("user", "Hello")
    mem.save(path)
    loaded = ConversationMemory.load(path)
    assert loaded.to_prompt() == "user: Hello"


def test_entity_memory_add_and_retrieve():
    mem = EntityMemory()
    mem.add_message("hero", "user", "Hi")
    mem.add_message("villain", "user", "Boo")
    assert mem.to_prompt("hero") == "user: Hi"
    assert mem.to_prompt("villain") == "user: Boo"


def test_entity_memory_persistence(tmp_path):
    path = tmp_path / "entity_mem.jsonl"
    mem = EntityMemory()
    mem.add_message("hero", "user", "Hello")
    mem.save(path)
    loaded = EntityMemory.load(path)
    assert loaded.to_prompt("hero") == "user: Hello"
