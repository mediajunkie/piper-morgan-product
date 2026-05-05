"""
Lens Inference (#763 GLUE-FOLLOWUP)

Maps classified intents to conversational lens types.
The lens tracks "what aspect of the user's world" the conversation is about,
enabling follow-up queries to inherit context.

Phase 2: Rule-based mapping (intent category/action → lens type)
Phase 3: LLM lens decoder (for complex follow-ups rules can't handle)
"""

import json
import re
from typing import Any, Optional

import structlog

from services.domain.models import Intent
from services.shared_types import ConversationalLens, IntentCategory

logger = structlog.get_logger()

# Intent action → lens mapping.
# Actions not listed here fall through to category-based mapping.
ACTION_TO_LENS: dict[str, str] = {
    # Calendar actions
    "meeting_time": ConversationalLens.CALENDAR,
    "schedule_meeting": ConversationalLens.CALENDAR,
    "cancel_meeting": ConversationalLens.CALENDAR,
    "reschedule_meeting": ConversationalLens.CALENDAR,
    "check_availability": ConversationalLens.CALENDAR,
    "list_meetings": ConversationalLens.CALENDAR,
    "agenda": ConversationalLens.CALENDAR,
    # Issue actions
    "list_issues": ConversationalLens.ISSUES,
    "create_issue": ConversationalLens.ISSUES,
    "close_issue": ConversationalLens.ISSUES,
    "reopen_issue": ConversationalLens.ISSUES,
    "reopen_issue_query": ConversationalLens.ISSUES,
    "list_blockers": ConversationalLens.ISSUES,
    "count_issues": ConversationalLens.ISSUES,
    "list_pull_requests": ConversationalLens.ISSUES,
    "list_prs": ConversationalLens.ISSUES,
    "list_prs_query": ConversationalLens.ISSUES,
    "list_todos": ConversationalLens.ISSUES,
    # Project actions
    "project_status": ConversationalLens.PROJECTS,
    "project_timeline": ConversationalLens.PROJECTS,
    "work_summary": ConversationalLens.PROJECTS,
    # Issue #1039: GitHub milestone + release listing
    "list_milestones_query": ConversationalLens.PROJECTS,
    "list_releases_query": ConversationalLens.PROJECTS,
    # People actions
    "list_team": ConversationalLens.PEOPLE,
    "team_assignments": ConversationalLens.PEOPLE,
    "person_tasks": ConversationalLens.PEOPLE,
    "person_workload": ConversationalLens.PEOPLE,
    "team_workload": ConversationalLens.PEOPLE,
}

# Category → lens mapping (fallback when action isn't in ACTION_TO_LENS).
CATEGORY_TO_LENS: dict[IntentCategory, str] = {
    IntentCategory.STATUS: ConversationalLens.PROJECTS,
    IntentCategory.PRIORITY: ConversationalLens.ISSUES,
    IntentCategory.GUIDANCE: ConversationalLens.PROJECTS,
}

# Categories that should NOT get a lens (conversational, meta, etc.)
NO_LENS_CATEGORIES: set[IntentCategory] = {
    IntentCategory.CONVERSATION,
    IntentCategory.IDENTITY,
    IntentCategory.DISCOVERY,
    IntentCategory.UNKNOWN,
    IntentCategory.TRUST,
    IntentCategory.MEMORY,
}


def extract_lens_from_intent(intent: Intent) -> Optional[str]:
    """
    Infer the conversational lens from a classified intent.

    Checks action first (more specific), then category (broader).
    Returns None for conversational/meta intents that shouldn't set a lens.

    Args:
        intent: The classified intent

    Returns:
        A ConversationalLens value string, or None if no lens applies
    """
    if intent.category in NO_LENS_CATEGORIES:
        return None

    # Action-specific mapping (most precise)
    lens = ACTION_TO_LENS.get(intent.action)
    if lens:
        return lens

    # Category-based fallback
    lens = CATEGORY_TO_LENS.get(intent.category)
    if lens:
        return lens

    # For QUERY/EXECUTION/etc. without a specific mapping,
    # return GENERAL rather than None — this indicates the system
    # is engaged with a specific task but we don't know which lens.
    if intent.category not in NO_LENS_CATEGORIES:
        return ConversationalLens.GENERAL

    return None


def is_lens_reset(
    new_lens: Optional[str],
    current_lens: Optional[str],
    intent: Intent,
) -> bool:
    """
    Detect if the new intent represents an explicit topic change (lens reset).

    A lens reset occurs when:
    - The new lens is a DIFFERENT concrete lens than the current one
    - AND the intent was NOT resolved as a follow-up (it's a new classification)

    This clears the lens stack since the user has explicitly changed context.
    """
    if not current_lens or not new_lens:
        return False

    # Same lens or GENERAL doesn't reset
    if new_lens == current_lens or new_lens == ConversationalLens.GENERAL:
        return False

    # Different concrete lens AND not a follow-up = explicit topic change
    follow_up_type = intent.context.get("follow_up_type")
    if follow_up_type:
        # This was resolved as a follow-up — NOT a reset
        return False

    return True


# ============================================================================
# Phase 3: LLM Lens Decoder
# ============================================================================

# Max message length to try the LLM decoder.
# Longer messages are likely new topics, not follow-ups.
MAX_DECODER_MESSAGE_LENGTH = 60

LENS_DECODER_PROMPT = """You are analyzing a conversational follow-up.

Recent conversation:
{conversation_history}

Current lens: {current_lens}
New message: "{message}"

Is this message a follow-up to the conversation above?
If yes, determine the intent within the current conversational context.

Respond with ONLY a JSON object:
{{
  "is_follow_up": true/false,
  "category": "query|execution|status|priority",
  "action": "the_intent_action",
  "lens": "{current_lens}",
  "entities": ["entity1", "entity2"],
  "reasoning": "brief explanation"
}}

If NOT a follow-up (new topic), respond:
{{"is_follow_up": false}}"""


def _format_conversation_history(
    turns: list[Any],
    max_turns: int = 3,
) -> str:
    """Format recent turns for the LLM decoder prompt."""
    recent = turns[-max_turns:] if len(turns) > max_turns else turns
    lines = []
    for i, turn in enumerate(recent, 1):
        # str(ConversationalLens.CALENDAR) gives "ConversationalLens.CALENDAR",
        # but .value gives "calendar" — use the value for cleaner prompts.
        lens_val = turn.lens.value if hasattr(turn.lens, "value") else turn.lens
        lens_info = f" [lens: {lens_val}]" if turn.lens else ""
        action_info = f" (action: {turn.intent.action})" if turn.intent else ""
        lines.append(f'Turn {i}: "{turn.message}"{action_info}{lens_info}')
    return "\n".join(lines)


def should_try_llm_decoder(
    message: str,
    current_lens: Optional[str],
) -> bool:
    """
    Heuristic: should we try the LLM decoder for this message?

    Conditions:
    - There IS a current lens (conversation has established context)
    - Message is short enough to plausibly be a follow-up
    - Message doesn't look like a greeting or meta-query
    """
    if not current_lens:
        return False

    if len(message) > MAX_DECODER_MESSAGE_LENGTH:
        return False

    # Skip obvious non-follow-ups
    lower = message.strip().lower()
    skip_prefixes = (
        "hello",
        "hi ",
        "hey",
        "good morning",
        "what can you",
        "who are you",
        "what's your name",
    )
    if any(lower.startswith(p) for p in skip_prefixes):
        return False

    return True


async def decode_follow_up_with_llm(
    message: str,
    turns: list[Any],
    current_lens: str,
    llm_service: Any,
    continuation_hint: Optional[str] = None,  # Issue #852
) -> Optional[Intent]:
    """
    Use the LLM to decode a complex follow-up that rules can't handle.

    This handles elliptical phrases ("And Sarah?"), comparative queries
    ("What about tomorrow instead?"), lens shifts within topic
    ("Who's attending?"), and action shifts ("Cancel the 2pm").

    Issue #852: Also handles contextual offer continuations when a
    continuation_hint is provided (user said "yes" to a contextual offer).

    Args:
        message: The user's follow-up message
        turns: Recent ConversationTurn objects
        current_lens: The current conversational lens
        llm_service: LLM service for the completion call
        continuation_hint: Optional hint about what was offered (#852)

    Returns:
        A resolved Intent if it's a follow-up, None if it's a new topic
    """
    history = _format_conversation_history(turns)

    # Issue #852: Enrich history with continuation context
    if continuation_hint:
        history += (
            f'\n\nPrevious offer: The user was offered "{continuation_hint}" '
            "and appears to be accepting."
        )

    prompt = LENS_DECODER_PROMPT.format(
        conversation_history=history,
        current_lens=current_lens,
        message=message,
    )

    try:
        response = await llm_service.complete(
            task_type="intent_classification",
            prompt=prompt,
        )

        # Parse JSON from response
        json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response, re.DOTALL)
        if not json_match:
            logger.warning("lens_decoder_no_json", response_preview=response[:100])
            return None

        parsed = json.loads(json_match.group(0))

        if not parsed.get("is_follow_up", False):
            return None

        # Build resolved intent
        category_str = parsed.get("category", "query").lower()
        try:
            category = IntentCategory(category_str)
        except ValueError:
            category = IntentCategory.QUERY

        return Intent(
            category=category,
            action=parsed.get("action", "unknown"),
            confidence=0.85,  # LLM decoder confidence
            context={
                "inherited_lens": parsed.get("lens", current_lens),
                "entities": parsed.get("entities", []),
                "follow_up_type": "llm_decoded",
                "reasoning": parsed.get("reasoning", ""),
            },
        )

    except (json.JSONDecodeError, KeyError) as e:
        logger.warning("lens_decoder_parse_error", error=str(e))
        return None
    except Exception as e:
        logger.error("lens_decoder_failed", error=str(e))
        return None
