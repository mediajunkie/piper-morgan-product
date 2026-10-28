"""#1762 epic 6 — the unrendered remainder of a capped list, and the offer that cashes it.

WHAT THIS IS FOR (the three ratified pieces this composes, none of them new):

1. **GatherOutcome contract §5b** (CXO, Arch-confirmed joint invariant of epics
   #1 and #2): *"'…and N more' is a claim the assistant must be able to CASH."*
   A render cap may shorten what the user SEES; it must never change what the
   system believes it HAS.
2. **The #1738 joint invariant** (ruled 09-10): the renderer **consumes**
   provenance and may never **write** it, and the model's context gets the
   **OUTCOME, not the rendered string**. The remainder living in a structured
   outcome is that invariant's storage half — history carrying only the
   rendered string is the defect it names.
3. **The #1739 acceptance contract**: "show me the rest" is an **armed offer
   over the stored remainder**, consumed through THE predicate
   (``evaluate_acceptance``) — never a bespoke word-set.

WHY A SEPARATE STORE, NOT THE ``last_offer`` RAIL (the load-bearing design call):

CXO's constraint, and it is the one that decides the shape — *"a capped-list
offer is exactly the kind a user answers LATE: they read the five, think, and
come back."* But the ``last_offer`` rail lives exactly ONE turn (``process_
intent`` always-clears it at turn start — the #852 invariant), so an
intervening turn kills it and the later "yes" lands on nothing.

The fix is NOT to make ``last_offer`` survive. That rail's one-turn invariant is
load-bearing for two other mechanisms: the #1770 no-clobber peek
(``_peek_last_offer``) is sound *only because* a non-None value there was armed
THIS turn, and the #1529 binding semantic depends on the same. A multi-turn arm
on that rail would silently suppress every soft offer for the whole window and
falsify the peek's soundness argument.

So the remainder gets its OWN store (``ConversationContext.pending_list_
remainder``) with its OWN lifetime, and the one-turn rail is untouched. CXO's
tier ruling is what licenses the longer lifetime: *arm survival is per-tier;
COLLABORATE/READ arms MAY survive; only CONFIRM must not* — and a list read is
the cheapest tier there is.

THE SURVIVAL FORM, STATED (the convention every #1739 adoption follows):
**READ × PRIVATE → LOW_CEREMONY, PERSISTING arm.** Stronger than the §5a SILENT
re-arm the other READ seams take, and deliberately so — §5a survives a state
question, this survives arbitrary intervening turns. What bounds it:

  - it is cleared when CASHED (spent — everything has been shown),
  - cleared on DECLINE (and the turn falls through to normal processing —
    a decline never composes a reply here),
  - REPLACED whenever a newer capped list is rendered (last list wins, so the
    offer always refers to the list the user most recently saw),
  - STALE past ``REMAINDER_MAX_AGE_MINUTES``, and
  - never able to fire anything: cashing prints lines already gathered. The
    worst case of a mistaken accept is a list the user did not want — one
    turn, no state change, no re-fetch.

AND IF IT CANNOT BE RETURNED, SAY SO (CXO, §5b-i): if the stored remainder is
gone or stale, the honest turn says the list moved and offers a fresh read.
**A silent re-fetch presented as "the rest" is a fabrication of continuity** —
the user believes they are holding items 6-340 of the list they saw, and they
are not. Nothing in this module fetches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import NamedTuple, Optional, Sequence

import structlog

logger = structlog.get_logger(__name__)


# PPM's threshold ruling, 2026-09-13: skip the offer when the hidden remainder
# is 3 or fewer items — just render them all. CXO named that one was needed
# ("a cap that hides two items and then offers to reveal them is ceremony");
# PPM set the number, erring toward SHOWING rather than ASKING. Revisit on a
# real Colleague Test, not on taste.
REMAINDER_OFFER_THRESHOLD = 3

# How long a stored remainder stays cashable. NOT a fresh arbitrary number:
# it is ``ConversationContext.max_age_minutes`` — the age at which this
# codebase already declares a conversation stale. A remainder older than the
# conversation that produced it has no claim to be "the list you saw".
REMAINDER_MAX_AGE_MINUTES = 30


@dataclass
class ListRemainder:
    """The unrendered tail of a capped list — the outcome half of §5b.

    ``lines`` holds the SAME per-item strings the render loop produced for the
    items it showed, sliced at the cap. That is the point: the shown half and
    the stored half come from one pass over one gathered set, so cashing
    replays exactly what the render would have printed. The renderer never
    re-derives anything from its own output (#1738's invariant), and the cash
    turn never re-fetches (Arch: *"RETURNS them, from the outcome, not a
    re-fetch that might disagree with the claim"*).
    """

    kind: str  # user-facing noun: "open issues", "labels", …
    shown: int  # how many the arming render displayed
    held_total: int  # how many items we actually HAD in hand
    source_total_display: str  # the SOURCE's count, verbatim ("340", "1000+")
    lines: tuple[str, ...]  # the unshown held items, pre-rendered
    offer_text: str  # the rendered ask (#1665 input adequacy)
    armed_at: datetime = field(default_factory=datetime.now)
    # #1783: this offer's own declaration that it accepts interrogative
    # REQUESTS naming the remainder ("could you show me the rest?"). READ only;
    # the predicate raises if a non-READ seam passes it.
    accepts_request_questions: bool = False

    @property
    def age_seconds(self) -> float:
        return (datetime.now() - self.armed_at).total_seconds()

    def is_stale(self) -> bool:
        return self.age_seconds > REMAINDER_MAX_AGE_MINUTES * 60


@dataclass
class ListComplete:
    """#2040 (Arch): the fact that the last list was rendered WHOLE.

    Recorded only when :func:`compose_capped_list` printed every item the
    source said existed (no remainder offered, nothing unfetched), so "that
    was the full list" is a claim code made true, not one it guesses. A
    SEPARATE record from :class:`ListRemainder` on purpose: it is never an
    armed offer, holds no lines, and no acceptance seam reads it, so it can
    never bind a "yes". It lives one turn (popped at the top of every turn in
    ``_process_intent_internal``): the line it licenses says "that", meaning
    the reply just before, so any other turn in between voids it.
    """

    kind: str
    shown: int
    recorded_at: datetime = field(default_factory=datetime.now)

    def is_stale(self) -> bool:
        return (datetime.now() - self.recorded_at).total_seconds() > (
            REMAINDER_MAX_AGE_MINUTES * 60
        )


class CappedListRender(NamedTuple):
    """What :func:`compose_capped_list` hands back to a handler.

    ``body`` is the list block (and, when earned, the offer clause) ready to
    append to the handler's own header. ``remainder`` is the thing to ARM, or
    None when there is nothing cashable to offer. ``complete`` (#2040) is the
    whole-list fact to record, or None when the render left anything out.
    """

    body: str
    remainder: Optional[ListRemainder]
    complete: Optional[ListComplete] = None


GITHUB_LIST_PAGE_CAP = 100


def page_floor(count: int, page_cap: int = GITHUB_LIST_PAGE_CAP) -> tuple:
    """#1778/#1781/#1782: a count taken from a FULL API page is a FLOOR, not a total.

    The GitHub list endpoints return one page (per_page=100, unpaginated at our
    call sites); ``len(page)`` equals the true total only while the repo is
    under the cap. At the cap, presenting the number as exact is a fabricated
    denominator (CXO §5b-i decision 3: "if the source says 1000+, we say 1000+").

    Returns ``(display, is_floor)``: ``("100+", True)`` at/over the cap,
    ``("37", False)`` under it. Feed ``display`` to headlines and to
    ``compose_capped_list(source_total_display=...)`` when ``is_floor``.
    """
    return (f"{count}+", True) if count >= page_cap else (str(count), False)


def compose_capped_list(
    *,
    lines: Sequence[str],
    cap: int,
    kind: str,
    source_total: Optional[int],
    source_total_display: Optional[str] = None,
    asked_count: Optional[int] = None,
) -> CappedListRender:
    """Render a capped list so its "and there are more" claim is CASHABLE.

    Args:
        lines: one pre-rendered string per item we HOLD, in display order —
            the full held set, not a slice. Each carries its own leading
            newline (the idiom every one of these handlers already uses).
        cap: how many to show.
        kind: the user-facing noun for the set ("open issues", "labels").
        source_total: what the SOURCE says it has. May exceed ``len(lines)``
            when the gather returned a page (search_issues total_count vs. a
            50-item page). None = the source stated no total, so what we hold
            is all there is known to be.
        asked_count: #2186 (CXO's ruling 2026-10-28 11:21): the user ASKED for
            this many ("show my last two"). When we hold more than that, show
            exactly that many and close with ``That's the {n} you asked for,
            out of {total}.`` — no offer (offering the rest after a slice the
            user chose is an unsolicited nudge), but the rest of the held page
            is still stored, so "show me the rest" cashes. When we hold no more
            than was asked, the ordinary logic applies (everything held is on
            screen). None = no count was asked; nothing changes.
        source_total_display: the denominator to PRINT, when the source's own
            count is not an exact integer. CXO §5b-i decision 3: *if the
            source says ``1000+``, we say ``1000+`` — a cap rendered as an
            exact number is a fabricated denominator.* Honest boundary, stated
            (m-44): no source behind the GitHub six reports a capped count
            today, so every current caller leaves this None and gets the exact
            figure. The parameter exists so that a source which starts capping
            has somewhere truthful to put it, instead of the fabrication being
            the path of least resistance.

    Copy is CXO's, verbatim where it applies (§5b-i):

        "That's 5 of 340 — say the word and I'll pull the rest."

    Decision 1 — "5 of 340", NOT "…and 335 more": same fact, but the first
    tells the user what they are HOLDING and the second what is missing, and a
    remainder count invites subtraction nobody asked them to do.
    Decision 2 — the affordance, never the syntax: "say the word", not
    "say 'show me the rest'". Teaching the parser's dialect is the #1579
    failure. The consume half accordingly runs THE shared acceptance
    vocabulary, with the list phrasings only ADDED on top (never substituted).
    """
    held = len(lines)
    total = source_total if source_total is not None else held
    # A source total below what we hold would be incoherent; trust the items
    # we can actually count rather than printing a denominator smaller than
    # the numerator.
    total = max(total, held)
    display = source_total_display or str(total)
    unheld = total - held
    if asked_count is not None and asked_count > 0 and held > asked_count:
        # #2186: the user chose the size. Show it, name what they asked for
        # against what exists, print no offer, keep the rest cashable.
        trailer = f"That's the {asked_count} you asked for, out of {display}."
        remainder = ListRemainder(
            kind=kind,
            shown=asked_count,
            held_total=held,
            source_total_display=display,
            lines=tuple(lines[asked_count:]),
            offer_text=trailer,
            accepts_request_questions=True,
        )
        return CappedListRender("".join(lines[:asked_count]) + "\n\n" + trailer, remainder)
    hidden_held = max(0, held - cap)

    if hidden_held <= REMAINDER_OFFER_THRESHOLD:
        # PPM's threshold: the hidden tail is ceremony — show them all. This
        # is also the ONLY branch that can reach render == data in the #1762
        # class-(a) sense, and it reaches it for free.
        body = "".join(lines)
        if unheld > 0:
            # We showed everything we hold and the source has more we never
            # fetched. No offer — there is nothing cashable — but say what is
            # in hand rather than let the header's total imply we showed it.
            body += f"\n\nThat's all {held} I have in front of me, out of {display}."
            return CappedListRender(body, None)
        # #2040: every item the source has is on screen; record that fact.
        # A source whose own count is not exact ("1000+") never vouches.
        exact = display == str(total)
        complete = ListComplete(kind=kind, shown=held) if held and exact else None
        return CappedListRender(body, None, complete)

    if unheld == 0:
        offer = f"That's {cap} of {display} — say the word and I'll pull the rest."
    else:
        # The source holds more than we ever gathered, so "the rest" would be
        # a promise we cannot keep from the outcome — and keeping it by
        # re-fetching is precisely the fabricated continuity §5b-i forbids.
        # Offer what is actually cashable, and name the two numbers.
        offer = (
            f"That's {cap} of {display} — I have {held} of them in front of me; "
            "say the word and I'll show you those."
        )

    remainder = ListRemainder(
        kind=kind,
        shown=cap,
        held_total=held,
        source_total_display=display,
        lines=tuple(lines[cap:]),
        offer_text=offer,
        accepts_request_questions=True,
    )
    return CappedListRender("".join(lines[:cap]) + "\n\n" + offer, remainder)


# The offer's OWN copy teaches these (#1769's taught-vocabulary idiom): "say
# the word and I'll pull the rest" makes "the rest" a phrase the user was
# invited to use. They are ADDED to the shared LOW-tier vocabulary, never
# substituted for it — CXO §5b-i decision 2 is that the affordance must not
# become a syntax, so a plain "yes" has to work and does (ACCEPT_PATTERNS).
LIST_REMAINDER_TAUGHT_ACCEPTS: tuple[str, ...] = (
    "the rest",
    "rest",
    "show me the rest",
    "show the rest",
    "show me the others",
    "the others",
    "let me see the rest",
    "let's see the rest",
    "lets see the rest",
    "see the rest",
    "all of them",
    "show them all",
    "show me all of them",
    "the whole list",
    "show me the whole list",
    "say the word",
    "the word",
)


# #2040 (CXO's ruling, verbatim): a remainder ask with NOTHING held, right
# after a list rendered whole (a ``ListComplete`` fact is present). A
# statement, not an ask; nothing is appended and nothing is fetched.
# CXO 2026-10-15 17:16, verbatim.
NOTHING_HELD_REPLY = "That was the whole list. There's nothing more to show."

# #2040 (Arch's condition; CXO's words 2026-10-15 17:16, verbatim): a remainder
# ask with nothing held and NO whole-list fact. It claims only what code holds,
# and nothing about the previous turn.
HOLD_ONLY_REPLY = (
    "I'm not holding any more of that list. Ask for it again and I'll pull a fresh one."
)


def render_cash(remainder: ListRemainder) -> str:
    """The turn that CASHES the offer — from the outcome, never a re-fetch."""
    n = len(remainder.lines)
    if remainder.held_total > remainder.shown + n:  # pragma: no cover - defensive
        # Cannot happen from compose_capped_list (lines[cap:] is exactly the
        # held tail); guarded so a future caller that hand-builds a remainder
        # can't quietly under-report.
        logger.warning("list_remainder_shape_mismatch", kind=remainder.kind)
    intro = f"Here's the rest — the other {n} {remainder.kind}."
    if str(remainder.held_total) != remainder.source_total_display:
        intro = (
            f"Here are the other {n} {remainder.kind} I have in front of me — "
            f"that's {remainder.held_total} of {remainder.source_total_display} in all."
        )
    return intro + "".join(remainder.lines)


def render_moved(remainder: ListRemainder) -> str:
    """The honest turn when the stored remainder can't be returned (§5b-i).

    Never a silent re-fetch: the user believes they are holding items 6-N of
    the list they SAW, and a freshly-pulled set is a different object wearing
    that description.
    """
    return (
        f"That list has moved on since I showed it to you, so I don't have the rest of those "
        f"{remainder.kind} in front of me any more. I'd rather say that than hand you a set "
        f"that may have changed underneath you — ask me for them again and I'll pull a fresh list."
    )
