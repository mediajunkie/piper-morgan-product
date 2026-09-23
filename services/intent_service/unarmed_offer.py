"""Offer-shaped-question enforcement at the conversational floor's output seam (#1855).

**The contract (CXO, ratified by Arch 2026-09-23):** *the floor may SUGGEST an
action in the imperative, but may only ASK "want me to X?" when X is armed this
turn.* An unarmed offer-question is a contract violation, not a style choice.

**The defect this closes.** PM, 2026-09-23, twice: the floor composed
*"Want me to add 'One Job' with the Design-in-Product/one-job repo to your
projects now?"*, PM answered *"Yes, please."*, and nothing was armed — so the
bare affirmative had nothing to bind to and the honest no-result fallback fired.
The acceptance predicate's exactly-armed rule (``acceptance.py``, #1694 (b)) is
the CORRECT half: it refused to bind a "yes" to a guessed action. The *offer*
was the lie, and the fix belongs on the producer side.

**Where this sits.** ``TestUnarmedAskSiteRatchet`` (#1766) censuses
question-emitting sites STATICALLY and names its own boundary honestly:

    "...and above all LLM FREE TEXT — the conversational floor can generate a
    question in prose at runtime; no static census can see it. Those surfaces'
    ask-only-when-armed compliance is Present, not Enforced."

This module is the RUNTIME closure of exactly that named gap. It inherits that
ratchet's literal-scanning discipline deliberately: anchored openers, a
sentence-final ``?``, no clever NLP. Narrow by construction — a false negative
leaves today's status quo, a false positive mangles legitimate copy.

**Scope (layer 1 only).** Detect and REWRITE. Actually arming the offer (so the
floor may legitimately ask) is layer 2 — #1856's extractor / the Inversion's
slot emission — and is deliberately not built here.
"""

import re
from typing import Callable, List, NamedTuple, Optional, Tuple

import structlog

logger = structlog.get_logger()


# ---------------------------------------------------------------------------
# The detector
# ---------------------------------------------------------------------------

# The narrow, ratified family (design 2026-09-23; Arch: "narrow detector,
# anchored family"). Four openers, each anchored at a sentence START, each
# requiring a sentence-final "?". Neighbours OUTSIDE the family are deliberately
# NOT covered — notably "Do you want me to ...?" and mid-sentence offers. That
# under-coverage is the status quo, not a regression, and widening the family is
# a reviewed decision, not a patch.
_OFFER_OPENERS: Tuple[str, ...] = (
    r"want\s+me\s+to",
    r"would\s+you\s+like\s+me\s+to",
    r"should\s+i",
    r"shall\s+i",
)

_OFFER_SENTENCE_RE = re.compile(
    r"^(?:" + "|".join(_OFFER_OPENERS) + r")\s+(?P<predicate>\S.*?)\s*\?$",
    re.IGNORECASE | re.DOTALL,
)

# Leading decoration a sentence may carry in floor markdown (list bullet,
# emphasis). Stripped before the anchored match so "- Want me to ...?" is still
# read as sentence-initial. Mirrors the ask-census's trailing-closer strip.
_LEADING_DECORATION = " \t\n>-*•_`—–"


class OfferSentence(NamedTuple):
    """One detected offer-shaped question, with its span in the source text."""

    start: int
    end: int
    sentence: str  # the sentence verbatim, decoration stripped
    predicate: str  # what was offered, e.g. "add 'One Job' ... to your projects now"


def _split_sentences(text: str) -> List[Tuple[int, int]]:
    """Literal sentence spans: end at ``.``/``!``/``?``/newline.

    Scanning, not parsing. Returns (start, end) offsets into ``text`` covering
    everything (whitespace between sentences belongs to the following span's
    lead, which the caller strips).

    One refinement, itself literal: ``.``/``!``/``?`` only terminate when the
    next character is whitespace or end-of-text, so ``docs/README.md`` and
    ``v1.2`` do not saw a sentence in half mid-token.
    """
    spans: List[Tuple[int, int]] = []
    start = 0
    last = len(text) - 1
    for i, ch in enumerate(text):
        if ch == "\n" or (ch in ".!?" and (i == last or text[i + 1].isspace())):
            spans.append((start, i + 1))
            start = i + 1
    if start < len(text):
        spans.append((start, len(text)))
    return spans


def detect_offer_questions(text: str) -> List[OfferSentence]:
    """Find every offer-shaped question in ``text``.

    Narrow by construction: the opener must start the sentence and the sentence
    must end in ``?``. Imperative suggestions ("Say: add project X") and non-offer
    questions ("What's the repo?") do not match.
    """
    if not text or "?" not in text:
        return []

    found: List[OfferSentence] = []
    for start, end in _split_sentences(text):
        raw = text[start:end]
        lead = len(raw) - len(raw.lstrip(_LEADING_DECORATION))
        candidate = raw[lead:].strip()
        if not candidate:
            continue
        match = _OFFER_SENTENCE_RE.match(candidate)
        if not match:
            continue
        # Map the stripped candidate back onto the source text.
        abs_start = start + lead
        abs_end = abs_start + len(candidate)
        found.append(
            OfferSentence(
                start=abs_start,
                end=abs_end,
                sentence=candidate,
                predicate=match.group("predicate").strip(),
            )
        )
    return found


# ---------------------------------------------------------------------------
# The rewrite
# ---------------------------------------------------------------------------

# The one-line imperative a user can satisfy in a single message. Kept BYTE-FOR-
# BYTE identical to CanonicalHandlers._ADD_PROJECT_IMPERATIVE (#1856); the copy
# lives in two places rather than importing the 5k-line handler module at floor
# response time, and `test_floor_unarmed_offer_seam_1855.py` asserts the two are
# equal so drift is loud rather than silent. Square brackets, not angle brackets
# (#1738: the web render swallows `<name>` as an unknown tag).
ADD_PROJECT_IMPERATIVE = "add project [name] with repo [owner/repo]"

# An owner/name repository token, as the app's own suggested phrasing prints it.
_REPO_TOKEN_RE = re.compile(r"\b(?P<repo>[\w.-]+/[\w.-]+)\b")

# A quoted span — the only name shape read out of the floor's own prose. If the
# model did not quote the name, no name is bound and the rewrite degrades to the
# bracket template rather than guessing which words were the name.
_QUOTED_NAME_RE = re.compile(r"['\"‘“](?P<name>[^'\"’”\n]{1,80})['\"’”]")

# Vocabulary that marks the predicate as an add-a-project offer.
_ADD_VERB_RE = re.compile(r"\b(?:add|create|set\s+up|start)\b", re.IGNORECASE)
_PROJECT_NOUN_RE = re.compile(r"\bprojects?\b", re.IGNORECASE)


def _bind_add_project_command(predicate: str) -> Optional[str]:
    """Compose the routable one-liner for an add-a-project offer, or None.

    ⚠️ Read over the FLOOR'S OWN composed sentence, never over a user utterance —
    this is not interpretation-layer extraction and adds no user-facing phrasing
    coverage. Two anchored captures (a quoted name, an ``owner/name`` token) and
    a hard round-trip gate.

    The round-trip gate is what keeps this from recommending a known-failing
    action (the #1108 shape): whatever command we are about to suggest is fed
    back through #1856's REAL ``extract_add_project_slots`` and must parse to the
    same slots. If it does not — or the extractor is unavailable — we return None
    and the caller falls back to the bracket template, which the app already
    suggests verbatim.
    """
    if not (_ADD_VERB_RE.search(predicate) and _PROJECT_NOUN_RE.search(predicate)):
        return None

    name_match = _QUOTED_NAME_RE.search(predicate)
    if not name_match:
        return None
    name = name_match.group("name").strip()
    if not name:
        return None

    repo_match = _REPO_TOKEN_RE.search(predicate)
    repo = repo_match.group("repo") if repo_match else None

    try:
        from services.onboarding.portfolio_service import (
            extract_add_project_slots,
            is_plausible_project_name,
        )
    except ImportError:  # pragma: no cover - degrade to the bracket template
        return None

    if not is_plausible_project_name(name):
        return None

    command = f"add project {name}"
    if repo:
        command = f"{command} with repo {repo}"

    # Round-trip: the suggestion must parse back to exactly what we bound.
    slots = extract_add_project_slots(command)
    if slots.get("name") != name or slots.get("repo") != repo:
        return None
    return command


# The catalog of offers whose action the floor CAN name as a routable command.
# One entry today (add-project, PM's live case). Layer 2 replaces this with real
# arming; until then it is the honest middle: a command we have verified parses.
_COMMAND_BINDERS: Tuple[Tuple[Callable[[str], Optional[str]], str], ...] = (
    (_bind_add_project_command, ADD_PROJECT_IMPERATIVE),
)


def rewrite_offer_sentence(predicate: str) -> str:
    """Turn an offered action into an imperative suggestion, never a yes/no ask.

    Three tiers, most specific first:

    1. **Bound command** — the action maps to a routable one-liner whose slots we
       found in the floor's own sentence AND which round-trips through the real
       extractor: ``To do that, say: add project One Job with repo owner/name.``
    2. **Bracket template** — the action family is recognised but the slots are
       not bound: ``To do that, say: add project [name] with repo [owner/repo].``
       The user keeps the affordance and the phrasing is one the app already
       teaches.
    3. **Degrade** — the action is not in the catalog. Name it, ask nothing, and
       suggest no command string we have not verified routes:
       ``If you'd like me to <predicate>, just tell me directly.``

    Never a bare deletion: every tier returns a sentence, so the reply cannot be
    left dangling around a hole where the question used to be.
    """
    for binder, template in _COMMAND_BINDERS:
        if not _matches_family(binder, predicate):
            continue
        bound = binder(predicate)
        return f"To do that, say: {bound or template}."
    return f"If you'd like me to {predicate}, just tell me directly."


def _matches_family(binder: Callable[[str], Optional[str]], predicate: str) -> bool:
    """Does this predicate belong to a catalog entry's action family?

    Separate from the binder's slot work: family membership decides tier 2 vs
    tier 3, slot binding decides tier 1 vs tier 2.
    """
    if binder is _bind_add_project_command:
        return bool(_ADD_VERB_RE.search(predicate) and _PROJECT_NOUN_RE.search(predicate))
    return False  # pragma: no cover - single-entry catalog


def enforce_armed_offers(
    text: str,
    *,
    armed_offer: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    intent_category: Optional[str] = None,
    intent_action: Optional[str] = None,
) -> Tuple[str, int]:
    """Rewrite unarmed offer-questions in ``text``; return (text, rewrites).

    ``armed_offer`` is the NAME of the rail that armed an offer for this turn
    (``"workflow_offer"`` / ``"last_offer"`` / ``"interview_offer"``), or None
    when nothing is armed as far as the seam can tell. When something IS armed
    the text passes through byte-for-byte: handlers' own armed offers (standup
    interview invitation, reminder clarify) are the reason the parameter exists.

    None is the FAIL-SAFE default on purpose. A door that cannot prove an arm
    degrades a question into an imperative suggestion — the user can still act,
    and nothing can mis-fire. The opposite default would reinstate the defect.

    Every rewrite is logged with the ORIGINAL sentence so #1595's corpus lane
    sees each instance rather than the rewrite silently absorbing the evidence
    of how often the floor does this (Arch, ratifying: "the correct
    default-to-corpus move").
    """
    if not text:
        return text, 0

    offers = detect_offer_questions(text)
    if not offers:
        return text, 0

    if armed_offer:
        logger.info(
            "floor_offer_question_armed",
            armed_offer=armed_offer,
            offers=len(offers),
            session_id=session_id,
            user_id=user_id,
            intent_category=intent_category,
        )
        return text, 0

    out = text
    # Right to left so earlier spans keep their offsets.
    for offer in reversed(offers):
        replacement = rewrite_offer_sentence(offer.predicate)
        out = out[: offer.start] + replacement + out[offer.end :]
        logger.warning(
            "floor_unarmed_offer_rewritten",
            original_sentence=offer.sentence,
            offered_action=offer.predicate,
            rewritten_sentence=replacement,
            session_id=session_id,
            user_id=user_id,
            intent_category=intent_category,
            intent_action=intent_action,
        )
    return out, len(offers)
