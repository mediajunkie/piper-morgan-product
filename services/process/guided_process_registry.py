"""
Guided Process census — issue #1867.

ADR-059 put onboarding "on ice" as a code comment
(``services/process/adapters.py``, the commented-out
``registry.register(OnboardingProcessAdapter())``), and nothing else in the
codebase enumerated which ``ProcessType`` members are actually wired to the
``ProcessRegistry`` versus dark. #1856 found the live consequence: a
guided-process session got created for the dark onboarding surface and asked
a question no later turn could ever answer (see
``services/intent_service/canonical_handlers.py::_handle_add_project`` for
the live instance this census found — reported, not fixed here per #1867's
scope).

This module is the single source of truth for "is process X registered right
now" — declarative status entries PLUS a function that re-derives the answer
by calling the real registration entry points, so the declared table can
never drift silently from what's actually wired (a mismatch raises loud, it
does not get silently trusted). ``tests/test_architecture_enforcement.py::
TestGuidedProcessStartersRegistered1867`` consumes both: the declared table
to know which processes session-start call sites may legally name, and the
live-derivation function to keep the table honest.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet

from services.process.registry import ProcessRegistry, ProcessType, get_process_registry


class GuidedProcessStatus(str, Enum):
    """Whether a ``ProcessType`` is actually consulted by ``ProcessRegistry``
    at runtime (LIVE) or not (DARK — no registered adapter, so
    ``check_active_processes``/``check_suspended_processes`` never sees it)."""

    LIVE = "live"
    DARK = "dark"


@dataclass(frozen=True)
class GuidedProcessInfo:
    """One row of the census: a ``ProcessType`` and its registration status,
    with the source that decided the status (ADR/issue + the file:line where
    the decision actually lives, so a reader can go verify it directly)."""

    process_type: ProcessType
    status: GuidedProcessStatus
    adapter: str  # class name, or "(none)" when no adapter exists at all
    source: str  # ADR/issue + file:line pointer backing the status


# THE CENSUS TABLE — every ``ProcessType`` member, MEASURED against the
# actual registration sites 2026-09-24 (issue #1867). Adding a new
# ``ProcessType`` member without a row here fails
# ``test_every_process_type_has_a_census_row`` below — the enum can't drift
# out from under this table silently.
GUIDED_PROCESSES: tuple[GuidedProcessInfo, ...] = (
    GuidedProcessInfo(
        process_type=ProcessType.ONBOARDING,
        status=GuidedProcessStatus.DARK,
        adapter="OnboardingProcessAdapter",
        source=(
            "ADR-059 'onboarding on ice'; services/process/adapters.py:609 — "
            "`# registry.register(OnboardingProcessAdapter())` is commented out"
        ),
    ),
    GuidedProcessInfo(
        process_type=ProcessType.STANDUP,
        status=GuidedProcessStatus.LIVE,
        adapter="StandupProcessAdapter",
        source="services/process/adapters.py:610 — register_default_processes()",
    ),
    GuidedProcessInfo(
        process_type=ProcessType.SLOT_FILLING,
        status=GuidedProcessStatus.LIVE,
        adapter="SlotFillingProcessAdapter",
        source=(
            "#765 GLUE-SLOTFILL; services/intent/intent_service.py:346 — "
            "IntentService.__init__ registers it directly (not via "
            "register_default_processes)"
        ),
    ),
    GuidedProcessInfo(
        process_type=ProcessType.CLARIFICATION,
        status=GuidedProcessStatus.DARK,
        adapter="(none)",
        source=(
            "services/process/registry.py ProcessType docstring — 'Future "
            "(Advanced Layer)'; no adapter class exists anywhere in the tree"
        ),
    ),
    GuidedProcessInfo(
        process_type=ProcessType.PLANNING,
        status=GuidedProcessStatus.DARK,
        adapter="(none)",
        source=(
            "services/process/registry.py ProcessType docstring — 'Future "
            "(Advanced Layer)'; no adapter class exists anywhere in the tree"
        ),
    ),
    GuidedProcessInfo(
        process_type=ProcessType.FEEDBACK,
        status=GuidedProcessStatus.DARK,
        adapter="(none)",
        source=(
            "services/process/registry.py ProcessType docstring — 'Future "
            "(Advanced Layer)'; no adapter class exists anywhere in the tree"
        ),
    ),
)


def live_process_types() -> FrozenSet[ProcessType]:
    """The declared-LIVE set from the census table above."""
    return frozenset(
        info.process_type for info in GUIDED_PROCESSES if info.status == GuidedProcessStatus.LIVE
    )


def compute_live_registered_types() -> FrozenSet[ProcessType]:
    """Re-derive "what's actually registered" by calling the REAL
    registration entry points, against a scratch registry — never the
    live app singleton — so this can never observe or leave stray process
    state.

    Two entry points feed the singleton in production (`services/container/
    initialization.py::_initialize_process_registry`,
    `services/intent/intent_service.py::IntentService.__init__`):

    1. ``services.process.adapters.register_default_processes()`` — called
       verbatim (the real function, not a re-implementation), so a future
       edit to it (re-enabling onboarding, adding a new adapter) is picked
       up automatically.
    2. The slot-filling registration ``IntentService.__init__`` performs
       (``services/intent/intent_service.py:346``,
       ``registry.register(self.slot_filling_adapter)``) is mirrored here
       rather than invoked via a full ``IntentService`` (too heavy to
       construct for a registry probe — LLM classifier, DB-backed
       conversation manager, etc.). ``_assert_slot_filling_registration_line_present``
       is a canary so a change to that exact call site fails this function
       LOUD instead of silently going stale.
    """
    _assert_slot_filling_registration_line_present()

    from services.process.adapters import register_default_processes
    from services.slot_filling.slot_filling_adapter import SlotFillingProcessAdapter

    previous_instance = ProcessRegistry._instance
    ProcessRegistry.reset_instance()
    try:
        register_default_processes()
        get_process_registry().register(SlotFillingProcessAdapter())
        return frozenset(get_process_registry().registered_types)
    finally:
        # Never leave the probe's scratch registry installed as the
        # singleton — restore exactly what was there before this call,
        # even if the previous value was None (a not-yet-initialized app).
        ProcessRegistry._instance = previous_instance


_SLOT_FILLING_REGISTRATION_RE = re.compile(r"registry\.register\(self\.slot_filling_adapter\)")


def _assert_slot_filling_registration_line_present() -> None:
    """Canary for the mirrored registration in ``compute_live_registered_types``.

    ``IntentService.__init__`` is too heavy to construct just to probe the
    registry (real LLM classifier + DB-backed conversation manager), so
    ``compute_live_registered_types`` mirrors its one registration line
    instead of calling it. If that exact line ever moves, is renamed, or is
    removed, the mirror would silently go stale — this assertion makes that
    LOUD instead: it reads the real source and fails if the line it mirrors
    is no longer there.
    """
    with open("services/intent/intent_service.py", encoding="utf-8") as fh:
        content = fh.read()
    assert _SLOT_FILLING_REGISTRATION_RE.search(content), (
        "services/intent/intent_service.py no longer contains "
        "`registry.register(self.slot_filling_adapter)` — "
        "compute_live_registered_types() mirrors this exact line to avoid "
        "constructing a full IntentService. Update the mirror in "
        "services/process/guided_process_registry.py to match the new "
        "registration site."
    )
