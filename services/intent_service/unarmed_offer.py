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

**Layer 1 (2026-09-23).** Detect and REWRITE: an offer-question the floor has
not armed becomes an imperative suggestion.

**Layer 2 (2026-09-24, Arch-approved — this module's ``arm`` outcome).** The
other half of CXO's sentence: the floor may ASK when X *is* armed this turn, so
where tier 1 genuinely BINDS a command the seam now ARMS it and lets the
question stand. The arming precondition is exactly tier 1's existing
round-trip: a catalogued action family, slots read out of the floor's OWN
sentence, and a composed imperative that parses back through the real
extractor. Anything less is still a suggestion. The arm lands in the #846
one-slot store as a ``confirm_pending_action`` record whose ``pending_action``
carries the COMMAND STRING (``kind`` = ``floor_bound_offer``) — on a crisp
accept the carrier re-runs that text through the ordinary rail, so the action
executes by exactly the path the user would have taken by typing it. No second
implementation of any action lives here.

⚠️ **Without an arming callback this module behaves as layer 1 did, exactly.**
The callback is the rollback switch: a door that does not pass one cannot arm.
"""

import re
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple

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
    r"do\s+you\s+want\s+me\s+to",  # fifth opener, Arch + CXO ratified 2026-09-23 evening
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


def _is_add_project_family(predicate: str) -> bool:
    """Family membership for the add-a-project catalogue entry.

    Separate from the binder's slot work: family membership decides tier 2 vs
    tier 3, slot binding decides tier 1 vs tier 2 (and, in layer 2, arm vs
    rewrite).
    """
    return bool(_ADD_VERB_RE.search(predicate) and _PROJECT_NOUN_RE.search(predicate))


class CommandFamily(NamedTuple):
    """One catalogued action the floor may name — and, on a bind, ARM.

    ``name`` is both the family's identity in tests/logs and the rail action
    recorded on the armed ``pending_action``. ⚠️ **Joining this catalogue has
    three requirements, all testable** (#1855 layer 2): a real extractor the
    composed command round-trips through, a rail path that executes from the
    COMMAND TEXT alone (the carrier re-runs the string; it cannot hand a
    handler a pre-resolved Intent), and a round-trip test in
    ``test_floor_armed_offer_layer2_1855.py`` — whose denominator pin asserts
    this catalogue is exactly the tested set.

    ⚠️ **Non-destructive families only.** The carrier's re-run classifies the
    command afresh, so the ``destructive_confirmed`` marker (#1190) cannot ride
    it — a family whose handler needs that marker to avoid asking its own
    second confirmation must not be catalogued until arming carries an Intent.
    An explicit imperative is EXECUTE framing at the #1509 consent gate, which
    is why a non-destructive WRITE like add-project executes in one turn.
    """

    name: str
    matches: Callable[[str], bool]
    bind: Callable[[str], Optional[str]]
    template: str


# The catalogue of offers whose action the floor CAN name as a routable command
# — and, when the slots bind, ARM. One entry today (add-project, PM's live
# case). Growth is the only extension point, and it is ratchet-shaped: see
# CommandFamily's three requirements.
COMMAND_FAMILIES: Tuple[CommandFamily, ...] = (
    CommandFamily(
        name="add_project",
        matches=_is_add_project_family,
        bind=_bind_add_project_command,
        template=ADD_PROJECT_IMPERATIVE,
    ),
)


def bind_catalogued_command(predicate: str) -> Optional[Tuple[CommandFamily, str]]:
    """The tier-1 bind, exposed: (family, command) or None.

    This IS the arming precondition — the seam arms exactly when this returns a
    pair. Nothing is guessed: the family must match, the slots must come out of
    the floor's own sentence, and the composed command must round-trip through
    the family's real extractor.
    """
    for family in COMMAND_FAMILIES:
        if not family.matches(predicate):
            continue
        command = family.bind(predicate)
        if command:
            return family, command
        return None  # family matched, slots did not bind → tier 2, never an arm
    return None


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
    for family in COMMAND_FAMILIES:
        if not family.matches(predicate):
            continue
        bound = family.bind(predicate)
        return f"To do that, say: {bound or family.template}."
    return f"If you'd like me to {predicate}, just tell me directly."


# ---------------------------------------------------------------------------
# The arm (#1855 layer 2)
# ---------------------------------------------------------------------------

# The offer KIND this module's armed records carry. Declared here, beside the
# binder that produces it, the way every other kind is declared in its own home
# module (CONSENT_CHECK_KIND, DRAFTED_ISSUE_KIND, REMINDER_TIME_QUESTION_KIND…).
# ``destructive_confirm._CONFIRM_KINDS`` carries the literal (its home module
# imports THIS one's siblings, so importing back would be circular) and the
# layer-2 suite pins the two against each other.
FLOOR_BOUND_OFFER_KIND = "floor_bound_offer"

# ⚠️ COPY SURFACE, CXO-owned. Ruled 2026-09-24 (acceptance contract §3, the
# quotability test): the rendered ask must state the same named parameters that
# compose the stored command, explicitly enough that a user reading only the
# question could reconstruct what they are confirming. The seam therefore
# REPLACES the model's offer sentence with this form before arming, so what the
# user read and what is bound cannot drift. One placeholder: ``{command}``.
# The property, not this string, is the rule — a second family gets whatever
# form states ITS parameters. Setting this to None restores the model's own
# wording (layer-1 behavior for the question text; arming unchanged).
ARMED_QUESTION_FORM: Optional[str] = "Want me to {command}? Say yes, or tell me otherwise."


def build_floor_bound_offer_record(*, command: str, question: str, action: str) -> Dict[str, Any]:
    """The #846 record an armed floor offer stores (the #1190 carrier's shape).

    ``question`` is the RENDERED ask — the sentence the user is reading this
    turn. It rides under the key ``question`` because that is the key the
    acceptance seam actually threads into ``evaluate_acceptance`` as
    ``armed_question`` (#1665); ``offer_message``/``ask_rendered`` mirror it
    under the design's own names so the record reads as the design describes
    it. At the NAMED_OBJECT tier an accept against a record with no rendered
    ask is REFUSED (Arch condition (a)) — this record can never be that record.
    """
    from services.intent_service.destructive_confirm import (
        CONFIRM_PENDING_ACTION_WORKFLOW,
    )

    return {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        # #1665: the ALREADY-RENDERED ask, verbatim, stored at arm time.
        "question": question,
        "offer_message": question,
        "ask_rendered": True,
        "pending_action": {
            "kind": FLOOR_BOUND_OFFER_KIND,
            # The BINDING is the command string, not a parsed guess: the
            # carrier re-runs it through the ordinary rail on accept.
            "command": command,
            "action": action,
            "summary": command,
        },
        "decline_message": (f"No problem — I haven't done it. When you want it, say: {command}."),
    }


def _try_arm(
    text: str,
    offer: OfferSentence,
    arm_offer: Callable[[Dict[str, Any]], bool],
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    intent_category: Optional[str] = None,
    intent_action: Optional[str] = None,
) -> Optional[str]:
    """Arm this offer and return the text to render, or None to fall through.

    None means "not armable" and the caller rewrites — the fail-safe direction
    in every failure mode there is: no bind, a callback that refuses, a
    callback that raises. An offer we could not arm must never be left standing
    as a question, because that is precisely the defect #1855 closes.
    """
    bound = bind_catalogued_command(offer.predicate)
    if bound is None:
        return None
    family, command = bound

    sentence = offer.sentence
    out = text
    if ARMED_QUESTION_FORM:
        sentence = ARMED_QUESTION_FORM.format(command=command)
        out = text[: offer.start] + sentence + text[offer.end :]

    record = build_floor_bound_offer_record(command=command, question=sentence, action=family.name)
    try:
        armed = arm_offer(record)
    except Exception as exc:  # silent-ok: LOGGED, and it degrades to the rewrite — an arming store that raises must not cost the user their reply, and the fallback is the fail-safe direction (no question stands)
        logger.warning(
            "floor_offer_arm_failed",
            error=str(exc),
            command=command,
            session_id=session_id,
            user_id=user_id,
        )
        return None
    if not armed:
        logger.warning(
            "floor_offer_arm_refused",
            command=command,
            session_id=session_id,
            user_id=user_id,
        )
        return None

    logger.info(
        "floor_offer_armed",
        command=command,
        family=family.name,
        question=sentence,
        normalized=bool(ARMED_QUESTION_FORM),
        session_id=session_id,
        user_id=user_id,
        intent_category=intent_category,
        intent_action=intent_action,
    )
    return out


def enforce_armed_offers(
    text: str,
    *,
    armed_offer: Optional[str] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    intent_category: Optional[str] = None,
    intent_action: Optional[str] = None,
    arm_offer: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> Tuple[str, int]:
    """Enforce ask-only-when-armed in ``text``; return (text, rewrites).

    ``armed_offer`` is the NAME of the rail that armed an offer for this turn
    (``"workflow_offer"`` / ``"last_offer"`` / ``"interview_offer"``), or None
    when nothing is armed as far as the seam can tell. When something IS armed
    the text passes through byte-for-byte: handlers' own armed offers (standup
    interview invitation, reminder clarify) are the reason the parameter exists.

    None is the FAIL-SAFE default on purpose. A door that cannot prove an arm
    degrades a question into an imperative suggestion — the user can still act,
    and nothing can mis-fire. The opposite default would reinstate the defect.

    ``arm_offer`` is the layer-2 ARMING CALLBACK (#1855 layer 2): given a
    ready-built #846 record it stores it and returns True. Passing None keeps
    LAYER-1 BEHAVIOR EXACTLY — that is the rollback switch, and the fail-safe
    default. Three outcomes now, in order:

    * **pass** — something is already armed this turn (``armed_offer``), or no
      offer-shaped question is present.
    * **arm** — a callback is present, exactly one offer-question is present,
      and tier 1 BINDS its command (catalogued family + slots from the floor's
      own sentence + round-trip through the real extractor). The question
      stands (optionally normalized to ``ARMED_QUESTION_FORM``), the record is
      armed, ``floor_offer_armed`` is logged, and the count is 0 — an armed
      question is not a rewrite. The seam does NOT re-scan its own armed
      question: an armed offer-question is the legitimate form.
    * **rewrite** — everything else, layer 1 unchanged.

    ⚠️ The arm is deliberately limited to a SINGLE detected offer. Two
    questions in one reply would make "which one did yes bind to?" ambiguous,
    and the #846 store holds one slot — so a multi-offer reply is rewritten
    rather than half-armed.

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

    if not armed_offer and arm_offer is not None and len(offers) == 1:
        armed_text = _try_arm(
            text,
            offers[0],
            arm_offer,
            session_id=session_id,
            user_id=user_id,
            intent_category=intent_category,
            intent_action=intent_action,
        )
        if armed_text is not None:
            return armed_text, 0

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
