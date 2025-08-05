"""Parse multi-entity interactions from free-form text.

This module provides :func:`parse_interaction` which extracts structured
``(entity, role, content)`` tuples from a block of text.  It currently uses a
simple rule-based approach based on regular expressions. Each line of input is
expected to follow the pattern ``"Entity (role): content"``.  Lines that do not
match the pattern are ignored.

The parser is intentionally lightweight so it can run in environments without
network access or heavy dependencies.  To use a language model for more
sophisticated parsing, replace the implementation of
:func:`parse_interaction` with a call to your LLM of choice.  The function
signature is designed to be compatible with such a swap; simply have the LLM
produce JSON or another structured format and convert it to a list of tuples.

Example
-------
>>> text = "Alice (user): Hello Bob\nBob (assistant): Hi Alice"
>>> parse_interaction(text)
[('Alice', 'user', 'Hello Bob'), ('Bob', 'assistant', 'Hi Alice')]

"""
from __future__ import annotations

import re
from typing import List, Tuple

# Regular expression capturing ``Entity (role): content``
_LINE_RE = re.compile(r"^\s*(?P<entity>[^():\n]+)\s*\((?P<role>[^)]+)\)\s*:\s*(?P<content>.+?)\s*$")


def parse_interaction(text: str) -> List[Tuple[str, str, str]]:
    """Parse ``text`` into ``(entity, role, content)`` tuples.

    Parameters
    ----------
    text:
        Multiline string describing interactions. Each line should be of the
        form ``"Entity (role): content"``.

    Returns
    -------
    list of tuple
        A list of ``(entity, role, content)`` triples in the order they appear
        in the input.
    """

    interactions: List[Tuple[str, str, str]] = []
    for line in text.splitlines():
        match = _LINE_RE.match(line)
        if match:
            interactions.append(
                (
                    match.group("entity").strip(),
                    match.group("role").strip(),
                    match.group("content").strip(),
                )
            )
    return interactions
