"""#1571 half 2 — nearest-wired-capability hint on files-family declines.

Incident (PM live, 2026-08-10): PM said "file it in [owner/repo]" (as the LLM
floor had just taught). The phrase misclassified into the files family; the
canned unwired-decline replied "I can't do that from chat yet" — a FALSE
denial as experienced (create_issue IS wired and PM had used it minutes
earlier). The decline was honest about the misclassified action but useless
about the obvious intent.

The fix: when declining a files-family WRITE whose ask looks issue-like, the
decline copy appends ONE sentence offering the working create-issue form.
Trust properties preserved (#1231/#1333): honest-gap (still a decline),
actionable (the hint IS the action), once-per-response (single sentence,
single decline), and deterministic template — NEVER an LLM call.

Derivation, not hand-writing (MAX_INFERENCE_SITES=0 spirit): the hint's action
phrase is derived from wired_chat_actions() — the same registry the #1517
manifest reads. If the create-issue capability ever unwires or renames, the
hint vanishes rather than teaching a dead form.

Layer: pure decline-copy tests (deterministic template text; no LLM, no
routing — routing coverage lives in test_unwired_execution_derived_decline_1333).
"""

from services.intent_service.unwired_writes import (
    GENERIC_UNWIRED_WRITE_DECLINE,
    UNWIRED_WRITE_DECLINES,
    get_unwired_write_decline,
)

# Mirrors test_unwired_write_honest_degrade_1331 — the hinted copy must keep
# the same honesty properties as the base decline.
_FABRICATED_SUCCESS_MARKERS = [
    "✓", "✅", "created", "added", "done!", "successfully", "i've created", "i have created",
]
_HONEST_DECLINE_MARKERS = ["can't", "cannot", "can not", "not yet", "yet"]

_INCIDENT_MESSAGE = "file it in mediajunkie/piper-morgan-product"


class TestIssueLikeFilesFamilyHint:
    """Files-family decline + issue-like ask → one working create-issue hint."""

    def test_incident_shape_gets_the_hint(self):
        # The exact #1571 shape: a file-verb action aimed at an owner/repo.
        msg = get_unwired_write_decline("file_issue", original_message=_INCIDENT_MESSAGE)
        low = msg.lower()
        assert "create an issue" in low, f"no working create-issue form offered: {msg!r}"
        assert "titled" in low, f"hint must show the canonical titled-form: {msg!r}"

    def test_hint_derived_phrase_matches_registry(self):
        # The phrase is derived from the wired registry, not hand-written:
        # "create_issue" -> "create an issue". Assert the derivation source
        # actually contains the action the hint is built from.
        from services.intent_service.workflow_dispatcher import wired_chat_actions

        assert "create_issue" in wired_chat_actions()
        msg = get_unwired_write_decline("file_issue", original_message=_INCIDENT_MESSAGE)
        assert "create an issue" in msg.lower()

    def test_hint_vanishes_when_capability_not_wired(self, monkeypatch):
        # Derivation guard: if the registry stops offering a create-issue-shaped
        # action, the hint MUST disappear (never teach a dead form — the exact
        # false-affirmation dual of the #1426 false-denial class).
        import services.intent_service.workflow_dispatcher as wd

        monkeypatch.setattr(
            wd, "wired_chat_actions", lambda: ["create_todo", "list_todos"]
        )
        msg = get_unwired_write_decline("file_issue", original_message=_INCIDENT_MESSAGE)
        assert "create an issue" not in msg.lower()
        assert msg.startswith(GENERIC_UNWIRED_WRITE_DECLINE)

    def test_issue_wording_in_message_triggers_hint(self):
        msg = get_unwired_write_decline(
            "create_file", original_message="file a bug about the login timeout"
        )
        assert "create an issue" in msg.lower()

    def test_hint_appears_exactly_once(self):
        msg = get_unwired_write_decline("file_issue", original_message=_INCIDENT_MESSAGE)
        assert msg.lower().count("create an issue") == 1

    def test_hinted_copy_keeps_honesty_properties(self):
        # #1231/#1333: still an honest decline, never a confabulated success.
        msg = get_unwired_write_decline("file_issue", original_message=_INCIDENT_MESSAGE)
        low = msg.lower()
        assert any(m in low for m in _HONEST_DECLINE_MARKERS)
        for marker in _FABRICATED_SUCCESS_MARKERS:
            assert marker not in low, f"confabulated-success marker {marker!r}: {msg!r}"


class TestHintScopeIsNarrow:
    """The hint fires ONLY for files-family + issue-like — nowhere else."""

    def test_files_family_without_issue_shape_gets_no_hint(self):
        msg = get_unwired_write_decline(
            "create_file", original_message="make a new markdown file for my notes"
        )
        assert msg == GENERIC_UNWIRED_WRITE_DECLINE

    def test_non_files_family_curated_copy_unchanged(self):
        # create_milestone is issue-adjacent but NOT files-family: curated
        # copy stays byte-identical (the #1331 curated wording is protected).
        msg = get_unwired_write_decline(
            "create_milestone", original_message="add a milestone for the issue sprint"
        )
        assert msg == UNWIRED_WRITE_DECLINES["create_milestone"]

    def test_no_message_context_no_repo_no_issue_token_no_hint(self):
        # Files-family action alone, with no issue-like signal at all.
        msg = get_unwired_write_decline("upload_file", original_message="upload the file")
        assert msg == GENERIC_UNWIRED_WRITE_DECLINE

    def test_backward_compatible_single_arg_call(self):
        # The pre-#1571 call shape (action only) must behave exactly as before.
        assert (
            get_unwired_write_decline("archive_repository")
            == GENERIC_UNWIRED_WRITE_DECLINE
        )
        assert (
            get_unwired_write_decline("create_milestone")
            == UNWIRED_WRITE_DECLINES["create_milestone"]
        )
