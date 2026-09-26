"""#1772 residual — the floor's post-compose SCOPE GUARD.

**The defect this closes.** #1717 made the floor's source-failed directive
honest at the PROMPT layer ("name only the checks explicitly listed as
FAILED above... never imply a source failed when it was simply not
consulted"). Three independent measurement rounds
(``dev/2026/09/15/1772-scope-leak-measurement.md``,
``dev/2026/09/24/1772-candidate-measurement-2026-09-24.md``,
``dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md``) showed the
model does not reliably comply: on a single armed source-failed flag
(``reminders``), anthropic's floor composed a second sentence claiming
*"For the rest of your status ... I don't have your todos, calendar, or
project updates in front of me this turn"* at rates of 50% -> 20% -> 10%
across three copy revisions of the same prompt. A prompt instruction is a
request the model can decline; this module makes the honesty property
STRUCTURAL instead — the same move #1717 itself made (unify the composition
path rather than trust wording to hold).

**The ruling.** CXO ruled BUILD (not accept the residual): a measured rate is
a promise about phrasing, not a property of the mechanism, and it will
re-open on every future copy change. Arch ruled the mechanism SOUND: the
``SOURCE_FAILED_FLAGS`` registry already tracks the armed set per turn, so a
post-compose filter against it needs nothing new invented. Arch's condition,
carried as part of the ruling, not optional polish: the guard must not
over-trigger on a sentence that MENTIONS or QUOTES an unarmed source without
claiming a failed/unchecked read (a successful read, a reference to earlier
conversation, or an offer to check). See
``mailboxes/lead/read/rule-cxo-to-lead-cc-arch-pm-1772-residual-build-the-guard-not-accept-10-percent-2026-09-25.md``
and the adjacent Arch reply.

**What this is, and is not.** This is deterministic POST-COMPOSE OUTPUT
FILTERING, not intent classification or argument extraction — it runs after
the LLM has composed a reply and never feeds a routing decision. It is NOT a
new entry in ``TestExtractionPatternRatchet``'s scanned surfaces (that
ratchet scans named symbols in ``pre_classifier.py``, ``todo_handlers.py``,
``drafted_issue.py``, and ``intent_service.py``'s slot-fill helper — none of
which this module touches).

**The classifier, precisely.** A sentence is dropped iff:
  1. it names at least one source family that is NOT in this turn's armed
     set (``UNARMED_FAMILIES_MATCHED`` below), AND
  2. it contains a failure-claim verb/phrase (``_FAILURE_CLAIM_RE``) —
     "don't have ... in front of me", "couldn't check", "wasn't able to",
     "no access to", "not available", "unchecked", "failed to ...", etc.

A sentence naming BOTH an armed and an unarmed source under a failure claim
(the N>=2 case — e.g. "I couldn't check your reminders or your calendar this
turn" when only ``reminders`` is armed) is KEPT, not dropped: it also
contains a TRUE claim about the armed source, and removing the whole
sentence would lose that true claim to filter the false half. Decided and
documented here rather than left implicit; see
``test_scope_guard_1772.TestArmedPlusUnarmedSentence`` for the pinned case.

**Fail-safe direction.** Per CXO: over-filtering a false positive (dropping
a legitimate sentence) costs less than under-filtering a false claim
(leaving a scope leak in). When a sentence is genuinely ambiguous under this
narrow classifier, the classifier's own narrowness already resolves it —
false positives (dropping legitimate content) are also a live cost the
Arch-mandated adversarial pass exists to bound, so this module is built
narrow by construction rather than reaching for the widest possible net.

**Zero-cost when nothing is armed.** ``apply_scope_guard`` returns the input
text UNCHANGED, with no regex work at all, when ``armed_check_names`` is
empty — a turn with no source-failed flag never runs the scan (#1772 AC).
"""

import re
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Sequence, Tuple

import structlog

logger = structlog.get_logger()


# ---------------------------------------------------------------------------
# The source-vocabulary registry — synonym table (#1772, built from the
# SOURCE_FAILED_FLAGS registry's own check_name vocabulary plus the leak
# corpus's actual nouns, per the issue's explicit instruction: "keep it a
# small explicit table in code, documented, and covered by tests").
# ---------------------------------------------------------------------------


class SourceFamily(NamedTuple):
    """One source-noun vocabulary family the guard recognizes in reply prose.

    ``check_names`` names the ``SOURCE_FAILED_FLAGS`` registry check_name(s)
    (``services/intent_service/conversational_floor.py``) this family maps
    to. A family whose ``check_names`` is EMPTY (see ``calendar`` below) can
    never be armed — #1772's own measurement found the model naming
    "calendar" as an unavailable source despite there being no registered
    ``*_source_failed`` flag for it at all (the model invented the
    category). An empty ``check_names`` family is therefore always treated
    as unarmed, which is the correct behavior with no special-casing: the
    intersection with any armed set is always empty.
    """

    id: str
    check_names: FrozenSet[str]
    phrases: FrozenSet[str]


SOURCE_FAMILIES: Tuple[SourceFamily, ...] = (
    SourceFamily(
        id="todos",
        # Covers BOTH todo-related SOURCE_FAILED_FLAGS check_names — the
        # corpus never distinguishes "pending" from "completed" when naming
        # the family generically as "todos"/"todo list".
        check_names=frozenset({"pending todos", "completed todos"}),
        phrases=frozenset(
            {
                "todos",
                "todo list",
                "to-do list",
                "to-dos",
                "pending todos",
                "completed todos",
            }
        ),
    ),
    SourceFamily(
        id="reminders",
        check_names=frozenset({"reminders"}),
        phrases=frozenset({"reminders", "reminder"}),
    ),
    SourceFamily(
        id="calendar",
        # NOT a registered SOURCE_FAILED_FLAGS check — see class docstring.
        # Always unarmed by construction (empty check_names intersects
        # nothing), which is exactly the property #1772's measurement showed
        # was needed: the model names this category despite it never being
        # armable.
        check_names=frozenset(),
        phrases=frozenset({"calendar", "calendars", "meeting", "meetings"}),
    ),
    SourceFamily(
        id="projects",
        check_names=frozenset({"projects"}),
        phrases=frozenset({"projects", "project board", "project updates", "project"}),
    ),
    SourceFamily(
        id="github",
        check_names=frozenset({"GitHub"}),
        phrases=frozenset({"github", "repo", "repos", "repository", "issues"}),
    ),
)


def _compile_phrase_pattern(family: SourceFamily) -> "re.Pattern[str]":
    # Longest-first is cosmetic here (we only need presence, not the longest
    # matched span), kept for readability/debuggability of the compiled
    # pattern rather than correctness.
    phrases_sorted = sorted(family.phrases, key=len, reverse=True)
    alternation = "|".join(re.escape(p) for p in phrases_sorted)
    return re.compile(rf"\b(?:{alternation})\b", re.IGNORECASE)


_FAMILY_PATTERNS: Dict[str, "re.Pattern[str]"] = {
    f.id: _compile_phrase_pattern(f) for f in SOURCE_FAMILIES
}

_FAMILIES_BY_ID: Dict[str, SourceFamily] = {f.id: f for f in SOURCE_FAMILIES}


# ---------------------------------------------------------------------------
# The failure-claim vocabulary — built from the leak corpus's actual verbs
# (issue #1772's own list): "don't have ... in front of me", "couldn't
# check", "wasn't able to", "no access to", "not available this turn",
# "unchecked", "failed". Narrow and literal by construction, same discipline
# as ``unarmed_offer.py``'s anchored-opener family: a false negative leaves
# today's status quo (a leak this guard doesn't catch — no regression), a
# false positive mangles legitimate copy (bounded by the adversarial-pass
# test corpus below).
# ---------------------------------------------------------------------------

_FAILURE_CLAIM_RE = re.compile(
    r"("
    r"don'?t have\b|didn'?t have\b|doesn'?t have\b|"
    r"couldn'?t check\b|could not check\b|"
    r"wasn'?t able to\b|was not able to\b|"
    r"haven'?t been able to\b|hasn'?t been able to\b|"
    r"no access to\b|"
    r"not available\b|unavailable\b|"
    r"\bunchecked\b|"
    r"failed to (?:check|load|pull up|verify|reach)\b|"
    r"haven'?t checked\b|hasn'?t checked\b|"
    r"wasn'?t checked\b|was not checked\b"
    r")",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Sentence splitting — literal, not NLP. Splits on paragraph breaks first (so
# dropping every sentence in a paragraph drops the whole paragraph cleanly),
# then on whitespace following a sentence-terminal ., !, or ?.
# ---------------------------------------------------------------------------

_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _families_matched(sentence: str) -> List[str]:
    return [fid for fid, pattern in _FAMILY_PATTERNS.items() if pattern.search(sentence)]


def _sentence_verdict(sentence: str, armed_set: FrozenSet[str]) -> Tuple[bool, List[str]]:
    """Returns (should_drop, unarmed_family_ids_named).

    A sentence is dropped only when it (a) names a family whose check_names
    do not intersect ``armed_set`` AND (b) carries a failure-claim phrase.
    A sentence naming an unarmed family ALONGSIDE an armed one is kept — see
    module docstring.
    """
    if not _FAILURE_CLAIM_RE.search(sentence):
        return False, []

    matched = _families_matched(sentence)
    if not matched:
        return False, []

    armed_matched = [fid for fid in matched if _FAMILIES_BY_ID[fid].check_names & armed_set]
    unarmed_matched = [fid for fid in matched if fid not in armed_matched]

    if not unarmed_matched:
        return False, []
    if armed_matched:
        # N>=2 case: the sentence also makes a TRUE claim about an armed
        # source. Dropping it would lose that true claim to filter the false
        # half — keep it whole. Decided and pinned, not incidental.
        return False, []
    return True, unarmed_matched


def _is_fragment(text: str) -> bool:
    """Heuristic floor for 'not really an answer any more' (#1772 AC).

    Narrow, literal: fewer than 3 whitespace-separated words, or empty after
    stripping. Matches the module's overall discipline of cheap literal
    checks over cleverness.
    """
    stripped = text.strip()
    if not stripped:
        return True
    return len(stripped.split()) < 3


def build_fallback_sentence(armed_check_names: Sequence[str]) -> str:
    """The armed-set honest sentence the SOURCE_FAILED_FLAGS registry
    already licenses, composed from the check_names actually armed this
    turn.

    # CXO copy pass owed (#1772 guard fallback) — this is placeholder-safe
    # (never fabricates, never claims an unarmed source), not yet a
    # reviewed final string.
    """
    names = ", ".join(armed_check_names)
    return f"I couldn't check {names} this turn."


def apply_scope_guard(
    text: str,
    armed_check_names: Sequence[str],
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    intent_category: Optional[str] = None,
) -> Tuple[str, int]:
    """The #1772 post-compose scope guard.

    Drops any sentence that CLAIMS an unarmed source failed/was
    unavailable/unchecked this turn (never rewrites — a dropped claim is
    removed, not softened). If dropping empties the reply or leaves only a
    fragment, falls back to the armed-set honest sentence
    (``build_fallback_sentence``).

    Args:
        text: the composed LLM reply, already past the other output-seam
            filters (scaffolding strip, placeholder-slot strip).
        armed_check_names: this turn's armed SOURCE_FAILED_FLAGS
            check_names, in registry order (empty => no scan at all, zero
            cost — #1772 AC).

    Returns:
        (filtered_text, dropped_sentence_count)
    """
    armed_set = frozenset(armed_check_names)
    if not armed_set:
        return text, 0
    if not text:
        return text, 0

    dropped_count = 0
    unarmed_named: List[str] = []

    paragraphs = _PARAGRAPH_SPLIT_RE.split(text)
    kept_paragraphs: List[str] = []
    for paragraph in paragraphs:
        sentences = _SENTENCE_SPLIT_RE.split(paragraph)
        kept_sentences: List[str] = []
        for sentence in sentences:
            if not sentence.strip():
                continue
            drop, unarmed = _sentence_verdict(sentence, armed_set)
            if drop:
                dropped_count += 1
                unarmed_named.extend(unarmed)
                continue
            kept_sentences.append(sentence)
        if kept_sentences:
            kept_paragraphs.append(" ".join(kept_sentences))

    if dropped_count == 0:
        return text, 0

    filtered = "\n\n".join(kept_paragraphs)

    if _is_fragment(filtered):
        filtered = build_fallback_sentence(armed_check_names)

    logger.warning(
        "floor_scope_guard_dropped",
        dropped_sentences=dropped_count,
        unarmed_sources=sorted(set(unarmed_named)),
        session_id=session_id,
        user_id=user_id,
        intent_category=intent_category,
    )

    return filtered, dropped_count
