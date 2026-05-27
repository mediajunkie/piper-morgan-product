"""
Slot extraction engine for parsing user messages into slot values.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

Provides:
- LLM-based multi-slot extraction from natural language
- Skip-filled-slots logic (never re-ask for provided info)
- Grouped prompting (ask 2-3 related slots together)
"""

import json
from typing import Any, Optional

import structlog

from services.slot_filling.slot_template import SlotDefinition, SlotState, SlotTemplate

logger = structlog.get_logger()

# Maximum slots to prompt for at once (avoid interrogation feel)
MAX_PROMPT_GROUP_SIZE = 3


async def extract_slots(
    message: str,
    template: SlotTemplate,
    llm_service,
    existing_values: Optional[dict[str, Any]] = None,
    conversation_history: Optional[list[dict[str, str]]] = None,
) -> dict[str, Any]:
    """
    Extract slot values from a user message using LLM.

    Args:
        message: The user's message to extract slots from
        template: The slot template defining expected slots
        llm_service: LLM service with complete() method
        existing_values: Already-filled slot values (for update detection)
        conversation_history: Optional recent turns for antecedent resolution
            (e.g., "the doc" / "that one" / "it"). Format is OpenAI-style:
            [{"role": "user"|"assistant", "content": "..."}, ...].
            When provided, the LLM is instructed to resolve antecedent
            phrases against the most recent matching entity in history.
            See #1122 MULTI-TURN-DOC-ANTECEDENT (option B implementation).

    Returns:
        Dict of slot_name → extracted_value (only for slots found in message).
        Returns empty dict if extraction fails (graceful fallback).
    """
    if not message or not message.strip():
        return {}

    prompt = _build_extraction_prompt(message, template, existing_values, conversation_history)

    try:
        response = await llm_service.complete(
            task_type="slot_extraction",
            prompt=prompt,
            system=(
                "You are a slot extraction engine. Extract structured data from user messages. "
                "Respond ONLY with valid JSON. No explanation, no markdown."
            ),
        )
        return _parse_extraction_response(response, template)
    except Exception as e:
        logger.warning(
            "slot_extraction_failed",
            error=str(e),
            template=template.name,
            message_preview=message[:50],
        )
        return {}


def _build_extraction_prompt(
    message: str,
    template: SlotTemplate,
    existing_values: Optional[dict[str, Any]] = None,
    conversation_history: Optional[list[dict[str, str]]] = None,
) -> str:
    """Build the LLM prompt for slot extraction.

    When conversation_history is provided, prepends a Recent conversation
    section and adds antecedent-resolution instructions. See #1122 option B.
    """
    slot_descriptions = []
    for slot in template.slots:
        desc = f'- "{slot.name}" ({slot.slot_type.value}): {slot.display_name}'
        if slot.extraction_hint:
            desc += f" — {slot.extraction_hint}"
        slot_descriptions.append(desc)

    existing_info = ""
    if existing_values:
        existing_info = "\nAlready known values (check if user is updating any of these):\n"
        for name, value in existing_values.items():
            existing_info += f'- {name}: "{value}"\n'

    history_section = ""
    antecedent_instructions = ""
    if conversation_history:
        # Render recent turns in a compact dialog format.
        # Cap at most-recent 8 turns to keep prompt manageable while still
        # covering typical antecedent windows (resolution rarely reaches back
        # beyond 3-4 turns in practice).
        recent = conversation_history[-8:]
        history_lines = []
        for turn in recent:
            role = turn.get("role", "user")
            content = (turn.get("content") or "").strip()
            if not content:
                continue
            # Truncate very long turns to avoid prompt bloat
            if len(content) > 500:
                content = content[:497] + "..."
            history_lines.append(f"{role}: {content}")
        if history_lines:
            history_section = (
                "\nRecent conversation (most recent last):\n"
                + "\n".join(history_lines)
                + "\n"
            )
            antecedent_instructions = (
                "- Resolve antecedent phrases like 'the doc', 'that doc', 'that one', "
                "'it', 'the one I mentioned' against the most recent matching "
                "entity in the conversation history above\n"
                "- Only resolve antecedents to entities of the SAME TYPE as the slot "
                "(e.g., 'the doc' resolves to a document name, not to a person)\n"
                "- If no matching entity exists in history, do NOT guess — omit the slot\n"
            )

    return f"""Extract slot values from the user's message for a "{template.display_name}" workflow.

Slots to extract:
{chr(10).join(slot_descriptions)}
{existing_info}{history_section}
User message: "{message}"

Instructions:
- Extract ONLY values explicitly stated or clearly implied in the message
- Do NOT guess or infer values that aren't mentioned
- For each found slot, include it in the JSON with its value as a string
- If a slot is not mentioned, do NOT include it in the response
- If the user is updating a previously known value, include the new value
{antecedent_instructions}
Respond with a JSON object mapping slot names to extracted values.
Example: {{"attendee": "Sarah", "day": "Tuesday", "time": "2pm"}}
If no slots can be extracted, respond with: {{}}"""


def _parse_extraction_response(response: str, template: SlotTemplate) -> dict[str, Any]:
    """Parse LLM response into slot values dict."""
    response = response.strip()

    # Strip markdown code fences if present
    if response.startswith("```"):
        lines = response.split("\n")
        # Remove first and last lines (```json and ```)
        lines = [line for line in lines if not line.strip().startswith("```")]
        response = "\n".join(lines).strip()

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        logger.warning("slot_extraction_json_parse_failed", response_preview=response[:100])
        return {}

    if not isinstance(parsed, dict):
        logger.warning("slot_extraction_not_dict", response_type=type(parsed).__name__)
        return {}

    # Filter to only valid slot names
    valid_names = {s.name for s in template.slots}
    result = {}
    for key, value in parsed.items():
        if key in valid_names and value is not None and str(value).strip():
            result[key] = str(value).strip()

    return result


def update_slot_state(state: SlotState, extracted: dict[str, Any]) -> SlotState:
    """
    Apply extracted values to the slot state.

    Updates existing values if re-extracted (slot update support).
    Returns the same state object (mutated).
    """
    for name, value in extracted.items():
        state.set_value(name, value)
    return state


def get_missing_required(state: SlotState) -> list[SlotDefinition]:
    """Get required slots that haven't been filled yet."""
    return state.unfilled_required


def get_next_prompt_group(state: SlotState, lens: Optional[str] = None) -> list[SlotDefinition]:
    """
    Get the next group of missing slots to prompt for.

    Respects slot grouping (slots with the same group number are asked together).
    Caps at MAX_PROMPT_GROUP_SIZE to avoid overwhelming the user.

    When a conversational lens is active and the template defines
    lens_group_priority, groups are ordered by the lens preference
    instead of the default numeric order (Issue #821).

    Returns:
        List of SlotDefinitions to prompt for (max MAX_PROMPT_GROUP_SIZE)
    """
    missing = state.unfilled_required
    if not missing:
        return []

    # Group missing slots by their group number
    grouped: dict[Optional[int], list[SlotDefinition]] = {}
    for slot in missing:
        grouped.setdefault(slot.group, []).append(slot)

    # Determine group ordering — lens-aware or default
    if lens and state.template.lens_group_priority and lens in state.template.lens_group_priority:
        # Use lens-specific ordering, then fall back for any groups not listed
        priority_order = state.template.lens_group_priority[lens]
        sorted_groups = [g for g in priority_order if g in grouped]
        # Append any remaining groups not in the priority list
        remaining = sorted(
            [g for g in grouped if g not in sorted_groups],
            key=lambda g: (g is None, g or 0),
        )
        sorted_groups.extend(remaining)
    else:
        # Default: sort by group number (None last)
        sorted_groups = sorted(grouped.keys(), key=lambda g: (g is None, g or 0))

    if not sorted_groups:
        return []

    first_group = grouped[sorted_groups[0]]

    # Cap at MAX_PROMPT_GROUP_SIZE
    return first_group[:MAX_PROMPT_GROUP_SIZE]
