"""GitHub-flavored markdown → Slack mrkdwn conversion (#1227).

Slack's ``chat.postMessage`` renders the ``text`` field as *mrkdwn*, which
differs from the GitHub-flavored markdown (GFM) the floor emits:

| concept     | GFM                | Slack mrkdwn      |
|-------------|--------------------|-------------------|
| bold        | ``**x**`` / ``__x__`` | ``*x*``          |
| italic      | ``*x*`` / ``_x_``  | ``_x_``           |
| headers     | ``# x`` … ``###### x`` | (none) → bold line |
| bullets     | ``- `` / ``* `` / ``+ `` | ``• ``         |
| links       | ``[label](url)``   | ``<url|label>``   |
| code        | `` `x` `` / ```` ```x``` ```` | same (preserved) |

Without this adapter, Slack shows literal ``**`` / ``#`` clutter (PM confirmed
on a live mobile test, #1227). The converter is **idempotent** and safe on
plain text (no formatting → unchanged), and code spans/blocks are protected
from every transform.
"""

from __future__ import annotations

import re

_CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]+`")

# Sentinel for bold output, so the italic pass (single ``*``) can't re-match the
# ``*x*`` that bold/header passes produce. Restored to ``*`` at the very end.
_BOLD = "\x01"


def markdown_to_mrkdwn(text: str) -> str:
    """Convert GitHub-flavored markdown to Slack mrkdwn. Idempotent."""
    if not text:
        return text

    # 1. Protect code (blocks first, then inline) from all transforms.
    stash: list[str] = []

    def _stash(match: "re.Match[str]") -> str:
        stash.append(match.group(0))
        return f"\x00C{len(stash) - 1}\x00"

    text = _CODE_BLOCK.sub(_stash, text)
    text = _INLINE_CODE.sub(_stash, text)

    # 2. Links: [label](url) → <url|label>
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r"<\2|\1>", text)

    # 3. Headers: ATX `#`..`######` line → bold line (mrkdwn has no headers).
    #    Emit the bold sentinel so the italic pass leaves it alone.
    text = re.sub(
        r"(?m)^[ \t]{0,3}#{1,6}[ \t]+(.*?)[ \t]*#*[ \t]*$",
        lambda m: f"{_BOLD}{m.group(1)}{_BOLD}",
        text,
    )

    # 4. Unordered list markers at line start: -, *, + → •  (BEFORE the bold/
    #    italic passes, so a list `*` is never confused with emphasis).
    text = re.sub(r"(?m)^([ \t]*)[-*+][ \t]+", r"\1• ", text)

    # 5. Bold: **x** / __x__ → sentinel-wrapped (restored to *x* at the end).
    text = re.sub(r"\*\*(.+?)\*\*", rf"{_BOLD}\1{_BOLD}", text)
    text = re.sub(r"__(.+?)__", rf"{_BOLD}\1{_BOLD}", text)

    # 6. Italic: remaining *x* → _x_ (no star/newline inside). _x_ already mrkdwn.
    text = re.sub(r"\*([^*\n]+?)\*", r"_\1_", text)

    # 7. Restore bold sentinels → *
    text = text.replace(_BOLD, "*")

    # 8. Restore protected code.
    for i, code in enumerate(stash):
        text = text.replace(f"\x00C{i}\x00", code)

    return text
