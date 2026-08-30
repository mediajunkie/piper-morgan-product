"""#1571 — the drafted-issue pending binding (the #1190 carrier's named next consumer).

PM's live sequence (verdict-7 tail 2026-08-10; repro'd in the 2026-08-15
baseline): the compose flow builds a draft, PM says "Please file it as is" —
and then: double-confirm friction ("want me to go ahead?"), a FABRICATED
"Filed! … #[issue number]" with the template placeholder showing, and a retry
that LOST the whole draft ("What should the issue be about?").

The fix binds the draft the moment the #1510 collaborate gate renders it:

- The collaborate turn in ``_handle_create_issue`` ARMS a pending action in
  the #846 session-scoped offer store (kind ``drafted_issue``) carrying the
  ORIGINAL classified Intent — the same deferred-action carrier shape #1190
  documents in ``destructive_confirm.py`` (whose ``TODO(#1571)`` names this
  module as the next consumer).
- "file it" / "file it as is" / "please file it" / a generic accept IS the
  confirmation — ONE turn, no second ask. Acceptance delegates to
  ``run_confirm_pending_action_workflow`` (the #1190 acceptance mirror): the
  original Intent is re-dispatched through the create_issue rail entry with
  the ``destructive_confirmed`` context marker, which the collaborate gate
  now honors as consent-already-given (the #1509 principle: the explicit
  confirmation IS the consent — never ask twice).
- Success copy derives from the ACTUAL tool result (the rail handler's
  "Created issue #N in repo: title" — the number comes from GitHub's
  response), never a template slot.
- FAILURE keeps the draft bound: any outcome that did not verifiably create
  (dispatch error, degraded-connector copy, clarification ask) re-arms the
  SAME pending record and says so honestly — retry does not lose the draft.
- Off-intent abandons per the carrier's rules (the pop already removed the
  offer; normal processing answers the new message). Declines/bare exits
  drop the draft with honest copy via the generic decline path.

#1627 (2026-08-15, round 2): while the draft's open question ("What should
the body say…?") is on the table, a PROSE ANSWER binds to the draft — it is
consumed at this seam (which runs above the whole 4-surface routing chain)
and never reaches any classification surface. The live theft: PM's long
body answer contained "delete …" and "(a destructive action)", and surface
1's greedy portfolio pattern (#1527 family, ``\\bdelete\\s+…(.+)``) claimed
the turn — "I couldn't find a project called '(a destructive action)…'" —
losing the composed body. The draft flow is floor-composed prose, not a
registered gathering process, so the #1623 mid-interview hold could not
cover it; this is the draft flow's own hold. It is NOT a turn lock:
file/accept phrases still file, declines and bare exits still drop the
draft honestly, and clearly-imperative asks still route normally
(abandoning the draft — the carrier's documented off-intent rule). See
``is_body_prose_answer`` for the discrimination and its stated limits.

#1630 (2026-08-15, the unarmed face of the same theft): "help me write a
ticket" with NO extractable subject used to arm nothing (no subject = no
draft yet), so the user's answer to "What's it about?" was a bare prose
turn — the exact #1627 steal shape, one turn earlier in the flow, with
nothing holding it above the greedy chain. The collaborate turn now arms a
minimal SUBJECTLESS carrier (``build_drafted_issue_offer`` with
``subject=None``) so the #1627 hold covers the first answer too: the FIRST
bound prose names the draft (``derive_subject_from_prose`` → title, and
``intent.context["title"]`` so the create rail files it — the subjectless
original message slot-fills nothing) and seeds the body per the existing
append semantics. Same discriminator, same seam, same exits — the
subjectless copy still teaches no file phrase until the draft has content
(#1571's never-teach-unbound rule).

#1649 (2026-08-18, teach-then-ignore): PM gave BOTH slots explicitly —
'open a new issue, with the subject "issue body test" and description "…"'
— and still got "What's it about?", then a truncated prose-derived title:
no extraction knew the subject/description marker words, so the gate armed
a subjectless carrier and the stated slots were discarded. The fix is at
the arm seam: ``_slotfill_issue_request`` now extracts quoted (and
anchored-unquoted) subject/title/called/named and description/body forms
from the ORIGINAL ask; the gate mirrors them into ``intent.context`` and
seeds them into the carrier (``build_drafted_issue_offer(body=…)``). Both
slots given → the shaped draft presents ready for "file it as is", no
question. One slot given → ask only for the gap; a body-only draft's first
bound prose is the TITLE answer (named, not appended — see
``_bind_body_prose``). No explicit slots → the #1630 derive-from-prose
path, unchanged. Extraction is deterministic and anchored to the stated
marker words — loose nouns are never scavenged into a title (a wrong
confident title is worse than the question).

Deliberately NOT built (flagged for Lead): instruction-shaped draft
refinement ("make the title snappier", "add a labels section"). #1627 binds
prose CONTENT (appended to the body verbatim); it does not interpret
editing instructions — an anchored-imperative refinement ask still abandons
the binding. Interpreting edits over an evolving floor-composed draft needs
a durable draft store and is a different design (the
routing-moratorium/corpus half of #1571 lives there too; durable fix is
Inversion Phase 2 context-carrying).

#1648 (PM live 2026-08-18, round 4 — the fabrication face): PM said "file
as is thanks" with the draft armed. The detector missed the variant (the
verb had no object: "file **as is**", not "file **it** as is"), the turn
read as an anchored EXECUTE imperative, fell through this seam as
off-intent, reached the LLM classifier, and the FLOOR then roleplayed the
entire filing across four turns ("Filed in test-piper-morgan. The issue is
in there now." — zero writes, no issue number, verified against GitHub).
Two fixes here, one at the prompt (see conversational_floor's action-claims
contract):

- ``_FILE_COMMAND_RE`` broadened: the draft-referring object is optional
  when an "as is" tail carries the reference; trailing pleasantries
  ("thanks", "thank you", "please") and short affirmative lead-ins ("yes,
  go ahead and file it") are absorbed. Still anchored full-message — a NEW
  ask ("file an issue about X") or "file" inside prose never matches (the
  #1631 lesson runs the other way here).
- The honest near-miss fallback: a turn that is file/submit-shaped ABOUT
  this draft but matches neither the file command, prose, accept/decline,
  nor exit RE-ASKS honestly and RE-ARMS — never a silent abandon into the
  routing chain mid-compose (where the floor is the surface most likely to
  claim it, and the floor cannot file anything). Genuinely-new file asks
  (a subject of their own: "file a bug about X") and every other command
  family still abandon and route normally per the carrier's rules.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

import structlog

from services.domain.models import Intent
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)

logger = structlog.get_logger(__name__)

DRAFTED_ISSUE_KIND = "drafted_issue"

# Full-message file commands (the phrases PM was TAUGHT and the phrases PM
# actually typed). Conservative: verb + a draft-referring object OR an
# "as is" tail (either carries the reference — #1648: PM's live "file as is
# thanks" had the tail but no object), optional politeness lead-in and
# trailing pleasantries, optional "in owner/repo" (the original #1571
# incident phrase — with a draft pending it is unambiguous and the named
# repo overrides the draft's). Anchored full-message so a NEW ask ("file an
# issue about X") never reads as accepting the old draft, and "file" inside
# prose never matches (#1631's lesson, run the other way).
_FILE_COMMAND_RE = re.compile(
    r"^(?:(?:please|yes|yeah|yep|sure|ok(?:ay)?)[,!\s]+)*"
    r"(?:go\s+ahead\s+(?:and\s+)?)?(?:just\s+)?"
    r"(?:file|create|submit|open)"
    r"(?:"
    r"\s+(?:it|this|that|the\s+(?:issue|ticket|draft))(?:\s+as[\s\-]is)?"
    r"|\s+as[\s\-]is"
    r")"
    r"(?:\s+in\s+(?P<repo>[\w.\-]+/[\w.\-]+))?"
    r"(?:[\s,!.]*(?:please|thanks|thank\s+you|thx|ty|cheers))*"
    r"\s*[.!]*$",
    re.IGNORECASE,
)


def detect_file_command(message: Optional[str]) -> Optional[Dict[str, Any]]:
    """Return ``{"repo": <override-or-None>}`` when the whole message is a
    file-this-draft command; ``None`` otherwise."""
    if not message:
        return None
    m = _FILE_COMMAND_RE.match(message.strip())
    if not m:
        return None
    return {"repo": m.group("repo")}


# --- #1627: mid-compose prose binding --------------------------------------

# A turn at/above soft_invocation.PROSE_LENGTH_FLOOR (or any multi-line
# turn) is prose regardless of how it opens. Body answers often LEAD with an
# imperative-looking verb ("Add a guard so that deleting a project…") or a
# politeness word the unanchored accept row would claim ("Please note
# that…"); commands are short and single-line — nobody types 200 characters
# of "close issue #108". The floor is deliberately above every taught
# command phrase and below PM's live stolen answer by a wide margin.
# #1631 lifted this shape check into soft_invocation (``is_prose_reply``,
# consulted by ``detect_offer_response`` itself) so EVERY armed offer kind
# gets it; ``is_body_prose_answer`` below imports the shared helper — one
# threshold, no drift.

# Anchored-imperative supplement: verb families the shared collaborate-gate
# execute check (collaboration_gate._EXECUTE_RE) deliberately omits — reads
# and destructives are consented elsewhere, so that regex never needed them.
# Mid-compose they are exactly the "clearly imperative unrelated ask" that
# must keep routing normally ("close issue #108", "list my reminders",
# "delete my reminders" — the #1527 phrase itself, as a command). Prefix
# structure mirrors _EXECUTE_RE's (politeness/address, go-ahead, can-you).
_COMMAND_SUPPLEMENT_RE = re.compile(
    r"^\s*"
    r"(?:(?:please|hey|hi|ok(?:ay)?|piper)[,!\s]+)*"
    r"(?:go\s+ahead\s+and\s+)?"
    r"(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?)?"
    r"(?:close|reopen|delete|remove|archive|restore|cancel|stop"
    r"|list|show|search|find|fetch|get|check|tell|give)\b",
    re.IGNORECASE,
)


def is_command_shaped(message: Optional[str]) -> bool:
    """#1648 — shared anchored-imperative read for armed-carrier seams: is
    this turn a command by shape (the collaborate-gate execute families, or
    the close/read/destructive supplement above)? Command-shaped turns are
    the carrier's documented off-intent exit — they abandon the binding and
    route normally. Factored out so the reminder-side carriers apply the
    SAME discrimination (one shape read, no drift)."""
    text = (message or "").strip()
    if not text:
        return False
    from services.intent_service.collaboration_gate import (
        FRAMING_EXECUTE,
        classify_framing,
    )

    if classify_framing(text) == FRAMING_EXECUTE:
        return True
    return bool(_COMMAND_SUPPLEMENT_RE.match(text))


# #1648: file/submit-headed near-misses. With a draft armed, a short
# imperative headed by the file family is ABOUT this draft unless it carries
# its own subject (a new ask). "file"/"submit" have no other deterministic
# meaning in the product, so a variant the anchored command regex doesn't
# know ("file the sucker", "file that thing now") would otherwise abandon
# silently into the routing chain — where the most likely claimant is the
# floor, which cannot file anything (the #1648 roleplay incident). create/
# open stay OUT of the near-miss head: "create a project…", "open the
# settings page" are genuine other asks.
_NEAR_MISS_FILE_RE = re.compile(
    r"^\s*(?:(?:please|yes|yeah|yep|sure|ok(?:ay)?|hey|hi|piper)[,!\s]+)*"
    r"(?:go\s+ahead\s+(?:and\s+)?)?(?:just\s+)?"
    r"(?:file|submit)\b",
    re.IGNORECASE,
)

# A file-family turn that names its OWN subject is a NEW ask, not a
# near-miss for this draft ("file an issue about X", "file a bug for the
# login timeout") — it abandons and routes normally, exactly as before.
_NEW_ASK_MARKER_RE = re.compile(
    r"\b(?:an?\s+(?:new\s+)?(?:issue|ticket|bug|story|task)\b|about\b|for\s+the\b)",
    re.IGNORECASE,
)


def is_file_near_miss(message: Optional[str]) -> bool:
    """#1648 — True when a turn is file/submit-shaped about the armed draft
    but didn't parse as a full file command: re-ask honestly, never abandon
    silently. False for new asks carrying their own subject."""
    text = (message or "").strip()
    if not text:
        return False
    if not _NEAR_MISS_FILE_RE.match(text):
        return False
    return not _NEW_ASK_MARKER_RE.search(text)


def is_body_prose_answer(message: Optional[str]) -> bool:
    """#1627 — with a drafted issue armed and its body question open, is this
    turn a prose ANSWER (bind to the draft) rather than a deliberate exit or
    an explicit command (fall through to the generic flow / normal routing)?

    Deterministic, and deliberately biased toward binding: a mis-bound
    command is recoverable (the draft re-arms, nothing files, the copy shows
    exactly what was captured), while a mis-routed body answer loses the
    composed prose to whichever greedy surface claims it — the live #1627
    failure. Known limits, stated honestly:

    - A SHORT turn that opens with an imperative verb from either anchored
      check ("add steps to reproduce") reads as a command and abandons the
      draft — instruction-shaped refinement is deliberately not built (see
      module docstring).
    - A question mid-compose ("what would make a good body?") is not an
      anchored imperative, so it BINDS as body text rather than being
      answered. Visible and recoverable; the alternative (routing it)
      silently abandons the draft.
    - A LONG turn that is genuinely a new imperative ask binds as prose —
      the length override is what protects body answers that open with
      "Please…"/"Add…", and it cannot tell those apart from a 200-character
      command. Interim guard; the durable fix is Inversion Phase 2
      context-carrying.
    """
    text = (message or "").strip()
    if not text:
        return False
    from services.intent_service.destructive_confirm import detect_bare_exit

    if detect_bare_exit(text):
        return False  # "cancel" / "stop" / "forget it" → honest decline
    from services.intent_service.soft_invocation import (
        detect_offer_response,
        is_prose_reply,
    )

    if is_prose_reply(text):
        # Checked BEFORE the accept/decline consult on purpose: the
        # unanchored accept/decline rows ("^please\s", "\bnot today\b")
        # match into long prose and would file or drop a half-shaped draft
        # off a substring of the body answer. (#1631 taught
        # detect_offer_response the same shape override, but this check must
        # stay FIRST here and cannot be delegated: prose means BIND to the
        # draft — without it a long "Add a guard…" answer would fall through
        # to the anchored-imperative checks below and route away as a
        # command.)
        return True

    if detect_offer_response(text) is not None:
        return False  # short accept/decline — the generic seam's business
    if is_command_shaped(text):
        # anchored imperative (create/update/remind families via the
        # collaborate-gate execute check; close/read/destructive families
        # via the supplement) — #1648 factored both into is_command_shaped,
        # same checks in the same order.
        return False
    return True


# #1630: a derived title is a HEADLINE, not the whole answer — cap it where
# GitHub titles stay scannable and let the body carry the prose verbatim.
_TITLE_MAX_CHARS = 80

# First sentence of a line: everything up to the first terminal punctuation
# mark followed by whitespace (or end). Deterministic-good-enough — an
# abbreviation period mid-sentence shortens the title, never loses prose
# (the body always carries the full answer).
_FIRST_SENTENCE_RE = re.compile(r"(.+?[.!?])(?:\s|$)")


# #1649 REWORK (PM live 2026-08-29, v64): slot-ANSWER extraction. PM answered
# the title re-ask with `title should be 'Login timeout' as I indicated in my
# initial request` and the ENTIRE correction sentence became the title — the
# bind path had no notion of a quoted value inside an answer. The rule: a
# quoted value in a slot-answer turn IS the value (both straight and curly,
# both single and double), and metacommentary ("should be", "as I
# indicated…") never enters the slot. Deterministic pure functions so they
# lift cleanly into the SessionSnapshot draft-state consumers (Inversion).
_ANSWER_QSPAN = "(?:\"([^\"]+)\"|“([^”]+)”|'([^']+)'|‘([^’]+)’)"
# Marker-led dictation, ANCHORED at the turn's start so quoted spans floating
# inside genuine body prose ("Users see 'session expired' after login") are
# never stolen — a body answer is not a title answer.
_ANSWER_MARKER_QUOTED_RE = re.compile(
    r"^\s*(?:ok(?:ay)?[,.\s]+|sure[,.\s]+|no[,.\s]+)?(?:please\s+)?"
    r"(?:(?:make|set|use|change)\s+)?(?:the\s+|its\s+)?(?:title|subject)\b\s*"
    r"(?:(?:should|must|could|can|will)\s+be\s+|(?:of|is|being|to)\s+|[:=,]\s*)?" + _ANSWER_QSPAN,
    re.IGNORECASE,
)
# The whole turn is one quoted span (plus optional terminal punctuation):
# `'Login timeout'` as the complete answer.
_ANSWER_BARE_QUOTED_RE = re.compile(r"^\s*" + _ANSWER_QSPAN + r"[\s.!?]*$")
# Unquoted dictation — only the unambiguous dictation verbs (`should/must
# be`, `set … to`), never bare `is`: "the subject is being spammed…" is
# prose about the issue, not a title dictation.
_ANSWER_MARKER_UNQUOTED_RE = re.compile(
    r"^\s*(?:(?:please\s+)?(?:make|set|change)\s+)?(?:the\s+|its\s+)?"
    r"(?:title|subject)\s+(?:(?:should|must)\s+be|to)\s+(.+?)\s*$",
    re.IGNORECASE,
)
# Trailing metacommentary on an unquoted dictation: ", as I indicated in my
# initial request", "like I said", "per my first message".
_ANSWER_METACOMMENT_RE = re.compile(
    r",?\s*(?:(?:exactly\s+)?(?:as|like)\s+I\s+\w+.*|per\s+my\s+.*)$",
    re.IGNORECASE,
)


def extract_title_answer(prose: str) -> Optional[str]:
    """The explicitly-DICTATED title inside a slot-answer turn, or None.

    None means the turn dictates nothing explicitly — the caller falls back
    to ``derive_subject_from_prose`` (bare answers like `Login timeout`
    keep titling the draft verbatim exactly as before)."""
    text = (prose or "").strip()
    if not text:
        return None
    for pattern in (_ANSWER_MARKER_QUOTED_RE, _ANSWER_BARE_QUOTED_RE):
        m = pattern.match(text)
        if m:
            value = next((g for g in m.groups() if g is not None), "").strip()
            if value:
                return value
    m = _ANSWER_MARKER_UNQUOTED_RE.match(text)
    if m:
        value = _ANSWER_METACOMMENT_RE.sub("", m.group(1))
        value = value.strip().strip("\"'‘’“”").rstrip(" .!?,;:").strip()
        if value:
            return value
    return None


def derive_subject_from_prose(prose: str) -> str:
    """#1630 — name a subjectless draft from its first bound prose answer.

    The subjectless ask ("help me write a ticket") slot-fills no title, so
    the first thing the user says ABOUT the issue is the best available
    subject: first non-empty line, trimmed to its first sentence, capped at
    a word boundary. The full prose still lands in the body verbatim — the
    title is a headline over it, and the user can keep shaping both before
    anything files.
    """
    first_line = next((ln.strip() for ln in prose.strip().splitlines() if ln.strip()), "")
    m = _FIRST_SENTENCE_RE.match(first_line)
    candidate = (m.group(1) if m else first_line).strip()
    candidate = candidate.strip("\"'‘’“”").rstrip(" .!?,;:")
    if len(candidate) > _TITLE_MAX_CHARS:
        cut = candidate[:_TITLE_MAX_CHARS].rsplit(" ", 1)[0].rstrip(" ,;:—-")
        candidate = f"{cut}…"
    return candidate


def _draft_summary(subject: Optional[str], repository: Optional[str]) -> str:
    """The carrier's one-line summary (what the generic confirm copy names)."""
    summary = f'file the drafted issue "{subject}"' if subject else "file the drafted issue"
    if repository:
        summary += f" in {repository}"
    return summary


def build_drafted_issue_offer(
    intent: Intent,
    subject: Optional[str],
    repository: Optional[str] = None,
    body: Optional[str] = None,
    question: Optional[str] = None,
) -> Dict[str, Any]:
    """The #846 pending-offer record binding a rendered draft (the generic
    deferred-action carrier shape documented in ``destructive_confirm.py``).

    ``subject=None`` (#1630) arms the minimal SUBJECTLESS carrier: the ask
    had no extractable subject, so the draft has no title yet — the first
    bound prose answer names it (see ``_bind_body_prose``).

    ``body`` (#1649) seeds an explicitly-STATED description (`…and
    description "Y"`) into the draft at arm time — the caller mirrors it
    into ``intent.context["description"]`` so "file it as is" files it.
    The key is present only when given, preserving the minimal-carrier
    shape #1630 pins; later prose binds append to it per the existing
    semantics.

    ``question`` (#1665): the ALREADY-RENDERED open ask the caller is about
    to surface (``collaboration_gate.draft_open_question`` — the same
    function the response copy embeds, so the stored string is a verbatim
    substring of what the user saw). Stored, never re-rendered; the re-arm
    seams below update it as the draft's open question changes state."""
    summary = _draft_summary(subject, repository)
    draft: Dict[str, Any] = {"title": subject, "repository": repository}
    if body:
        draft["body"] = body
    return {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": DRAFTED_ISSUE_KIND,
            "action": intent.action,
            "intent": intent,
            "summary": summary,
            "draft": draft,
        },
        "decline_message": (
            "Okay — I've set that draft aside. Nothing was filed. "
            "Ask me again anytime if you want to shape it back up."
        ),
    }


_DRAFT_RETAINED_LINE = (
    'Your draft is still here — say "file it" to try again, ' 'or "no" to drop it.'
)

# #1665: the open ask after a prose bind — one constant, embedded in the bind
# reply AND stored on the re-armed record (same string, no drift).
_POST_BIND_ASK = (
    "Keep going if there's more to add. When it's ready, say "
    '"file it as is" — or "no" to set the draft aside.'
)

# #1665: the open ask on the #1650 near-accept re-ask turn.
_NEAR_ACCEPT_ASK = 'Say "file it as is" to file this draft, or "no" to set it aside.'


def _reask_near_miss(
    pending_offer: Dict[str, Any],
    pending_action: Dict[str, Any],
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Dict[str, Any]:
    """#1648 — a file-shaped turn the detector didn't parse: say honestly
    that nothing was filed, name the moves that work, and RE-ARM the same
    offer. Never a silent abandon into the routing chain mid-compose."""
    draft = pending_action.get("draft") or {}
    has_content = bool((draft.get("title") or "").strip() or (draft.get("body") or "").strip())
    # #1571's never-teach-unbound rule: only teach the file phrase when the
    # draft actually has content behind it.
    if has_content:
        moves = (
            'Say "file it as is" to file it, keep adding content, '
            'or say "no" to set the draft aside.'
        )
    else:
        moves = (
            "Tell me what the issue should be about first — " 'or say "no" to set the draft aside.'
        )

    # #1665: the re-armed record's open question is this turn's re-ask copy
    # (set BEFORE the store so what's stored is what's said).
    pending_offer["question"] = moves
    rearmed = True
    try:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
    except Exception as e:  # silent-ok: #1648 — a store failure must not crash the turn; logged ERROR, and the copy below never claims a retained draft that isn't there
        logger.error("drafted_issue_near_miss_rearm_failed", error=str(e))
        rearmed = False

    logger.info(
        "drafted_issue_file_near_miss_reasked",
        session_id=session_id,
        rearmed=rearmed,
    )

    if not rearmed:
        return {
            "message": (
                "I didn't catch that as a file-it command, and I couldn't "
                "keep the draft bound either — nothing was filed. Ask me to "
                "draft the issue again and we'll rebuild it."
            ),
            "intent_data": _retained_intent_data(pending_action),
        }
    intent_data = _retained_intent_data(pending_action)
    intent_data["drafted_issue_reasked"] = True
    return {
        "message": (
            "I didn't catch that as a file-it command or more content for "
            f"the draft — nothing has been filed. {moves}"
        ),
        "intent_data": intent_data,
        "requires_clarification": True,
    }


def _retained_intent_data(pending_action: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "category": "execution",
        "action": pending_action.get("action") or "create_issue",
        "confidence": 1.0,
        "drafted_issue_pending": True,  # _apply_soft_offer clobber guard
        "drafted_issue_retained": True,
    }


def _bind_body_prose(
    pending_offer: Dict[str, Any],
    pending_action: Dict[str, Any],
    prose: str,
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Dict[str, Any]:
    """#1627 — append a prose answer to the bound draft's body, re-arm the
    SAME offer, and show the draft honestly. Consuming the turn here is the
    hold: no classification surface ever sees the prose."""
    draft = pending_action.setdefault("draft", {})
    # #1630: a SUBJECTLESS draft (armed at the "help me write a ticket" ask,
    # no extractable subject) is NAMED by its first bound answer — the prose
    # becomes both the subject (headline) and the body seed.
    titled_now = False
    explicit_title = False
    if not (draft.get("title") or "").strip():
        # #1649 REWORK (PM live 2026-08-29, v64): a slot-answer turn that
        # DICTATES its value ("title should be 'Login timeout' as I
        # indicated…") gives exactly the dictated string — the quoted value
        # wins over the raw message, and the metacommentary around it never
        # enters the slot. Only when the turn dictates nothing explicitly
        # does the derive-from-prose headline apply (bare `Login timeout`
        # answers keep working verbatim).
        explicit = extract_title_answer(prose)
        derived = explicit or derive_subject_from_prose(prose)
        if derived:
            draft["title"] = derived
            pending_action["summary"] = _draft_summary(derived, draft.get("repository"))
            titled_now = True
            explicit_title = explicit is not None
    existing = (draft.get("body") or "").strip()
    # #1649: a draft armed with an explicit description but NO subject asked
    # only for the title — so the first bound prose on a body-carrying,
    # untitled draft IS the title answer. Naming the draft consumes it;
    # appending it to the given description would duplicate the headline
    # into the body. An explicitly-DICTATED title (v64 rework) is a title
    # answer regardless of body state — its metacommentary must not seed
    # the body either.
    title_answer = titled_now and (bool(existing) or explicit_title)
    if title_answer:
        body = existing
    else:
        body = f"{existing}\n\n{prose.strip()}" if existing else prose.strip()
    draft["body"] = body

    # The filing path reads intent.context["description"] first
    # (_handle_create_issue's description precedence), so the bound body is
    # what actually lands in the created issue — a binding that didn't file
    # would be the #1571 original defect (teaching a phrase with nothing
    # behind it) wearing a new hat.
    intent = pending_action.get("intent")
    if intent is not None:
        intent.context = dict(intent.context or {})
        intent.context["description"] = body
        if titled_now:
            # #1630: the subjectless original message slot-fills no title at
            # the create rail (no "about X" to extract) — the derived title
            # must ride the intent's own context or "file it" would hit the
            # #1490 what-should-it-be-about re-ask, losing the one-confirm
            # promise the draft copy teaches.
            intent.context["title"] = draft["title"]

    # #1665: after a bind the draft's open question is the keep-going/file
    # ask — update the record BEFORE the store (what's stored is what's said).
    pending_offer["question"] = _POST_BIND_ASK
    rearmed = True
    try:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
    except Exception as e:  # silent-ok: #1627 — a store failure must not crash the compose turn; logged ERROR, and the copy below never claims a bound draft that isn't there
        logger.error("drafted_issue_body_bind_rearm_failed", error=str(e))
        rearmed = False

    logger.info(
        "drafted_issue_body_prose_bound",
        session_id=session_id,
        body_chars=len(body),
        rearmed=rearmed,
    )

    if not rearmed:
        return {
            "message": (
                "I've got what you wrote, but I couldn't keep the draft "
                "bound — nothing was filed. Ask me to draft the issue "
                "again and we'll rebuild it, including what you just said."
            ),
            "intent_data": _retained_intent_data(pending_action),
        }

    title = draft.get("title") or "(untitled)"
    intent_data = _retained_intent_data(pending_action)
    intent_data["drafted_issue_body_bound"] = True
    if title_answer:
        # #1649: the answer titled a draft whose body was explicitly given
        # up front — say what happened (titled, not appended).
        lead = "Got it — that's the title. Nothing is filed yet. " "Here's where it stands:\n\n"
    elif titled_now:
        # #1630: the first answer on a subjectless draft STARTED it — say
        # so, and show the derived title for shaping.
        lead = (
            "Got it — I've started the draft from that. Nothing is filed yet. "
            "Here's where it stands:\n\n"
        )
    else:
        lead = "Added to the draft — nothing is filed yet. Here's where it " "stands:\n\n"
    return {
        "message": (
            f"{lead}"
            f"**Title**: {title}\n\n"
            # (v64 rework) an explicitly-dictated title on a bodyless draft
            # leaves the body legitimately empty — say so, don't render blank.
            f"**Body**:\n{body or '(no body yet)'}\n\n"
            f"{_POST_BIND_ASK}"
        ),
        "intent_data": intent_data,
        "requires_clarification": True,
    }


async def handle_drafted_issue_turn(
    pending_offer: Dict[str, Any],
    message: str,
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """Kind-specific turn handling for a pending drafted issue, run BEFORE
    the generic accept/decline detection (the #1605/#1510 sanctioned
    handler-internal seam — the pop already happened).

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` to fall through to the generic offer flow
    (declines and bare exits drop honestly there via ``decline_message``;
    off-intent abandons per the carrier's rules).
    """
    from services.intent_service.soft_invocation import detect_offer_response

    pending_action = pending_offer.get("pending_action") or {}
    file_cmd = detect_file_command(message)
    if file_cmd is None:
        # #1627: a prose turn that answers the draft's open question BINDS
        # to the draft. Checked BEFORE the generic accept consult so the
        # unanchored accept rows ("^please\s", "^yes,?\s") can't file a
        # half-shaped draft off the front of a long body answer, and
        # returned BEFORE the off-intent fall-through so no classification
        # surface (surface 1's greedy portfolio pattern was the live thief)
        # ever sees body prose. Deliberate exits and explicit commands fall
        # through exactly as before — the hold is not a turn lock.
        if is_body_prose_answer(message):
            return _bind_body_prose(
                pending_offer,
                pending_action,
                message,
                session_id=session_id,
                user_id=user_id,
                intent_service=intent_service,
            )
        from services.intent_service.soft_invocation import (
            detect_confirm_response,
        )

        if detect_confirm_response(message) != "accept":
            # #1650: filing is a CONFIRM — only an anchored, crisp,
            # full-message affirmative (or a taught file phrase, handled
            # above) fires the create. A short turn the greedy generic rows
            # would claim ("please hold on a sec", "sure, whatever you
            # think") is a NEAR-ACCEPT: it must neither file (the aside
            # wasn't a yes) nor fall to off-intent (the pop would drop
            # composed work). Re-arm and re-ask — a confirm that neither
            # confirms nor declines re-asks.
            if detect_offer_response(message) == "accept":
                # #1665: this re-ask turn's open question (stored pre-store).
                pending_offer["question"] = _NEAR_ACCEPT_ASK
                rearmed = True
                try:
                    intent_service.workflow_offer_service.set_pending_offer(
                        session_id, pending_offer, user_id=user_id
                    )
                except Exception as e:  # silent-ok: #1650 — a store failure must not crash the re-ask turn; logged ERROR, and the copy below stays honest about whether the draft is still bound
                    logger.error("drafted_issue_rearm_failed", error=str(e))
                    rearmed = False
                logger.info(
                    "drafted_issue_near_accept_reasked",
                    session_id=session_id,
                    rearmed=rearmed,
                )
                if rearmed:
                    msg = (
                        "Just to be safe I haven't filed anything — I only "
                        f"file on a clear go-ahead. {_NEAR_ACCEPT_ASK}"
                    )
                else:
                    msg = (
                        "I haven't filed anything, but I couldn't keep the "
                        "draft bound either — ask me to draft the issue "
                        "again and we'll rebuild it."
                    )
                return {
                    "message": msg,
                    "intent_data": _retained_intent_data(pending_action),
                    "requires_clarification": True,
                }
            # #1648: a file/submit-shaped near-miss ("file the sucker",
            # variants the anchored command regex doesn't know) is ABOUT
            # this draft — re-ask honestly and re-arm, never a silent
            # abandon into the routing chain (where the floor roleplayed
            # the filing live). Disjoint from the #1650 near-accept above
            # (that branch requires a loose ACCEPT read; this one requires
            # NO offer-response read at all). Declines, bare exits, and
            # every other command family keep falling through exactly as
            # before.
            if detect_offer_response(message) is None and is_file_near_miss(message):
                return _reask_near_miss(
                    pending_offer,
                    pending_action,
                    session_id=session_id,
                    user_id=user_id,
                    intent_service=intent_service,
                )
            return None  # decline / bare-exit / explicit command → generic flow

    intent = pending_action.get("intent")
    if intent is None:
        logger.error("drafted_issue_missing_intent", session_id=session_id)
        return None

    # "file it in owner/repo" with a draft pending: the named repo wins.
    if file_cmd and file_cmd.get("repo"):
        intent.context = dict(intent.context or {})
        intent.context["repository"] = file_cmd["repo"]

    # The #1190 acceptance mirror — delegate, never a parallel dispatch path.
    from services.intent_service.workflow_entries import (
        run_confirm_pending_action_workflow,
    )

    result: Optional[Dict[str, Any]] = None
    try:
        result = await run_confirm_pending_action_workflow(
            session_id=session_id,
            user_id=user_id,
            context={
                "pending_action": pending_action,
                "intent_service": intent_service,
            },
        )
    except Exception as e:  # silent-ok: #1571 — a raised dispatch must NOT crash the confirmation turn (the draft would be lost, the exact live failure); logged ERROR + traceback, and the None path below re-arms the draft and tells the user honestly
        logger.error("drafted_issue_dispatch_raised", error=str(e), exc_info=True)
        result = None

    def _rearm() -> bool:
        """Failure keeps the draft bound — retry must not lose it. Returns
        False when the store write itself failed, so the copy never claims a
        retained draft that isn't there."""
        try:
            # #1665: the retained draft's open question is the retained line
            # (the reply's own copy — stored pre-store, never re-rendered).
            pending_offer["question"] = _DRAFT_RETAINED_LINE
            intent_service.workflow_offer_service.set_pending_offer(
                session_id, pending_offer, user_id=user_id
            )
            return True
        except Exception as e:  # silent-ok: #1571 — a store failure must not crash the turn; logged ERROR, and the False return keeps the user-facing copy honest (no false "draft is still here" claim)
            logger.error("drafted_issue_rearm_failed", error=str(e))
            return False

    def _retained_line(rearmed: bool) -> str:
        return (
            _DRAFT_RETAINED_LINE
            if rearmed
            else ("I couldn't keep the draft bound either — ask me again and " "we'll re-draft it.")
        )

    if result is None:
        rearmed = _rearm()
        logger.info(
            "drafted_issue_create_failed_draft_retained", session_id=session_id, rearmed=rearmed
        )
        return {
            "message": (
                "I wasn't able to file that issue just now — nothing was "
                f"created. {_retained_line(rearmed)}"
            ),
            "intent_data": _retained_intent_data(pending_action),
        }

    intent_data = result.get("intent_data") or {}
    if intent_data.get("issue_number") is None:
        # The rail answered but did NOT verifiably create (degraded-connector
        # copy, clarification ask, honest failure). Pass its honest message
        # through and keep the draft bound.
        rearmed = _rearm()
        logger.info(
            "drafted_issue_create_unverified_draft_retained",
            session_id=session_id,
            rail_action=pending_action.get("action"),
            rearmed=rearmed,
        )
        merged = dict(intent_data)
        merged.update(_retained_intent_data(pending_action))
        return {
            "message": f"{result.get('message', '')}\n\n{_retained_line(rearmed)}".strip(),
            "intent_data": merged,
        }

    # Verified create — the success copy is the rail handler's own, derived
    # from the actual tool result (real number, real repo). Never a template
    # slot.
    logger.info(
        "drafted_issue_filed",
        session_id=session_id,
        issue_number=intent_data.get("issue_number"),
    )
    return result
