"""The routing vocabulary: every action name some surface of the code knows.

One derivation, three readers (#2327, Arch 2026-11-14):

- ``tests/unit/services/intent_service/test_routing_vocabulary_1283.py`` (the
  reachability lint, ADR-077);
- ``floored_action_audit`` (the runtime check: a floored action name outside
  every vocabulary is a handler-gap candidate, the #2270 class);
- ``scripts/floored_action_tally.py`` (the audit's reader).

Two tiers, on purpose:

- ``importable_vocabulary()`` is built only from sets a served process can import
  (the registry, the rail, the mapper, the prompt's category-teaching names). The
  runtime check uses this and nothing else.
- The pre-classifier's emitted names are derived from ``pre_classifier.py``'s
  SOURCE TEXT, which is fine in a test or a script and wrong in a served process.
  That derivation lives in ``scripts/routing_vocabulary_full.py`` and is never
  imported here. Leaving it out can only OVER-report a pre-classifier name as
  outside the vocabulary (the safe direction); the tally script applies the full
  vocabulary and filters those out.

Names are derived, never hand-listed, except ``CATEGORY_TEACHING``, the prompt's
few-shot names that route by category (each carries its probe evidence).
"""

from __future__ import annotations

import string
from functools import lru_cache
from typing import FrozenSet, Set

# HOST's content bar for #2327 (2026-11-14), adopted by Arch: an action name is
# model output and a person can steer it, so it is recorded only when it is a
# short identifier: the shape ^[a-z][a-z0-9_]{0,39}$ (a lowercase letter, then up
# to 39 lowercase letters, digits or underscores). Over the cap or off the shape
# it is withheld, never truncated (a truncated name still leaks its first
# characters). The cap is the longest real name (34) plus a margin;
# ``test_floored_action_audit_2327.py`` pins every importable name against this,
# so a longer real name fails there first and the cap goes to HOST.
# Written as a character check, not a pattern: this package's regex count is a
# frozen ratchet (#1943) kept for patterns that read a person's words.
ACTION_NAME_MAX_LENGTH = 40
_NAME_FIRST = frozenset(string.ascii_lowercase)
_NAME_REST = frozenset(string.ascii_lowercase + string.digits + "_")


def fits_recorded_shape(name: object) -> bool:
    """True when ``name`` is a short identifier that may be recorded as written."""
    return (
        isinstance(name, str)
        and 0 < len(name) <= ACTION_NAME_MAX_LENGTH
        and name[0] in _NAME_FIRST
        and all(ch in _NAME_REST for ch in name)
    )


# The classification prompt's few-shot action names that route by CATEGORY (the
# action string is informational). Probe run 1 (2026-07-08) verified each.
CATEGORY_TEACHING: FrozenSet[str] = frozenset(
    {
        "get_role",  # IDENTITY (probe row 8 PASS)
        "provide_guidance",  # GUIDANCE (row 9)
        "create_ticket",  # EXECUTION (row 10)
        "generate_summary",  # SYNTHESIS (row 12)
        "clarification_needed",  # CONVERSATION (row 28, corpus-ratified)
        "get_time_info",  # QUERY general-fact teaching example
        "get_information",  # QUERY general-knowledge teaching example
        "specific_action_name",  # the format placeholder, not a name
    }
)


def registry_names() -> Set[str]:
    """Every canonical action in ``ACTION_REGISTRY``."""
    from services.intent_service.action_registry import ACTION_REGISTRY

    return {action for (_category, action) in ACTION_REGISTRY}


def rail_names() -> Set[str]:
    """Every action-triggered rail key (registration is idempotent)."""
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return set(get_action_workflows().keys())


def action_mapper_names() -> Set[str]:
    """The canonical values the ActionMapper maps the model's variants onto."""
    from services.intent_service.action_mapper import ActionMapper

    return set(ActionMapper.ACTION_MAPPING.values())


@lru_cache(maxsize=1)
def importable_vocabulary() -> FrozenSet[str]:
    """Registry, rail, mapper and category-teaching names. Computed once per
    process (every source is fixed after startup)."""
    return frozenset(
        registry_names() | rail_names() | action_mapper_names() | set(CATEGORY_TEACHING)
    )
