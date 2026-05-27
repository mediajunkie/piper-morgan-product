"""
Slot template definitions for declarative slot-filling workflows.

Issue #765: GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

Defines the data model for slot specifications:
- SlotDefinition: Individual slot with type, required flag, grouping
- SlotTemplate: Collection of slots for a workflow
- SlotState: Runtime state tracking filled/unfilled slots
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SlotType(str, Enum):
    """Types of slot values for extraction hints."""

    TEXT = "text"  # Free-form text (e.g., topic, description)
    DATETIME = "datetime"  # Date/time values (e.g., Tuesday at 2pm)
    ENTITY = "entity"  # Named entities (e.g., person names)
    CHOICE = "choice"  # Selection from predefined options


class ConfirmationStyle(str, Enum):
    """How to confirm filled slots with the user."""

    IMPLICIT = "implicit"  # "Got it — meeting with Sarah, Tuesday at 2pm. What's the topic?"
    EXPLICIT = "explicit"  # "I have: Sarah, Tuesday, 2pm, Q3 planning. Is that correct?"


@dataclass(frozen=True)
class SlotDefinition:
    """
    Defines a single slot in a slot-filling template.

    Attributes:
        name: Machine-readable identifier (e.g., "attendee")
        display_name: Human-readable label (e.g., "Who should attend")
        required: Whether this slot must be filled before completion
        slot_type: Type hint for extraction (text, datetime, entity, choice)
        extraction_hint: Optional hint for the LLM extractor
        group: Optional grouping index for grouped prompting (slots in
               the same group are asked together, max 2-3 per group)
        lens_prompts: Optional mapping of ConversationalLens value → contextual
                      prompt phrasing. When a lens is active, the prompt uses
                      this phrasing instead of the generic display_name.
                      Keys are lens string values (e.g., "calendar", "people").
    """

    name: str
    display_name: str
    required: bool = True
    slot_type: SlotType = SlotType.TEXT
    extraction_hint: Optional[str] = None
    group: Optional[int] = None
    lens_prompts: Optional[dict[str, str]] = None

    def prompt_for_lens(self, lens: Optional[str] = None) -> str:
        """Return the prompt phrasing appropriate for the given lens."""
        if lens and self.lens_prompts:
            return self.lens_prompts.get(lens, self.display_name)
        return self.display_name


@dataclass
class SlotTemplate:
    """
    Defines the slot specification for a workflow.

    A template declares what information a workflow needs and how
    to collect it naturally. Templates are registered with the
    SlotFillingManager and triggered when the user's intent matches.

    Attributes:
        name: Machine-readable template identifier
        display_name: Human-readable workflow name
        slots: Ordered list of slot definitions
        confirmation_style: How to confirm with the user (default: implicit)
        lens_group_priority: Optional mapping of ConversationalLens value →
                             preferred group ordering. When a lens is active,
                             groups are prompted in this order instead of the
                             default numeric order.
    """

    name: str
    display_name: str
    slots: list[SlotDefinition] = field(default_factory=list)
    confirmation_style: ConfirmationStyle = ConfirmationStyle.IMPLICIT
    lens_group_priority: Optional[dict[str, list[int]]] = None

    def __post_init__(self):
        if not self.slots:
            raise ValueError(f"SlotTemplate '{self.name}' must have at least one slot")
        if not any(s.required for s in self.slots):
            raise ValueError(f"SlotTemplate '{self.name}' must have at least one required slot")

    @property
    def required_slots(self) -> list[SlotDefinition]:
        """Return only required slot definitions."""
        return [s for s in self.slots if s.required]

    @property
    def optional_slots(self) -> list[SlotDefinition]:
        """Return only optional slot definitions."""
        return [s for s in self.slots if not s.required]

    @property
    def groups(self) -> dict[Optional[int], list[SlotDefinition]]:
        """Return slots organized by group number."""
        result: dict[Optional[int], list[SlotDefinition]] = {}
        for slot in self.slots:
            result.setdefault(slot.group, []).append(slot)
        return result


@dataclass
class SlotState:
    """
    Runtime state for an active slot-filling session.

    Tracks which slots are filled, their values, and the current
    prompt group for grouped prompting.

    Attributes:
        template: The slot template being filled
        filled_slots: Map of slot name → extracted value
        current_prompt_group: Which group we're currently prompting for
    """

    template: SlotTemplate
    filled_slots: dict[str, Any] = field(default_factory=dict)
    current_prompt_group: int = 0

    @property
    def unfilled_required(self) -> list[SlotDefinition]:
        """Return required slots that haven't been filled yet."""
        return [s for s in self.template.required_slots if s.name not in self.filled_slots]

    @property
    def unfilled_optional(self) -> list[SlotDefinition]:
        """Return optional slots that haven't been filled yet."""
        return [s for s in self.template.optional_slots if s.name not in self.filled_slots]

    @property
    def all_required_filled(self) -> bool:
        """Check if all required slots have values."""
        return len(self.unfilled_required) == 0

    @property
    def filled_count(self) -> int:
        """Number of slots that have been filled."""
        return len(self.filled_slots)

    @property
    def total_count(self) -> int:
        """Total number of slots in the template."""
        return len(self.template.slots)

    def get_value(self, slot_name: str) -> Optional[Any]:
        """Get the current value of a slot, or None if unfilled."""
        return self.filled_slots.get(slot_name)

    def set_value(self, slot_name: str, value: Any) -> None:
        """Set or update a slot value."""
        # Validate slot exists in template
        valid_names = {s.name for s in self.template.slots}
        if slot_name not in valid_names:
            raise ValueError(
                f"Slot '{slot_name}' not in template '{self.template.name}'. "
                f"Valid slots: {valid_names}"
            )
        self.filled_slots[slot_name] = value

    def clear_value(self, slot_name: str) -> None:
        """Clear a slot value (e.g., on cancel or reset)."""
        self.filled_slots.pop(slot_name, None)

    def clear_all(self) -> None:
        """Clear all filled slots."""
        self.filled_slots.clear()
        self.current_prompt_group = 0


# --- Built-in Templates ---

MEETING_TEMPLATE = SlotTemplate(
    name="schedule_meeting",
    display_name="Schedule a Meeting",
    slots=[
        SlotDefinition(
            name="attendee",
            display_name="Who should attend",
            required=True,
            slot_type=SlotType.ENTITY,
            extraction_hint="Person name(s) for the meeting",
            group=0,
            lens_prompts={
                "calendar": "Who should be there",
                "people": "Who needs to be in this meeting",
                "projects": "Who should attend from the team",
            },
        ),
        SlotDefinition(
            name="day",
            display_name="What day",
            required=True,
            slot_type=SlotType.DATETIME,
            extraction_hint="Day or date for the meeting",
            group=0,
            lens_prompts={
                "calendar": "Which day works",
                "people": "Which day works for everyone",
                "projects": "When works for this",
            },
        ),
        SlotDefinition(
            name="time",
            display_name="What time",
            required=True,
            slot_type=SlotType.DATETIME,
            extraction_hint="Time of day for the meeting",
            group=0,
            lens_prompts={
                "calendar": "What time works best",
                "people": "What time",
                "projects": "What time",
            },
        ),
        SlotDefinition(
            name="topic",
            display_name="What's the topic",
            required=True,
            slot_type=SlotType.TEXT,
            extraction_hint="Meeting subject or agenda",
            group=1,
            lens_prompts={
                "calendar": "What's the agenda",
                "people": "What should you cover",
                "projects": "Which project is this about",
            },
        ),
    ],
    confirmation_style=ConfirmationStyle.IMPLICIT,
    lens_group_priority={
        # CALENDAR: time/people first (group 0), then topic (group 1) — default order
        "calendar": [0, 1],
        # PEOPLE: same default order (attendees in group 0)
        "people": [0, 1],
        # PROJECTS: topic first (group 1), then logistics (group 0)
        "projects": [1, 0],
    },
)


# Issue #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING (2026-05-27):
# Template for the `update_document` action handler. Replaces the
# regex-based `_parse_document_update_query` in intent_service.py that
# was hitting Pattern-045 — tests passed against canonical phrasings
# but natural language ("update X (on Notion) with: ..." / "by adding
# ... to it: ...") flunked the regex. The slot-filling extractor uses
# the LLM to recover doc_name + content from arbitrary phrasings.
DOCUMENT_UPDATE_TEMPLATE = SlotTemplate(
    name="update_document",
    display_name="Update a Document",
    slots=[
        SlotDefinition(
            name="doc_name",
            display_name="Which document",
            required=True,
            slot_type=SlotType.ENTITY,
            extraction_hint=(
                "Name or title of the document to update. Examples: "
                "'Piper Morgan test page', 'the README', 'project roadmap'. "
                "May appear with words like 'doc', 'document', 'page', "
                "or with parenthetical platform notes like '(on Notion)'."
            ),
            group=0,
        ),
        SlotDefinition(
            name="content",
            display_name="What to add",
            required=True,
            slot_type=SlotType.TEXT,
            extraction_hint=(
                "The text content to append to the document as a new "
                "paragraph. Often introduced by 'with', 'with:', 'by "
                "adding', 'add a paragraph saying', etc. Preserve the "
                "user's exact wording — do not paraphrase or truncate."
            ),
            group=0,
        ),
    ],
    confirmation_style=ConfirmationStyle.IMPLICIT,
)
