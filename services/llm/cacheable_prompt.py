"""#2145: a prompt that knows where its static prefix ends.

``CacheablePrompt`` is a ``str`` (so it flows unchanged through ``LLMClient``'s
output filter, retries and fallbacks) that remembers how many leading
characters are identical on every call. The Anthropic leg turns that into one
``cache_control`` breakpoint at the end of the prefix, which caches the system
prompt and the prefix together. Other providers see a plain string (OpenAI
caches stable prefixes on its own). Anthropic caches only prefixes above a
per-model minimum; a shorter prefix is sent as-is and simply isn't cached.
"""

from __future__ import annotations


class CacheablePrompt(str):
    """``prefix + rest`` as one string, with ``cache_prefix_len == len(prefix)``."""

    cache_prefix_len: int

    def __new__(cls, prefix: str, rest: str) -> "CacheablePrompt":
        obj = super().__new__(cls, prefix + rest)
        obj.cache_prefix_len = len(prefix)
        return obj


def anthropic_user_content(prompt: str):
    """The ``messages[0].content`` for a prompt: a plain string, or two text
    blocks with the cache breakpoint after the static prefix."""
    n = getattr(prompt, "cache_prefix_len", 0)
    if isinstance(prompt, CacheablePrompt) and 0 < n < len(prompt):
        return [
            {"type": "text", "text": str(prompt[:n]), "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": str(prompt[n:])},
        ]
    return str(prompt)


def anthropic_system_content(system: str):
    """#2354: the ``system`` parameter: a plain string, or text blocks with the
    cache breakpoint after the static prefix (the reply prompt's fixed part)."""
    n = getattr(system, "cache_prefix_len", 0)
    if isinstance(system, CacheablePrompt) and 0 < n <= len(system):
        blocks = [{"type": "text", "text": str(system[:n]), "cache_control": {"type": "ephemeral"}}]
        if n < len(system):
            blocks.append({"type": "text", "text": str(system[n:])})
        return blocks
    return str(system)
