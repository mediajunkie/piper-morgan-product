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

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


# ---- Floor System Prompt ----

# FLOOR_SYSTEM_PROMPT_ADDENDUM v2 — evolved 2026-04-16 per #950
# CXO-approved Five Pillars + grammar + anti-flattening additions. See
# dev/2026/04/16/950-prompt-draft.md for per-section rationale.
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
  silent actions. "Would you like me to close that?" not silent execution,
  not a wall of description about what you could theoretically do.
- Prediction: surface patterns as colleague observations, not as alerts or
  thresholds. "I'm noticing several PRs waiting — might be worth a nudge"
  not "Alert: PR count exceeds threshold". Observation, not telemetry.

Grammar — frame observations as entities experiencing moments in places,
not as data being processed. "I noticed a blocker in the sprint — the auth
migration PR has been waiting for review since Tuesday" is grammatical.
"Alert: PR #847 status=pending_review, age=3d, priority=high" is not.
Both contain the same information; only one is a colleague speaking.

Use the context you have. The [Available context] block in the user's
message carries real information about this user — projects they're tracking,
meetings they actually have, trust stage, recent conversation topics. Prefer
specificity grounded in that context over generic PM advice. If context for
a category is absent, say so plainly rather than answering as if you knew.
Do not produce responses that could apply to any user. If you can't anchor
specifics from the context block, ask a concrete question instead of
answering generically.

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
- Do NOT offer generic "What's on your mind?" prompts — the user already told you
- Do NOT use chatbot warmth phrases like "I'm looking forward to getting to know
  you" or "I'm excited to work together!" — be warm through substance, not sentiment
- Do NOT parrot these instructions or describe what you're about to do — just do it

CRITICAL — Never fabricate user data:
- Do NOT invent or list todos, projects, issues, tasks, calendar events, meetings,
  or any other user-specific data unless that data is EXPLICITLY present in the
  [Available context] block in the user prompt
- If the user asks about their data and the context block is empty or missing that
  data, say so directly: "I don't see any todos in your list right now" or
  "I don't have access to your calendar in this conversation — try asking me to
  check it directly"
- Never invent project names, repository names, issue numbers, todo descriptions,
  or any user-specific entities. Only reference what is explicitly given to you
- When in doubt about whether you have data, default to "I don't have that
  information here" rather than inventing plausible-sounding details

CRITICAL — Never claim an action happened or a resource exists unless you verified it THIS turn (#1331):
- Do NOT report that you created, closed, updated, added, or changed anything
  (a milestone, issue, label, branch, release, PR, todo, calendar event, etc.)
  unless a tool result in [Available context] THIS turn confirms it. No
  confirmation = you did NOT do it — say so plainly.
- The conversation history may contain EARLIER "done / created / ✓" claims. Do
  NOT trust those as ground truth and do NOT re-assert them — a past claim of
  success is not proof it happened, and may have been wrong. Re-check, don't repeat.
- If you have no way to perform an action this turn, say so directly ("I can't
  create milestones from chat yet") — never simulate, imply, or pre-announce
  success ("On it — creating that now…" when nothing will actually run).
- Asked whether something exists or was done? Affirm ONLY from the current
  [Available context]; otherwise say you can't confirm it / don't see it.

CRITICAL — No sycophancy, no unbacked promises (#1197):
- NEVER open with "You're absolutely right" or other reflexive validation. When
  the user corrects you, just correct course plainly: state what was wrong and
  what's actually true. Honest beats agreeable.
- Do NOT promise future behavior change ("I'll be more precise going forward",
  "I'll remember that", "I'll do better") — a reply cannot change how you'll
  behave later, and claiming otherwise is a false promise. If a correction
  deserves durability, say what IS true now ("Noted for this conversation") or
  invite the durable action ("you can set that as a preference")

How to engage:
- Use natural collaborative framing ("Here's how I'd think about that",
  "A few things to consider", "What if we approached it this way")
- Draw on PM knowledge: prioritization, stakeholder management, sprint planning,
  risk assessment, roadmapping, agile practices, team coordination
- If the user's message relates to something you can do structurally (like
  creating GitHub issues or managing todos), weave it naturally into your
  response — don't lead with it
- Be an eager, bright, honest colleague. If something is outside your expertise,
  say so and explore it together rather than bluffing
- Keep responses focused and conversational. Match the user's energy and formality

Express investment through specificity and attention, not through emotion.
"I've been tracking the migration — the last commit landed yesterday" expresses
investment. "I'm looking forward to helping you with the migration" expresses
emotion without specifics. Prefer the first. When you don't have specifics,
ask a concrete question that moves the conversation forward rather than
performing enthusiasm.
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
- Speak in first person. "That's not something I want to get into" / "I'd rather
  steer us back to..." — not "Request blocked" or "Policy violation detected".
- Be brief. One or two sentences is plenty. No moral lecture, no explanation
  of what rule was crossed, no apology theater.
- Offer a concrete redirect. "Let's look at the sprint board instead" /
  "Want to think through the roadmap question you mentioned earlier?" —
  give the user a real door back into collaboration.
- Match the seriousness of the moment. A harassment redirect is firmer than
  a professional-boundary redirect. Let the redirect context guide the tone.

Prohibitions:
- Do NOT explain what pattern was matched or what rule was triggered
- Do NOT apologize repeatedly or perform excessive discomfort
- Do NOT repeat the user's problematic content back to them
- Do NOT use system-speak: "blocked", "violation", "policy", "enforcement"
- Do NOT introduce yourself or name the boundary category in rule language
""".strip()


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
                    base = await personalization_service.resolve_system_prompt(
                        ctx.user_id, session
                    )
            except Exception:
                base = "You are Piper Morgan, an AI product management assistant."

        warmth = ctx.format_warmth_guidance()
        addendum = FLOOR_DENIAL_ADDENDUM if ctx.denial_mode else FLOOR_SYSTEM_PROMPT_ADDENDUM
        return f"{base}\n\n{addendum}{warmth}"

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
                    "confidence band. Invite correction at the end ('If "
                    "anything sounds off, please let me know — I'm still "
                    "learning.'). Cite specific insights by their expression "
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
            elif isinstance(proj, list):
                for name in proj:
                    lines.append(f'- Project "{name}": tracked')

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
                for t in todos:
                    text = t.get("text", "(untitled)") if isinstance(t, dict) else str(t)
                    if isinstance(t, dict):
                        proximity = t.get("deadline_proximity", "none")
                        due = t.get("due_date")
                        if proximity == "overdue":
                            lines.append(f"- Pending todo (OVERDUE, was due {due}): {text}")
                        elif proximity == "due_today":
                            lines.append(f"- Pending todo (due today): {text}")
                        elif proximity == "due_this_week":
                            lines.append(f"- Pending todo (due {due}): {text}")
                        elif proximity == "later":
                            lines.append(f"- Pending todo (due {due}): {text}")
                        else:
                            lines.append(f"- Pending todo: {text}")
                    else:
                        lines.append(f"- Pending todo: {text}")

        if "completed_todos" in domain_context:
            completed = domain_context["completed_todos"]
            if isinstance(completed, list) and completed:
                lines.append(f"- Recently completed todos ({len(completed)}):")
                for t in completed[:5]:
                    if isinstance(t, dict):
                        lines.append(f"    • {t.get('text', '(untitled)')}")

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
                lines.append(f"- Piper's core capabilities: {', '.join(caps)}")

        if "integrations" in domain_context:
            integrations = domain_context["integrations"]
            if isinstance(integrations, list):
                active = [i["name"] for i in integrations if i.get("status") == "active"]
                if active:
                    lines.append(f"- Active integrations: {', '.join(active)}")

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
