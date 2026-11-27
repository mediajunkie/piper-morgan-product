"""2459 (Arch's ruling, part 2) and 2460 (what counts as typed): the one gate in
front of every GitHub issue write that takes an issue number (update, close,
reopen, comment).

The rule:

1. A number the person typed in THIS message is accepted (``typed_issue_number``,
   issue 2460 as amended by Arch, a permission rule over the person's own message):
   - a write carrying a field value (an update writing a title, body, label,
     assignee or milestone; a comment's body) counts a number MARKED as ``#N`` or
     ``issue N`` whose span lies outside every field value being written (the
     handler's own slots, located with case ignored, whitespace runs collapsed and
     one pair of surrounding quotes stripped); if a value is not in the message,
     only ``#N`` counts; bare digits never count ("rename it to Test issue 2" holds "issue 2"
     inside the new title, so it does not count; "change the title of issue 108 to
     Draft 3" counts 108, issue 1411's phrasing);
   - a write with no field value (close, reopen, a state-only update) also
     counts a bare number, but only when exactly ONE distinct number appears.
   Exactly one distinct counted number is the target; two or more are refused (the
   ask). Reads keep their own parse.
2. Otherwise the number is accepted only if it is the session's created head
   (``issue_head``: owner- and session-scoped, as ``_issue_referent_from_ledger``
   reads it) AND the created head is the session's referent under
   ``choose_issue_referent`` (no newer read showed a different issue or several),
   with the same repository when one is carried. A free-text write that typed no
   number at all takes the created head the same way (``source_created_head``).
3. Anything else is refused: the caller says its existing ask for a number (or the
   named ask when a single shown issue is the only candidate), and nothing is
   armed, recorded or sent. That covers a number taken from the RECENT ISSUE line
   for a shown issue, a router arg, the classifier's no-``#`` explicit number, and a
   model's guess.

The gate never trusts the router: it compares the candidate with the message text
and the ledger in code. A failed ledger read is "no created head" (refusal unless
typed), never a pass.

An accepted verdict is stamped on the intent (``GATE_CONTEXT_KEY``), so the same
intent re-dispatched by a repository answer is not gated a second time against a
ledger read that might fail on that turn. A confirmed "yes" carries the values its
question bound and is not gated again.

``issue_number_arg`` is the one normaliser for the issue key (``issue_number`` or
``issue``; the router emits both): the gate and the handlers read through it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, List, Mapping, Optional, Sequence, Set, Tuple

import structlog

from services.intent_service.shown_issue import (
    BARE_ISSUE_NUMBER_HINT,
    LEDGER_UNREADABLE,
    SHOWN_ISSUE_WHICH_ASK,
    CreatedIssueRef,
    choose_issue_referent,
    last_shown_issue,
)

logger = structlog.get_logger(__name__)

# Each handler's EXISTING ask for an issue number, moved here byte for byte so the
# gate's refusal and the handler's own no-number path say the same sentence. No new
# copy (2459: a refused write gets the existing ask).
UPDATE_ISSUE_NUMBER_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'update issue #123')."
)
COMMENT_ISSUE_NUMBER_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'comment on issue #123 saying...')."
)
# #2120: no search ran, so no "couldn't find" claim (close and its reopen twin).
CLOSE_ISSUE_NUMBER_ASK = (
    "I can close a particular issue if you give me its number, like "
    '"close #123". I don\'t search for finished issues or close them in '
    "bulk yet."
)
REOPEN_ISSUE_NUMBER_ASK = (
    "I can reopen a particular issue if you give me its number, like "
    '"reopen #123". I don\'t search for closed issues or reopen them in '
    "bulk yet."
)

#: Where an accepted verdict rides the intent's context.
GATE_CONTEXT_KEY = "issue_write_gate"

_ISSUE_KEYS = ("issue_number", "issue")

CreatedHeadReader = Callable[[Optional[str], Optional[str]], Awaitable[Optional[CreatedIssueRef]]]


def _as_issue_number(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str):
        text = value.strip().lstrip("#")
        if text.isdigit():
            n = int(text)
            return n if n > 0 else None
    return None


def issue_number_arg(mapping: Optional[Mapping[str, Any]]) -> Optional[int]:
    """The issue number a context or args dict carries, under ``issue_number`` or
    ``issue``, as one positive int. A non-integer value counts as absent."""
    if not isinstance(mapping, Mapping):
        return None
    for key in _ISSUE_KEYS:
        number = _as_issue_number(mapping.get(key))
        if number is not None:
            return number
    return None


def message_of(intent: Any) -> str:
    """The person's own message for this intent (the text the handlers parse)."""
    ctx = getattr(intent, "context", None) or {}
    return ctx.get("original_message") or getattr(intent, "original_message", None) or ""


def _digit_runs(text: str) -> List[Tuple[int, int]]:
    """``(start, end)`` of every maximal run of ASCII digits in ``text``."""
    runs: List[Tuple[int, int]] = []
    i, n = 0, len(text)
    while i < n:
        if "0" <= text[i] <= "9":
            j = i
            while j < n and "0" <= text[j] <= "9":
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    return runs


def _is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


def _issue_word_start(text: str, digit_start: int) -> Optional[int]:
    """Where a marked ``issue N`` form begins, when the digit run at ``digit_start``
    is written that way: the word ``issue`` (any case, not part of a longer word),
    one or more spaces, an optional ``#``, then the digits. Accepted: "issue 108",
    "Issue #108", "issue  108", "ISSUE 108". Not accepted: "issues 3", "issue-108",
    "issue108", "reissue 5", "issue\n108" (spaces only)."""
    k = digit_start
    if k > 0 and text[k - 1] == "#":
        k -= 1
    spaces_end = k
    while k > 0 and text[k - 1] == " ":
        k -= 1
    if k == spaces_end:
        return None
    word_start = k - len("issue")
    if word_start < 0 or text[word_start:k].casefold() != "issue":
        return None
    if word_start > 0 and _is_word_char(text[word_start - 1]):
        return None
    return word_start


_QUOTE_PAIRS = (('"', '"'), ("'", "'"), ("\u201c", "\u201d"), ("\u2018", "\u2019"))


def _normalised_with_map(text: str) -> Tuple[str, List[int]]:
    """``text`` case-folded with every whitespace run collapsed to one space, and for
    each character of that copy the index of the ORIGINAL character it came from (a
    collapsed run maps to its first whitespace character; a character that folds to
    several maps each of them to itself)."""
    out: List[str] = []
    index: List[int] = []
    in_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not in_space:
                out.append(" ")
                index.append(i)
            in_space = True
            continue
        in_space = False
        for folded in ch.casefold():
            out.append(folded)
            index.append(i)
    return "".join(out), index


def normalise_field_value(value: str) -> str:
    """A field value as it is located in the message (issue 2460, Arch's three
    normalisations, nothing else): ONE pair of surrounding quotes (straight or curly,
    single or double) stripped, then case ignored and whitespace runs collapsed."""
    text = (value or "").strip()
    for left, right in _QUOTE_PAIRS:
        if len(text) >= 2 and text.startswith(left) and text.endswith(right):
            text = text[1:-1].strip()
            break
    folded, _ = _normalised_with_map(text)
    return folded.strip()


def _value_spans(text: str, values: Sequence[str]) -> Tuple[List[Tuple[int, int]], bool]:
    """Every occurrence of each non-empty field value in ``text``, as spans of the
    ORIGINAL message, and whether EVERY such value was found. Located on the
    normalised copy (``_normalised_with_map``) and mapped back through its index:
    a match at normalised ``[a, b)`` is original ``[index[a], index[b - 1] + 1)``."""
    folded, index = _normalised_with_map(text)
    spans: List[Tuple[int, int]] = []
    all_found = True
    for value in values:
        needle = normalise_field_value(value)
        if not needle:
            continue
        start = folded.find(needle)
        if start < 0:
            all_found = False
            continue
        while start >= 0:
            end = start + len(needle)
            spans.append((index[start], index[end - 1] + 1))
            start = folded.find(needle, start + 1)
    return spans, all_found


def update_field_values(
    title: Any = None,
    body: Any = None,
    labels: Any = None,
    assignees: Any = None,
    milestone: Any = None,
) -> List[str]:
    """Every field value an update writes, as text (issue 2460, Arch's adjustment):
    the title, the body, each label, each assignee and the milestone. A state change
    is not a field value. Labels and assignees may be strings or ``{"name"}`` /
    ``{"login"}`` dicts."""
    out: List[str] = []

    def _add(v: Any) -> None:
        if isinstance(v, dict):
            v = v.get("name") or v.get("login") or v.get("title")
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            v = str(v)
        if isinstance(v, str) and v.strip():
            out.append(v)

    for v in (title, body, milestone):
        _add(v)
    for many in (labels, assignees):
        if isinstance(many, (list, tuple, set)):
            for v in many:
                _add(v)
        else:
            _add(many)
    return out


def _overlaps(span: Tuple[int, int], spans: Sequence[Tuple[int, int]]) -> bool:
    return any(span[0] < end and start < span[1] for start, end in spans)


def _free_text_readings(message: str, field_values: Sequence[str]) -> Tuple[Set[int], Set[int]]:
    """For a write with a free-text field (issue 2460 rule 1, as amended): the
    COUNTED numbers (marked ``#N`` or ``issue N`` whose span overlaps no occurrence
    of a field value; only ``#N`` when a field value is absent from the message or
    there is none), and the BARE numbers outside every field value (never counted)."""
    text = message or ""
    values = [v for v in field_values if isinstance(v, str) and v.strip()]
    spans, all_found = _value_spans(text, values)
    issue_form_ok = bool(values) and all_found
    counted: Set[int] = set()
    bare: Set[int] = set()
    for start, end in _digit_runs(text):
        number = int(text[start:end])
        hash_marked = start > 0 and text[start - 1] == "#"
        word_start = _issue_word_start(text, start) if issue_form_ok else None
        if hash_marked:
            span_start = start - 1
        elif word_start is not None:
            span_start = word_start
        else:
            if not _overlaps((start, end), spans):
                bare.add(number)
            continue
        if word_start is not None:
            span_start = min(span_start, word_start)
        if not _overlaps((span_start, end), spans):
            counted.add(number)
    return counted, bare


def typed_issue_candidates(
    message: str, has_free_text_field: bool, field_values: Sequence[str] = ()
) -> Set[int]:
    """Every DISTINCT number that counts as typed for a write (issue 2460).

    ``has_free_text_field`` means "this write carries at least one field value"
    (Arch's adjustment: an update's title, body, each label, each assignee, the
    milestone; a comment's body). The name is kept from the first ruling.

    - No field value (close, reopen, a state-only update): every run of digits,
      marked or bare.
    - At least one field value: a number MARKED as ``#N`` or ``issue N`` (case
      ignored; see ``_issue_word_start``) whose span in the message lies outside
      every occurrence of every field value (``field_values``, located after
      ``normalise_field_value``: case ignored, whitespace runs collapsed, one pair of
      surrounding quotes stripped from the value; nothing else; a number overlapping
      any occurrence, even partly, is excluded). When a field value is not found in
      the message, or none is given, only ``#N`` counts. Bare digits never count.

    Read by character class: no compiled pattern (the binder/extraction ratchets)."""
    text = message or ""
    if not has_free_text_field:
        return {int(text[a:b]) for a, b in _digit_runs(text)}
    counted, _ = _free_text_readings(text, field_values)
    return counted


def typed_issue_number(
    message: str, has_free_text_field: bool, field_values: Sequence[str] = ()
) -> Optional[int]:
    """The one issue number this write's message typed (issue 2460), or None when it
    typed none, typed two or more distinct ones, or typed ``#0``."""
    found = typed_issue_candidates(message, has_free_text_field, field_values)
    if len(found) != 1:
        return None
    (number,) = found
    return number if number > 0 else None


@dataclass(frozen=True)
class IssueWriteVerdict:
    """``shown`` (refusals only): the single SHOWN issue that is the session's
    referent, ``(repository, number)`` from the slot's data, when the refusal is
    because that shown issue is the only candidate referent. The caller then says
    ``SHOWN_ISSUE_WHICH_ASK`` (``refusal_line``) instead of its plain ask."""

    accepted: bool
    number: Optional[int] = None
    repository: Optional[str] = None
    reason: str = ""
    shown: Optional[Tuple[str, int]] = None
    #: Refusals only (issue 2460 follow-up): the ONE bare number the person typed
    #: outside every field value, on a write that carries a field value and typed no
    #: marked number. The caller then says ``BARE_ISSUE_NUMBER_HINT``, unless a shown
    #: issue is the referent (that statement comes first).
    bare: Optional[int] = None


def _same_repo(a: Optional[str], b: Optional[str]) -> bool:
    return bool(a) and bool(b) and str(a).casefold() == str(b).casefold()


def _stamp(intent: Any, verdict: IssueWriteVerdict) -> None:
    """Mark the intent's own context dict in place (never replaced: the #1459
    original_message ratchet). No context dict: nothing marked, so a re-dispatch is
    only gated again."""
    ctx = getattr(intent, "context", None)
    if not isinstance(ctx, dict):
        return
    try:
        ctx[GATE_CONTEXT_KEY] = {
            "number": verdict.number,
            "repository": verdict.repository,
            "reason": verdict.reason,
        }
    except Exception as e:  # silent-ok: logged; an unstamped intent is only gated again
        logger.warning("issue_write_gate_stamp_failed", error=str(e))


def _non_integer_issue_key(intent: Any) -> bool:
    """An issue key is present (context or router args) but is not an integer."""
    ctx = getattr(intent, "context", None) or {}
    for mapping in (ctx, ctx.get("inversion_args")):
        if not isinstance(mapping, Mapping):
            continue
        for key in _ISSUE_KEYS:
            value = mapping.get(key)
            if value not in (None, "") and _as_issue_number(value) is None:
                return True
    return False


async def _read_head(
    created_head: Optional[CreatedHeadReader], user_id: Optional[str], session_id: Optional[str]
) -> Optional[CreatedIssueRef]:
    """The owner-scoped created head; a reader that raises counts as unreadable."""
    if created_head is None or not user_id or not session_id:
        return None
    try:
        return await created_head(user_id, session_id)
    except Exception as e:  # silent-ok: logged; unreadable means the ask, never a pass
        logger.warning("issue_write_gate_ledger_failed", error=str(e))
        return LEDGER_UNREADABLE


def _shown_referent(
    head: Optional[CreatedIssueRef], user_id: Optional[str], session_id: Optional[str]
) -> Optional[Tuple[str, int]]:
    """The single shown issue when it is the session's referent (shown only, or a
    show newer than the create), from the slot's data; else None."""
    shown = last_shown_issue(session_id, user_id)
    if shown is None or not getattr(shown, "single", False):
        return None
    chosen = choose_issue_referent(head, shown)
    if chosen is None or (chosen[0], chosen[1]) != (shown.repository, shown.number):
        return None
    return chosen


def _refuse(
    action: Any,
    reason: str,
    number: Optional[int],
    repository: Optional[str],
    shown: Optional[Tuple[str, int]] = None,
    bare: Optional[int] = None,
) -> IssueWriteVerdict:
    logger.info(
        "issue_write_gate_refused",
        action=action,
        reason=reason,
        named=bool(shown),
        bare_hint=bare is not None,
    )
    return IssueWriteVerdict(False, number, repository, reason, shown, bare)


def single_bare_number(message: str, field_values: Sequence[str]) -> Optional[int]:
    """Issue 2460 follow-up: the one bare number in a field-value write's message that
    sits outside every field value, when the message has NO counted (marked) number
    and exactly one such bare number; else None. Read by the same scan the rule uses,
    so "bare" and "counted" cannot disagree with ``typed_issue_candidates``."""
    values = [v for v in field_values if isinstance(v, str) and v.strip()]
    _, all_found = _value_spans(message or "", values)
    if not values or not all_found:
        # A value the message does not hold cannot be located, so no number can be
        # shown to sit outside it: the plain ask stands.
        return None
    counted, bare = _free_text_readings(message or "", field_values)
    if counted or len(bare) != 1:
        return None
    (number,) = bare
    return number if number > 0 else None


def refusal_line(verdict: IssueWriteVerdict, plain_ask: str) -> str:
    """What a refused write says: the named ask when the only candidate referent is
    a single shown issue, else the handler's existing ask, byte for byte."""
    if verdict.shown is not None:
        repository, number = verdict.shown
        return SHOWN_ISSUE_WHICH_ASK.format(number=number, repository=repository)
    if verdict.bare is not None:
        return BARE_ISSUE_NUMBER_HINT.format(number=verdict.bare)
    return plain_ask


async def gate_issue_write(
    intent: Any,
    candidate: Any,
    *,
    has_free_text_field: bool,
    repository: Optional[str],
    user_id: Optional[str],
    session_id: Optional[str],
    created_head: Optional[CreatedHeadReader],
    stamp: bool = True,
    source_created_head: bool = False,
    field_values: Sequence[str] = (),
) -> IssueWriteVerdict:
    """Decide whether ``candidate`` (the number the write would act on, or None when
    the write found none) may be written. ``has_free_text_field`` picks the 2460
    form (True: an update writing a title or body, a comment; False: close, reopen,
    an update writing neither). ``field_values``: the free-text value(s) this write
    will write (the handler's own slots), so a number inside one never counts. ``repository`` is the
    repository the write would use when the turn carries one (context or slot-fill),
    else None. ``created_head`` reads the owner-scoped ledger head
    (``IntentService._issue_referent_from_ledger``). ``source_created_head``: with
    no candidate and no typed number, accept the created head when it is the
    referent (the verdict's ``number`` then names it).

    ``stamp=False`` (the ask-time callers) leaves the intent untouched: an ask binds
    only what its question shows (the #2304/#2379 pins).

    A refusal carries ``shown`` when the session's referent is a single shown issue
    (see ``refusal_line``), except for a repository mismatch, a non-integer issue
    key, or two or more typed numbers, which keep the plain ask."""
    action = getattr(intent, "action", None)
    number = _as_issue_number(candidate)
    ctx = getattr(intent, "context", None) or {}

    stamped = ctx.get(GATE_CONTEXT_KEY)
    if number is not None and isinstance(stamped, dict) and stamped.get("number") == number:
        return IssueWriteVerdict(
            True, number, stamped.get("repository") or repository, "gated_earlier"
        )

    message = message_of(intent)
    typed_set = typed_issue_candidates(message, has_free_text_field, field_values)
    if len(typed_set) >= 2:
        return _refuse(action, "several_typed", number, repository)
    typed = typed_issue_number(message, has_free_text_field, field_values)
    # Issue 2460 follow-up: only for a write that carries a field value and typed no
    # marked number. Not used for several typed numbers, a repository mismatch or a
    # non-integer key, which keep the plain ask.
    bare_hint = single_bare_number(message, field_values) if has_free_text_field else None

    if number is None:
        if _non_integer_issue_key(intent):
            return _refuse(action, "non_integer", None, repository)
        if source_created_head and not typed_set:
            head = await _read_head(created_head, user_id, session_id)
            usable = head if head is not None and not head.unreadable else None
            if usable is not None:
                chosen = choose_issue_referent(usable, last_shown_issue(session_id, user_id))
                if chosen == (usable.repository, usable.number):
                    if repository and not _same_repo(repository, usable.repository):
                        return _refuse(action, "repository_differs", None, repository)
                    verdict = IssueWriteVerdict(
                        True, usable.number, usable.repository, "created_head"
                    )
                    if stamp:
                        _stamp(intent, verdict)
                    return verdict
            return _refuse(
                action,
                "no_number",
                None,
                repository,
                _shown_referent(head, user_id, session_id),
                bare_hint,
            )
        # The ledger is read only when a single shown issue could be the referent
        # (the named ask); otherwise the plain ask needs no read.
        shown = last_shown_issue(session_id, user_id)
        if shown is None or not getattr(shown, "single", False):
            return _refuse(action, "no_number", None, repository, None, bare_hint)
        head = await _read_head(created_head, user_id, session_id)
        return _refuse(
            action,
            "no_number",
            None,
            repository,
            _shown_referent(head, user_id, session_id),
            bare_hint,
        )

    args_number = issue_number_arg(ctx.get("inversion_args"))
    if args_number is not None and args_number != number:
        # The router's number is not what this write acts on; logged, never used.
        logger.info(
            "issue_write_gate_args_differ", action=action, args_number=args_number, number=number
        )

    if typed is not None and number == typed:
        verdict = IssueWriteVerdict(True, number, repository, "typed")
        if stamp:
            _stamp(intent, verdict)
        return verdict

    head = await _read_head(created_head, user_id, session_id)
    usable = head if head is not None and not head.unreadable else None
    if usable is not None and usable.number == number:
        chosen = choose_issue_referent(usable, last_shown_issue(session_id, user_id))
        if chosen is not None and chosen[1] == number and _same_repo(chosen[0], usable.repository):
            if repository and not _same_repo(repository, usable.repository):
                return _refuse(action, "repository_differs", number, repository)
            verdict = IssueWriteVerdict(True, number, usable.repository, "created_head")
            if stamp:
                _stamp(intent, verdict)
            return verdict
        return _refuse(
            action,
            "created_head_not_newest",
            number,
            repository,
            _shown_referent(head, user_id, session_id),
            bare_hint,
        )
    return _refuse(
        action,
        "not_typed_or_created",
        number,
        repository,
        _shown_referent(head, user_id, session_id),
        bare_hint,
    )
