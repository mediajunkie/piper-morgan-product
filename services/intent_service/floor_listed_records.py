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
- for each reference, EVERY place it came from: each provenance/context key
  whose items carry that number, plus ``history`` (a prior turn) and ``user``
  (the user's own words this turn) when they hold it too, or ``absent`` when
  none does (Arch's 11:02 refinement: the offline query asks whether ANY source
  matches the asked scope, so a first-match would mis-flag a legitimate list)
  — the mis-attribution datum
  (``#2183 <- high_priority_issues`` on a turn whose router args said
  ``milestone: MVP``);
- which record-shaped reads the context assembler ran this turn, by provenance
  key and filter (``high_priority_issues[priority:high]``), so a week of events
  can be queried for "listed records with no read of that scope" without a
  judgment in code (ADR-080 D6: no interpretation layer over output).

What it does NOT do: change the reply. Arch's 10-15 ruling starts rung 2
log-only; a redaction is a later decision on the measured rate. The event is
``floor_record_references`` (Arch's name, ruling 10:45 10-28); the derived query,
``floor_listed_records_without_read``, is a read over these events joined to
``inversion_live_decision`` by session, because the floor itself never sees the
router's verdict (no inversion key reaches it — checked 2026-10-28).

``reference_relations`` (Arch, 2026-10-29, #2042): for each ``#N`` in the reply,
the ``active_milestones`` titles that appear (exact, case-insensitive) in the
same sentence as ``#N``, and for each one whether any slice item for ``#N``
carries that milestone (today always false: no slice has the field). It measures
the invented-relation subclass rung 2 could not see, because ``#31`` IS in
context and so is "Beta launch"; only the claim that one belongs to the other
is made up. A sentence runs between ``.``, ``!`` or ``?`` followed by whitespace or the end
of the text, or a newline, so a title like ``v0.9`` can match. A single-reference aside
that asserts a relation now fires the event. Still log-only.

No regular expressions: the binder ratchet (#1943, ``TestBinderFileRatchet``)
holds every file in this package at a shrink-only ceiling, unlisted files at
zero, and this is a reader, not a binder. Token scanning is enough for ``#N``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

_STRIP_CHARS = "*_`()[]{}<>\"'.,;:!?"
_LIST_MARKERS = ("- ", "* ", "• ", "– ")


def record_references(text: Optional[str]) -> List[str]:
    """Every ``#N`` reference in ``text``, first-seen order, de-duplicated.

    A character scan, no regex (the #1595 ratchet): a ``#`` not preceded by a
    letter or digit, followed by digits, is a reference wherever it sits, so
    ``**#2183**:``, ``(#2018)``, a markdown link ``[#2194](…/issues/2194)``,
    ``#2194—and``, and ``#2194/#2186`` all count (2026-10-29, Arch's probe on
    the #2184 served turn: the old whitespace-token scan saw none of the last
    three shapes and the rung-2 event stayed silent). ``a#1`` and a URL's
    ``/issues/2194`` are not references. A bare ``#`` or ``#word`` is not one.
    """
    if not text:
        return []
    seen: List[str] = []
    n = len(text)
    i = 0
    while i < n:
        if text[i] == "#" and (i == 0 or not text[i - 1].isalnum()):
            j = i + 1
            while j < n and text[j].isdigit():
                j += 1
            digits = text[i + 1 : j]
            if digits and digits not in {s[1:] for s in seen}:
                seen.append("#" + digits)
            i = j
            continue
        i += 1
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


_NUMBER_FIELDS = ("number", "issue_number", "pr_number", "id")


def _numbers_in(value: Any, out: set, depth: int = 0) -> None:
    """Collect ``#N`` for every record number inside a context value (dicts,
    lists, scalars; bounded depth). A dict's ``number``/``id``-style fields
    count; so does any ``#N`` token inside a string."""
    if depth > 6 or value is None:
        return
    if isinstance(value, Mapping):
        for k, v in value.items():
            if k in _NUMBER_FIELDS and isinstance(v, (int, str)) and str(v).isdigit():
                out.add("#" + str(v))
            else:
                _numbers_in(v, out, depth + 1)
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            _numbers_in(v, out, depth + 1)
    elif isinstance(value, str):
        out.update(record_references(value))


def reference_sources(
    refs: List[str],
    domain_context: Optional[Mapping[str, Any]],
    history: Optional[Sequence[Mapping[str, Any]]] = None,
    user_message: Optional[str] = None,
) -> Dict[str, List[str]]:
    """Per reference, every source that holds it: each context key (sorted)
    whose items carry it, then ``history``, then ``user``; ``["absent"]`` when
    none does. All sources, not the first (Arch, 2026-10-28 11:02)."""
    by_key: Dict[str, set] = {}
    for key in sorted(domain_context or {}):
        found: set = set()
        _numbers_in((domain_context or {}).get(key), found)
        if found:
            by_key[key] = found
    hist: set = set()
    for turn in history or []:
        hist.update(record_references(str(turn.get("content", ""))))
    user = set(record_references(user_message))
    out: Dict[str, List[str]] = {}
    for r in refs:
        sources = [k for k, nums in by_key.items() if r in nums]
        if r in hist:
            sources.append("history")
        if r in user:
            sources.append("user")
        out[r] = sources or ["absent"]
    return out


def _sentences(text: str) -> List[str]:
    """Spans of ``text`` between sentence terminators (a character scan).

    ``.``, ``!`` and ``?`` end a sentence only when followed by whitespace or
    the end of the text; a newline always does. So ``v0.9`` stays whole.
    """
    out: List[str] = []
    start = 0
    n = len(text)
    for i, ch in enumerate(text):
        if ch == "\n" or (ch in ".!?" and (i + 1 == n or text[i + 1].isspace())):
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return out


def _milestone_names(value: Any) -> set:
    """Lowercased milestone names a ``milestone`` field holds (str, or a
    mapping with ``title``/``name``)."""
    if isinstance(value, str):
        return {value.strip().lower()} if value.strip() else set()
    if isinstance(value, Mapping):
        out: set = set()
        for k in ("title", "name"):
            v = value.get(k)
            if isinstance(v, str) and v.strip():
                out.add(v.strip().lower())
        return out
    return set()


def _milestones_of_number(value: Any, number: str, out: set, depth: int = 0) -> None:
    """Collect the milestone names carried by every item whose record number is
    ``number`` (digits only), anywhere in a context value."""
    if depth > 6 or value is None:
        return
    if isinstance(value, Mapping):
        mine = any(
            k in _NUMBER_FIELDS and isinstance(v, (int, str)) and str(v) == number
            for k, v in value.items()
        )
        if mine and "milestone" in value:
            out.update(_milestone_names(value["milestone"]))
        for v in value.values():
            if isinstance(v, (Mapping, list, tuple, set)):
                _milestones_of_number(v, number, out, depth + 1)
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            _milestones_of_number(v, number, out, depth + 1)


def _is_boundary(hay: str, at: int, beyond: int) -> bool:
    """The character at ``at`` separates words: not alphanumeric, and not a
    ``.`` that joins two alphanumerics (``v1.2`` is one token, so ``v1`` does
    not end at its dot)."""
    ch = hay[at]
    if ch.isalnum():
        return False
    if ch == "." and 0 <= beyond < len(hay) and hay[beyond].isalnum():
        return False
    return True


def _whole_word_in(needle: str, hay: str) -> bool:
    """``needle`` occurs in ``hay`` with a non-alphanumeric character (or the
    text's edge) on both sides (Arch's condition, 2026-10-29 20:06: a bare
    substring made ``v1`` a relation inside ``v1.2``, and ``MVP`` inside
    ``MVPs``). A character check, no regex."""
    if not needle:
        return False
    start = 0
    while True:
        i = hay.find(needle, start)
        if i < 0:
            return False
        j = i + len(needle)
        before_ok = i == 0 or _is_boundary(hay, i - 1, i - 2)
        after_ok = j == len(hay) or _is_boundary(hay, j, j + 1)
        if before_ok and after_ok:
            return True
        start = i + 1


def reference_relations(
    message: Optional[str],
    refs: Sequence[str],
    domain_context: Optional[Mapping[str, Any]],
) -> Dict[str, Dict[str, bool]]:
    """``{"#31": {"Beta launch": False}}``: per reference, each ``active_milestones``
    title found in the same sentence as the reference, mapped to whether any
    context item for that number carries that milestone. Empty when no title
    shares a sentence with a reference. Pure; a character scan, no regex."""
    if not message or not refs or not domain_context:
        return {}
    titles: List[str] = []
    for m in domain_context.get("active_milestones") or []:
        t = m.get("title") if isinstance(m, Mapping) else None
        if isinstance(t, str) and t.strip() and t.strip() not in titles:
            titles.append(t.strip())
    if not titles:
        return {}
    wanted = set(refs)
    out: Dict[str, Dict[str, bool]] = {}
    for sentence in _sentences(message):
        low = sentence.lower()
        present = [t for t in titles if _whole_word_in(t.lower(), low)]
        if not present:
            continue
        for r in record_references(sentence):
            if r not in wanted:
                continue
            carried: set = set()
            for v in domain_context.values():
                _milestones_of_number(v, r[1:], carried)
            rel = out.setdefault(r, {})
            for t in present:
                rel[t] = rel.get(t, False) or t.lower() in carried
    return out


def listed_records_event(
    message: Optional[str],
    prompt_text: Optional[str],
    provenance: Optional[Mapping[str, Mapping[str, Any]]] = None,
    domain_context: Optional[Mapping[str, Any]] = None,
    history: Optional[Sequence[Mapping[str, Any]]] = None,
    user_message: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """The event payload for a reply that enumerates records, else ``None``.

    Fires when the reply carries two or more record references or list lines
    (Arch's "enumerates two or more record references"), or when ANY reference
    is absent from the prompt (one invented number is already the #2040 case),
    or when ``reference_relations`` is non-empty (a single-reference aside that
    pairs a record with a milestone, Arch 2026-10-29).
    Pure function of its inputs; the caller logs it and changes nothing.
    """
    refs = record_references(message)
    lines = count_list_lines(message)
    sourced = set(record_references(prompt_text))
    unsourced = [r for r in refs if r not in sourced]
    relations = reference_relations(message, refs, domain_context)
    if len(refs) < 2 and lines < 2 and not unsourced and not relations:
        return None
    return {
        "references": refs,
        "reference_count": len(refs),
        "unsourced_references": unsourced,
        "reference_sources": reference_sources(refs, domain_context, history, user_message),
        "list_lines": lines,
        "context_reads": context_reads(provenance, domain_context),
        "reference_relations": relations,
    }


__all__ = (
    "record_references",
    "reference_sources",
    "reference_relations",
    "count_list_lines",
    "context_reads",
    "listed_records_event",
)
