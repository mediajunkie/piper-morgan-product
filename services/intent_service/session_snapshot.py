"""SessionSnapshot — the conversational state the router has never seen (#1595 Phase 2.0).

THE PROBLEM THIS SOLVES (the structural one, not an instance): every turn-theft,
orphaned-answer, and stolen-aside incident of 2026-08 shares one mechanism — the
routing surfaces decide where a turn goes with ZERO knowledge that the session
has an open question, an armed offer, an active interview, or a draft in
compose. The kind-specific pop-seam handlers (#1605/#1571/#1627/#1648…) each
guard their own flow; nothing guards the chain as a whole. This snapshot is the
whole-chain fix: the Inversion's constrained routing call receives it as
context, so "an answer is expected here" is finally a routing input.

CONTRACT (Lead-authored, 2026-08-19 — implementation must not weaken these):

1. **READ-ONLY, NEVER POPPING.** Assembly peeks at stores; it must never pop an
   offer, claim a turn, advance a process, or write ANY state. A snapshot
   assembled twice in a row must observe the identical world (idempotence — the
   duty-cycle rule applied to code). Anything requiring a mutating read is
   excluded from the snapshot by definition.
2. **CHEAP AND SYNCHRONOUS-SHAPED.** Target < 10ms and zero LLM calls. Store
   reads that can block go through the same session-scoped in-memory stores the
   pop seam already uses; the DB-backed reads (ledger head, stored prefs) reuse
   existing cached paths only. No new queries hotter than what process_intent
   already runs.
3. **FAIL-OPEN, FIELD BY FIELD.** A store read that errors yields that FIELD as
   None/empty — never a raised exception, never a fabricated value, and never
   a withheld snapshot (an empty snapshot is still a snapshot; m-44: absent
   field ≠ verified-empty field is fine HERE because the consumer treats every
   field as advisory routing context, not as fact for user copy).
4. **BOUNDED SERIALIZATION.** serialize_for_prompt() output ≤ 500 tokens
   (~1800 chars enforced) with a deterministic field order, so prompt drift is
   diff-visible and the golden pin stays meaningful. Free-text fields (open
   question, draft title) are truncated with ellipsis at their stated caps.
5. **NO USER PROSE BEYOND LABELED SLOTS.** The snapshot carries system state
   and SHORT labeled excerpts (question copy, draft title) — never message
   history. History stays the floor's business (ADR D4 holds: the classifier
   never sees history; this snapshot is state, not transcript).

Consumers: inversion_shadow (Phase 2.1 rerun) first, then the live routing call
per category flip (Phase 2.2). NOT a public API — the floor and handlers must
not start reading routing context from here (one-direction dependency).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

# Serialization caps (contract item 4). Change ONLY with a golden-pin update in
# the same commit — the pin exists to make this line's edits reviewable.
MAX_SERIALIZED_CHARS = 1800
QUESTION_EXCERPT_CHARS = 140
TITLE_EXCERPT_CHARS = 80


@dataclass(frozen=True)
class SessionSnapshot:
    """Deterministic conversational state for one (session, user) at one turn."""

    # --- armed state (the #846 one-slot store, PEEKED never popped) ---
    pending_offer_kind: Optional[str] = None  # e.g. "drafted_issue", "issue_repo_question"
    pending_offer_question: Optional[str] = None  # short excerpt of the open ask
    pending_offer_is_confirm: bool = False  # rides the strict #1650 detector if True

    # --- active process (the #1623 registry, read-only probe) ---
    active_process_type: Optional[str] = None  # e.g. "standup"

    # --- draft state (the #1571 carrier's compose face) ---
    draft_in_compose: bool = False
    draft_title: Optional[str] = None  # None while untitled (#1630 subjectless arm)

    # --- recent referents (the #1394 session-activity ledger, heads only) ---
    recent_issue_number: Optional[int] = None
    recent_issue_repo: Optional[str] = None

    # --- standing preferences (the #1510/#1605 stores, fail-safe reads) ---
    declared_working_mode: Optional[str] = None  # "execute" | "collaborate" | None
    stored_clear_verb: Optional[str] = None  # per-verb reminder default, if any

    # --- assembly bookkeeping (never serialized into the prompt) ---
    field_errors: Tuple[str, ...] = field(default=())  # names of fields that failed open


def serialize_for_prompt(snap: SessionSnapshot) -> str:
    """Render the snapshot as the routing call's context block.

    Deterministic order, labeled lines, omitted-when-empty — the router should
    see ONLY signal. Golden-pinned in tests; edits here require updating the
    pin in the same commit (that requirement is the feature, not overhead).
    """
    lines = []
    if snap.pending_offer_kind:
        q = _clip(snap.pending_offer_question, QUESTION_EXCERPT_CHARS)
        confirm = " (yes/no confirm)" if snap.pending_offer_is_confirm else ""
        lines.append(f"OPEN QUESTION{confirm}: [{snap.pending_offer_kind}] {q or '(question text unavailable)'}")
        lines.append(
            "RULE: a turn that plausibly ANSWERS the open question routes to that "
            "flow's handler, not to a fresh operation. Explicit unrelated commands still route normally."
        )
    if snap.active_process_type:
        lines.append(f"ACTIVE PROCESS: {snap.active_process_type} (mid-exchange; answers belong to it)")
    if snap.draft_in_compose:
        t = _clip(snap.draft_title, TITLE_EXCERPT_CHARS)
        lines.append(f"DRAFT IN COMPOSE: {t or '(untitled)'} — prose likely extends the draft")
    if snap.recent_issue_number is not None:
        repo = f" in {snap.recent_issue_repo}" if snap.recent_issue_repo else ""
        lines.append(f"RECENT ISSUE: #{snap.recent_issue_number}{repo} (bare 'it'/'that issue' likely refers here)")
    if snap.declared_working_mode:
        lines.append(f"DECLARED MODE: {snap.declared_working_mode}")
    if snap.stored_clear_verb:
        lines.append(f"STORED CLEAR-VERB: {snap.stored_clear_verb}")
    out = "\n".join(lines)
    if len(out) > MAX_SERIALIZED_CHARS:  # contract item 4 — loud, not silent
        raise ValueError(
            f"SessionSnapshot serialization {len(out)} chars exceeds the {MAX_SERIALIZED_CHARS} cap — "
            "a field grew past its excerpt clip; fix the clip, never raise the cap silently."
        )
    return out


def _clip(text: Optional[str], cap: int) -> Optional[str]:
    if text is None:
        return None
    text = " ".join(text.split())
    return text if len(text) <= cap else text[: cap - 1].rstrip() + "…"
