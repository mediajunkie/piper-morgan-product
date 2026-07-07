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

from services.intent_service.pre_classifier import PreClassifier


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


class TestStakeholderUpdateRouting:
    def test_judge_experiment_query_routes_to_stakeholder_update(self):
        """The exact failing query from the 2026-06-16 judge experiment."""
        intent = _classify(
            "Write a short update for the OpenLaws CEO John Phamvan on where "
            "we are with the Piper Morgan alpha testing."
        )
        assert intent is not None
        assert intent.action == "write_stakeholder_update"
        assert intent.action != "update_document_query"

    def test_draft_status_update_for_routes_to_stakeholder_update(self):
        intent = _classify("Draft a status update for the board")
        assert intent is not None
        assert intent.action == "write_stakeholder_update"

    def test_write_something_to_send_to_routes_to_stakeholder_update(self):
        intent = _classify("Write something to send to Jake about the beta timeline")
        assert intent is not None
        assert intent.action == "write_stakeholder_update"

    def test_explicit_stakeholder_update_phrase_routes(self):
        intent = _classify("I need a stakeholder update on the alpha program")
        assert intent is not None
        assert intent.action == "write_stakeholder_update"


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
