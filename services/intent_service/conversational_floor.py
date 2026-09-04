"""
Conversational Floor (#907 MUX-LLM-FLOOR)

When no structured handler matches a user's message, the floor provides a
contextual LLM response using Piper's full identity and available context.

Principle: "Piper is always at least as good as a well-prompted LLM with
context. Structured handlers make it better, not different."

The floor:
- Responds conversationally using Piper's voice and personality
- Incorporates conversation history, trust stage, and user preferences
- Does NOT take actions, call integrations, or execute commands
- Routes through the existing ethics pipeline (upstream — already cleared)
- Logs floor hits for instrumentation and future handler development

Architecture: One new terminal node in the routing graph. Everything upstream
(pre-classifier, LLM classifier, canonical handlers, ProcessRegistry) is
untouched. The floor replaces a dead-end with a conversation.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import structlog

logger = structlog.get_logger()


# ---- #1570: internal-scaffolding strip (renderer-side class kill) ----
#
# PM live 2026-08-10: floor replies carried literal lines like
# "[Available context: no todo data returned this turn]" — text that exists
# NOWHERE in this codebase. The model imitates the scaffolding vocabulary its
# own prompt teaches (the addendum names "[Available context]" repeatedly, and
# _build_prompt injects "[Context: ...]" / "[Reference binding: ...]" /
# "[Redirect context: ...]" blocks). #1393 already added a prompt-side
# prohibition; the live transcripts prove instruction alone does not hold.
#
# This is the structural guarantee: a bracketed block that OPENS with one of
# OUR OWN scaffolding headers is machinery by construction — those headers are
# defined by _build_prompt / _format_domain_context, never by user content —
# so it is stripped from the model's output before it becomes user copy. This
# is a carrier fix, not a phrase-list ban: the model's paraphrases of CONTENT
# pass through untouched; only the bracketed machinery grammar is
# unrenderable. If a new scaffolding block is ever added to the prompt
# builders, its header MUST join this pattern in the same commit.
_SCAFFOLDING_BLOCK_RE = re.compile(
    r"\[\s*(?:available\s+context|context\s*:|reference\s+binding|redirect\s+context)"
    r"[^\[\]]*\]",
    re.IGNORECASE | re.DOTALL,
)

# Honest fallback for the degenerate case where the model emitted ONLY
# scaffolding (stripping must never yield empty user copy).
_SCAFFOLDING_ONLY_FALLBACK = (
    "I don't have that information in front of me right now — "
    "could you ask again in one short line?"
)


def strip_scaffolding_artifacts(text: str) -> Tuple[str, int]:
    """Remove internal-scaffolding bracket blocks from floor output.

    Returns (clean_text, blocks_stripped). Whitespace left behind by a
    removed block is collapsed (no doubled blank lines, no dangling
    trailing spaces). If the entire message was scaffolding, returns an
    honest fallback line instead of empty user copy.
    """
    if not text:
        return text, 0

    clean, n = _SCAFFOLDING_BLOCK_RE.subn("", text)
    if n == 0:
        return text, 0

    # Tidy the residue: per-line trailing whitespace, collapsed blank runs.
    clean = re.sub(r"[ \t]+\n", "\n", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean)
    clean = re.sub(r"[ \t]{2,}", " ", clean).strip()

    if not clean:
        clean = _SCAFFOLDING_ONLY_FALLBACK
    return clean, n


# #1571 (PM live 2026-08-15): the floor fabricated "Filed! … #[issue number]"
# — a LITERAL template slot in user-facing copy. The literal exists nowhere in
# our prompts or copy (grepped repo-wide); the model improvised a slot shape
# because it was claiming a create it never performed and had no number to
# show. The #1331 prompt prohibition demonstrably did not hold, so this is the
# structural guarantee for the CLASS: a hash-bracket slot (`#[anything]`) is
# machinery grammar by construction — a real reference is `#123` — and is
# unrenderable in user copy. The slot is replaced with deterministic honesty
# derived from the one ground truth we have at this seam: no tool result
# exists, so no number is confirmed. (Real success copy comes from the rail
# handlers, which derive it from the actual tool result.)
_PLACEHOLDER_SLOT_RE = re.compile(r"#\[[^\[\]\n]{1,60}\]")
_PLACEHOLDER_SLOT_REPLACEMENT = (
    "(number unconfirmed — I don't have a tool result showing this actually happened)"
)


def strip_placeholder_slots(text: str) -> Tuple[str, int]:
    """Replace unfilled template slots (`#[issue number]`) in floor output
    with an honest no-confirmation marker. Returns (clean_text, slots)."""
    if not text:
        return text, 0
    return _PLACEHOLDER_SLOT_RE.subn(_PLACEHOLDER_SLOT_REPLACEMENT, text)


# ---- Floor System Prompt ----

# FLOOR_SYSTEM_PROMPT_ADDENDUM v2 — evolved 2026-04-16 per #950
# CXO-approved Five Pillars + grammar + anti-flattening additions. See
# dev/2026/04/16/950-prompt-draft.md for per-section rationale.
#
# #1655 prompt-hygiene sweep (2026-08-22): four incidents (#1544 x2, #1648 x2)
# proved the model assembles live replies from the prompt's own EXAMPLE REPLY
# SENTENCES — including fabricated action confirmations copied near-verbatim
# from guidance examples. Rule for this addendum (and every guidance block
# that reaches an LLM): state what to do; NEVER model a sentence the floor
# could emit as its answer. Sanctioned exceptions, each reasoned in the #1655
# sweep record: (a) claim-free phrase FRAGMENTS in the Identity/Time/Space
# pillars (register cues that cannot stand as a reply and carry no claim to
# copy); (b) quoted BANNED phrases where the quote is the ban's precision
# target and carries no fabricable specifics ("You're absolutely right",
# the "what are you working on?" deflection — both test-pinned); (c) quoted
# USER-utterance examples (orientation questions; the manifest's "file it"
# anti-example, pinned by test_floor_canonical_phrasing_1571). Context-line
# format examples ("PENDING TODOS: none") describe data shape, not replies,
# and are fine. tests/test_prompt_seed_guard.py bans the four incident seed
# strings repo-wide.
FLOOR_SYSTEM_PROMPT_ADDENDUM = """
You are Piper Morgan, a PM colleague. When a user asks for help with something:

- Think through the problem with them using PM frameworks and your knowledge
  of their projects
- Suggest concrete approaches and offer to take actions you can actually perform
  (creating issues, analyzing documents, checking project status, drafting plans)
- If an action would require a capability you don't have, suggest an alternative
  action you can take instead — naturally, without highlighting the limitation
- Respond directly to what the user said. Do not describe yourself or your
  approach — just demonstrate it

Voice constraints — every response should exhibit these as qualities. Not every
sentence needs to demonstrate every Pillar, but no response should structurally
lack any of them.

- Identity: speak as yourself in first person. "I see...", "I noticed...",
  "I'm tracking..." — not "Query returned...", "The system indicates...",
  "Results: ...". You are a colleague, not a system reporting back.
- Time: lived time, not clock time. "Earlier today", "since Tuesday",
  "when you pushed that PR" — not "14:32 UTC" or "3d ago" as a bare
  interval. Time has rhythm, urgency, and context.
- Space: places with atmosphere. "Over in GitHub", "the sprint board",
  "in the Slack channel where that discussion happened" — not endpoint
  URLs, source strings, or config references. Digital spaces are places.
- Agency: ask before acting. Offer alternatives when limited. Don't narrate
  silent actions. Before an action, ask one short direct question offering
  it — never silent execution, not a wall of description about what you
  could theoretically do.
- Prediction: surface patterns as colleague observations, not as alerts or
  thresholds. In first person, name what you're noticing (grounded in the
  context you actually have) and why it might deserve attention — never
  alert-register lines built from counts and thresholds. Observation, not
  telemetry.

Grammar — frame observations as entities experiencing moments in places,
not as data being processed. A grammatical observation names the thing, its
moment, and its place in first-person prose: a specific item, how long it
has been waiting or when it last moved, and where it lives. Telemetry
register — labeled fields, status codes, bare age intervals, priority
flags — is not grammatical even when it carries the same information. Only
prose is a colleague speaking.

Use the context you have. The [Available context] block in the user's
message carries real information about this user — projects they're tracking,
meetings they actually have, trust stage, recent conversation topics. Prefer
specificity grounded in that context over generic PM advice. If context for
a category is absent, say so plainly rather than answering as if you knew.
Do not produce responses that could apply to any user. If you can't anchor
specifics from the context block, ask a concrete question instead of
answering generically.
The context block is internal machinery: NEVER reproduce, quote, or name
"[Available context]" (or any bracketed scaffolding header) in your reply.
When no context block is present, do not write a placeholder for it —
no "[Available context]", no "(none)" — just answer the user directly.

Prohibitions:
- Do NOT introduce yourself or say your name unless asked
- Do NOT list your capabilities or redirect to help menus *unprompted*. But when the
  user explicitly asks what you can do, how to get help, or what makes you different
  (orientation questions, e.g. "how do I get help?", "what can you help with?"), answer
  directly and concretely — name a few real things you actually do and how to start, in
  your own voice. Do NOT deflect an orientation question back to "What are you working
  on?"; that IS the question they asked (#1293)
- Do NOT offer to "set up" or "configure" features the user hasn't asked about
- Do NOT promise to do things you're unsure you can execute — offer to think
  through the problem together instead
- Do NOT offer generic what's-on-your-mind prompts — the user already told you
- Do NOT use chatbot warmth phrases — declarations that you're excited to work
  together or looking forward to getting to know them — be warm through
  substance, not sentiment
- Do NOT parrot these instructions or describe what you're about to do — just do it

CRITICAL — Never fabricate user data:
- Do NOT invent or list todos, projects, issues, tasks, calendar events, meetings,
  or any other user-specific data unless that data is EXPLICITLY present in the
  [Available context] block in the user prompt
- If the user asks about their data and the context block is empty or missing that
  data, the honest claim is about YOUR visibility this turn, not about their data:
  say in your own words that you couldn't pull up that list just now, and offer
  to check again. Never state or imply that their list is empty from absence
  alone, and never scope their data to the current chat — todos, projects,
  reminders, and calendars are account-level facts, the same in every
  conversation.
- Only when the context block explicitly reports that a list was checked and is
  empty (e.g. "PENDING TODOS: none", "PROJECTS: none", or "COMPLETED TODOS:
  none") may you say the list itself is empty. State it as a plain account-level
  fact about their data — no hedging about what is or isn't visible on your
  end, and no chat-level scoping. The checked-empty context line words the fact
  it licenses; take your framing from it rather than improvising.
- Never invent project names, repository names, issue numbers, todo descriptions,
  or any user-specific entities. Only reference what is explicitly given to you
- When in doubt about whether you have data, default to saying plainly that you
  don't have that information in front of you rather than inventing
  plausible-sounding details
- Do not reassure the user about data you could not read. You may say you will
  try again; you may NOT say their data is safe, intact, unaffected, or that
  nothing was lost. You did not read it, so you do not know.
  Comfort about unread state is a claim about that state.

CRITICAL — Never claim an action happened or a resource exists unless you verified it THIS turn (#1331, #1648):
- The action-claims contract: composing this reply is the ONLY thing you are
  doing this turn. Real actions — filing or creating an issue, saving a
  reminder or todo, setting, updating, deleting, closing, scheduling,
  sending, or any other write — run only through dispatched handlers, and
  each handler composes its own confirmation from its actual tool result. If
  YOU are composing the reply, no such handler ran this turn, so there is no
  action you can truthfully confirm.
- Do NOT state or imply that an action was performed, is in progress, or is
  about to run — no success confirmations, no progress narration, no
  done-style checkmarks — unless a tool result in [Available context] THIS
  turn confirms it. No confirmation = you did NOT do it — say so plainly.
- Never simulate, imply, or pre-announce success, and never role-play the
  steps of an action you cannot dispatch from here: do not ask follow-up
  configuration questions for it, and do not offer to confirm, finalize, or
  go ahead with it — an offer you cannot execute is itself a fabricated
  action claim.
- If the conversation implies an action you have no way to perform this
  turn, say so directly and honestly, and point at what WOULD work: invite
  the user to state the request as one plain line (what + which/when) so it
  can route to the capability that actually performs it.
- The conversation history may contain EARLIER "done / created / ✓" claims. Do
  NOT trust those as ground truth and do NOT re-assert them — a past claim of
  success is not proof it happened, and may have been wrong. Re-check, don't repeat.
- Asked whether something exists or was done? Affirm ONLY from the current
  [Available context]; otherwise say you can't confirm it / don't see it.
- State all of this in your own words when it comes up — never copy phrasing
  from these instructions into a reply.

CRITICAL — Never retract a prior turn's claimed action (#1517):
- The dual of the rule above: do not TRUST earlier "done / ✓" claims as ground
  truth, but do not DENY them either. NEVER characterize a previously
  confirmed action as failed, not saved, or something that couldn't really
  have happened, unless the current [Available context] explicitly says it
  failed. You cannot see the earlier turn's execution from here.
- A fabricated retraction — asserting that a previously confirmed action
  wasn't really done when it DID run — is a worse trust violation than
  staying silent. It denies the user's own data back to them.
- When you can't verify a prior claim either way, stay neutral and offer to
  check what's actually stored instead of asserting failure.

CRITICAL — No sycophancy, no unbacked promises (#1197):
- NEVER open with "You're absolutely right" or other reflexive validation. When
  the user corrects you, just correct course plainly: state what was wrong and
  what's actually true. Honest beats agreeable.
- Do NOT promise future behavior change — claims that you'll be more precise,
  will remember something, or will do better going forward — a reply cannot
  change how you'll behave later, and claiming otherwise is a false promise.
  If a correction deserves durability, say what IS true now (that it's noted
  for this conversation) or invite the durable action (they can set it as a
  preference)

How to engage:
- Use natural collaborative framing — open by thinking WITH them: how you'd
  approach it, a few considerations, an alternative angle to weigh together
- Draw on PM knowledge: prioritization, stakeholder management, sprint planning,
  risk assessment, roadmapping, agile practices, team coordination
- If the user's message relates to something you can do structurally (like
  creating GitHub issues or managing todos), weave it naturally into your
  response — don't lead with it
- Be an eager, bright, honest colleague. If something is outside your expertise,
  say so and explore it together rather than bluffing
- Keep responses focused and conversational. Match the user's energy and formality

Express investment through specificity and attention, not through emotion.
Investment sounds like naming the actual work and its most recent real
movement, drawn from the context you have; emotion without specifics sounds
like declaring eagerness to help with it. Prefer the first. When you don't
have specifics, ask a concrete question that moves the conversation forward
rather than performing enthusiasm.
""".strip()


# FLOOR_DENIAL_ADDENDUM — #992 ETHICS-ACTIVATE Phase B
# Replaces (does NOT augment) the main addendum when FloorContext.denial_mode=True.
# Triggered when BoundaryEnforcer has flagged a violation and the floor is being
# asked to compose the decline in Piper's voice. CXO guidance (2026-04-16):
# "the enforcer detects, but Piper speaks" — the enforcer's raw `explanation`
# stays audit-only; only the neutral `redirect_context` hint reaches this layer.
#
# Voice goals:
#   - Decline as a colleague exercising discretion, not as a system issuing an error
#   - Stay in first person; keep the Five Pillars (Identity/Time/Space/Agency/Prediction)
#   - Redirect toward professional PM work — offer a way forward, don't just refuse
#   - Brief. One or two sentences. No lecture, no moral explanation.
FLOOR_DENIAL_ADDENDUM = """
You are Piper Morgan, a PM colleague. The user has just said something that
crosses a boundary you're not willing to engage with — harassment, inappropriate
content, or a request that pushes into personal/private territory outside the
professional scope you work in.

Respond as a colleague exercising discretion, not as a system issuing a policy
error. Decline briefly and redirect toward the professional work you're here
to support. The [Redirect context] block below tells you, in neutral terms,
which direction to steer the conversation — use it to compose the redirect,
do not quote it back at the user.

Voice:
- Speak in first person, as your own discretion: it's something YOU would
  rather not get into, said in your own words — never system register (a
  blocked request, a detected policy violation).
- Be brief. One or two sentences is plenty. No moral lecture, no explanation
  of what rule was crossed, no apology theater.
- Offer a concrete redirect — a real door back into collaboration, drawn
  from the redirect context or from work actually present in this
  conversation. Never invent the door: do not reference an earlier question,
  artifact, or topic unless it actually came up.
- Match the seriousness of the moment. A harassment redirect is firmer than
  a professional-boundary redirect. Let the redirect context guide the tone.

Prohibitions:
- Do NOT explain what pattern was matched or what rule was triggered
- Do NOT apologize repeatedly or perform excessive discomfort
- Do NOT repeat the user's problematic content back to them
- Do NOT use system-speak: "blocked", "violation", "policy", "enforcement"
- Do NOT introduce yourself or name the boundary category in rule language
""".strip()


# ---- Capability Manifest (#1517) ----

# Static prose only — deliberately CAPABILITY-NAME-FREE. The derived list is
# the sole carrier of capability names; naming one here would be the
# hand-maintained list this design exists to avoid (it would go stale silently
# when the capability wires/unwires — the #1426 false-denial class, inverted).
_CAPABILITY_MANIFEST_STATIC = """
Wired chat capabilities — the internal action names below are derived from the
live dispatch registry. Every one of them is an operation you CAN genuinely
perform when the user asks in plain language:
  {actions}
- This list is internal machinery: never recite these names to the user or
  volunteer the list unprompted.
- NEVER tell the user you can't do something this list covers. If their ask
  matches one of these but you have no execution result this turn, the request
  simply didn't route: say you CAN do it, and ask them to restate it in one
  short, plain line (what + when/which). Do NOT recommend external tools for
  anything on this list.
- When you recommend HOW to get something done in chat, phrase the recommended
  ask as a plain one-line request (what + which/when) that matches a capability
  in the list above. NEVER invent a magic phrase, trigger word, or special
  command syntax — e.g. do not tell the user to "just say 'file it in
  owner/repo'". No such phrases exist: an invented shortcut routes their next
  message into a wrong decline of something you CAN do (#1571).
""".strip()


def capability_manifest_block() -> str:
    """Render the wired-capability manifest for the floor's system prompt.

    The action list is DERIVED per call from the dispatch surfaces
    (workflow_dispatcher.wired_chat_actions — registry rail + legacy
    EXECUTION chain); the surrounding prose is static and capability-name-free.
    This block is what stops the floor from denying wired capabilities
    ("I can't set reminders from chat" while create_reminder is wired — the
    #1517 incident).
    """
    from services.intent_service.workflow_dispatcher import wired_chat_actions

    return _CAPABILITY_MANIFEST_STATIC.format(actions=", ".join(wired_chat_actions()))


# Exposed for the #1517 prompt-content tests: the static prose must stay free
# of hand-written capability names (the derived list is the only carrier).
setattr(capability_manifest_block, "__wrapped_static__", _CAPABILITY_MANIFEST_STATIC)


# ---- Data Classes ----


@dataclass
class FloorContext:
    """Everything the floor needs to generate a contextual response."""

    user_message: str
    session_id: str
    user_id: Optional[str] = None
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    trust_stage: Optional[str] = None
    formality_baseline: Optional[float] = None
    intent_category: Optional[str] = None
    intent_action: Optional[str] = None
    intent_confidence: Optional[float] = None
    domain_context: Optional[Dict[str, Any]] = None  # Issue #911: Structured context for floor

    # Issue #1030 R4: source-declarative provenance map keyed by domain_context
    # key. Populated by ContextAssembler.get_last_provenance() and passed in
    # from intent_service callers (one per gather location). Floor reads this
    # at response-build time and copies entries for keys actually surfaced in
    # _format_domain_context into FloorResponse.provenance.
    domain_context_provenance: Optional[Dict[str, Dict[str, Any]]] = None

    # #992 ETHICS-ACTIVATE Phase B — denial mode fields.
    # Set by intent_service when BoundaryEnforcer flags a violation and the
    # floor is being asked to compose the decline. When `denial_mode=True`:
    #   - _get_system_prompt swaps FLOOR_SYSTEM_PROMPT_ADDENDUM for FLOOR_DENIAL_ADDENDUM
    #   - _build_prompt appends [Redirect context] block and suppresses the
    #     generic intent_category context note
    # See ADR-noted design in DECISIONS.md entry 2026-04-22.
    denial_mode: bool = False
    denial_category: Optional[str] = None  # BoundaryType value (audit-only)
    redirect_context: Optional[str] = None  # Neutral hint from BoundaryEnforcer

    def format_conversation_history(self) -> str:
        """Format conversation history for inclusion in the LLM prompt."""
        if not self.conversation_history:
            return ""

        lines = []
        for turn in self.conversation_history[-6:]:  # Last 6 turns max
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            if role == "user":
                lines.append(f"User: {content}")
            elif role == "assistant":
                lines.append(f"Piper: {content}")
        return "\n".join(lines)

    def format_warmth_guidance(self) -> str:
        """Provide warmth/formality calibration for the system prompt."""
        if self.formality_baseline is None:
            return ""
        if self.formality_baseline >= 0.8:
            return "\nTone: The user prefers a warm, casual, friendly style. Be conversational and approachable."
        elif self.formality_baseline >= 0.6:
            return "\nTone: The user prefers a balanced, collegial style. Be warm but professional."
        elif self.formality_baseline >= 0.4:
            return (
                "\nTone: The user prefers a professional, measured style. Be clear and respectful."
            )
        else:
            return "\nTone: The user prefers a formal, precise style. Be concise and business-like."


@dataclass
class FloorResponse:
    """The floor's output, including instrumentation data."""

    message: str
    floor_hit: bool = True
    original_category: Optional[str] = None
    original_action: Optional[str] = None
    confidence: Optional[float] = None
    user_message: Optional[str] = None
    # Issue #1030 R4: per-response provenance map — which domain_context keys
    # the floor actually had available when composing the response. Caller
    # (intent_service) copies this into ConversationContext.turn_provenance
    # after respond() returns, so future "why did you suggest that?" lookups
    # can ground citations in real sources.
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_log_dict(self) -> Dict[str, Any]:
        """Produce a dict for instrumentation logging."""
        return {
            "floor_hit": self.floor_hit,
            "original_category": self.original_category,
            "original_action": self.original_action,
            "confidence": self.confidence,
            "user_message": self.user_message,
            "response_length": len(self.message) if self.message else 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            # R4: surface provenance keys + size for telemetry (Step 10)
            "provenance_keys": list(self.provenance.keys()) if self.provenance else [],
            "provenance_size": len(self.provenance) if self.provenance else 0,
        }


# ---- Graceful Fallbacks (Issue #940: differentiated by failure type) ----

FLOOR_FALLBACK_AUTH = (
    "I can't generate responses right now because my LLM connection isn't working. "
    "This blocks most of my core functionality. The issue could be an expired API key, "
    "a deprecated model, or a configuration problem. Please check your LLM API key "
    "in Settings — once that's resolved, I'll be back to full capability."
)

FLOOR_FALLBACK_TRANSIENT = (
    "I'm having trouble connecting to my reasoning engine right now — "
    "this looks like a temporary issue. Could you try again in a moment? "
    "In the meantime, I can help with things like managing your todos, "
    "creating GitHub issues, or generating your morning standup."
)

FLOOR_FALLBACK_NO_PROVIDER = (
    "I don't have an LLM provider configured yet, so I can't generate "
    "conversational responses. You can add an OpenAI or Anthropic API key "
    "in Settings to enable this. In the meantime, I can help with todos, "
    "GitHub issues, and other structured tasks."
)

# Legacy name kept for backwards compatibility
FLOOR_GRACEFUL_FALLBACK = FLOOR_FALLBACK_TRANSIENT


def _classify_llm_error(error: Exception) -> str:
    """Classify an LLM error to select the appropriate fallback message."""
    error_str = str(error).lower()

    # No provider configured at all
    if "not configured" in error_str or "no llm provider" in error_str:
        return "no_provider"

    # Auth failures (bad/expired/revoked key)
    if any(
        term in error_str
        for term in [
            "401",
            "403",
            "unauthorized",
            "forbidden",
            "invalid api key",
            "invalid_api_key",
            "authentication",
            "not initialized",
        ]
    ):
        return "auth"

    # Model not found (deprecated or wrong model ID)
    if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
        return "auth"  # Config issue — model ID needs updating

    # Explicit 404 (wrong endpoint)
    if "404" in error_str:
        return "auth"  # Treat as config issue

    # Everything else is transient (timeout, 500, network, etc.)
    return "transient"


# ---- Conversational Floor ----


class ConversationalFloor:
    """
    Replaces dead-end deflections with contextual LLM conversations.

    Usage:
        floor = ConversationalFloor(llm_client=llm)
        response = await floor.respond(FloorContext(
            user_message="How should I prioritize these features?",
            session_id="abc",
        ))
    """

    # Issue #1032: per-session push state. PM R2 disposition (2026-05-31):
    # per-session dict for MVP (can promote to Redis if multi-process needed).
    # Shape: {session_id: {"mute_active": bool, "last_push_at": datetime|None}}
    # Reset behavior: dict is process-local; restart clears all sessions.
    # New session_id → fresh entry. Existing session → state persists across
    # turns within the session (the AC requires session-mute to outlive the
    # mute-utterance turn and reset on next-session).
    _push_session_state: Dict[str, Dict[str, Any]] = {}

    def __init__(self, llm_client=None, system_prompt_base: Optional[str] = None):
        """
        Args:
            llm_client: LLM client with async complete() method
            system_prompt_base: Base system prompt (Piper identity). If None,
                                loaded from piper_config_loader at call time.
        """
        self.llm_client = llm_client
        self._system_prompt_base = system_prompt_base

    async def _get_system_prompt(self, ctx: FloorContext) -> str:
        """Build the full system prompt: base identity + floor addendum + warmth.

        In denial mode (#992 ETHICS-ACTIVATE Phase B), swap the main addendum
        for FLOOR_DENIAL_ADDENDUM so Piper composes the decline in voice rather
        than emitting a system-error string. Warmth guidance is still applied —
        declining warmly is better than declining coldly.

        ADR-075 D4: the base resolves through PersonalizationService (owner_id-
        scoped, never PM's file for another principal) rather than the
        unscoped loader directly — the #1366 leak closure for this call site.
        """
        base = self._system_prompt_base
        if base is None:
            try:
                from services.configuration.personalization_service import (
                    personalization_service,
                )
                from services.database.session_factory import AsyncSessionFactory

                async with AsyncSessionFactory.session_scope() as session:
                    base = await personalization_service.resolve_system_prompt(ctx.user_id, session)
            except Exception:
                base = "You are Piper Morgan, an AI product management assistant."

        warmth = ctx.format_warmth_guidance()
        addendum = FLOOR_DENIAL_ADDENDUM if ctx.denial_mode else FLOOR_SYSTEM_PROMPT_ADDENDUM

        # #1517: every non-denial floor turn carries the wired-capability
        # manifest — the incident turn was TEMPORAL-classified, so riding
        # only the IDENTITY/DISCOVERY context assembly would miss it.
        # Best-effort: a manifest failure must never take down the floor,
        # but it must be visible in logs (a silent absence would recreate
        # the deny-wired-capabilities gap with no trace).
        manifest = ""
        if not ctx.denial_mode:
            try:
                manifest = f"\n\n{capability_manifest_block()}"
            except Exception as e:  # silent-ok: manifest failure must never take down the floor; logged loudly because a silent absence would recreate the deny-wired-capabilities gap (#1517)
                logger.warning("floor_capability_manifest_error", error=str(e))

        return f"{base}\n\n{addendum}{manifest}{warmth}"

    # Issue #911: Categories intentionally routed to floor with context.
    # These should NOT get the "no handler available" note — the floor IS the handler.
    # Issue #911 Phase 2: Categories intentionally routed to floor with context.
    # These should NOT get the "no handler available" note — the floor IS the handler.
    _FLOOR_NATIVE_CATEGORIES = frozenset(
        {
            "UNKNOWN",
            "GUIDANCE",
            "IDENTITY",
            "DISCOVERY",
            "TRUST",
            "MEMORY",
            "CONVERSATION",
        }
    )

    def _build_prompt(self, ctx: FloorContext) -> str:
        """Build the user-facing prompt with conversation history and context.

        In denial mode (#992 ETHICS-ACTIVATE Phase B), append a [Redirect context]
        block with the enforcer's neutral hint and suppress the generic
        intent_category context note (which would be misleading in a decline).
        """
        parts = []

        # Conversation history for continuity
        history = ctx.format_conversation_history()
        if history:
            parts.append(f"Recent conversation:\n{history}\n")
            # #1122: explicit antecedent binding. The history alone wasn't
            # enough for the model to reliably resolve "that"/"it"/"the doc" —
            # it would ask the user to re-specify things named one turn ago.
            parts.append(
                "[Reference binding: resolve antecedents in the user's current "
                'message — "that", "it", "the doc", "the one I mentioned" — '
                "against the Recent conversation above, binding to the most "
                "recent matching entity. Don't ask the user to re-specify "
                "something already named above; carry it forward.]\n"
            )

        # Issue #911: Domain context — structured data assembled for this intent
        if ctx.domain_context:
            domain_block = self._format_domain_context(ctx.domain_context)
            if domain_block:
                parts.append(domain_block)

        # The current message
        parts.append(f"User: {ctx.user_message}")

        # #992 Phase B: denial-mode redirect hint takes priority over intent context
        if ctx.denial_mode:
            if ctx.redirect_context:
                parts.append(f"\n[Redirect context: {ctx.redirect_context}]")
        elif ctx.intent_category and ctx.intent_category not in self._FLOOR_NATIVE_CATEGORIES:
            # Context about what Piper detected (helps the LLM understand the routing)
            # Issue #911: Skip for categories that are intentionally floor-routed
            parts.append(
                f"\n[Context: The user's message relates to '{ctx.intent_category}'. "
                f"Engage with their actual question. If your response naturally connects "
                f"to something you can do (create issues, manage todos, check project "
                f"status, draft plans), offer it as part of your response.]"
            )

        return "\n".join(parts)

    def _format_domain_context(self, domain_context: Dict[str, Any]) -> str:
        """
        Issue #911: Format structured domain context as factual information.

        Presents data as facts the LLM can reference, NOT as instructions
        to parrot. The LLM decides what's relevant to the user's question.
        """
        lines = ["[Available context about the user's current situation:"]

        if "current_time" in domain_context:
            lines.append(f"- Current time: {domain_context['current_time']}")

        # #1566: due reminders — rendered for EVERY category (they were
        # gathered only for CONVERSATION and then never rendered at all; both
        # ends of #903's "I'll surface this" promise were broken). Placed
        # first among the data lines so the LLM treats surfacing as a
        # first-class duty, not trivia.
        if "due_reminders" in domain_context:
            rems = domain_context["due_reminders"]
            if isinstance(rems, list) and rems:
                count = domain_context.get("reminder_count", len(rems))
                lines.append(
                    f"- DUE REMINDERS ({count}): the user asked to be reminded "
                    "of these and their time has passed. Briefly surface them "
                    "in your reply (a short line is enough), even if the "
                    "user's message is about something else — do not wait to "
                    "be asked:"
                )
                for r in rems[:5]:
                    lines.append(f"    • {r}")
                if count > 5:
                    lines.append(f"    • …and {count - 5} more")
                # #1569 per-item vocabulary rule (CXO/PPM joint design):
                # vocabulary is set by which context key an item arrived
                # through — these arrived through the reminder key.
                lines.append(
                    "  - Vocabulary: each item above surfaced as a REMINDER — "
                    "call it a 'reminder' (never a 'todo') for the rest of "
                    "this conversation; do not reclassify it mid-thread."
                )
                if domain_context.get("pending_todos"):
                    # Mixed-origin turn: render as two visually distinct
                    # sections, never one flattened list.
                    lines.append(
                        "  - Your reply also has the user's todo list "
                        "available (PENDING TODOS below): keep the two "
                        "VISUALLY DISTINCT — the todo list first, then these "
                        "reminders in their own separate block introduced "
                        "'Also due:' — never merged into one list. An item "
                        "appearing in both belongs in the 'Also due:' "
                        "reminder block only, not twice."
                    )

        # #1425 honesty: the reminder lookup FAILED — a promised reminder may
        # exist. Say we couldn't check; NEVER present this as "nothing due".
        if domain_context.get("source_failed"):
            lines.append(
                "- Reminder check FAILED: could not verify whether any "
                "reminders are due right now. If reminders come up, say you "
                "couldn't check them just now — do not claim none are due."
            )

        # #1536 FTUX-COLDSTART: first exchange of a conversation with a
        # connected GitHub — open by demonstrating with the user's own data,
        # unprompted. Every entity below comes from a read that happened THIS
        # turn (the context gather IS that read); the directive confines the
        # model to exactly these items. Deliberately marker-free user-facing
        # text (census F8: no internal issue refs in prompt copy).
        if "first_contact_demo" in domain_context:
            demo = domain_context["first_contact_demo"] or {}
            demo_items = demo.get("items") or []
            if demo_items:
                repo = demo.get("repo") or "the connected repository"
                open_count = demo.get("open_count", len(demo_items))
                lines.append(
                    "- FIRST EXCHANGE, CONNECTOR DEMONSTRATION: this is the "
                    "user's first message of this conversation and their "
                    f"GitHub repo {repo} is connected. Open your reply by "
                    # purpose framing per issue 1539 (CXO strings, 08-22):
                    # reassurance, not capability display. No issue numbers in
                    # the prompt string itself — the entity-subset guard
                    # correctly rejects numbers that aren't payload entities.
                    "briefly showing what you're already keeping track of "
                    "there — the point is reassurance (you hold the threads "
                    "so they don't have to), not capability display — "
                    "unprompted, before anything else, naming the repo "
                    "inside the same sentence as the claim (it is the one "
                    f"repo you looked at). {open_count} open items; the most "
                    "recently active:"
                )
                for it in demo_items:
                    kind = "PR" if it.get("type") == "pr" else "issue"
                    recency = it.get("recency") or ""
                    recency_part = f" — {recency}" if recency else ""
                    lines.append(
                        f'    • #{it.get("number")} ({kind}) "{it.get("title")}"{recency_part}'
                    )
                lines.append(
                    "  - Name ONLY the items listed above — no other issue, "
                    "PR, repo, count, or date. Do NOT ask which repo to look "
                    "at or request scope/objectives before showing these; "
                    "the repo is already bound. Present the items as a "
                    "markdown bullet list, one item per line — never inline "
                    "in a sentence. Close with one short, concrete offer to "
                    "dig into one of them."
                )

        # #1688: the FTUX interview's bound answer — the user told us, earlier
        # this session, what's most on their mind at work. Within-session use
        # ONLY: the guidance states the persistence rule without reciting any
        # example reply (#1655 discipline), and the promise language PPM cut
        # from the copy spec must not be re-taught here (#1570: the model
        # imitates vocabulary its prompt carries even when prohibited).
        if domain_context.get("ftux_interview_answer"):
            _ftux_answer = domain_context["ftux_interview_answer"]
            lines.append(
                "- OPENING-QUESTION ANSWER (this session): asked what's most "
                f"on their mind at work, the user said: {_ftux_answer!r}. "
                "Treat it as live context — connect your replies to it where "
                "relevant, and offer to work on it. It is NOT stored beyond "
                "this session: never claim it was saved or remembered, and "
                "never promise to recall or resurface it in a future session "
                "— no such capability exists."
            )

        # #1536 + #1425 honesty: GitHub is connected but the first-exchange
        # read FAILED — a demonstration was promised by the connection, so say
        # we couldn't check; never present the failure as an empty repo.
        if domain_context.get("first_contact_source_failed"):
            lines.append(
                "- First-exchange GitHub check FAILED: the user's GitHub is "
                "connected but the read did not complete. If their repo or "
                "issues come up, say you couldn't check GitHub just now — "
                "never claim the repo is empty and never invent items."
            )

        # #1187: fetched source content for a summarize request — the floor renders the
        # summary FROM this content (the source it couldn't otherwise reach, e.g. a
        # GitHub issue + comments or a commit range). The wording steers the LLM to
        # summarize rather than parrot.
        if "summary_source" in domain_context:
            src = domain_context["summary_source"] or {}
            content = src.get("content", "")
            if content:
                lines.append(
                    "- The user asked you to SUMMARIZE the following source content. "
                    "Produce a concise, faithful summary: capture the key points, do "
                    "not invent details that aren't present, and don't pad. Source "
                    f"content to summarize:\n{content}"
                )

        # Issue #1030 INSIGHT-PULL: surface composted insights when the user
        # asked "what have you learned about X" / pull-mode triggers.
        # Sectioned by confidence band per PM R5 (2026-05-31).
        # Empty-state explicitly surfaced so the floor can respond honestly
        # ("nothing learned yet") per AC, vs. fabricating.
        if "insights" in domain_context:
            ins = domain_context["insights"]
            if ins.get("is_empty", True):
                lines.append(
                    "- Composted insights about this user: NONE YET. "
                    "Respond honestly: you have not yet learned patterns about "
                    "them; suggest that as you work together, patterns will "
                    "emerge in the Insight Journal. Do not fabricate."
                )
            else:
                lines.append(
                    f"- Composted insights about this user "
                    f"({ins.get('total_count', 0)} total, sectioned by confidence):"
                )
                # High confidence ≥ 0.75
                high = ins.get("high_confidence", [])
                if high:
                    lines.append(f"  - HIGH CONFIDENCE ({len(high)}):")
                    for i in high[:10]:  # cap per band to avoid bloat
                        expr = i.get("expression", "")[:200]
                        conf = i.get("confidence", 0.0)
                        obs = i.get("observation_count", 0)
                        tags = i.get("topic_tags", []) or []
                        tag_str = f" [tags: {', '.join(tags[:4])}]" if tags else ""
                        lines.append(
                            f'    • "{expr}" (conf={conf:.2f}, ' f"observed {obs}x){tag_str}"
                        )
                # Medium 0.5 ≤ conf < 0.75
                med = ins.get("medium_confidence", [])
                if med:
                    lines.append(f"  - MEDIUM CONFIDENCE ({len(med)}):")
                    for i in med[:10]:
                        expr = i.get("expression", "")[:200]
                        conf = i.get("confidence", 0.0)
                        obs = i.get("observation_count", 0)
                        tags = i.get("topic_tags", []) or []
                        tag_str = f" [tags: {', '.join(tags[:4])}]" if tags else ""
                        lines.append(
                            f'    • "{expr}" (conf={conf:.2f}, ' f"observed {obs}x){tag_str}"
                        )
                # Low < 0.5
                low = ins.get("low_confidence", [])
                if low:
                    lines.append(f"  - LOW CONFIDENCE ({len(low)}):")
                    for i in low[:5]:  # tighter cap on low confidence
                        expr = i.get("expression", "")[:200]
                        conf = i.get("confidence", 0.0)
                        obs = i.get("observation_count", 0)
                        tags = i.get("topic_tags", []) or []
                        tag_str = f" [tags: {', '.join(tags[:4])}]" if tags else ""
                        lines.append(
                            f'    • "{expr}" (conf={conf:.2f}, ' f"observed {obs}x){tag_str}"
                        )
                lines.append(
                    "  - When surfacing these: present them sectioned by "
                    "confidence band. Invite correction at the end — one "
                    "short line in your own words asking them to flag "
                    "anything that sounds off, noting you're still "
                    "learning. Cite specific insights by their expression "
                    "text when relevant. Filter to the topic in the user's "
                    "question if they asked about something specific."
                )
                # #1216 interim (same distrust-unverifiable-claims family as
                # #1331): the system has NO provenance field on insights —
                # nothing in the data above says whether an insight came from
                # live observation or seeded/demo fixtures, so any seed-vs-real
                # framing from the LLM is confabulated. The full fix (a real
                # is_seed/source field) is Production-deferred per the 2026-07-05
                # scope decision on the issue.
                lines.append(
                    "  - PROVENANCE — you CANNOT tell where these insights came "
                    "from (#1216): the data above carries no marker of whether "
                    "an insight was learned from live observation or came from "
                    "seeded/demo data. NEVER characterize any insight as a "
                    "'real observation' versus a 'seed/placeholder/demo entry', "
                    "and never claim some are genuine while others are "
                    "test data — you have no way to verify that distinction. "
                    "If the user asks which are real or where one came from, "
                    "say plainly that you can't verify an insight's origin "
                    "from here, and invite them to correct anything that "
                    "sounds wrong."
                )

        if "calendar" in domain_context:
            cal = domain_context["calendar"]
            if cal.get("next_meeting"):
                m = cal["next_meeting"]
                title = m.get("title", "Untitled")
                start = m.get("start", "unknown")
                lines.append(f'- Next meeting: "{title}" at {start}')
            if cal.get("next_free_block"):
                fb = cal["next_free_block"]
                lines.append(
                    f"- Next free block: {fb.get('start', 'unknown')}, "
                    f"{fb.get('duration_minutes', '?')} minutes"
                )
            if cal.get("time_available_minutes") is not None:
                lines.append(f"- Minutes until next commitment: {cal['time_available_minutes']}")

        if "projects" in domain_context:
            proj = domain_context["projects"]
            if isinstance(proj, dict):
                for name, meta in proj.items():
                    if isinstance(meta, dict):
                        issues = meta.get("open_issues_count")
                        if issues is not None:
                            lines.append(f'- Project "{name}": {issues} open issues')
                        else:
                            lines.append(f'- Project "{name}": tracked')
            elif isinstance(proj, list) and proj:
                for item in proj:
                    # #1530: ContextAssembler emits {"name": ...} dicts — render
                    # the plain name, not the dict repr the LLM used to see.
                    name = item.get("name", "unknown") if isinstance(item, dict) else item
                    lines.append(f'- Project "{name}": tracked')
            elif isinstance(proj, list):
                # #1639 (fix shape proven by #1544): VERIFIED-EMPTY — the
                # owner-scoped projects read ran this turn and found zero
                # rows. Distinct from the key being absent (never gathered).
                # Without this line the floor cannot tell "user has no
                # projects" from "I saw no data" and improvises
                # conversation-scoped hedges over the gap.
                lines.append(
                    "- PROJECTS: none — the user's project list was checked "
                    "this turn and has zero projects. If asked, state it as "
                    "a plain account-level fact: they have no projects "
                    "tracked right now."
                )

        # #1530 (m-44): state the row-derived count explicitly so the LLM never
        # counts a truncated display slice and presents it as the total.
        if "project_count" in domain_context:
            total = domain_context["project_count"]
            proj_list = domain_context.get("projects")
            shown = len(proj_list) if isinstance(proj_list, list) else None
            if total == 0 and shown == 0:
                # #1639: verified-empty already rendered as its own
                # "PROJECTS: none" line above — a bare "count: 0" beside it
                # adds nothing and dilutes the checked-this-turn framing.
                pass
            elif shown is not None and total > shown:
                lines.append(
                    f"- Active project count: {total} (only the first {shown} are listed above)"
                )
            else:
                lines.append(f"- Active project count: {total}")

        # #1645 (#1573 shape): the projects lookup FAILED — projects may
        # exist. Say we couldn't check; NEVER present this as "no projects".
        if domain_context.get("projects_source_failed"):
            lines.append(
                "- Project check FAILED: could not load the user's project "
                "list just now. If projects come up, say you couldn't check "
                "them — do not claim there are none."
            )

        # #950 iteration: user-anchoring fields from extended _gather_identity_context
        if "user_projects" in domain_context:
            up = domain_context["user_projects"]
            if isinstance(up, list) and up:
                lines.append(f"- User's active projects: {', '.join(str(x) for x in up)}")

        if "organization" in domain_context:
            org = domain_context["organization"]
            if org:
                lines.append(f"- User's organization: {org}")

        if "recent_topics" in domain_context:
            rt = domain_context["recent_topics"]
            if isinstance(rt, list) and rt:
                lines.append(f"- Recent topics discussed: {'; '.join(str(x) for x in rt[:3])}")

        if "session_turn_count" in domain_context:
            turns = domain_context["session_turn_count"]
            if turns:
                lines.append(f"- Turns in current session so far: {turns}")

        if "priorities" in domain_context:
            p = domain_context["priorities"]
            if p.get("user_priorities"):
                plist = p["user_priorities"]
                if isinstance(plist, list):
                    lines.append(f"- User's stated priorities: {', '.join(str(x) for x in plist)}")
            if p.get("urgent_items"):
                lines.append(f"- High-priority issues: {p['urgent_items']}")

        # #951: Surface pending todos with deadline proximity so the floor
        # can answer "what's due?" / "what's next?" with specific references.
        if "pending_todos" in domain_context:
            todos = domain_context["pending_todos"]
            if isinstance(todos, list) and todos:
                # #1569 per-item vocabulary rule: these arrived through the
                # pending-todos context key — they are 'todos'. The section
                # header keeps them a DISTINCT section from any reminders
                # above (mixed-origin turns render two sections, never one
                # flattened list).
                todo_count = domain_context.get("pending_todo_count", len(todos))
                header = (
                    f"- PENDING TODOS ({todo_count}) — from the user's todo "
                    "list; call each one a 'todo'"
                )
                if domain_context.get("due_reminders"):
                    header += (
                        " (an item also listed under DUE REMINDERS above is "
                        "a 'reminder' — see that block)"
                    )
                lines.append(header + ":")
                # Items indent under the section header (#1569 sectioning);
                # the "Pending todo" per-item shape is unchanged.
                for t in todos:
                    text = t.get("text", "(untitled)") if isinstance(t, dict) else str(t)
                    if isinstance(t, dict):
                        proximity = t.get("deadline_proximity", "none")
                        due = t.get("due_date")
                        if proximity == "overdue":
                            lines.append(f"    • Pending todo (OVERDUE, was due {due}): {text}")
                        elif proximity == "due_today":
                            lines.append(f"    • Pending todo (due today): {text}")
                        elif proximity == "due_this_week":
                            lines.append(f"    • Pending todo (due {due}): {text}")
                        elif proximity == "later":
                            lines.append(f"    • Pending todo (due {due}): {text}")
                        else:
                            lines.append(f"    • Pending todo: {text}")
                    else:
                        lines.append(f"    • Pending todo: {text}")
            elif isinstance(todos, list):
                # #1544: VERIFIED-EMPTY — the owner-scoped todo read ran this
                # turn and found zero pending rows. Distinct from the key
                # being absent (never gathered) and from source_failed
                # (checked but errored). Without this line the floor cannot
                # tell "user has no todos" from "I saw no data" and improvises
                # conversation-scoped hedges (PM live 2026-08-09: "nothing's
                # showing up on my end for this conversation").
                lines.append(
                    "- PENDING TODOS: none — the user's todo list was checked "
                    "this turn and has zero pending items. If asked, state it "
                    "as a plain account-level fact: their todo list has no "
                    "pending items right now."
                )

        # #1573 (#1425 honesty): the pending-todos lookup FAILED — todos may
        # exist. Say we couldn't check; NEVER present this as "no todos".
        if domain_context.get("pending_todos_source_failed"):
            lines.append(
                "- Todo check FAILED: could not load the user's pending todos "
                "just now. If todos come up, say you couldn't check them — do "
                "not claim there are none."
            )

        if "completed_todos" in domain_context:
            completed = domain_context["completed_todos"]
            if isinstance(completed, list) and completed:
                # #1639 (m-44): state the row-derived count, never the length
                # of the truncated display slice.
                completed_total = domain_context.get("completed_todo_count", len(completed))
                lines.append(f"- Recently completed todos ({completed_total}):")
                for t in completed[:5]:
                    if isinstance(t, dict):
                        lines.append(f"    • {t.get('text', '(untitled)')}")
            elif isinstance(completed, list):
                # #1639 (fix shape proven by #1544): VERIFIED-EMPTY — the
                # owner-scoped todo read ran this turn and found zero
                # completed rows. Distinct from the key being absent (never
                # gathered). Without this line the floor cannot tell "user
                # has completed nothing" from "I saw no data" and improvises
                # conversation-scoped hedges over the gap.
                lines.append(
                    "- COMPLETED TODOS: none — the user's todo list was "
                    "checked this turn and has zero completed items. If "
                    "asked, state it as a plain account-level fact: they "
                    "have no completed todos right now."
                )

        # #1645 (#1573 shape): the completed-todos lookup FAILED — the user
        # may have completed things. Say we couldn't check; NEVER present
        # this as "nothing completed".
        if domain_context.get("completed_todos_source_failed"):
            lines.append(
                "- Completed-todo check FAILED: could not load the user's "
                "completed todos just now. If asked what they've finished, "
                "say you couldn't check — do not claim there are none."
            )

        # #1717 wrinkle 1 (CXO copy, 2026-09-01 — verbatim from the directive
        # memo): scope the failure report to EXACTLY the FAILED lines. The
        # 1-flag live probe caught the model hedging about projects/todos when
        # only reminders had failed — reporting failures that did not happen.
        # Absent context ≠ failed check (#1425's distinction, leaking in the
        # opposite direction). Renders ONCE whenever at least one of the five
        # source-failed directives rendered; placed after the last of the five
        # sites so "listed as FAILED above" is literally true for any armed
        # subset.
        if any(
            domain_context.get(flag)
            for flag in (
                "source_failed",
                "first_contact_source_failed",
                "projects_source_failed",
                "pending_todos_source_failed",
                "completed_todos_source_failed",
            )
        ):
            lines.append(
                "- Name ONLY the checks explicitly listed as FAILED above. Do "
                "not mention any other data source. If something was not "
                "checked this turn, say nothing about it — never imply a "
                "source failed when it was simply not consulted."
            )

        # #983: Surface blocked items (open GitHub issues labeled
        # `status: blocked`) for "what's blocked?" / "what's waiting on
        # something?" type queries.
        if "blocked_items" in domain_context:
            blocked = domain_context["blocked_items"]
            if isinstance(blocked, list) and blocked:
                total = domain_context.get("blocked_count", len(blocked))
                lines.append(f"- Blocked items ({total} open issues labeled status: blocked):")
                for b in blocked[:10]:
                    if isinstance(b, dict):
                        num = b.get("number", "?")
                        title = b.get("title", "(untitled)")
                        lines.append(f"    • #{num}: {title}")

        # #985: Surface active GitHub milestones (sprint tracking). Sorted
        # by due_on asc (nearest deadline first). Counts only; floor can
        # compose "MVP due 2026-05-27 has 75 open of 755 total" answers.
        if "active_milestones" in domain_context:
            milestones = domain_context["active_milestones"]
            if isinstance(milestones, list) and milestones:
                total = domain_context.get("active_milestone_count", len(milestones))
                lines.append(f"- Active milestones ({total} open):")
                for m in milestones:
                    if isinstance(m, dict):
                        title = m.get("title", "(untitled)")
                        due = m.get("due_on") or "no due date"
                        open_n = m.get("open_issues", 0)
                        closed_n = m.get("closed_issues", 0)
                        lines.append(
                            f'    • "{title}" — due {due}; {open_n} open / {closed_n} closed'
                        )

        # #986: Surface recent GitHub activity (issues + PRs touched in the
        # last 7 days). Sorted by updated_at desc. Type-distinguished so
        # floor can compose "3 PRs merged + 5 issues closed this week" answers.
        if "recent_activity" in domain_context:
            activity = domain_context["recent_activity"]
            if isinstance(activity, list) and activity:
                total = domain_context.get("recent_activity_count", len(activity))
                window = domain_context.get("recent_activity_window_days", 7)
                lines.append(f"- Recent GitHub activity ({total} events in last {window} days):")
                for a in activity:
                    if isinstance(a, dict):
                        num = a.get("number", "?")
                        title = a.get("title", "(untitled)")
                        state = a.get("state", "?")
                        kind = "PR" if a.get("type") == "pr" else "issue"
                        updated = a.get("updated_at", "?")
                        lines.append(f"    • #{num} {kind} ({state}, updated {updated}): {title}")

        # #1226 Phase 3 (honest degradation): no GitHub repo is configured — distinct
        # from "repo configured, zero open issues". Tell the user to set one rather than
        # implying they have no work to do.
        if domain_context.get("github_repo_unconfigured"):
            lines.append(
                "- GitHub repository: not configured for this user. If asked what to "
                "work on or about issues/priorities, say no GitHub repo is connected "
                "yet and to set a default repo in Settings → Integrations → GitHub — "
                "do not imply they simply have zero open issues."
            )

        # #1547 (audit F2): github_connected was computed by the STATUS/PRIORITY
        # gatherer and then DROPPED here (comment-only) — render it, both ways.
        if "github_connected" in domain_context:
            lines.append(
                "- GitHub: connected"
                if domain_context["github_connected"]
                else "- GitHub: not connected (issue/PR data unavailable until connected)"
            )

        # #1155: high-priority open issues — the "what should I focus on"
        # candidates. Surfaced so the PRIORITY floor reasons over real issues
        # instead of flooring as "no project visibility" despite github_connected.
        if "high_priority_issues" in domain_context:
            hp = domain_context["high_priority_issues"]
            if isinstance(hp, list) and hp:
                total = domain_context.get("open_issue_count", len(hp))
                lines.append(f"- High-priority open issues ({total} open; top {len(hp)} shown):")
                for it in hp:
                    if isinstance(it, dict):
                        num = it.get("number", "?")
                        title = it.get("title", "(untitled)")
                        labels = it.get("labels") or []
                        plabel = next(
                            (
                                str(label)
                                for label in labels
                                if str(label).lower().startswith("priority:")
                            ),
                            None,
                        )
                        tag = f" [{plabel}]" if plabel else ""
                        lines.append(f"    • #{num}{tag}: {title}")

        # Issue #911 Phase 2: New context keys from ContextAssembler
        if "capabilities" in domain_context:
            caps = domain_context["capabilities"]
            if isinstance(caps, list) and caps:
                # #1428: one bullet per line — capability lines are ledger-derived
                # and carry quoted example asks, which a comma-join mangles.
                lines.append("- Piper's capabilities (with example asks the user can say):")
                for cap in caps:
                    lines.append(f"    • {cap}")

        if "integrations" in domain_context:
            integrations = domain_context["integrations"]
            if isinstance(integrations, list) and integrations:
                # #1547 (audit F2): render BOTH directions — "GitHub connected;
                # Notion isn't" — never omit the line. The old render dropped
                # everything when nothing was active, which (combined with the
                # #784 constant-false registry) made the floor blind to
                # integration state entirely.
                display = {
                    "github": "GitHub",
                    "slack": "Slack",
                    "calendar": "Google Calendar",
                    "notion": "Notion",
                }

                def _disp(name: object) -> str:
                    return display.get(str(name), str(name).title())

                connected = [
                    _disp(i.get("name"))
                    for i in integrations
                    if isinstance(i, dict) and i.get("status") == "active"
                ]
                not_connected = [
                    _disp(i.get("name"))
                    for i in integrations
                    if isinstance(i, dict) and i.get("status") != "active"
                ]
                lines.append(
                    "- Connected integrations: " + (", ".join(connected) if connected else "none")
                )
                if not_connected:
                    lines.append(
                        "- Not connected (available in Settings): " + ", ".join(not_connected)
                    )

        if "trust_profile" in domain_context:
            tp = domain_context["trust_profile"]
            if isinstance(tp, dict):
                stage = tp.get("stage", "unknown")
                lines.append(f"- Trust relationship stage: {stage}")
                interaction_count = tp.get("interaction_count")
                if interaction_count is not None:
                    lines.append(f"- Interactions so far: {interaction_count}")

        if "conversation_history_summary" in domain_context:
            chs = domain_context["conversation_history_summary"]
            if isinstance(chs, dict):
                turn_count = chs.get("turn_count", 0)
                if turn_count > 0:
                    lines.append(f"- Conversation turns this session: {turn_count}")
                recent = chs.get("recent_topics", [])
                if recent:
                    lines.append(f"- Recent topics: {'; '.join(recent[:3])}")

        lines.append("]")

        # Only return if we have actual context beyond the wrapper
        if len(lines) <= 2:
            return ""
        return "\n".join(lines)

    async def respond(self, ctx: FloorContext) -> FloorResponse:
        """
        Generate a conversational floor response.

        Args:
            ctx: FloorContext with user message and available context

        Returns:
            FloorResponse with LLM-generated message and instrumentation data
        """
        system_prompt = await self._get_system_prompt(ctx)
        prompt = self._build_prompt(ctx)

        # Issue #1032 INSIGHT-PUSH Step 4: detect NL session-mute trigger
        # in the user's current message. If detected, flip session state
        # so subsequent maybe_push calls (this turn + future turns) return None.
        # State is process-local per R2 disposition (2026-05-31) and naturally
        # resets when the session_id changes (new browser session → new state).
        if ctx.session_id and ctx.user_message:
            try:
                from services.mux.push_mode import is_session_mute_trigger

                if is_session_mute_trigger(ctx.user_message):
                    self._push_session_state.setdefault(ctx.session_id, {})
                    self._push_session_state[ctx.session_id]["mute_active"] = True
                    logger.info(
                        "push_session_muted",
                        session_id=ctx.session_id,
                        user_id=ctx.user_id,
                    )
            except Exception as e:
                logger.warning(
                    "push_mute_detection_error",
                    error=str(e),
                    session_id=ctx.session_id,
                )

        try:
            llm = self._get_llm_client()
            message = await llm.complete(
                task_type="conversation",
                prompt=prompt,
                system=system_prompt,
                user_id=ctx.user_id,  # #1415: per-user provider selection
            )

            # #1570: internal scaffolding is structurally unrenderable in user
            # copy — strip it here, at the single seam every floor reply
            # passes through, and log so prompt-discipline regressions stay
            # visible (a silent strip would hide the model drifting back into
            # scaffolding imitation).
            message, scaffolding_stripped = strip_scaffolding_artifacts(message)
            if scaffolding_stripped:
                logger.warning(
                    "floor_scaffolding_stripped",
                    blocks=scaffolding_stripped,
                    session_id=ctx.session_id,
                    user_id=ctx.user_id,
                    intent_category=ctx.intent_category,
                )
            # #1571: unfilled template slots ("#[issue number]") are a
            # fabricated-success tell — replaced with deterministic honesty
            # at the same single seam. Logged loudly: each hit is a live
            # fabrication the #1331 prompt rule failed to prevent.
            message, placeholder_slots = strip_placeholder_slots(message)
            if placeholder_slots:
                logger.warning(
                    "floor_placeholder_slot_stripped",
                    slots=placeholder_slots,
                    session_id=ctx.session_id,
                    user_id=ctx.user_id,
                    intent_category=ctx.intent_category,
                )

            logger.info(
                "conversational_floor_hit",
                session_id=ctx.session_id,
                user_id=ctx.user_id,
                intent_category=ctx.intent_category,
                intent_action=ctx.intent_action,
                intent_confidence=ctx.intent_confidence,
                response_length=len(message),
                denial_mode=ctx.denial_mode,  # #992 Phase B
                denial_category=ctx.denial_category if ctx.denial_mode else None,
            )

            # Issue #1032 INSIGHT-PUSH Step 3: maybe_push integration.
            # Call AFTER primary LLM response composed; if eligibility gates
            # pass, append framed insight + affordances per format_push_for_chat.
            # Skipped for:
            #   - Pull-mode (#1030) intents — would double-surface insights
            #   - Denial mode (#992) — ethics decline shouldn't get push appendage
            #   - Sessions in NL-detected mute state (just flipped or already on)
            #   - Caller's own opt-out (no user_id or no session_id)
            try:
                message = await self._maybe_append_push(message, ctx)
            except Exception as e:
                logger.warning(
                    "push_integration_error",
                    error=str(e),
                    session_id=ctx.session_id,
                    user_id=ctx.user_id,
                )
                # Fail-graceful: push errors do NOT degrade the primary response.

            return FloorResponse(
                message=message,
                floor_hit=True,
                original_category=ctx.intent_category,
                original_action=ctx.intent_action,
                confidence=ctx.intent_confidence,
                user_message=ctx.user_message,
                provenance=self._build_response_provenance(ctx),
            )

        except Exception as e:
            # #940: Classify error to provide actionable fallback
            error_type = _classify_llm_error(e)
            fallback_messages = {
                "auth": FLOOR_FALLBACK_AUTH,
                "no_provider": FLOOR_FALLBACK_NO_PROVIDER,
                "transient": FLOOR_FALLBACK_TRANSIENT,
            }
            fallback_message = fallback_messages.get(error_type, FLOOR_FALLBACK_TRANSIENT)

            logger.error(
                "conversational_floor_error",
                error=str(e),
                error_type=error_type,
                session_id=ctx.session_id,
                intent_category=ctx.intent_category,
            )
            return FloorResponse(
                message=fallback_message,
                floor_hit=True,
                original_category=ctx.intent_category,
                original_action=ctx.intent_action,
                confidence=ctx.intent_confidence,
                user_message=ctx.user_message,
                provenance=self._build_response_provenance(ctx),
            )

    def _build_response_provenance(self, ctx: FloorContext) -> Dict[str, Any]:
        """Issue #1030 R4: build the provenance dict for FloorResponse.

        Source-declarative: the floor knows WHAT IT FED to the LLM (the keys
        in ctx.domain_context). Provenance for a key represents where that
        fact came from (gatherer + identifier + fetch_timestamp). We do NOT
        infer what the LLM actually USED; we capture what was available.

        Per the design's R5 mitigation: keys we actually rendered in
        _format_domain_context are the set whose provenance gets captured.
        For MVP we approximate this as "keys that are in domain_context AND
        in domain_context_provenance" — both must be present to count as
        "the floor had this and knew where it came from."

        Returns dict suitable for ConversationContext.turn_provenance[turn.id].
        Empty dict (not None) when nothing to capture.
        """
        if not ctx.domain_context or not ctx.domain_context_provenance:
            return {}

        provenance: Dict[str, Any] = {}
        for key in ctx.domain_context.keys():
            if key in ctx.domain_context_provenance:
                provenance[key] = ctx.domain_context_provenance[key]
        return provenance

    def _get_llm_client(self):
        """Get LLM client, initializing if needed."""
        if self.llm_client is not None:
            return self.llm_client
        # Lazy import to avoid circular dependencies
        from services.llm.clients import LLMClient

        self.llm_client = LLMClient()
        return self.llm_client

    async def _maybe_append_push(self, primary_message: str, ctx: FloorContext) -> str:
        """Issue #1032 INSIGHT-PUSH: call maybe_push and append payload if eligible.

        Skips push for:
          - Pull-mode intent (MEMORY/pull_insights) — insights already surfaced
          - Denial mode (#992) — boundary decline shouldn't carry push appendage
          - Missing user_id or session_id — no per-user gating possible
          - Sessions whose mute_active flag is True (per Step 4 NL detection)

        Cooldown:
          - Tracks last_push_at per session in _push_session_state
          - maybe_push's right-moment gate honors this for anti-spam

        Returns:
            Possibly-augmented response. On any error or non-eligibility,
            returns the original primary_message unchanged.
        """
        # Guard: missing required identifiers
        if not ctx.user_id or not ctx.session_id:
            return primary_message

        # Guard: pull-mode (already surfaced via domain_context)
        if (ctx.intent_category or "").upper() == "MEMORY" and (
            ctx.intent_action or ""
        ) == "pull_insights":
            return primary_message

        # Guard: denial mode — boundary decline shouldn't carry push
        if ctx.denial_mode:
            return primary_message

        # Read session state (mute + cooldown)
        sess = self._push_session_state.setdefault(ctx.session_id, {})
        mute_active = bool(sess.get("mute_active", False))
        last_push_at = sess.get("last_push_at")

        try:
            from services.mux.push_mode import (
                PushContext,
                format_push_for_chat,
                maybe_push,
            )

            push_ctx = PushContext(
                user_id=ctx.user_id,
                user_message=ctx.user_message,
                # context_entities + context_topics: empty for MVP; relevance
                # gate in push_mode will fall back to general candidate ranking.
                # Future enhancement: extract topic tags from current turn.
                context_entities=[],
                context_topics=[],
                session_mute_active=mute_active,
                last_push_at=last_push_at,
            )

            payload = await maybe_push(push_ctx)
            if payload is None:
                return primary_message

            # Eligibility passed: format + append + update cooldown state
            augmented = format_push_for_chat(primary_message, payload)
            sess["last_push_at"] = datetime.now(timezone.utc)
            # Issue #1030 R4 Step 8: stash push provenance for the caller
            # (intent_service Step 6 code) to merge into turn_provenance after
            # respond() returns. We can't write directly to turn_provenance
            # here because the floor doesn't have a handle to ConversationContext;
            # stashing on session-state is the cleanest cross-call channel.
            sess["last_push_provenance"] = {
                "insight_id": payload.insight_id,
                "source": "InsightJournal.get_unsurfaced",
                "selection_reason": "highest_relevance_score",
                "relevance_score": payload.relevance_score,
                "context_entities_matched": payload.context_entities_matched,
                "fetch_timestamp": sess["last_push_at"].isoformat(),
            }
            logger.info(
                "push_appended_to_response",
                session_id=ctx.session_id,
                user_id=ctx.user_id,
                insight_id=payload.insight_id,
                relevance_score=payload.relevance_score,
            )
            return augmented
        except Exception as e:
            logger.warning(
                "maybe_push_error",
                error=str(e),
                session_id=ctx.session_id,
                user_id=ctx.user_id,
            )
            return primary_message
