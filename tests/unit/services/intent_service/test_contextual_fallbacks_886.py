"""
Tests for Issue #886: Contextual fallback copy for not-implemented EXECUTION actions.

CXO-authored replacement copy that provides colleague-level responses
instead of the generic "I don't have that capability yet" message.
"""

import pytest

from services.intent.intent_service import IntentService


class TestContextualFallbacks:
    """Test _get_contextual_fallback returns the right copy for each query type."""

    def setup_method(self):
        """Create a minimal IntentService for testing the fallback method."""
        # _get_contextual_fallback is a sync method that only uses self for the method call.
        # We can instantiate with __new__ to avoid __init__ dependencies.
        self.service = IntentService.__new__(IntentService)

    # --- Scheduling ---

    def test_schedule_meeting_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="schedule_meeting",
            original_message="Schedule a meeting about the roadmap",
        )
        assert "can't create calendar events yet" in result
        assert "GitHub issue" in result or "agenda" in result

    def test_book_meeting_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="schedule_meeting",
            original_message="Book a meeting with the team",
        )
        assert "can't create calendar events yet" in result

    # --- Reminders ---

    def test_remind_me_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="set_reminder",
            original_message="Remind me to review PRs tomorrow",
        )
        # #1426: the old pin here asserted the FALSE DENIAL ("can't set
        # reminders yet") — reminders shipped in #903; this fallback fires only
        # on mapper-missed phrasings, so the honest copy coaches the re-phrase.
        assert "I can set reminders" in result
        assert "remind me tomorrow" in result

    def test_set_reminder_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="set_reminder",
            original_message="Set a reminder to check deploys",
        )
        assert "I can set reminders" in result
        assert "can't set reminders" not in result

    # --- Document creation ---

    def test_create_doc_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="create_document",
            original_message="Create a doc from this conversation",
        )
        assert "can't create documents yet" in result
        assert "summarize" in result

    def test_create_document_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="create_document",
            original_message="Make a doc with our decisions",
        )
        assert "can't create documents yet" in result

    # --- Batch issue creation ---

    def test_batch_create_issues_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="batch_create_issues",
            original_message="Create issues from this meeting's action items",
        )
        assert "can't batch-create issues" in result
        assert "one at a time" in result

    def test_action_items_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="create_issues",
            original_message="Turn these action items into tickets",
        )
        assert "can't batch-create issues" in result

    # --- Close issues ---

    def test_close_issues_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="Close completed issues",
        )
        # Updated after #902: close issues now works, fallback is helpful redirect
        assert "I can close issues" in result
        assert "issue number" in result

    def test_close_issue_singular(self):
        result = self.service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="Close the issue about testing",
        )
        # Updated after #902: close issues now works
        assert "I can close issues" in result

    # --- Post to Slack ---

    def test_post_to_channel_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="post_message",
            original_message="Post this update to the team channel",
        )
        assert "can't post to Slack channels yet" in result
        assert "draft" in result

    def test_post_slack_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="post_slack",
            original_message="Post this to the slack channel",
        )
        assert "can't post to Slack channels yet" in result

    # --- Complete todo ---
    # Removed: test_complete_todo_returns_contextual_copy
    # Issue #904 implemented todo completion, so the "can't complete todos"
    # fallback was removed. Todo completion now handled by pre-classifier
    # and todo_handlers.

    # --- Upload file ---

    def test_upload_file_returns_contextual_copy(self):
        result = self.service._get_contextual_fallback(
            mapped_action="upload_file",
            original_message="Upload a file to the knowledge base",
        )
        # #1426: old pin asserted the FALSE DENIAL ("can't accept file uploads
        # yet") — the Files page + upload API are shipped; copy points there.
        assert "/files" in result
        assert "can't accept file uploads" not in result

    def test_upload_knowledge_variant(self):
        result = self.service._get_contextual_fallback(
            mapped_action="upload_knowledge",
            original_message="Upload this file to the knowledge base",
        )
        assert "/files" in result

    # --- Generic fallback ---

    def test_unmatched_action_returns_generic_fallback(self):
        result = self.service._get_contextual_fallback(
            mapped_action="unknown_weird_action",
            original_message="Do something completely unexpected",
        )
        assert "I don't have that capability yet" in result
        assert "What can you do?" in result

    def test_empty_message_returns_generic_fallback(self):
        result = self.service._get_contextual_fallback(
            mapped_action="unknown",
            original_message="",
        )
        assert "I don't have that capability yet" in result

    def test_none_message_returns_generic_fallback(self):
        result = self.service._get_contextual_fallback(
            mapped_action="unknown",
            original_message=None,
        )
        assert "I don't have that capability yet" in result


class TestContextualFallbacksNeverCrash:
    """Verify fallback method is resilient — never raises, always returns a string."""

    def setup_method(self):
        self.service = IntentService.__new__(IntentService)

    @pytest.mark.parametrize(
        "action,message",
        [
            ("", ""),
            (None, None),
            ("create_issue", "Create issues from meeting action items"),
            ("unknown", "schedule a meeting about the roadmap"),
            ("post_message", "POST THIS UPDATE TO THE TEAM CHANNEL"),
        ],
    )
    def test_always_returns_string(self, action, message):
        result = self.service._get_contextual_fallback(
            mapped_action=action or "",
            original_message=message,
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_case_insensitive_matching(self):
        """Original message should match regardless of case."""
        result = self.service._get_contextual_fallback(
            mapped_action="schedule_meeting",
            original_message="SCHEDULE A MEETING about the roadmap",
        )
        assert "can't create calendar events yet" in result
