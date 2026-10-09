"""#1256 — "write a stakeholder update" must not misroute to update_document_query.

The bug (LLM-as-judge, 2026-06-16): "Write a short update for the OpenLaws CEO
John Phamvan on where we are with the Piper Morgan alpha testing" hit
DOCUMENT_QUERY_PATTERNS' loose `update ... with` regex (greedily bridging
"update for the CEO ... where we are WITH") → update_document_query at
confidence 1.0 → "which document do you want to update?" instead of a memo.

Fix: STAKEHOLDER_UPDATE_PATTERNS checked BEFORE the document patterns, emitting
`write_stakeholder_update` (registry disposition FLOOR — the floor drafts the
prose; the action is the named gateway for the Wave-2 stakeholder-update skill).
"""

from __future__ import annotations

import pytest

from services.intent_service.pre_classifier import PreClassifier
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


class TestStakeholderUpdateRouting:
    """#1595 Phase 3, rule-10-licensed deletion (2026-10-09): STAKEHOLDER_
    UPDATE_PATTERNS is now PARTIAL -- 3 of 4 literals deleted, 1 SURVIVES
    (`\\bwrite\\s+(?:me\\s+)?(?:a|an)?\\s*(?:\\w+\\s+){0,3}update\\s+for\\b`).
    test_judge_experiment_query_routes_to_stakeholder_update below proved
    that survivor load-bearing under rule 10(B) (restored, NOT converted
    -- see the class attribute's own comment in pre_classifier.py); the
    other three tests are Rule-10(A) conversions, each citing the
    STAKEHOLDER_UPDATE_PATTERNS corpus row that proves the destination
    (write_stakeholder_update, live via the read_floor_2 group) is
    unaffected by deleting their own literals."""

    def test_judge_experiment_query_routes_to_stakeholder_update(self):
        """The exact failing query from the 2026-06-16 judge experiment.

        Rule-10(B): this phrase is NOT one of STAKEHOLDER_UPDATE_PATTERNS'
        5 claimed corpus rows (none of them contains "... on X WITH Y",
        the DOCUMENT_QUERY_PATTERNS collision shape #1256 exists to
        prevent) -- a same-day attempt to delete the "write ... update
        for" literal broke this exact test: the phrase mis-routed to
        `update_document_query` (DOCUMENT_QUERY_PATTERNS' loose "update
        ... with" regex re-claimed it), reopening the original #1256
        production bug. The literal was restored (and only it) per rule
        10(B); this assertion is UNCHANGED from before this epic's
        deletion work -- surface 1 still claims it directly, zero LLM
        call, same as always."""
        intent = _classify(
            "Write a short update for the OpenLaws CEO John Phamvan on where "
            "we are with the Piper Morgan alpha testing."
        )
        assert intent is not None
        assert intent.action == "write_stakeholder_update"
        assert intent.action != "update_document_query"

    @pytest.mark.asyncio
    async def test_draft_status_update_for_routes_to_stakeholder_update(self, monkeypatch):
        """Cites STAKEHOLDER_UPDATE_PATTERNS' own corpus row "Draft a status
        update for the board" (today's rule-10 deposit, MATCH, live via
        read_floor_2) — this test's phrase IS that row verbatim."""
        message = "Draft a status update for the board"
        intent = _classify(message)
        assert (
            intent is None
        ), f"STAKEHOLDER_UPDATE_PATTERNS is deleted — surface 1 should decline (got {intent!r})"
        await assert_inversion_routes(
            monkeypatch,
            message,
            live_categories="read_floor_2",
            expected_action="write_stakeholder_update",
        )

    @pytest.mark.asyncio
    async def test_write_something_to_send_to_routes_to_stakeholder_update(self, monkeypatch):
        """Cites STAKEHOLDER_UPDATE_PATTERNS' own corpus row "Write something
        to send to Jake about the beta timeline" (today's rule-10 deposit,
        MATCH, live via read_floor_2) — this test's phrase IS that row
        verbatim."""
        message = "Write something to send to Jake about the beta timeline"
        intent = _classify(message)
        assert (
            intent is None
        ), f"STAKEHOLDER_UPDATE_PATTERNS is deleted — surface 1 should decline (got {intent!r})"
        await assert_inversion_routes(
            monkeypatch,
            message,
            live_categories="read_floor_2",
            expected_action="write_stakeholder_update",
        )

    @pytest.mark.asyncio
    async def test_explicit_stakeholder_update_phrase_routes(self, monkeypatch):
        """Cites STAKEHOLDER_UPDATE_PATTERNS' own corpus row "I need a
        stakeholder update on the alpha program" (today's rule-10 deposit,
        MATCH, live via read_floor_2) — this test's phrase IS that row
        verbatim."""
        message = "I need a stakeholder update on the alpha program"
        intent = _classify(message)
        assert (
            intent is None
        ), f"STAKEHOLDER_UPDATE_PATTERNS is deleted — surface 1 should decline (got {intent!r})"
        await assert_inversion_routes(
            monkeypatch,
            message,
            live_categories="read_floor_2",
            expected_action="write_stakeholder_update",
        )


class TestDocumentUpdateNonRegression:
    """The #522/#681 document-routing behavior must survive untouched."""

    def test_update_doc_still_routes_to_document_query(self):
        intent = _classify("Update the project plan doc")
        assert intent is not None
        assert intent.action == "update_document_query"

    def test_update_x_with_y_still_routes_to_document_query(self):
        """The loose `update ... with` shape stays for genuine doc edits."""
        intent = _classify("Update the roadmap with the new dates")
        assert intent is not None
        assert intent.action == "update_document_query"

    def test_edit_doc_still_routes_to_document_query(self):
        intent = _classify("Edit the onboarding document")
        assert intent is not None
        assert intent.action == "update_document_query"
