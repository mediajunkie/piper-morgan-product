"""
Tests for slot extraction engine.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation
Phase 2: Slot Extraction + Skip Logic

Tests cover:
- LLM-based extraction from full/partial/empty messages
- Slot update (override existing value)
- Skip-filled detection (missing required)
- Grouped prompting (next prompt group selection)
- Graceful fallback on LLM failure
"""

from unittest.mock import AsyncMock

import pytest

from services.slot_filling.slot_extractor import (
    MAX_PROMPT_GROUP_SIZE,
    _build_extraction_prompt,
    _parse_extraction_response,
    extract_slots,
    get_missing_required,
    get_next_prompt_group,
    update_slot_state,
)
from services.slot_filling.slot_template import (
    MEETING_TEMPLATE,
    SlotDefinition,
    SlotState,
    SlotTemplate,
    SlotType,
)


@pytest.fixture
def mock_llm():
    """Mock LLM service that returns configurable JSON responses."""
    llm = AsyncMock()
    llm.complete = AsyncMock(return_value="{}")
    return llm


@pytest.fixture
def meeting_state():
    """Fresh slot state for the meeting template."""
    return SlotState(template=MEETING_TEMPLATE)


# --- extract_slots Tests ---


class TestExtractSlots:
    @pytest.mark.asyncio
    async def test_full_extraction(self, mock_llm):
        """All slots extracted from a complete message."""
        mock_llm.complete.return_value = (
            '{"attendee": "Sarah", "day": "Tuesday", "time": "2pm", "topic": "Q3 planning"}'
        )
        result = await extract_slots(
            "Set up a meeting with Sarah Tuesday at 2pm about Q3 planning",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result["attendee"] == "Sarah"
        assert result["day"] == "Tuesday"
        assert result["time"] == "2pm"
        assert result["topic"] == "Q3 planning"

    @pytest.mark.asyncio
    async def test_partial_extraction(self, mock_llm):
        """Only some slots extracted from a partial message."""
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        result = await extract_slots(
            "Schedule something with Sarah",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {"attendee": "Sarah"}

    @pytest.mark.asyncio
    async def test_empty_extraction(self, mock_llm):
        """No slots parseable from message."""
        mock_llm.complete.return_value = "{}"
        result = await extract_slots(
            "Schedule a meeting",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {}

    @pytest.mark.asyncio
    async def test_empty_message(self, mock_llm):
        """Empty message returns empty dict without calling LLM."""
        result = await extract_slots("", MEETING_TEMPLATE, mock_llm)
        assert result == {}
        mock_llm.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_whitespace_only_message(self, mock_llm):
        """Whitespace-only message returns empty dict."""
        result = await extract_slots("   ", MEETING_TEMPLATE, mock_llm)
        assert result == {}
        mock_llm.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_llm_failure_returns_empty(self, mock_llm):
        """LLM failure returns empty dict (graceful fallback)."""
        mock_llm.complete.side_effect = RuntimeError("LLM unavailable")
        result = await extract_slots(
            "Meeting with Sarah Tuesday at 2pm",
            MEETING_TEMPLATE,
            mock_llm,
        )
        assert result == {}

    @pytest.mark.asyncio
    async def test_existing_values_passed_to_prompt(self, mock_llm):
        """Existing values are included in the extraction prompt for update detection."""
        mock_llm.complete.return_value = '{"time": "4pm"}'
        result = await extract_slots(
            "Actually make it 4pm",
            MEETING_TEMPLATE,
            mock_llm,
            existing_values={"attendee": "Sarah", "time": "3pm"},
        )
        assert result == {"time": "4pm"}
        # Verify existing values were in the prompt
        call_kwargs = mock_llm.complete.call_args
        assert "Sarah" in call_kwargs.kwargs.get(
            "prompt", call_kwargs.args[1] if len(call_kwargs.args) > 1 else ""
        )

    @pytest.mark.asyncio
    async def test_llm_called_with_correct_task_type(self, mock_llm):
        """LLM is called with 'slot_extraction' task type."""
        mock_llm.complete.return_value = "{}"
        await extract_slots("test message", MEETING_TEMPLATE, mock_llm)
        mock_llm.complete.assert_called_once()
        call_kwargs = mock_llm.complete.call_args
        assert call_kwargs.kwargs.get("task_type") == "slot_extraction"

    @pytest.mark.asyncio
    async def test_markdown_fences_stripped(self, mock_llm):
        """JSON wrapped in markdown code fences is handled."""
        mock_llm.complete.return_value = '```json\n{"attendee": "Sarah"}\n```'
        result = await extract_slots("With Sarah", MEETING_TEMPLATE, mock_llm)
        assert result == {"attendee": "Sarah"}


# --- _parse_extraction_response Tests ---


class TestParseExtractionResponse:
    def test_valid_json(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "time": "2pm"}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah", "time": "2pm"}

    def test_invalid_json(self):
        result = _parse_extraction_response("not json at all", MEETING_TEMPLATE)
        assert result == {}

    def test_json_array_not_dict(self):
        result = _parse_extraction_response('["Sarah", "2pm"]', MEETING_TEMPLATE)
        assert result == {}

    def test_invalid_slot_names_filtered(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "invalid_slot": "value"}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah"}
        assert "invalid_slot" not in result

    def test_null_values_filtered(self):
        result = _parse_extraction_response('{"attendee": "Sarah", "time": null}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_empty_string_values_filtered(self):
        result = _parse_extraction_response('{"attendee": "Sarah", "time": ""}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_whitespace_values_filtered(self):
        result = _parse_extraction_response(
            '{"attendee": "Sarah", "time": "   "}', MEETING_TEMPLATE
        )
        assert result == {"attendee": "Sarah"}

    def test_markdown_fences_stripped(self):
        result = _parse_extraction_response('```json\n{"attendee": "Sarah"}\n```', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}

    def test_values_stripped(self):
        result = _parse_extraction_response('{"attendee": "  Sarah  "}', MEETING_TEMPLATE)
        assert result == {"attendee": "Sarah"}


# --- update_slot_state Tests ---


class TestUpdateSlotState:
    def test_fill_empty_state(self, meeting_state):
        extracted = {"attendee": "Sarah", "day": "Tuesday"}
        update_slot_state(meeting_state, extracted)
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.get_value("day") == "Tuesday"
        assert meeting_state.filled_count == 2

    def test_update_existing_value(self, meeting_state):
        meeting_state.set_value("time", "3pm")
        update_slot_state(meeting_state, {"time": "4pm"})
        assert meeting_state.get_value("time") == "4pm"
        assert meeting_state.filled_count == 1

    def test_empty_extraction_no_change(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        update_slot_state(meeting_state, {})
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.filled_count == 1

    def test_additive_extraction(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        update_slot_state(meeting_state, {"day": "Tuesday", "time": "2pm"})
        assert meeting_state.filled_count == 3
        assert meeting_state.get_value("attendee") == "Sarah"
        assert meeting_state.get_value("day") == "Tuesday"


# --- get_missing_required Tests ---


class TestGetMissingRequired:
    def test_all_missing(self, meeting_state):
        missing = get_missing_required(meeting_state)
        assert len(missing) == 4  # All meeting slots are required

    def test_some_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        missing = get_missing_required(meeting_state)
        assert len(missing) == 2
        names = [s.name for s in missing]
        assert "time" in names
        assert "topic" in names

    def test_all_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        missing = get_missing_required(meeting_state)
        assert len(missing) == 0


# --- get_next_prompt_group Tests ---


class TestGetNextPromptGroup:
    def test_first_group_returned(self, meeting_state):
        """With all slots missing, returns group 0 (attendee, day, time)."""
        group = get_next_prompt_group(meeting_state)
        names = [s.name for s in group]
        # Group 0 has attendee, day, time
        assert "attendee" in names
        assert "day" in names
        assert "time" in names

    def test_capped_at_max_size(self):
        """Prompt group capped at MAX_PROMPT_GROUP_SIZE."""
        # Create template with many slots in one group
        slots = [SlotDefinition(name=f"s{i}", display_name=f"Slot {i}", group=0) for i in range(5)]
        template = SlotTemplate(name="big", display_name="Big", slots=slots)
        state = SlotState(template=template)
        group = get_next_prompt_group(state)
        assert len(group) <= MAX_PROMPT_GROUP_SIZE

    def test_skips_to_next_group(self, meeting_state):
        """When group 0 is filled, returns group 1."""
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        group = get_next_prompt_group(meeting_state)
        assert len(group) == 1
        assert group[0].name == "topic"

    def test_empty_when_all_filled(self, meeting_state):
        meeting_state.set_value("attendee", "Sarah")
        meeting_state.set_value("day", "Tuesday")
        meeting_state.set_value("time", "2pm")
        meeting_state.set_value("topic", "Q3 planning")
        group = get_next_prompt_group(meeting_state)
        assert len(group) == 0

    def test_ungrouped_slots_handled(self):
        """Slots without a group (None) are handled correctly."""
        template = SlotTemplate(
            name="test",
            display_name="Test",
            slots=[
                SlotDefinition(name="a", display_name="A", group=0),
                SlotDefinition(name="b", display_name="B"),  # group=None
            ],
        )
        state = SlotState(template=template)
        state.set_value("a", "filled")
        # Should return the ungrouped slot
        group = get_next_prompt_group(state)
        assert len(group) == 1
        assert group[0].name == "b"

    def test_partial_group_fill(self, meeting_state):
        """When some slots in a group are filled, only missing ones returned."""
        meeting_state.set_value("attendee", "Sarah")
        # day and time still missing in group 0
        group = get_next_prompt_group(meeting_state)
        names = [s.name for s in group]
        assert "attendee" not in names
        assert "day" in names
        assert "time" in names


# --- _build_extraction_prompt Tests ---


class TestBuildExtractionPrompt:
    def test_includes_slot_descriptions(self):
        prompt = _build_extraction_prompt("test message", MEETING_TEMPLATE)
        assert "attendee" in prompt
        assert "day" in prompt
        assert "time" in prompt
        assert "topic" in prompt

    def test_includes_user_message(self):
        prompt = _build_extraction_prompt("Meeting with Sarah", MEETING_TEMPLATE)
        assert "Meeting with Sarah" in prompt

    def test_includes_existing_values(self):
        prompt = _build_extraction_prompt(
            "Actually 4pm",
            MEETING_TEMPLATE,
            existing_values={"attendee": "Sarah", "time": "3pm"},
        )
        assert "Sarah" in prompt
        assert "3pm" in prompt

    def test_no_existing_values(self):
        prompt = _build_extraction_prompt("Schedule a meeting", MEETING_TEMPLATE)
        assert "Already known" not in prompt


# --- Conversation History / Antecedent Resolution Tests (#1122 option B) ---


class TestConversationHistoryInPrompt:
    """Verify _build_extraction_prompt renders conversation history when present."""

    def test_no_history_no_section(self):
        """Without conversation_history, prompt has no Recent conversation section."""
        prompt = _build_extraction_prompt("Schedule something", MEETING_TEMPLATE)
        assert "Recent conversation" not in prompt
        assert "antecedent" not in prompt.lower()

    def test_empty_history_no_section(self):
        """Empty conversation_history list also skips the section."""
        prompt = _build_extraction_prompt(
            "Schedule something",
            MEETING_TEMPLATE,
            conversation_history=[],
        )
        assert "Recent conversation" not in prompt

    def test_history_renders_user_and_assistant_turns(self):
        """Both roles appear in the prompt's Recent conversation section."""
        history = [
            {"role": "user", "content": "Update the Piper Morgan test page"},
            {"role": "assistant", "content": "Found Piper Morgan test page. What to add?"},
        ]
        prompt = _build_extraction_prompt(
            "Add a paragraph to the doc",
            MEETING_TEMPLATE,
            conversation_history=history,
        )
        assert "Recent conversation" in prompt
        assert "Piper Morgan test page" in prompt
        assert "Found Piper Morgan test page" in prompt

    def test_history_triggers_antecedent_instructions(self):
        """When history is present, antecedent-resolution instructions appear."""
        history = [{"role": "user", "content": "Update the Project Plan"}]
        prompt = _build_extraction_prompt(
            "Add a new section to the doc",
            MEETING_TEMPLATE,
            conversation_history=history,
        )
        assert "antecedent" in prompt.lower()
        assert "the doc" in prompt or "that doc" in prompt

    def test_history_caps_at_8_turns(self):
        """Only the most-recent 8 turns appear; older ones are pruned."""
        history = [
            {"role": "user", "content": f"turn-{i}"} for i in range(15)
        ]
        prompt = _build_extraction_prompt(
            "follow-up",
            MEETING_TEMPLATE,
            conversation_history=history,
        )
        # Last 8 should appear (turn-7 through turn-14)
        for i in range(7, 15):
            assert f"turn-{i}" in prompt
        # Earlier ones should NOT appear
        for i in range(0, 7):
            assert f"turn-{i}:" not in prompt and f"turn-{i} " not in prompt

    def test_history_truncates_long_turns(self):
        """Long turn content is truncated to keep prompt manageable."""
        long_content = "x" * 1000
        history = [{"role": "user", "content": long_content}]
        prompt = _build_extraction_prompt(
            "short follow-up",
            MEETING_TEMPLATE,
            conversation_history=history,
        )
        # Should NOT contain the full 1000-char string
        assert long_content not in prompt
        # Should contain the truncation indicator
        assert "..." in prompt

    def test_history_skips_empty_content_turns(self):
        """Turns with empty/whitespace content are skipped."""
        history = [
            {"role": "user", "content": "real message"},
            {"role": "assistant", "content": ""},
            {"role": "assistant", "content": "   "},
            {"role": "user", "content": "another real message"},
        ]
        prompt = _build_extraction_prompt(
            "follow-up",
            MEETING_TEMPLATE,
            conversation_history=history,
        )
        assert "real message" in prompt
        assert "another real message" in prompt


class TestExtractSlotsWithHistory:
    """Verify extract_slots() passes conversation_history through to the prompt."""

    @pytest.mark.asyncio
    async def test_extract_slots_accepts_conversation_history_param(self, mock_llm):
        """extract_slots() takes a conversation_history kwarg without erroring."""
        mock_llm.complete.return_value = '{"attendee": "Sarah"}'
        result = await extract_slots(
            "Meeting with that one",
            MEETING_TEMPLATE,
            mock_llm,
            conversation_history=[
                {"role": "user", "content": "Earlier I mentioned Sarah"},
            ],
        )
        # The mock returned {"attendee": "Sarah"}; verify it passed through
        assert result == {"attendee": "Sarah"}

    @pytest.mark.asyncio
    async def test_extract_slots_history_appears_in_llm_prompt(self, mock_llm):
        """The prompt sent to the LLM contains the conversation history."""
        mock_llm.complete.return_value = "{}"
        await extract_slots(
            "Add to the doc",
            MEETING_TEMPLATE,
            mock_llm,
            conversation_history=[
                {"role": "user", "content": "Update Piper Morgan test page"},
            ],
        )
        # Inspect the prompt that was passed to llm.complete
        call_args = mock_llm.complete.call_args
        prompt = call_args.kwargs.get("prompt") or call_args.args[0]
        assert "Piper Morgan test page" in prompt
        assert "Recent conversation" in prompt

    @pytest.mark.asyncio
    async def test_extract_slots_no_history_omits_section(self, mock_llm):
        """Without history, the LLM prompt has no Recent conversation section."""
        mock_llm.complete.return_value = "{}"
        await extract_slots(
            "Schedule a meeting",
            MEETING_TEMPLATE,
            mock_llm,
        )
        call_args = mock_llm.complete.call_args
        prompt = call_args.kwargs.get("prompt") or call_args.args[0]
        assert "Recent conversation" not in prompt
