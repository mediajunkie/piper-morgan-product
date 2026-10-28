"""#2042 rung 2 — the floor's LISTED-RECORDS event (log-only; measurement, not a rewrite).

The class Arch diagnosed on #2042 (2026-10-28): the floor makes record claims
from context slices on a turn where no read with the asked scope ran. #2184 is
its served instance — three real issue numbers from the high-priority slice,
re-labelled as "the MVP milestone's issues" with the count taken from the
milestones slice. #2040 is the older case — numbers that were in no slice at
all. Both are one class; the second is the narrower sub-signal (pure invention).

What this module does: at the floor's single seam, after every rewrite, it
looks at the reply the user will see and records, per turn:

- the record references the reply enumerates (``#N`` tokens, de-duplicated)
  and how many list lines it rendered;
- which of those references appear NOWHERE in the prompt the model was given
  (history, context block, the user's own words) — the pure-invention signal;
- which record-shaped reads the context assembler ran this turn, by provenance
  key and filter (``high_priority_issues[priority:high]``), so a week of events
  can be queried for "listed records with no read of that scope" without a
  judgment in code (ADR-080 D6: no interpretation layer over output).

What it does NOT do: change the reply. Arch's 10-15 ruling starts rung 2
log-only; a redaction is a later decision on the measured rate. The event is
``floor_listed_records``; the derived query Arch named,
``floor_listed_records_without_read``, is a read over these events joined to
``inversion_live_decision`` by session, because the floor itself never sees the
router's verdict (no inversion key reaches it — checked 2026-10-28).

No regular expressions: the binder ratchet (#1943, ``TestBinderFileRatchet``)
holds every file in this package at a shrink-only ceiling, unlisted files at
zero, and this is a reader, not a binder. Token scanning is enough for ``#N``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

_STRIP_CHARS = "*_`()[]{}<>\"'.,;:!?"
_LIST_MARKERS = ("- ", "* ", "• ", "– ")


def record_references(text: Optional[str]) -> List[str]:
    """Every ``#N`` token in ``text``, first-seen order, de-duplicated.

    Markdown emphasis and surrounding punctuation are stripped before the
    test, so ``**#2183**:`` and ``(#2018)`` both count. A bare ``#`` or a
    ``#word`` is not a record reference.
    """
    if not text:
        return []
    seen: List[str] = []
    for raw in text.replace("\n", " ").split():
        tok = raw.strip(_STRIP_CHARS)
        if len(tok) < 2 or not tok.startswith("#"):
            continue
        digits = tok[1:]
        if digits.isdigit() and digits not in {s[1:] for s in seen}:
            seen.append("#" + digits)
    return seen


def count_list_lines(text: Optional[str]) -> int:
    """Lines rendered as list items: ``- ``, ``* ``, ``• ``, ``– `` or ``1.``/``1)``."""
    if not text:
        return 0
    n = 0
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(_LIST_MARKERS):
            n += 1
            continue
        head = s.split(" ", 1)[0]
        if len(head) >= 2 and head[-1] in ".)" and head[:-1].isdigit():
            n += 1
    return n


def context_reads(
    provenance: Optional[Mapping[str, Mapping[str, Any]]],
    domain_context: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    """The record-shaped reads the assembler ran this turn, as ``key[filter]``.

    Provenance is the assembler's own record of what it fetched (#1030 R4:
    source, filter, fetch_timestamp per key). A key present in the context but
    absent from provenance is reported as ``key[?]`` so the gap is visible
    rather than silently dropped.
    """
    out: List[str] = []
    prov = provenance or {}
    for key in sorted(prov):
        entry = prov[key] or {}
        scope = entry.get("filter") or entry.get("source") or "?"
        out.append(f"{key}[{scope}]")
    for key in sorted(domain_context or {}):
        if key not in prov and isinstance((domain_context or {}).get(key), (list, dict)):
            out.append(f"{key}[?]")
    return out


def listed_records_event(
    message: Optional[str],
    prompt_text: Optional[str],
    provenance: Optional[Mapping[str, Mapping[str, Any]]] = None,
    domain_context: Optional[Mapping[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """The event payload for a reply that enumerates records, else ``None``.

    Fires when the reply carries two or more record references or list lines
    (Arch's "enumerates two or more record references"), or when ANY reference
    is absent from the prompt (one invented number is already the #2040 case).
    Pure function of its inputs; the caller logs it and changes nothing.
    """
    refs = record_references(message)
    lines = count_list_lines(message)
    sourced = set(record_references(prompt_text))
    unsourced = [r for r in refs if r not in sourced]
    if len(refs) < 2 and lines < 2 and not unsourced:
        return None
    return {
        "references": refs,
        "reference_count": len(refs),
        "unsourced_references": unsourced,
        "list_lines": lines,
        "context_reads": context_reads(provenance, domain_context),
    }


__all__ = (
    "record_references",
    "count_list_lines",
    "context_reads",
    "listed_records_event",
)
