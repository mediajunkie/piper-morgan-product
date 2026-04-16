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

Prohibitions:
- Do NOT introduce yourself or say your name unless asked
- Do NOT list your capabilities or redirect to help menus
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

    def __init__(self, llm_client=None, system_prompt_base: Optional[str] = None):
        """
        Args:
            llm_client: LLM client with async complete() method
            system_prompt_base: Base system prompt (Piper identity). If None,
                                loaded from piper_config_loader at call time.
        """
        self.llm_client = llm_client
        self._system_prompt_base = system_prompt_base

    def _get_system_prompt(self, ctx: FloorContext) -> str:
        """Build the full system prompt: base identity + floor addendum + warmth."""
        base = self._system_prompt_base
        if base is None:
            try:
                from services.configuration.piper_config_loader import piper_config_loader

                base = piper_config_loader.get_system_prompt()
            except Exception:
                base = "You are Piper Morgan, an AI product management assistant."

        warmth = ctx.format_warmth_guidance()
        return f"{base}\n\n{FLOOR_SYSTEM_PROMPT_ADDENDUM}{warmth}"

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
        """Build the user-facing prompt with conversation history and context."""
        parts = []

        # Conversation history for continuity
        history = ctx.format_conversation_history()
        if history:
            parts.append(f"Recent conversation:\n{history}\n")

        # Issue #911: Domain context — structured data assembled for this intent
        if ctx.domain_context:
            domain_block = self._format_domain_context(ctx.domain_context)
            if domain_block:
                parts.append(domain_block)

        # The current message
        parts.append(f"User: {ctx.user_message}")

        # Context about what Piper detected (helps the LLM understand the routing)
        # Issue #911: Skip for categories that are intentionally floor-routed
        if ctx.intent_category and ctx.intent_category not in self._FLOOR_NATIVE_CATEGORIES:
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
        system_prompt = self._get_system_prompt(ctx)
        prompt = self._build_prompt(ctx)

        try:
            llm = self._get_llm_client()
            message = await llm.complete(
                task_type="conversation",
                prompt=prompt,
                system=system_prompt,
            )

            logger.info(
                "conversational_floor_hit",
                session_id=ctx.session_id,
                user_id=ctx.user_id,
                intent_category=ctx.intent_category,
                intent_action=ctx.intent_action,
                intent_confidence=ctx.intent_confidence,
                response_length=len(message),
            )

            return FloorResponse(
                message=message,
                floor_hit=True,
                original_category=ctx.intent_category,
                original_action=ctx.intent_action,
                confidence=ctx.intent_confidence,
                user_message=ctx.user_message,
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
            )

    def _get_llm_client(self):
        """Get LLM client, initializing if needed."""
        if self.llm_client is not None:
            return self.llm_client
        # Lazy import to avoid circular dependencies
        from services.llm.clients import LLMClient

        self.llm_client = LLMClient()
        return self.llm_client
