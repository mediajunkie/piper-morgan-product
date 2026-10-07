"""
Todo Intent Handlers - Natural language interface for todo operations

Issue #285: CORE-ALPHA-TODO-INCOMPLETE
Wires chat commands to TodoManagementService. NOTE (#1427 → 2026-08-30):
services/api/todo_management.py — the mocked, unmounted todos REST surface
this file once borrowed request models from (PM-081) — was disposed in the
census disposal Batch 3 (the model import here had long been unused). Chat —
this file — and the Lists API are the live todos surfaces. The live
/api/v1/todos REST routes are web/api/routes/todos.py (a different module).

Enhanced with consciousness injection (#407 MUX-VISION-STANDUP-EXTRACT)
for more alive, present-feeling responses.

Issue #904: CANONICAL-TODO-COMPLETE — Added fuzzy text matching for
completion ("complete the PR review" matches "Review the PR for auth").

Example commands:
- "add todo: Review PR #285"
- "show my todos"
- "show all my todos" (includes completed)
- "mark todo 1 as complete"
- "complete the PR review todo"
- "delete todo about meeting"
"""

import re
import string
from typing import Any, List, Optional, Tuple
from uuid import UUID

import structlog
from sqlalchemy.exc import SQLAlchemyError

from services.consciousness.todo_consciousness import (
    format_next_todo_conscious,
    format_todo_completed_conscious,
    format_todo_created_conscious,
    format_todo_deleted_conscious,
    format_todo_list_conscious,
)
from services.domain.models import Intent, Todo
from services.intent_service.temporal_utils import DURATION_NUMBER_SRC
from services.todo.todo_management_service import TodoManagementService

logger = structlog.get_logger()

# Words that don't contribute to meaningful matching
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "and",
        "or",
        "but",
        "is",
        "it",
        "my",
        "your",
        "this",
        "that",
        "i",
        "me",
        "we",
        "do",
        "did",
        "has",
        "have",
        "had",
        "be",
        "been",
        "todo",
        "task",
        "item",
        "thing",
    }
)

# Minimum fuzzy match score to consider a match
_FUZZY_MATCH_THRESHOLD = 0.3


# --- shared title matcher (pure, module-level) ------------------------------
#
# #904 built this as TodoIntentHandlers methods for the completion path;
# the #1527 named-target delete gate (destructive_confirm.
# build_todo_delete_confirmation) needs the SAME matching — same word-overlap
# score, same _FUZZY_MATCH_THRESHOLD — so the mechanism lives here as pure
# functions and both callers delegate. One matcher, two policies: completion
# takes the best match (unchanged #904 behavior); the DESTRUCTIVE delete gate
# branches on the candidate count (single → title-bound confirm, several →
# ask which, none → honest didn't-find). Pure functions by design (the
# SessionSnapshot-lift note): no self, no I/O — the todos list comes in as
# an argument.


def _meaningful_words(text: str) -> frozenset:
    """The non-stopword word set of ``text`` (lowercased)."""
    return frozenset(w for w in re.findall(r"\w+", text.lower()) if w not in _STOPWORDS)


def fuzzy_todo_match_score(query: str, candidate: str) -> float:
    """Score how well query words match candidate words (0.0 to 1.0).

    Word overlap with stopword filtering: the fraction of meaningful query
    words found in the candidate (#904's mechanism, verbatim).
    """
    query_words = _meaningful_words(query)
    candidate_words = _meaningful_words(candidate)

    if not query_words:
        return 0.0

    overlap = query_words & candidate_words
    return len(overlap) / len(query_words)


def match_todos_by_text(search_text: str, todos: List[Todo]) -> List[Tuple[float, Todo]]:
    """All todos scoring >= _FUZZY_MATCH_THRESHOLD against ``search_text``,
    best first (stable sort: list order breaks ties)."""
    if not todos or not search_text:
        return []
    scored = [(fuzzy_todo_match_score(search_text, todo.text), todo) for todo in todos]
    scored = [(score, todo) for score, todo in scored if score >= _FUZZY_MATCH_THRESHOLD]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def resolve_named_todo_target(search_text: str, todos: List[Todo]) -> List[Todo]:
    """Resolve a NAMED todo target to its candidate rows — exact → fuzzy.

    Exact tier: a candidate whose meaningful word set equals the query's
    exactly. A UNIQUE exact match wins outright (so "call mom" against
    ["call mom", "call the dentist"] is one match, not an ambiguity).
    Otherwise every fuzzy candidate at the shared threshold comes back,
    best first — the caller decides what multiple candidates mean (the
    delete gate asks which; completion's best-match policy never calls
    this, it takes ``match_todos_by_text``'s head).
    """
    query_words = _meaningful_words(search_text)
    if not query_words:
        return []
    scored = match_todos_by_text(search_text, todos)
    exact = [todo for _, todo in scored if _meaningful_words(todo.text) == query_words]
    if len(exact) == 1:
        return exact
    return [todo for _, todo in scored]


# --- #1914: clause-boundary split + ordinal binding for complete_todo -------
#
# PM live (alpha v156, 2026-10-01): "Mark the first one complete and leave
# the second one pending." The old single-pattern extractor took EVERYTHING
# after the completion verb as the target, including the conjunction and a
# whole second clause that is an explicit no-op ("...and leave the second
# one pending.") — so the fuzzy matcher had nothing sane to search against.
#
# Fix is two bounded pieces:
#   1. Split the message at an UNQUOTED clause joiner ("and"/"but"/"then")
#      followed by a no-op/imperative verb ("leave", "keep", "don't", ...)
#      BEFORE any extraction runs. A quoted/named todo title containing
#      "and" is never split (the boundary must fall outside any quoted
#      span) — "mark 'review the PR and ship it' done" keeps its title.
#   2. When the surviving target is ordinal/positional ("the first one",
#      "#2", "the last one"), bind it by POSITION against the same
#      candidate list the floor just rendered (due reminders) via the
#      #1906 pick-target binder (``_resolve_pick_target`` — shared, not
#      reimplemented) rather than fuzzy word-matching a sentence like
#      "first one" against todo text, which can never score.

# Quoted/named-title spans — same shape as reminder_clear's named-target
# regex, used here only to PROTECT an "and" inside a title from the clause
# split below (never to extract from).
_QUOTE_SPAN_RE = re.compile(r"[\"'“‘]([^\"'”’]*)[\"'”’]")

# Clause joiner ("and" / "and then" / "but" / "then") immediately followed
# by a no-op/imperative verb phrase — the shape of a trailing instruction
# the completion handler must acknowledge, never fold into the target or
# act on (#1914). Deliberately narrow: an "and" followed by anything NOT in
# this verb list is left alone (it may be part of the todo's own text).
_CLAUSE_JOINER_RE = re.compile(
    r"""
    ,?\s+(?:and\s+then|and|but|then)\s+
    (?=(?:please\s+)?
        (?:leave|keep|don'?t|do\s+not|skip|ignore|
           wait(?:\s+on)?|hold\s+off(?:\s+on)?|stop)\b
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Ordinal/positional shape — "the first one", "second", "#2", "the last
# one". Detection only (NOT the binder itself — that's the shared
# ``_resolve_pick_target`` from reminder_clear, imported where used); this
# just decides whether to attempt position binding before falling back to
# fuzzy text matching.
_ORDINAL_SHAPE_RE = re.compile(
    r"\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last)\b" r"|#\s*\d+\b",
    re.IGNORECASE,
)


# --- Arch's (a), #1943 (2026-10-06): the ROUTER names the targets ---------
#
# "LLM decides meaning, code decides permission." The Inversion router emits
# ``args.targets`` / ``args.exclude`` for complete_todo (the mini-grammar in the
# rail entry's description: "1" ordinal · "1-3" range · "last" · "all" ·
# "name:<text>"). Code here does two things only: RESOLVE those tokens against
# the real candidate list, and hold the MUTATION BOUNDARY — one resolved item
# completes; two or more, or any carve-out, arms the #1190 confirm that
# enumerates what will be touched and what won't. No regex interprets the
# user's words on this path; the binders below it are what this replaces.

BATCH_COMPLETE_IDS_KEY = "batch_complete_ids"
BATCH_COMPLETE_TEXTS_KEY = "batch_complete_texts"
BATCH_COMPLETE_LEFT_KEY = "batch_complete_left_texts"

# Clear-family build plan piece 1 (2026-10-07): delete_todo's own carrier
# keys on the #1190 pending-action record — same shape as the complete
# batch keys above, kept separate so a clear_todos resolver entry (piece 2)
# can bind either verb's ids without the two colliding on one context key.
BATCH_DELETE_IDS_KEY = "batch_delete_ids"
BATCH_DELETE_TEXTS_KEY = "batch_delete_texts"
BATCH_DELETE_LEFT_KEY = "batch_delete_left_texts"

_ORDINAL_TOKEN_RE = re.compile(r"^#?(\d{1,3})$")
_RANGE_TOKEN_RE = re.compile(r"^#?(\d{1,3})\s*[-–—]\s*#?(\d{1,3})$")


def _router_target_tokens(value: Any) -> List[str]:
    """``targets``/``exclude`` as the router sent them: a list of strings, or
    one comma/semicolon-joined string. Anything else is "no targets"."""
    if isinstance(value, str):
        return [p.strip() for p in re.split(r"[,;]", value) if p.strip()]
    if isinstance(value, list):
        return [str(p).strip() for p in value if str(p).strip()]
    return []


def resolve_router_targets(
    tokens: List[str],
    candidates: List[Todo],
    ordinal_candidates: Optional[List[Todo]] = None,
) -> Tuple[List[Todo], List[str]]:
    """Resolve mini-grammar tokens against ``candidates`` (list order = the
    order the user saw). Returns (resolved, unresolved-tokens). Never guesses:
    an ordinal past the end, a range with nothing in it, or a name matching
    nothing is UNRESOLVED and reported; a name matching several candidates
    with the SAME text resolves to all of them (two reminders both called
    "check the test card again" are both meant); a name matching several
    DIFFERENT texts is unresolved (the caller asks)."""
    picked: List[Todo] = []
    unresolved: List[str] = []
    seen: set = set()

    def _add(t: Todo) -> None:
        if t.id not in seen:
            seen.add(t.id)
            picked.append(t)

    # CXO's rule (1943): positions index ONLY the numbered list the user saw.
    # Callers that have no such list pass [] — every ordinal is then unresolved.
    positional = candidates if ordinal_candidates is None else ordinal_candidates
    n = len(positional)
    for raw in tokens:
        tok = raw.strip().strip("\"'“”‘’").strip()
        low = tok.lower()
        if not tok:
            continue
        if low == "all":
            for t in candidates:
                _add(t)
            continue
        if low == "last":
            if n:
                _add(positional[-1])
            else:
                unresolved.append(raw)
            continue
        m = _RANGE_TOKEN_RE.match(tok)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            lo, hi = min(a, b), max(a, b)
            span = [positional[i - 1] for i in range(lo, hi + 1) if 1 <= i <= n]
            if span:
                for t in span:
                    _add(t)
            else:
                unresolved.append(raw)
            continue
        m = _ORDINAL_TOKEN_RE.match(tok)
        if m:
            i = int(m.group(1))
            if 1 <= i <= n:
                _add(positional[i - 1])
            else:
                unresolved.append(raw)
            continue
        name = tok[5:].strip().strip("\"'“”‘’").lower() if low.startswith("name:") else low
        exact = [t for t in candidates if (t.text or "").strip().lower() == name]
        if not exact:
            partial = [
                t
                for t in candidates
                if name in (t.text or "").lower() or (t.text or "").strip().lower() in name
            ]
            if len({(t.text or "").strip().lower() for t in partial}) == 1:
                exact = partial
            elif not partial:
                exact = resolve_named_todo_target(name, candidates)
                if len({(t.text or "").strip().lower() for t in exact}) > 1:
                    exact = []
        if exact:
            for t in exact:
                _add(t)
        else:
            unresolved.append(raw)
    return picked, unresolved


def _is_positional(token: str) -> bool:
    t = token.strip().strip("\"'“”‘’").lower()
    return t == "last" or bool(_ORDINAL_TOKEN_RE.match(t)) or bool(_RANGE_TOKEN_RE.match(t))


def _collapse_titles(texts: List[str]) -> List[Tuple[str, int]]:
    """Duplicate titles collapse with a count, order of first appearance kept
    (CXO: two identical quoted titles read as a rendering bug)."""
    out: List[Tuple[str, int]] = []
    index: dict = {}
    for t in texts:
        if t in index:
            out[index[t]] = (t, out[index[t]][1] + 1)
        else:
            index[t] = len(out)
            out.append((t, 1))
    return out


def _title_phrase(texts: List[str]) -> str:
    parts = [f'"{t}"' + (f" ({c} items)" if c > 1 else "") for t, c in _collapse_titles(texts)]
    if len(parts) <= 1:
        return parts[0] if parts else ""
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def _leaving_line(left: List[str]) -> str:
    """CXO: titles when 3 or fewer are left, a count above that, nothing when none."""
    if not left:
        return ""
    if len(left) <= 3:
        return f"Leaving {_title_phrase(left)} as is."
    return f"Leaving the other {len(left)} as is."


def _confirm_question(
    verb: str,
    targets: List[str],
    left: List[str],
    *,
    one_item_template: Optional[str] = None,
) -> str:
    """Shared body of the enumerating #1190 confirm: count first, titles
    verbatim in the user's order, duplicates collapsed; bullets instead of a
    sentence above 5 targets. ``verb`` is the imperative ("Complete" /
    "Delete"). ``one_item_template`` (delete's DESTRUCTIVE always-confirm
    rule, #1943 follow-on) renders a SINGLE target as its own sentence
    ("Delete the reminder \"X\"?") instead of "{Verb} 1 reminder: \"X\"?" —
    complete_todo never calls this path with one target (a single resolved
    item completes directly, no confirm), so this branch is additive and
    does not change complete_todo's pinned strings."""
    n = len(targets)
    noun = "reminder" if n == 1 else "reminders"
    leaving = _leaving_line(left)
    if n == 1 and one_item_template is not None:
        q = one_item_template.format(title=targets[0])
        if leaving:
            q += f" {leaving}"
        return q + " (yes/no)"
    if n > 5:
        lines = [f"{verb} {n} {noun}?"] + [
            f"• {t}" + (f" ({c} items)" if c > 1 else "") for t, c in _collapse_titles(targets)
        ]
        if leaving:
            lines.append(leaving)
        lines.append("(yes/no)")
        return "\n".join(lines)
    q = f"{verb} {n} {noun}: {_title_phrase(targets)}?"
    if leaving:
        q += f" {leaving}"
    return q + " (yes/no)"


def _batch_confirm_question(targets: List[str], left: List[str]) -> str:
    """CXO string 1: count first, titles verbatim in the user's order,
    duplicates collapsed; bullets instead of a sentence above 5 targets."""
    return _confirm_question("Complete", targets, left)


def _delete_confirm_question(targets: List[str], left: List[str]) -> str:
    """CXO string D1/D2/D3 (clear-family build plan piece 1, 2026-10-07):
    delete_todo's DESTRUCTIVE counterpart of ``_batch_confirm_question`` —
    delete ALWAYS confirms, even a single resolved target, so the n==1 case
    (never reached by complete_todo) renders its own sentence."""
    return _confirm_question(
        "Delete", targets, left, one_item_template='Delete the reminder "{title}"?'
    )


def _mutation_summary(
    verb_past: str,
    header_suffix: str,
    none_header: str,
    fail_verb: str,
    fail_suffix: str,
    done: List[str],
    failed: List[Tuple[str, str]],
    left: List[str],
) -> str:
    """Shared body of the post-"yes" summary (CXO string 3 and its delete
    counterpart, D4): the count and bullets report only what actually
    happened; a target that was gone by the time "yes" landed is named
    separately with its own reason; the summary never restates the confirm."""
    n = len(done)
    lines = (
        [f"{verb_past} {n} reminder{'s' if n != 1 else ''}{header_suffix}:"] if n else [none_header]
    )
    lines += [f"• {t}" + (f" ({c} items)" if c > 1 else "") for t, c in _collapse_titles(done)]
    for text, why in failed:
        lines.append(f"Couldn't {fail_verb} \"{text}\"{fail_suffix} — it's {why}.")
    if left:
        lines.append(f"Left {_title_phrase(left)} as is.")
    return "\n".join(lines)


def _batch_summary(done: List[str], failed: List[Tuple[str, str]], left: List[str]) -> str:
    """CXO string 3: the count and bullets report only what actually
    completed; a target that was gone by the time "yes" landed is named
    separately; the summary never restates the confirm."""
    return _mutation_summary(
        "Marked", " done", "Marked nothing done:", "mark", " done", done, failed, left
    )


def _delete_summary(done: List[str], failed: List[Tuple[str, str]], left: List[str]) -> str:
    """CXO string D4 (clear-family build plan piece 1): delete_todo's
    counterpart of ``_batch_summary`` — "Deleted" rather than "Marked …
    done", and a missing id reports "already gone" (delete's own ``why``,
    parallel to complete's "no longer there")."""
    return _mutation_summary("Deleted", "", "Deleted nothing:", "delete", "", done, failed, left)


def _delete_decline_message(targets: List[str]) -> str:
    """CXO string D5/D6: the Okay-family decline for a delete confirm —
    names the one title when there's exactly one target, else the count."""
    n = len(targets)
    if n == 1:
        return f'Okay — I won\'t delete "{targets[0]}". Nothing has been changed.'
    return f"Okay — I won't delete those {n}. Nothing has been changed."


def _quote_list(texts: List[str]) -> str:
    q = [f'"{t}"' for t in texts]
    if len(q) <= 1:
        return q[0] if q else ""
    return ", ".join(q[:-1]) + " and " + q[-1]


def _in_quoted_span(text: str, pos: int) -> bool:
    """Is ``pos`` inside one of ``text``'s quoted spans?"""
    return any(m.start() <= pos < m.end() for m in _QUOTE_SPAN_RE.finditer(text))


def _split_completion_clause(message: str) -> Tuple[str, Optional[str]]:
    """Split ``message`` at the first UNQUOTED clause-joiner boundary.

    Returns (head, tail) — ``tail`` is the trailing no-op clause text (never
    acted on, only acknowledged), or None when no boundary is found. A
    boundary inside a quoted/named title is skipped (#1914): the title
    keeps any "and" it contains.
    """
    for m in _CLAUSE_JOINER_RE.finditer(message):
        if _in_quoted_span(message, m.start()):
            continue
        head = message[: m.start()].rstrip()
        tail = message[m.end() :].strip()
        if head and tail:
            return head, tail
    return message, None


def _reminder_due_iso(todo: Todo) -> Optional[str]:
    """ISO-8601 ``reminder_date`` for a due-reminder candidate, for
    ``_resolve_pick_target``'s "the overdue one" status binding (#1914) —
    mirrors ``reminder_clear._due_iso``'s reminder-noun branch, computed
    fresh against candidates refetched at answer time (no persisted
    carrier for this path; see ``TodoIntentHandlers._due_reminder_todos``)."""
    from services.utils.datetime_utils import ensure_utc

    dt = ensure_utc(getattr(todo, "reminder_date", None))
    return dt.isoformat() if dt is not None else None


# --- #1648: the reminder time-clarify carrier -------------------------------
#
# Instance 2 of the #1648 fabrication incident: handle_create_reminder's
# honest time-clarify ask ("When should I remind you?") returned a bare
# question with NOTHING armed — so the answer turn ("at 3pm") had nothing to
# bind to, traversed the whole routing chain as an orphan, and landed on the
# floor, which roleplayed the save ("Reminder set for 3pm today", no 📅
# line, no row). The fix is the #1190/#846 deferred-action carrier shape the
# drafted-issue flow uses: the clarify ask ARMS a pending offer (kind
# ``reminder_time_question``) binding the task text; the next turn's time
# answer is consumed at the offer seam — before any classification surface —
# and the REAL save runs (the 📅 confirmation is composed from the actual
# row write, never improvised). A turn that answers with no parseable time
# RE-ASKS honestly and RE-ARMS; a full reminder restatement or an unrelated
# command abandons via the pop and routes normally, per the carrier's rules.

REMINDER_TIME_QUESTION_KIND = "reminder_time_question"

# Generic-accept landing (a bare "yes" doesn't answer "when?") — registered
# action_triggered=False in workflow_entries, the #1605 clarify precedent.
CLARIFY_REMINDER_TIME_WORKFLOW = "clarify_reminder_time"

# A full reminder restatement ("remind me to X at 3pm") carries its own task
# AND time — it must route normally (the pre-classifier claims it
# deterministically) so the full handler re-extracts both, rather than this
# seam saving the OLD task text under the new time. Mirrors
# PreClassifier.REMINDER_PATTERNS.
_REMINDER_RESTATEMENT_RE = re.compile(
    r"\b(?:remind\s+me\s+(?:to|about)\b|set\s+(?:a\s+)?reminder\b|"
    r"create\s+(?:a\s+)?reminder\b|don'?t\s+let\s+me\s+forget\b|"
    r"need\s+to\s+remember\s+to\b)",
    re.IGNORECASE,
)

_TIME_SIGNAL_RE = None  # compiled lazily — needs TodoIntentHandlers._TIME_EXPR


def _has_time_signal(message: str) -> bool:
    """Does the turn carry any time expression parse_reminder_time could
    bind? Uses the class's _TIME_EXPR (kept mirrored with the parser) plus
    the bare day words the parser handles honestly ("today" → ask-shaped
    when unbindable, never a silent default). Without this gate, an
    arbitrary answer would fall into the parser's tomorrow-morning DEFAULT
    and save a time the user never said (#1490's silent-default class)."""
    global _TIME_SIGNAL_RE
    if _TIME_SIGNAL_RE is None:
        _TIME_SIGNAL_RE = re.compile(
            rf"(?:{TodoIntentHandlers._TIME_EXPR})|\btoday\b|\btonight\b",
            re.IGNORECASE,
        )
    return bool(_TIME_SIGNAL_RE.search(message))


def _strip_trailing_time_expressions(text: str) -> str:
    """Shed trailing punctuation and time expressions so the saved todo text
    is clean ("buy milk at 3pm tomorrow." → "buy milk"). Loop until stable:
    the tail sheds ".", then "at 3pm", then "tomorrow" (#1490). Factored
    from _extract_reminder_text so the #1654 task-answer seam and the
    primary extraction share one strip."""
    while text:
        stripped = text.rstrip(".,!?;: ").strip()
        stripped = re.sub(
            rf"\s+{TodoIntentHandlers._TIME_EXPR}\s*$",
            "",
            stripped,
            flags=re.IGNORECASE,
        ).strip()
        if stripped == text:
            break
        text = stripped
    return text


_PURE_TIME_RE = None  # compiled lazily — needs TodoIntentHandlers._TIME_EXPR


def _is_pure_time_expression(text: str) -> bool:
    """Is the WHOLE text just time expressions ("at 3pm", "tomorrow at 9")?
    #1654: a pure-time answer to the TASK question means the task is still
    missing — it must re-ask, never save the time expression AS the task.
    (The trailing strip can't catch it: a time at the very start of the
    string has no preceding whitespace for the tail regex to anchor on.)"""
    global _PURE_TIME_RE
    if _PURE_TIME_RE is None:
        unit = rf"(?:{TodoIntentHandlers._TIME_EXPR}|today|tonight)"
        _PURE_TIME_RE = re.compile(rf"\s*{unit}(?:[\s,]+{unit})*[\s.!?]*", re.IGNORECASE)
    return bool(_PURE_TIME_RE.fullmatch(text))


def _format_reminder_when(when, user_tz=None) -> str:
    """#1572: the ONE reminder clock-face renderer (save confirmation + list).

    With a stored user tz: the USER'S wall clock, labeled with the zone
    abbreviation ("Saturday, August 29 at 4:00 PM PDT"). Without one: the
    pre-#1572 face labeled "UTC", unchanged (fail-safe; never an unlabeled
    face — #1535/#1589's rule)."""
    from services.utils.user_timezone import resolve_zone

    zone = resolve_zone(user_tz)
    if zone is not None:
        local = when.astimezone(zone)
        # %Z can render empty for some zones; the IANA name is the honest
        # fallback label ("America/Los_Angeles" beats an unlabeled face).
        label = local.strftime("%Z") or user_tz
        return local.strftime("%A, %B %-d at %-I:%M %p ") + label
    return when.strftime("%A, %B %-d at %-I:%M %p UTC")


def _reminder_saved_message(text: str, reminder_dt, time_label: str, user_tz=None) -> str:
    """The one true save confirmation (📅 line included) — composed only
    beside an actual row write. Factored from handle_create_reminder so the
    #1648 time-answer seam and the primary path share one copy source."""
    time_display = time_label
    if reminder_dt:
        # PM live 2026-08-15: this rendered a UTC instant with no label
        # ("Saturday at 11:42 PM" for a 4:42 PM PT save) — the #1542/#1589
        # unlabeled-clock-face shape. #1572: with a stored user tz the face
        # is now the user's clock, labeled; without one it stays UTC and
        # SAYS so (the reminders list uses the same renderer).
        time_display = _format_reminder_when(reminder_dt, user_tz)

    # #1562: labels from the bare-clock branch start with "at" ("at 5pm") —
    # strip a LEADING "at" so the copy never reads "(scheduled for at 5pm)".
    # Same doublet family as #1490's "tomorrow at at 3pm".
    schedule_label = re.sub(r"^at\s+", "", time_label)

    # Issue #1096 slice 2 (Pattern-073 discipline): verification-bounded
    # phrasing — surfaced "in conversation", the mechanism we actually have.
    # #1569: reminders ARE todos in storage (unified model, PM-ratified) —
    # the closing sentence TEACHES that relationship.
    return (
        f"Reminder saved: **{text}** "
        f"(scheduled for {schedule_label}).\n\n"
        f"📅 {time_display}\n\n"
        f"It lives with your todos (you'll see it on the Todos page) "
        f"and I'll surface it in conversation once it's due."
    )


# --- #1654: the reminder task-clarify carrier -------------------------------
#
# #1648's class, one question earlier: handle_create_reminder's OTHER honest
# ask — the no-task clarify ("I didn't catch what you'd like to be reminded
# about", the one PM hit twice on 08-18 via the colon-form parse misses) —
# armed nothing, so its answer (a bare task phrase) orphaned into the routing
# chain. Same carrier treatment, task-question kind: the ask ARMS a pending
# offer holding the ORIGINAL message; the next turn's answer binds as the
# TASK. Then either the time is already known from the original message
# (rare — e.g. "remind me at 3pm", where a time parsed but the task didn't)
# and the REAL save runs, or the flow chains into the EXISTING #1648 time
# question. The colon-form PARSE miss itself stays #1606/corpus — this
# carrier only guarantees the ask, once fired, holds its answer.

REMINDER_TASK_QUESTION_KIND = "reminder_task_question"

# Generic-accept landing (a bare "yes" doesn't answer "what?") — registered
# action_triggered=False in workflow_entries (the #1605/#1648 clarify
# precedent).
CLARIFY_REMINDER_TASK_WORKFLOW = "clarify_reminder_task"

# #1665: ONE render of the time ask, shared by the primary time-clarify
# branch (#1648) and the #1654 chain arm — stored on the armed record
# verbatim, embedded in the reply, never re-rendered.
_TIME_ASK = "When should I remind you? " "(For example: 'at 3pm tomorrow' or 'in 2 hours'.)"


def build_reminder_task_offer(original_message: str, user_id, question=None) -> dict:
    """The #846 pending-offer record arming the task question (#1654).

    Carries the ORIGINAL message — strings only, so the payload snapshots
    cleanly — letting the answer turn recover a time the user already gave
    ("remind me at 3pm"); the time is re-parsed at answer time, never
    serialized. ``question`` (#1665): the ALREADY-RENDERED ask the caller
    returns this turn — stored verbatim, never re-rendered. An open
    question, NOT a yes/no (pinned outside the #1664 confirm-kind set)."""
    return {
        "workflow_type": CLARIFY_REMINDER_TASK_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": REMINDER_TASK_QUESTION_KIND,
            "action": "create_reminder",
            "original_message": original_message,
            "user_id": str(user_id) if user_id else None,
            "summary": "set a reminder",
        },
        "decline_message": ("Okay — I haven't set a reminder. Nothing was saved."),
    }


def build_reminder_time_offer(task_text: str, user_id, question=None) -> dict:
    """The #846 pending-offer record arming the time question (the generic
    deferred-action carrier shape documented in destructive_confirm.py).

    ``question`` (#1665): the ALREADY-RENDERED "when?" ask the caller returns
    this turn — stored verbatim, never re-rendered, so the SessionSnapshot's
    pending_offer_question matches what the user saw. An open question, NOT
    a yes/no (pinned outside the #1664 confirm-kind set)."""
    return {
        "workflow_type": CLARIFY_REMINDER_TIME_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": REMINDER_TIME_QUESTION_KIND,
            "action": "create_reminder",
            "task_text": task_text,
            "user_id": str(user_id) if user_id else None,
            "summary": f'set a reminder for "{task_text}"',
        },
        "decline_message": ("Okay — I haven't set that reminder. Nothing was saved."),
    }


class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to TodoManagementService for persistence.
    """

    def __init__(self):
        """Initialize with TodoManagementService."""
        self.todo_service = TodoManagementService()

    async def get_due_reminders(self, user_id: UUID) -> Optional[List[str]]:
        """
        Issue #903: Get reminders that are due now or overdue.

        Returns a list of reminder text strings for surfacing at greeting time.
        Queries todos where reminder_date <= now and status != completed.

        Issue #1491: both sides of the due-ness comparison are normalized to
        aware-UTC (the #1429 standup guard shape). reminder_date comes back
        tz-aware from Postgres timestamptz but tz-naive from backends that
        drop tzinfo (e.g. SQLite in tests); the old naive `datetime.now()`
        against an aware row raised TypeError, which the swallow below turned
        into the None sentinel — so saved reminders never surfaced (live on
        v30, 2026-08-07). Naive rows are assumed UTC per ensure_utc().
        """
        from datetime import datetime, timezone

        from services.utils.datetime_utils import ensure_utc

        todo_count: Optional[int] = None
        reminders_considered = 0
        try:
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)
            todo_count = len(todos)
            now = datetime.now(timezone.utc)
            due = []
            for todo in todos:
                reminder_date = getattr(todo, "reminder_date", None)
                if reminder_date is None or todo.completed:
                    continue
                reminders_considered += 1
                # #1491/#1429 guard: coerce the row aware-UTC before comparing.
                if ensure_utc(reminder_date) <= now:
                    due.append(todo.text)
            return due
        except Exception as e:  # silent-ok: logged at error w/ exc_info; None sentinel -> assembler flags source_failed instead of "no reminders due" (#1425)
            # #1491/#1423: error-level, never warning-swallow — this failure
            # hid the v30 TypeError for days because warnings don't surface.
            logger.error(
                "Failed to fetch due reminders (source failed)",
                error=str(e),
                todo_count=todo_count,
                reminders_considered=reminders_considered,
                exc_info=True,
            )
            return None

    async def handle_complete_todo_targets(
        self,
        intent: Intent,
        session_id: Optional[str],
        user_id: UUID,
        offer_service: Any,
        principal: Optional[str],
    ) -> Optional[Tuple[str, bool]]:
        """Arch's (a), #1943: act on ROUTER-named targets. Returns
        ``(message, question_armed)`` when this path owns the turn, or
        ``None`` when the router named no targets (the legacy handler runs).

        Copy: CXO's ruling 2026-10-06 (five strings, verbatim). Scope rule
        (CXO): an ORDINAL or RANGE resolves ONLY against the list the user was
        last shown NUMBERED (``conversation_context.last_numbered_list``);
        with no numbered list shown, an ordinal is unresolved — the reply
        shows the active list numbered (which then grounds the next turn).
        Names and "all" resolve against the due reminders when any, else the
        active to-dos. Nothing changes on an unresolved turn.

        - confirmed re-entry (the #1190 "yes" re-dispatches this intent with
          ``destructive_confirmed`` + the bound ids): complete exactly the
          bound rows (#1666) and report only what actually completed.
        - one resolved item, no carve-out: complete it (today's reply).
        - two or more, or any ``exclude``: arm the enumerating confirm —
          nothing changes this turn.
        """
        from services.intent_service.destructive_confirm import (
            CONFIRM_PENDING_ACTION_WORKFLOW,
            CONFIRMED_CONTEXT_KEY,
        )

        ctx = dict(intent.context or {})
        args = ctx.get("inversion_args") or {}
        targets = _router_target_tokens(args.get("targets")) if isinstance(args, dict) else []
        exclude = _router_target_tokens(args.get("exclude")) if isinstance(args, dict) else []
        if not targets and not ctx.get(BATCH_COMPLETE_IDS_KEY):
            return None

        # ── confirmed re-entry: complete exactly what the user confirmed ──
        if ctx.get(CONFIRMED_CONTEXT_KEY) and ctx.get(BATCH_COMPLETE_IDS_KEY):
            ids = list(ctx.get(BATCH_COMPLETE_IDS_KEY) or [])
            texts = list(ctx.get(BATCH_COMPLETE_TEXTS_KEY) or [])
            left = list(ctx.get(BATCH_COMPLETE_LEFT_KEY) or [])
            done_texts: List[str] = []
            failed: List[Tuple[str, str]] = []
            for tid, text in zip(ids, texts):
                try:
                    ok = await self.todo_service.complete_todo(todo_id=UUID(tid), user_id=user_id)
                except Exception as e:  # silent-ok: counted + reported per item (CXO: the summary reports only what completed)
                    logger.warning("batch_complete_item_failed", todo_id=tid, error=str(e))
                    ok = None
                if ok:
                    done_texts.append(text)
                else:
                    failed.append((text, "no longer there"))
            logger.info(
                "Todo batch completed via router targets",
                completed=len(done_texts),
                failed=len(failed),
                left=len(left),
                user_id=user_id,
            )
            return _batch_summary(done_texts, failed, left), False

        # ── candidate sets: what names/"all" index, and what ordinals may index ──
        due = await self._due_reminder_todos(user_id)
        if due:
            name_pool, pool_kind = due, "due reminders"
        else:
            name_pool = await self.todo_service.list_todos(user_id=user_id, include_completed=False)
            pool_kind = "active to-dos"
        if not name_pool:
            return (f"You have no {pool_kind} to mark done.", False)
        numbered = self._recall_numbered_list(session_id, principal or user_id)
        ordinal_pool: List[Todo] = []
        ordinal_kind = pool_kind
        if numbered is not None:
            by_id = {t.id: t for t in name_pool}
            ordinal_pool = [by_id[i] for i in numbered.ids if i in by_id]
            ordinal_kind = numbered.kind

        picked, unresolved = resolve_router_targets(
            targets, name_pool, ordinal_candidates=ordinal_pool
        )
        excluded, unresolved_ex = (
            resolve_router_targets(exclude, name_pool, ordinal_candidates=ordinal_pool)
            if exclude
            else ([], [])
        )
        unresolved += unresolved_ex
        if unresolved:
            # CXO string 4: nothing changes; name the list actually searched;
            # show it numbered (which grounds the next ordinal), cap 10.
            listing_pool = (
                ordinal_pool
                if any(_is_positional(t) for t in unresolved) and ordinal_pool
                else name_pool
            )
            listing_kind = (
                ordinal_kind if listing_pool is ordinal_pool and ordinal_pool else pool_kind
            )
            first = unresolved[0]
            if _is_positional(first):
                n = re.sub(r"^#", "", first.strip())
                head = (
                    f"There's no number {n} in your {listing_kind}. You have {len(listing_pool)}:"
                )
            else:
                name = first[5:].strip() if first.lower().startswith("name:") else first
                head = f'I couldn\'t find "{name}" in your {listing_kind}. You have:'
            lines = [head] + [f"{i + 1}. {t.text}" for i, t in enumerate(listing_pool[:10])]
            if len(listing_pool) > 10:
                lines.append(f"…and {len(listing_pool) - 10} more.")
            if picked:
                # CXO 2026-10-06 (flaw 1): some targets DID resolve, but nothing holds
                # the rest of the ask — a one-item answer would complete ONE item and
                # silently drop the others. Promise only what the state holds (#1766).
                lines.append(
                    "Nothing has been changed. Say it again with the right name or number."
                )
            else:
                lines.append("Tell me which one, and I'll mark it done.")
            # CXO 2026-10-06 (flaw 2): "the numbered list last shown" is the rows ON
            # SCREEN — record only the capped slice, so ordinal 11 can never ground
            # against a row the user never saw.
            shown = listing_pool[:10]
            self._remember_numbered_list(
                session_id,
                principal or user_id,
                listing_kind,
                [t.id for t in shown],
                [t.text for t in shown],
            )
            return "\n".join(lines), False

        ex_ids = {t.id for t in excluded}
        picked = [t for t in picked if t.id not in ex_ids]
        if not picked:
            return ("Nothing matched after the exceptions. Nothing has been changed.", False)
        left = [t.text for t in name_pool if t.id not in {p.id for p in picked}]

        if len(picked) == 1 and not exclude:
            completed = await self.todo_service.complete_todo(
                todo_id=UUID(picked[0].id), user_id=user_id
            )
            if completed:
                logger.info(
                    "Todo completed via router target", todo_id=str(picked[0].id), user_id=user_id
                )
                return format_todo_completed_conscious(completed), False
            return ("I couldn't complete that todo. It might have been deleted.", False)

        # ── two or more, or a carve-out: the mutation boundary asks, enumerating ──
        question = _batch_confirm_question([t.text for t in picked], left)
        bound_ctx = {
            **ctx,
            BATCH_COMPLETE_IDS_KEY: [t.id for t in picked],
            BATCH_COMPLETE_TEXTS_KEY: [t.text for t in picked],
            BATCH_COMPLETE_LEFT_KEY: left,
        }
        bound = Intent(
            category=intent.category,
            action=intent.action,
            original_message=intent.original_message,
            confidence=intent.confidence,
            context=bound_ctx,
        )
        if offer_service is None or not session_id:
            # No way to bind the answer — never arm what nothing can pop.
            return (
                "I can mark several at once, but I need a session to confirm first. "
                "Try them one at a time: 'complete todo 1'.",
                False,
            )
        offer_service.set_pending_offer(
            session_id,
            {
                "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
                "question": question,
                "pending_action": {
                    "kind": "todo_batch_complete",
                    "action": "complete_todo",
                    "intent": bound,
                    "summary": f"complete {len(picked)} items",
                },
                # CXO: the existing Okay-family decline, not a fourth phrasing.
                "decline_message": "Okay — I won't mark those done. Nothing has been changed.",
            },
            user_id=principal,
        )
        logger.info(
            "Todo batch confirm armed via router targets",
            picked=len(picked),
            left=len(left),
            session_id=session_id,
        )
        return question, True

    async def handle_delete_todo_targets(
        self,
        intent: Intent,
        session_id: Optional[str],
        user_id: UUID,
        offer_service: Any,
        principal: Optional[str],
    ) -> Optional[Tuple[str, bool]]:
        """Clear-family build plan piece 1 (2026-10-07): act on ROUTER-named
        targets, mirroring ``handle_complete_todo_targets`` (#1943). Returns
        ``(message, question_armed)`` when this path owns the turn, or
        ``None`` when the router named no targets (the legacy
        ``handle_delete_todo`` / #1666 single-delete gate runs unchanged).

        Resolution is identical to complete_todo's: the SAME resolver
        (``resolve_router_targets``), the SAME ordinal scope rule (an
        ordinal/range binds ONLY against ``conversation_context.
        last_numbered_list`` — the list the user was last shown numbered),
        and the SAME unresolved reply, with "mark it done" swapped for
        "delete it" (CXO: "delete" in place of "mark done"; nothing else
        about the ask changes, and there is no separate verb question here —
        the verb is already "delete", unlike the clear-family resolver's
        own ambiguous-verb ask).

        DESTRUCTIVE departs from complete_todo in exactly one place: delete
        ALWAYS arms the enumerating #1190 confirm, even for a single
        resolved target with no carve-out (every consent cell for a
        DESTRUCTIVE effect is CONFIRM — Arch's ruling carried from #1666).
        The confirmed "yes" re-entry deletes EXACTLY the ids bound onto the
        carrier at ask time (``BATCH_DELETE_IDS_KEY``) — never a re-resolve
        of ``inversion_args`` — and reports only what actually deleted.
        """
        from services.intent_service.destructive_confirm import (
            CONFIRM_PENDING_ACTION_WORKFLOW,
            CONFIRMED_CONTEXT_KEY,
        )

        ctx = dict(intent.context or {})
        args = ctx.get("inversion_args") or {}
        targets = _router_target_tokens(args.get("targets")) if isinstance(args, dict) else []
        exclude = _router_target_tokens(args.get("exclude")) if isinstance(args, dict) else []
        if not targets and not ctx.get(BATCH_DELETE_IDS_KEY):
            return None

        # ── confirmed re-entry: delete exactly what the user confirmed ──
        if ctx.get(CONFIRMED_CONTEXT_KEY) and ctx.get(BATCH_DELETE_IDS_KEY):
            ids = list(ctx.get(BATCH_DELETE_IDS_KEY) or [])
            texts = list(ctx.get(BATCH_DELETE_TEXTS_KEY) or [])
            left = list(ctx.get(BATCH_DELETE_LEFT_KEY) or [])
            done_texts: List[str] = []
            failed: List[Tuple[str, str]] = []
            for tid, text in zip(ids, texts):
                try:
                    ok = await self.todo_service.delete_todo(todo_id=UUID(tid), user_id=user_id)
                except Exception as e:  # silent-ok: counted + reported per item (same shape as the complete batch path)
                    logger.warning("batch_delete_item_failed", todo_id=tid, error=str(e))
                    ok = None
                if ok:
                    done_texts.append(text)
                else:
                    failed.append((text, "already gone"))
            logger.info(
                "Todo batch deleted via router targets",
                deleted=len(done_texts),
                failed=len(failed),
                left=len(left),
                user_id=user_id,
            )
            return _delete_summary(done_texts, failed, left), False

        # ── candidate sets: what names/"all" index, and what ordinals may index ──
        due = await self._due_reminder_todos(user_id)
        if due:
            name_pool, pool_kind = due, "due reminders"
        else:
            name_pool = await self.todo_service.list_todos(user_id=user_id, include_completed=False)
            pool_kind = "active to-dos"
        if not name_pool:
            return (f"You have no {pool_kind} to delete.", False)
        numbered = self._recall_numbered_list(session_id, principal or user_id)
        ordinal_pool: List[Todo] = []
        ordinal_kind = pool_kind
        if numbered is not None:
            by_id = {t.id: t for t in name_pool}
            ordinal_pool = [by_id[i] for i in numbered.ids if i in by_id]
            ordinal_kind = numbered.kind

        picked, unresolved = resolve_router_targets(
            targets, name_pool, ordinal_candidates=ordinal_pool
        )
        excluded, unresolved_ex = (
            resolve_router_targets(exclude, name_pool, ordinal_candidates=ordinal_pool)
            if exclude
            else ([], [])
        )
        unresolved += unresolved_ex
        if unresolved:
            # Same unresolved reply as complete_todo's; nothing changes.
            listing_pool = (
                ordinal_pool
                if any(_is_positional(t) for t in unresolved) and ordinal_pool
                else name_pool
            )
            listing_kind = (
                ordinal_kind if listing_pool is ordinal_pool and ordinal_pool else pool_kind
            )
            first = unresolved[0]
            if _is_positional(first):
                n = re.sub(r"^#", "", first.strip())
                head = (
                    f"There's no number {n} in your {listing_kind}. You have {len(listing_pool)}:"
                )
            else:
                name = first[5:].strip() if first.lower().startswith("name:") else first
                head = f'I couldn\'t find "{name}" in your {listing_kind}. You have:'
            lines = [head] + [f"{i + 1}. {t.text}" for i, t in enumerate(listing_pool[:10])]
            if len(listing_pool) > 10:
                lines.append(f"…and {len(listing_pool) - 10} more.")
            if picked:
                lines.append(
                    "Nothing has been changed. Say it again with the right name or number."
                )
            else:
                # "delete" in place of "mark done" (CXO) — no separate verb
                # clause here, the verb is already "delete".
                lines.append("Tell me which one, and I'll delete it.")
            shown = listing_pool[:10]
            self._remember_numbered_list(
                session_id,
                principal or user_id,
                listing_kind,
                [t.id for t in shown],
                [t.text for t in shown],
            )
            return "\n".join(lines), False

        ex_ids = {t.id for t in excluded}
        picked = [t for t in picked if t.id not in ex_ids]
        if not picked:
            return ("Nothing matched after the exceptions. Nothing has been changed.", False)
        left = [t.text for t in name_pool if t.id not in {p.id for p in picked}]
        if len(picked) == 1 and not exclude:
            # CXO 2026-10-07 source review: the Leaving line names what a CARVE-OUT spared.
            # A single named target with no exclude is exactly D1 — it does not recite
            # the rest of the list (and the summary says nothing about the rest either).
            left = []

        # ── DESTRUCTIVE: always confirm, even a single resolved target ──
        question = _delete_confirm_question([t.text for t in picked], left)
        bound_ctx = {
            **ctx,
            BATCH_DELETE_IDS_KEY: [t.id for t in picked],
            BATCH_DELETE_TEXTS_KEY: [t.text for t in picked],
            BATCH_DELETE_LEFT_KEY: left,
        }
        bound = Intent(
            category=intent.category,
            action=intent.action,
            original_message=intent.original_message,
            confidence=intent.confidence,
            context=bound_ctx,
        )
        if offer_service is None or not session_id:
            # No way to bind the answer — never arm what nothing can pop.
            return (
                "I can delete several at once, but I need a session to confirm first. "
                "Try them one at a time: 'delete todo 1'.",
                False,
            )
        offer_service.set_pending_offer(
            session_id,
            {
                "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
                "question": question,
                "pending_action": {
                    "kind": "todo_batch_delete",
                    "action": "delete_todo",
                    "intent": bound,
                    "summary": f"delete {len(picked)} item(s)",
                },
                "decline_message": _delete_decline_message([t.text for t in picked]),
            },
            user_id=principal,
        )
        logger.info(
            "Todo batch delete confirm armed via router targets",
            picked=len(picked),
            left=len(left),
            session_id=session_id,
        )
        return question, True

    @staticmethod
    def _remember_numbered_list(
        session_id: Optional[str], user_id: Any, kind: str, ids: List[str], texts: List[str]
    ) -> None:
        """Record the NUMBERED list just rendered on the session context (1943).
        Best-effort: a context failure never breaks the reply."""
        if not session_id:
            return
        try:
            from services.intent_service.conversation_context import (
                NumberedList,
                get_or_create_context,
            )

            ctx = get_or_create_context(session_id, user_id=user_id)
            ctx.last_numbered_list = NumberedList(kind=kind, ids=list(ids), texts=list(texts))
        except (
            Exception
        ) as e:  # silent-ok: logged; ordinals then read as unresolved (honest ask), never a guess
            logger.warning("numbered_list_remember_failed", error=str(e), session_id=session_id)

    @staticmethod
    def _recall_numbered_list(session_id: Optional[str], user_id: Any):
        if not session_id:
            return None
        try:
            from services.intent_service.conversation_context import get_or_create_context

            return get_or_create_context(session_id, user_id=user_id).last_numbered_list
        except Exception as e:  # silent-ok: logged; treated as "no numbered list shown"
            logger.warning("numbered_list_recall_failed", error=str(e), session_id=session_id)
            return None

    async def _due_reminder_todos(self, user_id: UUID) -> List[Todo]:
        """The SAME filter ``get_due_reminders`` applies (reminder_date set,
        not completed, reminder_date <= now), but returning the full Todo
        rows in list order rather than just their text — so an ordinal
        answer turn ("the first one") can bind by POSITION against exactly
        the candidates the floor's "flagging N reminders" copy rendered
        (#1914), via the shared #1906 pick-target binder. Kept as its own
        small query rather than refactoring ``get_due_reminders`` to share
        it — that method's error-path logging (todo_count,
        reminders_considered) is a distinct, already-depended-on contract.
        A query failure here fails open to an empty list (never a crash):
        the caller falls back to fuzzy text matching or an honest clarify.
        """
        from datetime import datetime, timezone

        from services.utils.datetime_utils import ensure_utc

        try:
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)
        except Exception as e:  # silent-ok: logged; caller treats [] as "no candidate list" (#1914)
            logger.error(
                "Due reminder todo lookup failed", error=str(e), user_id=user_id, exc_info=True
            )
            return []
        now = datetime.now(timezone.utc)
        due: List[Todo] = []
        for todo in todos:
            reminder_date = getattr(todo, "reminder_date", None)
            if reminder_date is None or todo.completed:
                continue
            if ensure_utc(reminder_date) <= now:
                due.append(todo)
        return due

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, create todo with database persistence, format response.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")

        text = self._extract_todo_text(original_message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        # Parse optional priority
        priority = self._extract_priority(original_message)

        try:
            # Create todo via service (database persistence)
            todo = await self.todo_service.create_todo(
                user_id=user_id, text=text, priority=priority
            )

            logger.info(
                "Todo created successfully",
                todo_id=str(todo.id),
                text=text,
                priority=priority,
                user_id=user_id,
            )

            # Format response with consciousness
            return format_todo_created_conscious(todo)

        except ValueError as e:
            logger.warning("Todo creation validation failed", error=str(e), user_id=user_id)
            return f"I had trouble with that: {str(e)}"

        # #1423: narrowed from `except Exception` — expected failures here are DB-layer
        # (unreachable/timeout/constraint), which SQLAlchemyError covers. Anything else
        # (a formatting bug, an attribute error) is a CODE bug and now propagates to the
        # route's degradation boundary instead of masquerading as "a temporary issue".
        except (SQLAlchemyError, OSError) as e:
            logger.error("Todo creation failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble saving that todo — it may be a temporary issue. You can try again, or rephrase with 'add todo: [your task]'."

    def _arm_time_question(
        self,
        intent_service,
        session_id: str,
        user_id,
        task_text: str,
        question: Optional[str] = None,
    ) -> None:
        """#1648: arm the reminder time-clarify carrier beside the honest
        ask, so the answer turn binds at the offer seam instead of orphaning
        into the routing chain (where the floor roleplayed the save live).
        Best-effort: a store failure is logged and the ask still goes out —
        the copy never claims anything was armed. ``question`` (#1665): the
        rendered ask the caller is about to return, stored on the record."""
        if intent_service is None or not session_id:
            return
        try:
            intent_service.workflow_offer_service.set_pending_offer(
                session_id,
                build_reminder_time_offer(task_text, user_id, question=question),
                user_id=str(user_id) if user_id else None,
            )
        except Exception as e:  # silent-ok: #1648 — arming is additive; the honest ask must go out regardless; logged ERROR
            logger.error(
                "reminder_time_question_arm_failed",
                error=str(e),
                session_id=session_id,
            )

    def _arm_task_question(
        self,
        intent_service,
        session_id: str,
        user_id,
        original_message: str,
        question: Optional[str] = None,
    ) -> None:
        """#1654: arm the reminder task-clarify carrier beside the honest
        no-task ask (the #1648 shape, one question earlier), so the answer
        turn binds at the offer seam instead of orphaning into the routing
        chain. Best-effort: a store failure is logged and the ask still goes
        out — the copy never claims anything was armed. ``question``
        (#1665): the rendered ask the caller is about to return, stored on
        the record."""
        if intent_service is None or not session_id:
            return
        try:
            intent_service.workflow_offer_service.set_pending_offer(
                session_id,
                build_reminder_task_offer(original_message, user_id, question=question),
                user_id=str(user_id) if user_id else None,
            )
        except Exception as e:  # silent-ok: #1654 — arming is additive; the honest ask must go out regardless; logged ERROR
            logger.error(
                "reminder_task_question_arm_failed",
                error=str(e),
                session_id=session_id,
            )

    async def handle_create_reminder(
        self,
        intent: Intent,
        session_id: str,
        user_id: UUID,
        intent_service=None,
    ) -> str:
        """
        Issue #903: Handle "remind me to X" — creates a time-annotated todo.

        Extracts the reminder text and time from the message, creates a todo
        with reminder_date set, and confirms with the parsed time.

        #1648: ``intent_service`` (optional, back-compat default None) lets
        the time-clarify asks arm the ``reminder_time_question`` carrier so
        the answer turn binds at the offer seam. Callers without it still
        get the honest ask — just without the binding.
        """
        from services.intent_service.temporal_utils import (
            PAST_TODAY_PREFIX,
            parse_reminder_time,
        )

        original_message = intent.original_message or intent.context.get("original_message", "")

        # Extract reminder text (strip "remind me to/about", "set a reminder to", etc.)
        text = self._extract_reminder_text(original_message)
        if not text:
            # #1654: the no-task clarify is #1648's class one question
            # earlier — it must ARM the task-question carrier so the answer
            # (a bare task phrase) binds at the offer seam, never orphans
            # into the routing chain (PM hit this twice on 08-18 via the
            # colon-form parse misses; the parse miss itself stays #1606).
            # #1665: rendered ONCE, stored on the armed record, returned.
            ask = (
                "I didn't catch what you'd like to be reminded about. "
                "Tell me the task (for example: 'review the beta notes'), "
                "or give me the whole thing — 'remind me to check in with "
                "the team in 2 hours'."
            )
            self._arm_task_question(
                intent_service,
                session_id,
                user_id,
                original_message,
                question=ask,
            )
            return ask

        # Parse time from message — on the USER'S clock when a tz is stored
        # (#1572; captured at login from the browser). None → the pre-#1572
        # server anchor, unchanged.
        from services.utils.user_timezone import get_user_timezone

        user_tz = await get_user_timezone(user_id)
        reminder_dt, time_label = parse_reminder_time(original_message, user_timezone=user_tz)

        # Issue #1490 invariant: parse_reminder_time returns None ONLY when
        # the message carried an explicit clock time it couldn't bind (e.g.
        # "at 25:99"). Never save with a silently-guessed default — echo the
        # unparsed time honestly and ask.
        # (RESTORED 2026-08-08: reverted by the arch-seat merge-drop incident,
        # d99b3d068/d5ae5484f — second casualty after the audit doc.)
        if reminder_dt is None:
            # #1648: BOTH honest asks arm the time-question carrier — the
            # answer turn ("at 3pm") must bind at the offer seam, never
            # orphan into the routing chain. #1665: the ask is rendered
            # ONCE, stored on the armed record, and returned — never two
            # renders that could drift.
            # #1562: explicit "today" + a clock time that has already passed
            # on the server clock — honest ask, never a silent roll to
            # tomorrow. (The server's clock is not the user's until
            # #1535/#747 lands, so this can fire while the time is still in
            # the user's future; the ask keeps the user in control either way.)
            if time_label.startswith(PAST_TODAY_PREFIX):
                passed_time = time_label[len(PAST_TODAY_PREFIX) :]
                ask = (
                    f"Did you mean tomorrow? "
                    f"Say 'remind me at {passed_time} tomorrow' — or give me "
                    f"another time — and I'll set it."
                )
                self._arm_time_question(intent_service, session_id, user_id, text, question=ask)
                return (
                    f"I caught the task — **{text}** — but {passed_time} today "
                    f"has already passed on my clock. {ask}"
                )
            ask = _TIME_ASK  # #1665: one render, shared with the #1654 chain
            self._arm_time_question(intent_service, session_id, user_id, text, question=ask)
            return (
                f"I caught the task — **{text}** — but couldn't work out "
                f'the time from "{time_label}". {ask}'
            )

        try:
            todo = await self.todo_service.create_todo(
                user_id=user_id,
                text=text,
                priority="medium",
                reminder_date=reminder_dt,
                due_date=reminder_dt,
            )

            logger.info(
                "Reminder created",
                todo_id=str(todo.id),
                text=text,
                reminder_date=str(reminder_dt),
                time_label=time_label,
                user_id=user_id,
            )

            # Format confirmation with time (#1648: factored to module level
            # so the time-answer seam shares the ONE real save confirmation —
            # per-line rationale comments live on _reminder_saved_message).
            return _reminder_saved_message(text, reminder_dt, time_label, user_tz=user_tz)

        except Exception as e:
            logger.error(
                "Reminder creation failed",
                error=str(e),
                user_id=user_id,
                exc_info=True,
            )
            return (
                "I had trouble saving that reminder. "
                "You can try again, or use 'add todo: [your task]' as a fallback."
            )

    # Issue #1490: time expressions a reminder message may carry, shared by the
    # time-first patterns (skip them to find the task) and the trailing strip
    # (remove them from the saved todo text). Mirrors what parse_reminder_time
    # in temporal_utils can actually parse.
    _TIME_EXPR = (
        r"(?:tomorrow(?:\s+(?:morning|afternoon|evening))?|tonight|"
        r"this\s+(?:morning|afternoon|evening)|"
        r"next\s+week|"
        r"(?:next|on)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
        # Issue #1542: duration numbers are digit OR word form ("in two
        # hours", "in an hour"). DURATION_NUMBER_SRC is imported from
        # temporal_utils (non-capturing) so this stays mirrored with what
        # find_explicit_duration can actually bind.
        rf"in\s+{DURATION_NUMBER_SRC}\s+(?:minutes?|mins?|hours?|hrs?|days?)|"
        # Issue #1490 (inverted-order reopen): "at" forms now cover
        # noon/midnight and an optional TRAILING "today" ("at 9:41 today"),
        # plus bare "3pm"/"9:41am" and bare noon/midnight — mirroring what
        # find_explicit_clock_time can bind. (RESTORED 2026-08-08, merge-drop.)
        r"(?:today\s+)?at\s+(?:\d{1,2}(?::\d{2})?\s*(?:am|pm)?|noon|midnight)(?:\s+today)?|"
        r"\d{1,2}(?::\d{2})?\s*(?:am|pm)|"
        r"noon|midnight)"
    )

    def _extract_reminder_text(self, message: str) -> Optional[str]:
        """
        Issue #903: Extract the actionable text from a reminder request.

        Strips command phrases like "remind me to", "set a reminder to", etc.

        Issue #1490: also handles [time-first, task-after-'to'] ordering
        ("remind me tomorrow at 3pm to review the PR"), trailing punctuation,
        and compound trailing time expressions ("tomorrow at 3pm").
        """
        import re

        time_expr = self._TIME_EXPR

        # Order matters — try most specific patterns first.
        # Time-first variants (Issue #1490) precede the generic forms: the
        # generic forms can't match them ('to|about' must directly follow the
        # command phrase), and the time-first forms can't match task-first
        # messages (a time expression must directly follow the command phrase),
        # so neither shadows the other.
        patterns = [
            rf"(?:please\s+)?remind\s+me\s+(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            rf"(?:please\s+)?set\s+(?:a\s+)?reminder\s+(?:for\s+)?(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            rf"(?:please\s+)?create\s+(?:a\s+)?reminder\s+(?:for\s+)?(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            r"(?:please\s+)?remind\s+me\s+(?:to|about)\s+(.+)",
            r"(?:please\s+)?set\s+(?:a\s+)?reminder\s+(?:to|for|about)\s+(.+)",
            r"(?:please\s+)?create\s+(?:a\s+)?reminder\s+(?:to|for|about)\s+(.+)",
            r"don'?t\s+let\s+me\s+forget\s+(?:to\s+)?(.+)",
            r"(?:i\s+)?need\s+to\s+remember\s+to\s+(.+)",
        ]

        message_lower = message.lower().strip()
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                # Strip trailing punctuation and time expressions so the todo
                # text is clean (#1490; shared with the #1654 task-answer
                # seam via the module-level helper).
                text = _strip_trailing_time_expressions(match.group(1).strip())
                # #1679: "set a reminder for tomorrow at 3pm" matches the
                # generic 'for'-form with group(1)="tomorrow at 3pm"; the
                # trailing strip sheds "at 3pm" but a LEADING time word has no
                # preceding whitespace to anchor on, leaving the residue
                # "tomorrow" — which then saved as a reminder literally titled
                # "tomorrow". A pure-time residue is NO task: return None so
                # the #1654 task-clarify carrier asks, instead of saving a
                # time expression as the thing to be reminded of.
                if text and not _is_pure_time_expression(text):
                    return text

        return None

    async def handle_list_reminders(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """
        Issue #1521: Handle "what reminders do I have?" — list the STORED
        reminders instead of misrouting to the temporal/calendar answer.

        Reads this user's active todos (owner-scoped via user_id, the #1493
        discipline) and reports the ones carrying a reminder_date, split into
        due-now/overdue vs upcoming. Both sides of the due-ness comparison are
        normalized aware-UTC per the #1491/#1429 guard shape (naive rows from
        tz-dropping backends are assumed UTC via ensure_utc, never TypeError).
        """
        from datetime import datetime, timezone

        from services.utils.datetime_utils import ensure_utc

        try:
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            reminders = [
                todo
                for todo in todos
                if getattr(todo, "reminder_date", None) is not None and not todo.completed
            ]

            logger.info(
                "Reminder list retrieved",
                user_id=user_id,
                todo_count=len(todos),
                reminder_count=len(reminders),
            )

            if not reminders:
                # Pattern-073 discipline: describe what was actually queried
                # (saved reminders), not a categorical "nothing scheduled".
                return (
                    "I checked your saved reminders and there are none right now. "
                    "You can set one with 'remind me to [task] tomorrow at 9am'."
                )

            now = datetime.now(timezone.utc)
            due: List[tuple] = []
            upcoming: List[tuple] = []
            for todo in reminders:
                when = ensure_utc(todo.reminder_date)
                (due if when <= now else upcoming).append((when, todo))
            due.sort(key=lambda pair: pair[0])
            upcoming.sort(key=lambda pair: pair[0])

            # #1572: render each line on the user's clock when a tz is
            # stored ("4:00 PM PDT"), else the labeled-UTC face unchanged
            # (#1521's honest label). Due-ness math above stays UTC.
            from services.utils.user_timezone import get_user_timezone

            user_tz = await get_user_timezone(user_id)

            # 1943 (CXO's rule, 2026-10-06): the list is NUMBERED, due first,
            # and exactly what was shown is recorded on the session so an
            # ordinal ("the first three", "#2") can resolve against it — and
            # against nothing else.
            ordered = list(due) + list(upcoming)
            numbers = {todo.id: i + 1 for i, (_when, todo) in enumerate(ordered)}

            def _line(when, todo) -> str:
                return (
                    f"{numbers[todo.id]}. **{todo.text}** — {_format_reminder_when(when, user_tz)}"
                )

            count = len(reminders)
            parts = [f"You have {count} reminder{'s' if count != 1 else ''} saved:"]
            # The blank line after each header is load-bearing (CXO's render check,
            # 10-06): under CommonMark an ordered list may interrupt a paragraph only
            # when it starts at 1, so "📅 Upcoming:" followed directly by "3. …" rendered
            # as one run-on paragraph. With the blank line, marked emits <ol start="3">
            # and the screen shows the same numbers the handler remembers.
            if due:
                parts.append("\n⏰ Due now:\n")
                parts.extend(_line(when, todo) for when, todo in due)
            if upcoming:
                parts.append("\n📅 Upcoming:\n")
                parts.extend(_line(when, todo) for when, todo in upcoming)
            self._remember_numbered_list(
                session_id,
                user_id,
                "reminders",
                [todo.id for _w, todo in ordered],
                [todo.text for _w, todo in ordered],
            )
            return "\n".join(parts)

        except Exception as e:  # silent-ok: logged at error w/ exc_info; user gets honest trouble-loading copy, never a false "no reminders" (#1425)
            logger.error(
                "Reminder list retrieval failed", error=str(e), user_id=user_id, exc_info=True
            )
            # #1425 discipline: a source failure must read as trouble-loading,
            # never as "no reminders".
            return (
                "I had trouble loading your reminders right now. "
                "You can try 'what reminders do I have?' again in a moment."
            )

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "show my todos" or "list todos" - shows active todos from database.

        Issue #904: Now supports "show all my todos" to include completed items.
        """
        try:
            original_message = intent.original_message or intent.context.get("original_message", "")
            include_completed = self._wants_completed_todos(original_message)

            # Get todos from database
            todos = await self.todo_service.list_todos(
                user_id=user_id, include_completed=include_completed
            )

            logger.info(
                "Todo list retrieved",
                user_id=user_id,
                count=len(todos),
                include_completed=include_completed,
            )

            # Format with consciousness
            return format_todo_list_conscious(todos, include_completed=include_completed)

        # #1423: narrowed from `except Exception` — expected failures are DB-layer
        # (unreachable/timeout), covered by SQLAlchemyError. Code bugs (e.g. in the
        # conscious formatter) now propagate to the route's degradation boundary
        # instead of vanishing into "try again in a moment".
        except (SQLAlchemyError, OSError) as e:
            logger.error("Todo list retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble loading your todos right now. You can try 'show my todos' again in a moment, or add a new one with 'add todo: [task]'."

    async def handle_next_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "what's my next todo?" or "next task" - shows highest priority todo."""
        try:
            # Get active todos from database (already sorted by priority)
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            logger.info("Next todo retrieved", user_id=user_id, has_todos=len(todos) > 0)

            if not todos:
                # Issue #1096 slice 3 (Pattern-073 discipline): describe what
                # was actually queried ("active todos") rather than the
                # categorical "nothing pending" (which would imply "nothing
                # pending in your life").
                return (
                    "I checked your active todos and there are none. "
                    "If something comes to mind, just say 'add todo: [task]'."
                )

            # Get the first todo (highest priority due to sorting in repository)
            next_todo = todos[0]

            # Format with consciousness
            return format_next_todo_conscious(next_todo, len(todos))

        except Exception as e:
            logger.error("Next todo retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble finding your next todo right now. You can try 'show my todos' to see your full list, or ask again in a moment."

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "mark todo 1 as complete" or "complete the PR review todo"

        Issue #904: Supports both number-based and fuzzy text-based matching.
        Number path: "mark todo 3 as complete" → completes todo #3 by position.
        Text path: "complete the PR review" → fuzzy matches against todo texts.

        Issue #1914: the message is first split at an unquoted clause
        boundary ("...and leave the second one pending") — the trailing
        clause is an explicit no-op, acknowledged in the reply but never
        acted on and never folded into the completion target. When the
        surviving target is ordinal/positional ("the first one", "#2"),
        it's bound by POSITION against the due-reminder candidates (the
        same source the floor's "flagging N reminders" copy renders from)
        via the shared #1906 pick-target binder, before falling back to
        fuzzy text matching.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")
        primary_message, noop_tail = _split_completion_clause(original_message)

        def _reply(message: str) -> str:
            # #1914: acknowledge a trailing no-op clause once, on every
            # return path — never silently dropped, never acted on.
            if noop_tail:
                return f"{message} Left the other one as is."
            return message

        try:
            # Get user's todo list
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            if not todos:
                return _reply(
                    "You don't have any active todos to complete. "
                    "Add one with 'add todo: [task]' first."
                )

            # Path 1: Try number-based matching first
            todo_number = self._extract_todo_id(primary_message)
            if todo_number is not None:
                try:
                    idx = int(todo_number) - 1
                    if idx < 0 or idx >= len(todos):
                        return _reply(
                            f"I couldn't find todo #{todo_number}. "
                            f"You have {len(todos)} active todos."
                        )
                    todo = todos[idx]
                except ValueError:
                    return _reply(
                        f"'{todo_number}' doesn't look like a number. "
                        "Try: 'mark todo 1 as complete'"
                    )
            else:
                # Path 2: Fuzzy text matching (Issue #904)
                completion_text = self._extract_completion_text(primary_message)
                if not completion_text:
                    return _reply(
                        "Which todo would you like to complete? "
                        "Try 'complete todo 1' or 'complete the [description]'."
                    )

                # #1914: an ordinal/positional target ("the first one",
                # "the last one", "#2") binds by POSITION against the
                # due-reminder candidates — the list the floor just
                # rendered — rather than fuzzy-matching "first one" against
                # each item's text (which can never score). Reuses the #1906
                # binder verbatim; never reimplemented.
                todo = None
                due_candidates: List[Todo] = []
                if _ORDINAL_SHAPE_RE.search(completion_text):
                    due_candidates = await self._due_reminder_todos(user_id)
                    if due_candidates:
                        from services.intent_service.reminder_clear import (
                            _resolve_pick_target,
                        )

                        texts = [t.text for t in due_candidates]
                        due_iso = [_reminder_due_iso(t) for t in due_candidates]
                        status, pick_idx = _resolve_pick_target(completion_text, texts, due_iso)
                        if status == "bound" and pick_idx is not None:
                            todo = due_candidates[pick_idx]

                # #1930 (CXO's 2026-10-04 ruling §1): an ambiguous text
                # target (more than one plausible match) asks WHICH one —
                # disambiguation, separate from the #1190 consent gate.
                # Reuses the SAME resolver the delete gate already asks
                # with (resolve_named_todo_target, destructive_confirm.py's
                # named-target leg) rather than building a new picker; a
                # unique exact-word-set match still collapses to one
                # (resolve_named_todo_target's own contract), so this is
                # behaviour-preserving for every single-match case the old
                # `_find_best_matching_todo` call already handled.
                if todo is None:
                    matches = resolve_named_todo_target(completion_text, todos)
                    if len(matches) > 1:
                        position_by_id = {t.id: i + 1 for i, t in enumerate(todos)}
                        candidates = ", ".join(
                            f'{position_by_id[t.id]}. "{t.text}"' for t in matches
                        )
                        return _reply(
                            f"I found {len(matches)} todos matching "
                            f"'{completion_text}': {candidates}. Which one "
                            "should I complete? Try 'complete todo [number]'."
                        )
                    todo = matches[0] if matches else None

                if todo is None:
                    if _ORDINAL_SHAPE_RE.search(completion_text) and not due_candidates:
                        # No candidate list to count against — point the
                        # copy at the ordinal form that actually works
                        # (#1914), instead of a generic "didn't find".
                        return _reply(
                            f"I couldn't find a todo matching '{completion_text}' — "
                            "I don't have a list to count against right now. "
                            "Try 'show my todos' to see the numbers, then "
                            "'complete todo 1'."
                        )
                    return _reply(
                        f"I couldn't find a todo matching '{completion_text}'. "
                        "Try 'show my todos' to see your list, then "
                        "'complete todo [number]'."
                    )

            if todo is None:  # every branch above returned or bound; this narrows the type (1947)
                return _reply(
                    "I couldn't work out which todo you meant. Try 'show my todos' first."
                )

            # Mark as complete
            # #1436: domain Todo.id is a str(uuid4); the service is typed UUID.
            # Same value either way — this makes the contract explicit.
            completed_todo = await self.todo_service.complete_todo(
                todo_id=UUID(todo.id), user_id=user_id
            )

            if completed_todo:
                logger.info("Todo completed", todo_id=str(todo.id), user_id=user_id)
                return _reply(format_todo_completed_conscious(completed_todo))
            else:
                return _reply("I couldn't complete that todo. It might have been deleted.")

        except Exception as e:
            logger.error("Todo completion failed", error=str(e), user_id=user_id, exc_info=True)
            return _reply(
                "I had trouble marking that as complete. You can try again with "
                "'complete todo [number]', or say 'show my todos' to check the list first."
            )

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        # #1666: a rail-confirmed delete carries the todo resolved AT ASK TIME
        # (destructive_confirm.build_todo_delete_confirmation stashed it before
        # the #1190 gate asked 'Delete todo N: "text"?'). Delete exactly what
        # the user confirmed — never a positional re-resolve of "todo N"
        # against a list that may have shifted between the ask and the yes.
        # Honored ONLY together with the confirmed marker: an unconfirmed
        # intent never carries a usable binding.
        from services.intent_service.destructive_confirm import (
            CONFIRMED_CONTEXT_KEY,
            RESOLVED_TODO_CONTEXT_KEY,
        )

        _ctx = intent.context or {}
        _resolved = _ctx.get(RESOLVED_TODO_CONTEXT_KEY)
        if _resolved and _ctx.get(CONFIRMED_CONTEXT_KEY):
            try:
                deleted = await self.todo_service.delete_todo(
                    todo_id=UUID(_resolved["todo_id"]), user_id=user_id
                )
            except Exception as e:  # silent-ok: error-logged with exc_info; user gets honest failure copy, no silent default (#1666 gate path)
                logger.error("Todo deletion failed", error=str(e), user_id=user_id, exc_info=True)
                return "I had trouble removing that todo. You can try again with 'delete todo [number]', or say 'show my todos' to verify the list."
            if deleted:
                logger.info("Todo deleted", todo_id=str(_resolved["todo_id"]), user_id=user_id)
                return format_todo_deleted_conscious(_resolved["text"])
            return "I couldn't delete that todo. It might have already been removed."

        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")
        todo_number = self._extract_todo_id(original_message)
        if not todo_number:
            return "Which todo should I remove? Try: 'delete todo [number]'"

        try:
            # Get user's todo list to find the todo by position
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            # Convert todo number to index
            try:
                idx = int(todo_number) - 1
                if idx < 0 or idx >= len(todos):
                    return (
                        f"I couldn't find todo #{todo_number}. You have {len(todos)} active todos."
                    )
            except ValueError:
                return f"'{todo_number}' doesn't look like a number. Try: 'delete todo 1'"

            # Get the todo at that position
            todo = todos[idx]
            todo_text = todo.text

            # Delete the todo
            # #1436: same str(uuid4) → UUID contract fix as complete_todo above.
            deleted = await self.todo_service.delete_todo(todo_id=UUID(todo.id), user_id=user_id)

            if deleted:
                logger.info("Todo deleted", todo_id=str(todo.id), user_id=user_id)
                return format_todo_deleted_conscious(todo_text)
            else:
                return "I couldn't delete that todo. It might have already been removed."

        except Exception as e:
            logger.error("Todo deletion failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble removing that todo. You can try again with 'delete todo [number]', or say 'show my todos' to verify the list."

    # #1693: the create-todo command TOKEN — 'todo', 'to-do', or 'to do'.
    # Accepted in the command position ONLY (the pattern lead-in), never by
    # normalizing the whole message: a pre-extraction rewrite of 'to do' →
    # 'todo' would corrupt captured task text ("add todo: remember to do
    # laundry" must save "remember to do laundry", not "remember todo
    # laundry").
    _TODO_TOKEN = r"to[-\s]?do"
    # #1693: separator between the token and the task text — colon
    # (existing), dash/en-dash/em-dash ('new todo - water the plants'), or
    # plain whitespace ('add todo buy oat milk', unchanged).
    _TODO_SEP = r"(?:\s*[:\-–—]\s*|\s+)"

    def _extract_todo_text(self, message: str) -> str:
        """Extract todo text from 'add todo: TEXT' pattern.

        Issue #940 UAT Finding 5: Accept natural phrasing with articles
        ('Add a todo:', 'create a new todo:') not just rigid 'add todo:'.

        Issue #1693 (PM live 8/29, v64): the routing delivered these to this
        handler and the EXTRACTION dropped them — 'new todo - water the
        plants' (dash separator, 'new' lead-in), 'add to-do: water the
        plants' (the teach-copy's own suggested form plus a hyphen — teach-
        then-deny in miniature), 'one more to-do - water the plants'. Fix is
        extraction-only: hyphenated/spaced token + dash separators + the
        new/another/one-more lead-ins. Task text is captured verbatim.
        """
        token, sep = self._TODO_TOKEN, self._TODO_SEP
        patterns = [
            # "add/create [a] [new|one more] todo: TEXT" (#940 + #1693)
            rf"(?:add|create)\s+(?:a\s+)?(?:new\s+|one\s+more\s+)?{token}{sep}(.+)",
            # "new todo - TEXT" / "another todo: TEXT" / "one more to-do - TEXT" (#1693)
            rf"(?:new|another|one\s+more)\s+{token}{sep}(.+)",
            # "todo: TEXT" at start of message
            rf"^{token}{sep}(.+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_priority(self, message: str) -> str:
        """Extract priority from message (low, medium, high, urgent).

        Whole-word matching (#1758): the bare substring checks fired on task
        text that merely contains the letters — 'highlight', 'thigh', 'below',
        'follow'. A bare word still sets priority when it stands alone
        ('this is high importance' → high); telling that apart from a content
        word ('buy a high chair') needs a marker vocabulary this extractor
        doesn't have — a known gap, pinned as such in the #1758 tests.
        """
        words = {w.strip(string.punctuation) for w in message.lower().split()}

        if "urgent" in words:
            return "urgent"
        elif "high" in words:
            return "high"
        elif "low" in words:
            return "low"
        else:
            return "medium"

    def _extract_todo_id(self, message: str) -> Optional[str]:
        """Extract todo ID from message (by number)."""
        # Try "todo N" or "todo #N" pattern
        match = re.search(r"todo\s+#?(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        # Try just a number after "mark" or "complete" or "delete"
        match = re.search(r"(?:mark|complete|delete|remove)\s+(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    # ------------------------------------------------------------------
    # Issue #904: Fuzzy text matching for todo completion
    # ------------------------------------------------------------------

    def _extract_completion_text(self, message: str) -> Optional[str]:
        """Extract the descriptive text from a completion request.

        Extracts the part of the message that describes which todo to complete.
        Returns None if the message uses a number (handled by _extract_todo_id).

        Examples:
            "complete the PR review todo" → "PR review"
            "finish the deployment task" → "deployment"
            "mark todo 3 as complete" → None (number-based)
        """
        # If a number is present, defer to number-based path
        if self._extract_todo_id(message) is not None:
            return None

        # Try various completion patterns and extract the descriptive part
        patterns = [
            # "complete todo X" (strip "todo" prefix from descriptive text)
            r"(?:complete|finish)\s+todo\s+(.+?)(?:\s*$)",
            # "complete the X todo/task"
            r"(?:complete|finish|done with)\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "mark the X as done/complete"
            r"mark\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(?:done|complete|finished)",
            # "mark done: X" or "mark done the X"
            r"mark\s+done:?\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "I'm done with X"
            r"(?:i'?m\s+)?done\s+with\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                # Clean up trailing noise
                text = re.sub(r"\s+(todo|task|item|thing)$", "", text, flags=re.IGNORECASE)
                if text:
                    return text

        return None

    def _find_best_matching_todo(self, search_text: str, todos: List[Todo]) -> Optional[Todo]:
        """Find the todo that best matches the search text using fuzzy word overlap.

        Returns the best matching todo if score >= threshold, else None.
        Delegates to the shared module-level matcher (see the "shared title
        matcher" block above) — the same mechanism the named-target delete
        gate resolves against.
        """
        scored = match_todos_by_text(search_text, todos)
        return scored[0][1] if scored else None

    # Shared with the named-target delete gate — one matcher, both callers
    # (see the module-level "shared title matcher" block).
    _fuzzy_match_score = staticmethod(fuzzy_todo_match_score)

    @staticmethod
    def _wants_completed_todos(message: str) -> bool:
        """Check if the user wants to see completed todos too.

        Issue #904: "show all my todos" or "show completed todos" includes done items.
        """
        message_lower = message.lower()
        return any(
            phrase in message_lower
            for phrase in [
                "all my todos",
                "all todos",
                "completed todos",
                "done todos",
                "finished todos",
                "including completed",
                "include completed",
                "show everything",
            ]
        )


# --- #1648: the reminder time-question turn handler -------------------------


# #1665: the re-ask turns' open question — one constant, embedded in the
# re-ask reply AND stored on the re-armed record (same string, no drift).
_TIME_REASK_TAIL = (
    "Tell me when (for example: 'at 3pm tomorrow' or 'in 2 hours'), " "or say 'no' to drop it."
)


def _rearm_time_question(intent_service, session_id, user_id, pending_offer) -> bool:
    """Re-arm the SAME offer (the pop already consumed it; a re-ask turn must
    re-store it or the next answer has nothing to bind to). Returns False on
    a store failure so the copy never claims a binding that isn't there.
    #1665: the re-armed record's open question becomes the re-ask tail every
    re-ask turn renders (set BEFORE the store — what's stored is what's said)."""
    try:
        pending_offer["question"] = _TIME_REASK_TAIL
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
        return True
    except Exception as e:  # silent-ok: #1648 — a store failure must not crash the turn; logged ERROR, and callers keep the user-facing copy honest
        logger.error("reminder_time_question_rearm_failed", error=str(e))
        return False


def _time_reask(
    task_text: str,
    detail: str,
    rearmed: bool,
) -> dict:
    """The honest re-ask shape: nothing saved, here's why, here's what works."""
    if rearmed:
        tail = _TIME_REASK_TAIL
    else:
        tail = (
            "I couldn't keep the reminder bound either — ask me again "
            "('remind me to … at …') and I'll set it fresh."
        )
    return {
        "message": (f"Nothing has been saved yet for **{task_text}** — {detail} {tail}"),
        "intent_data": {
            "category": "execution",
            "action": "create_reminder",
            "reminder_time_question_pending": rearmed,
            "reminder_time_reasked": True,
        },
        "requires_clarification": True,
    }


async def handle_reminder_time_turn(
    pending_offer: dict,
    message: str,
    *,
    session_id: str,
    user_id,
    intent_service,
) -> Optional[dict]:
    """#1648 — kind-specific turn handling for a pending reminder time
    question, run at the offer seam BEFORE any classification surface (the
    #1605/#1571 sanctioned handler-internal seam; the pop already happened).

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` falls through to the generic offer flow
    (declines and bare exits drop honestly via ``decline_message``; full
    reminder restatements and unrelated commands abandon via the pop and
    route normally — the pre-classifier claims restatements
    deterministically, so the full handler re-extracts task AND time).

    The save path is the REAL one: a row write via TodoManagementService,
    confirmed with the same 📅 copy the primary path composes — never an
    improvised confirmation (the floor roleplayed exactly that, live).

    #1654 (#1739 acceptance-contract adoption, epic 3 — 2026-09-12): the
    seam consults THE predicate (``acceptance.evaluate_acceptance``) at its
    REGISTRY-DECLARED axes with the arm-site's stored ask threaded (#1665),
    replacing the legacy ``detect_offer_response``. See the in-body comments
    for the tier judgment and the stated arm-survival form.
    """
    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )
    from services.intent_service.destructive_confirm import detect_bare_exit
    from services.intent_service.drafted_issue import is_command_shaped
    from services.intent_service.temporal_utils import (
        PAST_TODAY_PREFIX,
        parse_reminder_time,
    )

    payload = pending_offer.get("pending_action") or {}
    task_text = (payload.get("task_text") or "").strip()
    text = (message or "").strip()
    if not task_text or not text:
        if not task_text:
            logger.error("reminder_time_question_missing_task", session_id=session_id)
        return None

    # Principal binding (the #1605 discipline): the offer belongs to the user
    # who asked — a different principal's turn must not save under it.
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(user_id) != str(offer_user):
        logger.warning(
            "reminder_time_question_principal_mismatch",
            offer_user=offer_user,
            turn_user=str(user_id),
        )
        return {
            "message": "Let's hold off on that — nothing has been saved.",
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "principal_mismatch": True,
            },
        }

    if detect_bare_exit(text):
        return None  # generic flow → honest decline via decline_message

    # ── #1654 (#1739 adoption). AXES, MAPPED EXPLICITLY: the ARMED workflow
    #    (clarify_reminder_time) is registry-declared READ×PRIVATE →
    #    LOW_CEREMONY — the seam itself writes nothing off a verdict; the
    #    REAL save below runs only off an ANSWER turn that names a time.
    #    Zero-widening: the LOW-tier accept vocabulary is the legacy
    #    detect_offer_response rows plus only the crisp CONFIRM superset,
    #    and ACCEPT at this seam only ever re-asks (never fires), so the
    #    accept surface loosens nothing (#1652's argument, verbatim).
    _axes = declared_axes_for_workflow(CLARIFY_REMINDER_TIME_WORKFLOW)
    verdict = evaluate_acceptance(
        text,
        effect=_axes[0] if _axes else None,
        outwardness=_axes[1] if _axes else None,
        armed_question=pending_offer.get("question"),  # #1665: from the record
    )
    if verdict is AcceptanceVerdict.DECLINE:
        return None  # generic flow → honest decline via decline_message

    if _REMINDER_RESTATEMENT_RE.search(text):
        # A full restatement carries its own task and time — abandon via the
        # pop and let it route normally (deterministic pre-classifier claim).
        # Checked before the question gate: a restatement REPLACES the flow
        # regardless of shape, and the full handler re-asks anything unclear.
        logger.info("reminder_time_question_restatement_released", session_id=session_id)
        return None

    # ── ARM SURVIVAL — the SILENT LOW-tier form, stated per CXO's
    #    survival-must-be-stated rule (contract doc §5a READ row): a
    #    STATE_QUESTION verdict returns None, landing the turn on the
    #    generic seam's already-adopted READ branch — that branch re-arms
    #    THIS offer silently and normal processing answers the question.
    #    Silent (not the standup_complete_todo visible form) because nothing
    #    can fire from the survived arm: the save runs only off a fresh
    #    answer naming a time. Checked BEFORE the time-signal bind —
    #    contract axis (a): "did I say 3pm?" carries a parseable clock time,
    #    and before adoption it SAVED A REMINDER off a state question.
    if verdict is AcceptanceVerdict.STATE_QUESTION:
        logger.info(
            "reminder_time_question_state_question_falls_through",
            session_id=session_id,
        )
        return None

    if _has_time_signal(text):
        # #1572: the answer's time binds on the USER'S clock when known —
        # same anchor the primary path uses.
        from services.utils.user_timezone import get_user_timezone

        user_tz = await get_user_timezone(user_id or offer_user)
        reminder_dt, time_label = parse_reminder_time(text, user_timezone=user_tz)
        if reminder_dt is None:
            rearmed = _rearm_time_question(intent_service, session_id, user_id, pending_offer)
            if time_label.startswith(PAST_TODAY_PREFIX):
                passed_time = time_label[len(PAST_TODAY_PREFIX) :]
                detail = (
                    # This re-ask is emitted AFTER _rearm_time_question()
                    # above re-armed the one-slot store with this seam's
                    # stored ask (#1654) — the arm lives in the callee,
                    # outside the census's holder-local scan (#1766).
                    # ask-census: armed-in-turn via _rearm_time_question
                    f"{passed_time} today has already passed on my clock. "
                    f"Did you mean tomorrow?"
                )
            else:
                detail = f'I couldn\'t work out the time from "{time_label}".'
            logger.info(
                "reminder_time_question_unbindable_reasked",
                session_id=session_id,
                rearmed=rearmed,
            )
            return _time_reask(task_text, detail, rearmed)

        # The REAL save — the same write the primary path performs.
        principal = user_id or offer_user
        try:
            user_uuid = UUID(str(principal))
        except (ValueError, TypeError):
            return {
                "message": (
                    "I need you to be logged in to set reminders. " "Nothing has been saved."
                ),
                "intent_data": {
                    "category": "execution",
                    "action": "create_reminder",
                    "error_type": "AuthenticationRequired",
                },
            }
        try:
            todo = await intent_service.todo_handlers.todo_service.create_todo(
                user_id=user_uuid,
                text=task_text,
                priority="medium",
                reminder_date=reminder_dt,
                due_date=reminder_dt,
            )
        except Exception as e:  # silent-ok: #1648 — a failed write must surface as an HONEST failure (never a crash, never a success claim); logged ERROR + traceback
            logger.error(
                "reminder_time_question_save_failed",
                error=str(e),
                session_id=session_id,
                exc_info=True,
            )
            rearmed = _rearm_time_question(intent_service, session_id, user_id, pending_offer)
            return _time_reask(
                task_text,
                "I had trouble saving it just now.",
                rearmed,
            )

        logger.info(
            "reminder_time_question_saved",
            todo_id=str(todo.id),
            reminder_date=str(reminder_dt),
            time_label=time_label,
            session_id=session_id,
        )
        return {
            "message": _reminder_saved_message(task_text, reminder_dt, time_label, user_tz=user_tz),
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "confidence": 1.0,
                "reminder_saved": True,
            },
        }

    # No time signal in the turn.
    if verdict is not AcceptanceVerdict.ACCEPT and is_command_shaped(text):
        # An unrelated command abandons via the pop and routes normally —
        # the carrier's documented off-intent rule.
        return None

    # A bare "yes" doesn't answer "when?", and anything else unrecognized
    # gets the honest re-ask — never a silent abandon into the routing chain
    # mid-flow (#1648 direction 2).
    rearmed = _rearm_time_question(intent_service, session_id, user_id, pending_offer)
    logger.info(
        "reminder_time_question_reasked",
        session_id=session_id,
        rearmed=rearmed,
    )
    return _time_reask(
        task_text,
        "I still need a time for it.",
        rearmed,
    )


async def run_clarify_reminder_time_workflow(
    session_id: str,
    user_id=None,
    context=None,
):
    """Generic-accept landing for the time question (defense in depth — the
    kind-specific seam claims accepts itself, but a registered landing means
    a stray generic accept can never fall into _handle_unknown_intent and
    reach the floor): re-ask and re-arm. effect: READ (nothing written; the
    real write happens on an ANSWERED turn at the offer seam)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != REMINDER_TIME_QUESTION_KIND or intent_service is None:
        logger.error(
            "clarify_reminder_time_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    task_text = (payload.get("task_text") or "").strip() or "that"
    offer = {
        "workflow_type": CLARIFY_REMINDER_TIME_WORKFLOW,
        "pending_action": dict(payload),
        "decline_message": ("Okay — I haven't set that reminder. Nothing was saved."),
    }
    rearmed = _rearm_time_question(intent_service, session_id, user_id, offer)
    return _time_reask(task_text, "I still need a time for it.", rearmed)


# --- #1654: the reminder task-question turn handler --------------------------


# #1665: the re-ask turns' open question — one constant, embedded in the
# re-ask reply AND stored on the re-armed record (same string, no drift).
_TASK_REASK_TAIL = (
    "Tell me what the reminder should say (for example: "
    "'review the beta notes'), or say 'no' to drop it."
)


def _rearm_task_question(intent_service, session_id, user_id, pending_offer) -> bool:
    """Re-arm the SAME offer (the pop already consumed it; a re-ask turn must
    re-store it or the next answer has nothing to bind to). Returns False on
    a store failure so the copy never claims a binding that isn't there.
    #1665: the re-armed record's open question becomes the re-ask tail every
    re-ask turn renders (set BEFORE the store — what's stored is what's said)."""
    try:
        pending_offer["question"] = _TASK_REASK_TAIL
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
        return True
    except Exception as e:  # silent-ok: #1654 — a store failure must not crash the turn; logged ERROR, and callers keep the user-facing copy honest
        logger.error("reminder_task_question_rearm_failed", error=str(e))
        return False


def _task_reask(detail: str, rearmed: bool) -> dict:
    """The honest re-ask shape: nothing saved, here's why, here's what works."""
    if rearmed:
        tail = _TASK_REASK_TAIL
    else:
        tail = (
            "I couldn't keep the question open either — ask me again "
            "('remind me to … at …') and I'll set it fresh."
        )
    return {
        "message": f"No reminder has been saved yet — {detail} {tail}",
        "intent_data": {
            "category": "execution",
            "action": "create_reminder",
            "reminder_task_question_pending": rearmed,
            "reminder_task_reasked": True,
        },
        "requires_clarification": True,
    }


def _chain_time_question(
    intent_service, session_id, user_id, task_text: str, detail: str = ""
) -> dict:
    """#1654 → #1648 chaining: the task just bound but no usable time exists
    — arm the EXISTING time-question carrier (the same record the primary
    time-clarify branch arms) and ask. The two-question recovery: task
    answer here, time answer at handle_reminder_time_turn, REAL save there.
    #1665: _TIME_ASK is rendered once, stored on the armed record, and
    embedded verbatim in the reply."""
    armed = True
    try:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            build_reminder_time_offer(task_text, user_id, question=_TIME_ASK),
            user_id=str(user_id) if user_id else None,
        )
    except Exception as e:  # silent-ok: #1654 — a chain-arm failure must surface as the honest fallback tail below, never a crash; logged ERROR
        logger.error("reminder_task_chain_arm_failed", error=str(e), session_id=session_id)
        armed = False
    if armed:
        tail = _TIME_ASK
    else:
        tail = (
            "I couldn't keep the question open, though — ask me again "
            f"('remind me to {task_text} at …') and I'll set it."
        )
    prefix = f"Got it — **{task_text}**. "
    if detail:
        prefix += f"{detail} "
    return {
        "message": prefix + tail,
        "intent_data": {
            "category": "execution",
            "action": "create_reminder",
            "reminder_task_bound": True,
            "reminder_time_question_pending": armed,
        },
        "requires_clarification": True,
    }


async def handle_reminder_task_turn(
    pending_offer: dict,
    message: str,
    *,
    session_id: str,
    user_id,
    intent_service,
) -> Optional[dict]:
    """#1654 — kind-specific turn handling for a pending reminder TASK
    question (the no-task clarify's carrier), run at the offer seam BEFORE
    any classification surface (the #1605/#1648 sanctioned handler-internal
    seam; the pop already happened).

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` falls through to the generic offer flow
    (declines and bare exits drop honestly via ``decline_message``; full
    reminder restatements and pre-classifier-claimed commands abandon via
    the pop and route normally).

    Off-intent discrimination deviates from #1648's ``is_command_shaped``
    DELIBERATELY: the task-answer space is arbitrary imperative phrases, and
    the shared shape-read's verb heads (check/get/set/find/…) claim
    legitimate task answers — "check in with the team" is this ask's own
    example copy. The discriminator here is the pre-classifier's
    DETERMINISTIC claim instead (probed 2026-08-22: it claims every product
    command tried — "close issue #108", "give me my standup" — and NO bare
    task phrase). Same release-and-route-normally principle, at the
    granularity this answer space needs. A command-ish turn the
    pre-classifier can't claim would route to the LLM lane if released —
    exactly the orphan shape #1654 fixes — so it binds as a task instead
    (visible, declinable, recoverable).

    #1899: the pre-classifier's claim is checked FIRST (free, deterministic)
    and, when it declines, a second oracle — ``inversion_live.read_op_claims_turn``
    — gets one narrow shot: release ONLY when the Inversion router names a
    READ operation at live-flagged, high-confidence certainty. #1595 Phase 3
    keeps shrinking what the pre-classifier alone can recognise here (e.g.
    "list my reminders" stopped claiming once ``REMINDER_QUERY_PATTERNS``
    was deleted, and "show my todos" once ``TODO_QUERY_PATTERNS`` was — both
    now recover via this second oracle); a READ can never be the answer to
    "what should I remind you about?", so gating on it is structurally safe.
    Write/none/clarify still bind as a task, unchanged.

    A bound task with no bindable time CHAINS into the EXISTING #1648 time
    question; a time already known (from the original message — rare — or
    given in the answer itself) saves for REAL: the same row write and 📅
    copy the primary path composes, never an improvised confirmation.

    #1654 (#1739 acceptance-contract adoption, epic 3 — 2026-09-12): the
    seam consults THE predicate (``acceptance.evaluate_acceptance``) at its
    REGISTRY-DECLARED axes with the arm-site's stored ask threaded (#1665),
    replacing the legacy ``detect_offer_response``. The load-bearing gain is
    contract axis (a): before adoption a question the pre-classifier could
    not claim BOUND AS THE TASK ("what do you mean?" → "Got it — **what do
    you mean**"), and one it could claim was released with the arm's
    survival left to the generic seam by composition rather than decided
    here. See the in-body comments for tier + survival form.
    """
    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )
    from services.intent_service.destructive_confirm import detect_bare_exit
    from services.intent_service.temporal_utils import parse_reminder_time

    payload = pending_offer.get("pending_action") or {}
    original_message = (payload.get("original_message") or "").strip()
    text = (message or "").strip()
    if not text:
        return None

    # Principal binding (the #1605 discipline): the offer belongs to the user
    # who asked — a different principal's turn must not save under it.
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(user_id) != str(offer_user):
        logger.warning(
            "reminder_task_question_principal_mismatch",
            offer_user=offer_user,
            turn_user=str(user_id),
        )
        return {
            "message": "Let's hold off on that — nothing has been saved.",
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "principal_mismatch": True,
            },
        }

    if detect_bare_exit(text):
        return None  # generic flow → honest decline via decline_message

    # ── #1654 (#1739 adoption). AXES, MAPPED EXPLICITLY: the ARMED workflow
    #    (clarify_reminder_task) is registry-declared READ×PRIVATE →
    #    LOW_CEREMONY — the seam itself writes nothing off a verdict; the
    #    REAL save runs only off an ANSWER turn (and usually only after the
    #    chained time question). Zero-widening: the LOW-tier accept
    #    vocabulary is the legacy detect_offer_response rows plus only the
    #    crisp CONFIRM superset, and ACCEPT at this seam only ever re-asks
    #    (never fires) — before adoption "confirm" wasn't accept vocabulary
    #    at all and BOUND as the task text, so the widening is a strict
    #    improvement here.
    _axes = declared_axes_for_workflow(CLARIFY_REMINDER_TASK_WORKFLOW)
    verdict = evaluate_acceptance(
        text,
        effect=_axes[0] if _axes else None,
        outwardness=_axes[1] if _axes else None,
        armed_question=pending_offer.get("question"),  # #1665: from the record
    )
    if verdict is AcceptanceVerdict.DECLINE:
        return None  # generic flow → honest decline via decline_message

    if _REMINDER_RESTATEMENT_RE.search(text):
        # A full restatement carries its own task (and possibly time) —
        # abandon via the pop and let it route normally (deterministic
        # pre-classifier claim; the full handler re-extracts both). Checked
        # before the question gate: a restatement REPLACES the flow
        # regardless of shape.
        logger.info("reminder_task_question_restatement_released", session_id=session_id)
        return None

    # ── ARM SURVIVAL — the SILENT LOW-tier form, stated per CXO's
    #    survival-must-be-stated rule (contract doc §5a READ row): a
    #    STATE_QUESTION verdict returns None, landing the turn on the
    #    generic seam's already-adopted READ branch — that branch re-arms
    #    THIS offer silently and normal processing answers the question.
    #    Silent (not the standup_complete_todo visible form) because nothing
    #    can fire from the survived arm: a stale arm's worst case is a bound
    #    task and a fresh time question, one honest decline away from
    #    nothing. Checked BEFORE the pre-classifier release AND before the
    #    bind — contract axis (a): a question is a state query, never a task
    #    answer ("what do you mean?" used to bind as the task verbatim).
    if verdict is AcceptanceVerdict.STATE_QUESTION:
        logger.info(
            "reminder_task_question_state_question_falls_through",
            session_id=session_id,
        )
        return None

    if verdict is AcceptanceVerdict.ACCEPT:
        # A bare "yes" (or an accept-led / crisp-confirm turn) doesn't name
        # a task — the honest re-ask, never a silent abandon (#1648
        # direction 2).
        rearmed = _rearm_task_question(intent_service, session_id, user_id, pending_offer)
        logger.info(
            "reminder_task_question_reasked",
            session_id=session_id,
            rearmed=rearmed,
        )
        return _task_reask("I still need to know what it's for.", rearmed)

    # Off-intent: a turn the pre-classifier claims deterministically is
    # another product command — release it (routes normally; the question is
    # abandoned per the carrier's rules). See the docstring for why this is
    # NOT is_command_shaped.
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None:
        logger.info(
            "reminder_task_question_command_released",
            session_id=session_id,
            claimed_action=claimed.action,
        )
        return None

    # #1899 — surface 1 declined; a second, narrower oracle catches what
    # #1595 Phase 3's deletions no longer let it claim. A READ verdict can
    # NEVER sensibly complete "remind me to ___" (structural, not a
    # heuristic), so releasing on it alone is safe — write/none/clarify all
    # keep binding as before ("buy milk" must never release on a
    # create_todo hunch). See read_op_claims_turn's docstring for the full
    # four-gate account.
    from services.intent_service.inversion_live import (
        read_op_claims_turn,
        registry_category_for,
    )

    # #1920 (CXO/Arch 2026-10-02): a cross-family WRITE releases too — see
    # read_op_claims_turn; the carrier's family is create_reminder's.
    read_op = await read_op_claims_turn(
        text,
        session_id=session_id,
        user_id=user_id,
        intent_service=intent_service,
        carrier_category=registry_category_for("create_reminder"),
    )
    if read_op is not None:
        logger.info(
            "reminder_task_question_command_released",
            session_id=session_id,
            claimed_action=read_op,
        )
        return None

    # The turn IS the task. Answers often echo the ask's phrasing — strip a
    # leading "to "/"about " ("to buy milk" → "buy milk") — and may carry
    # their own time ("buy milk at 3pm tomorrow"), which is shed from the
    # saved text exactly as the primary extraction sheds it.
    task_text = re.sub(r"^(?:to|about)\s+", "", text, flags=re.IGNORECASE)

    if _is_pure_time_expression(task_text):
        # A pure-time answer to the TASK question ("at 3pm"): the task is
        # still missing — re-ask, never save a time expression AS the task.
        # Checked BEFORE the trailing strip: stripping a time-only answer
        # leaves a preposition residue ("at") that would bind as the task.
        rearmed = _rearm_task_question(intent_service, session_id, user_id, pending_offer)
        return _task_reask("that reads as a time, and I still need the task itself.", rearmed)

    answer_has_time = _has_time_signal(text)
    answer_dt = None
    answer_label = ""
    # #1572: both parse candidates (the answer's own time and the original
    # message's) bind on the USER'S clock when a tz is stored.
    from services.utils.user_timezone import get_user_timezone

    user_tz = await get_user_timezone(user_id or offer_user)
    if answer_has_time:
        answer_dt, answer_label = parse_reminder_time(text, user_timezone=user_tz)
    task_text = _strip_trailing_time_expressions(task_text)

    if not task_text or _is_pure_time_expression(task_text):
        # Belt for residues the pre-strip check can't see.
        rearmed = _rearm_task_question(intent_service, session_id, user_id, pending_offer)
        return _task_reask("that reads as a time, and I still need the task itself.", rearmed)

    # Time resolution: the answer's own time wins (freshest), then the
    # original message's (#1654's "already known (rare)" case) — each only
    # when an explicit signal is present (#1490 invariant: never the
    # parser's silent tomorrow-morning default). Explicit-but-unbindable
    # chains with an honest echo; no signal anywhere chains with the plain
    # ask.
    if answer_has_time:
        if answer_dt is None:
            return _chain_time_question(
                intent_service,
                session_id,
                user_id,
                task_text,
                detail=f'I couldn\'t work out the time from "{answer_label}".',
            )
        reminder_dt, time_label = answer_dt, answer_label
    elif original_message and _has_time_signal(original_message):
        orig_dt, orig_label = parse_reminder_time(original_message, user_timezone=user_tz)
        if orig_dt is None:
            return _chain_time_question(
                intent_service,
                session_id,
                user_id,
                task_text,
                detail=f'I couldn\'t work out the time from "{orig_label}".',
            )
        reminder_dt, time_label = orig_dt, orig_label
    else:
        return _chain_time_question(intent_service, session_id, user_id, task_text)

    # The REAL save — the same write the primary path performs.
    principal = user_id or offer_user
    try:
        user_uuid = UUID(str(principal))
    except (ValueError, TypeError):
        return {
            "message": ("I need you to be logged in to set reminders. " "Nothing has been saved."),
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "error_type": "AuthenticationRequired",
            },
        }
    try:
        todo = await intent_service.todo_handlers.todo_service.create_todo(
            user_id=user_uuid,
            text=task_text,
            priority="medium",
            reminder_date=reminder_dt,
            due_date=reminder_dt,
        )
    except Exception as e:  # silent-ok: #1654 — a failed write must surface as an HONEST failure (never a crash, never a success claim); logged ERROR + traceback
        logger.error(
            "reminder_task_question_save_failed",
            error=str(e),
            session_id=session_id,
            exc_info=True,
        )
        # Both task and time are known here — hold the flow at the #1648
        # time question (task stays bound), so the retry is one short
        # answer away instead of restarting the whole two-question flow.
        rearmed = _rearm_time_question(
            intent_service,
            session_id,
            user_id,
            build_reminder_time_offer(task_text, user_id),
        )
        return _time_reask(task_text, "I had trouble saving it just now.", rearmed)

    logger.info(
        "reminder_task_question_saved",
        todo_id=str(todo.id),
        reminder_date=str(reminder_dt),
        time_label=time_label,
        session_id=session_id,
    )
    return {
        "message": _reminder_saved_message(task_text, reminder_dt, time_label, user_tz=user_tz),
        "intent_data": {
            "category": "execution",
            "action": "create_reminder",
            "confidence": 1.0,
            "reminder_saved": True,
        },
    }


async def run_clarify_reminder_task_workflow(
    session_id: str,
    user_id=None,
    context=None,
):
    """Generic-accept landing for the task question (defense in depth — the
    kind-specific seam claims accepts itself, but a registered landing means
    a stray generic accept can never fall into _handle_unknown_intent and
    reach the floor): re-ask and re-arm. effect: READ (nothing written; the
    real write happens on an ANSWERED turn at the offer seam)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != REMINDER_TASK_QUESTION_KIND or intent_service is None:
        logger.error(
            "clarify_reminder_task_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    offer = {
        "workflow_type": CLARIFY_REMINDER_TASK_WORKFLOW,
        "pending_action": dict(payload),
        "decline_message": ("Okay — I haven't set a reminder. Nothing was saved."),
    }
    rearmed = _rearm_task_question(intent_service, session_id, user_id, offer)
    return _task_reask("I still need to know what it's for.", rearmed)
