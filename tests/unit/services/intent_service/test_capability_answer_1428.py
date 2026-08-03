"""
#1428 — the 'what can you do?' answer derives from the CHAT_POINTERS ledger.

Before this fix the DISCOVERY/IDENTITY capabilities list was built solely from
workflow-rail entry descriptions (services/intent_service/context_assembler.py),
which (a) systematically understated capabilities — canonical, elif-dispatched,
floor, and web-flow capabilities were all invisible — and (b) leaked internal
markers like "(#1124)" and rail-key names straight into the floor prompt
(census 2026-07-16, F8).

The fix (per the Arch-ratified #1433 design, §6 step 3): the ledger moved to
services/intent_service/chat_pointers.py — a single source that BOTH the
TestChatPointersReachabilityRatchet enforcement test and the product's
identity/capability answer path import. A capability joins the answer by
getting a POINTER row; CHAT_INVISIBLE surfaces are never claimed; no
hand-maintained capability list exists to drift.

D4: no classifier prompt changes — the touch point is the identity/capability
context gatherer, not classification.
"""

import re

import pytest

from services.intent_service.chat_pointers import (
    CHAT_INVISIBLE,
    CHAT_POINTERS,
    CORE_CAPABILITIES,
    POINTER,
    capability_answer_lines,
    pointer_utterances,
)


# ---------------------------------------------------------------------------
# Derivation: the answer's capability lines come from the ledger's POINTER rows
# ---------------------------------------------------------------------------


class TestCapabilityAnswerDerivesFromLedger:
    def test_every_pointer_utterance_appears_in_the_answer(self):
        """Every POINTER row's utterance is offered as an example ask."""
        lines = capability_answer_lines()
        for utterance in pointer_utterances():
            assert any(utterance in line for line in lines), (
                f"POINTER utterance {utterance!r} missing from the capability "
                f"answer — the answer must derive from the ledger, not a "
                f"hand-maintained list"
            )

    def test_added_pointer_row_joins_the_answer_by_existing(self):
        """The #1433 design intent: a new capability joins the answer by
        getting a ledger row — nothing else to update, nowhere to drift."""
        ledger = dict(CHAT_POINTERS)
        ledger["capability:frobnicate"] = POINTER(
            "frobnicate my widgets", expects=("execution", "frobnicate_widgets")
        )
        lines = capability_answer_lines(ledger)
        assert any("frobnicate my widgets" in line for line in lines), (
            "A POINTER row added to the ledger did not appear in the "
            "capability answer — the answer is not deriving from the ledger"
        )

    def test_chat_invisible_surfaces_are_not_claimed(self):
        """Honesty per capability state: only POINTER rows contribute; a
        CHAT_INVISIBLE surface must never be claimed as an ask."""
        ledger = {
            "page:/x": POINTER("do the x thing", expects=("query", "x_query")),
            "page:/y": CHAT_INVISIBLE(issue=1),
            "capability:z": CHAT_INVISIBLE(ref="ADR-063"),
        }
        lines = capability_answer_lines(ledger)
        ask_lines = [line for line in lines if line not in CORE_CAPABILITIES]
        assert ask_lines == ['you can ask me: "do the x thing"']

    def test_duplicate_utterances_dedupe(self):
        """Surfaces sharing an utterance (e.g. page:/settings/integrations/github
        and integration:github both use 'connect my github') yield ONE line."""
        ledger = {
            "page:/a": POINTER("connect my thing", expects=("guidance", "g")),
            "integration:a": POINTER("connect my thing", expects=("guidance", "g")),
        }
        lines = capability_answer_lines(ledger)
        matches = [line for line in lines if "connect my thing" in line]
        assert len(matches) == 1

    def test_answer_count_matches_ledger(self):
        """No extra hand-maintained entries: lines == core + one per unique
        POINTER utterance, exactly."""
        lines = capability_answer_lines()
        assert len(lines) == len(CORE_CAPABILITIES) + len(pointer_utterances())


# ---------------------------------------------------------------------------
# F8: no internal markers in the user-register answer
# ---------------------------------------------------------------------------


class TestNoInternalMarkerLeak:
    _INTERNAL_MARKERS = re.compile(
        r"#\d+"  # issue references like (#1124)
        r"|\b[a-z]+_[a-z_]+\b"  # snake_case rail keys / action tokens
        r"|\bvia action dispatch\b"
        r"|\bvia slot-filling\b"
        r"|\bdispatch(er)?\b"
        r"|\bregistry\b"
        r"|\brail\b"
    )

    def test_no_internal_markers_in_answer_lines(self):
        for line in capability_answer_lines():
            assert not self._INTERNAL_MARKERS.search(line), (
                f"Internal marker leaked into user-register capability line: "
                f"{line!r} (#1428 / census F8)"
            )

    def test_core_capabilities_are_user_register(self):
        for line in CORE_CAPABILITIES:
            assert not self._INTERNAL_MARKERS.search(line)


# ---------------------------------------------------------------------------
# Wiring: the identity/capability context gatherer uses the shared source
# ---------------------------------------------------------------------------


class TestIdentityContextUsesLedger:
    async def test_gather_identity_context_capabilities_are_ledger_derived(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler._gather_identity_context(user_id=None, session_id=None)
        assert result["capabilities"] == capability_answer_lines()

    async def test_gather_identity_context_has_no_marker_leak(self):
        """The concrete F8 regression check: the assembled context carries no
        issue-number or rail-internal markers."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler._gather_identity_context(user_id=None, session_id=None)
        joined = "\n".join(result["capabilities"])
        assert "#" not in joined
        assert "_" not in joined
        assert "dispatch" not in joined

    async def test_discovery_category_gets_same_derivation(self):
        """DISCOVERY ('what can you do?') and IDENTITY share the gatherer."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler.gather_context("DISCOVERY")
        assert result["capabilities"] == capability_answer_lines()


# ---------------------------------------------------------------------------
# Floor rendering: capabilities reach the prompt intact (and multi-line, so
# quoted example asks stay readable)
# ---------------------------------------------------------------------------


class TestFloorRendersLedgerCapabilities:
    def test_floor_renders_each_capability_line(self):
        from unittest.mock import MagicMock

        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor(llm_client=MagicMock())
        rendered = floor._format_domain_context({"capabilities": capability_answer_lines()})
        for line in capability_answer_lines():
            assert line in rendered
