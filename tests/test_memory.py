from memory import ConversationMemory


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
