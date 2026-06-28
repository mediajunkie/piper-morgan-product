"""Unit tests for OutputFilter (Issue #1017 Phase 2.1 scaffold).

Covers:
- profile_for() task_type → profile dispatch (including ratified mapping)
- Tier 1 PII rules (email/SSN/phone/credit-card detection + redaction)
- Tier 1 secret rules (API keys, bearer tokens, URL credentials)
- Tier 2 BoundaryEnforcer integration (with a mock enforcer)
- OutputFilter.filter() — passthrough / redact / canned-substitute paths
- OutputFilterDecision audit envelope shape (hashes only, never raw PII)
- Regenerate-trigger chain fields (attempt_number, prior_attempt_decision_id)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pytest

from services.ethics.output_filter import (
    Action,
    CANNED_VIOLATION_RESPONSE,
    FilterResult,
    OutputFilter,
    OutputFilterDecision,
    Profile,
    REDACTED_TOKEN,
    Severity,
    profile_for,
)
from services.ethics.output_filter_rules import (
    apply_boundary_rules,
    apply_pii_rules,
    apply_secret_rules,
)


# ============================================================================
# Profile registry
# ============================================================================


class TestProfileFor:
    def test_conversation_is_user_visible(self):
        assert profile_for("conversation") == Profile.USER_VISIBLE

    def test_question_answering_is_user_visible(self):
        assert profile_for("question_answering") == Profile.USER_VISIBLE

    def test_summarize_is_user_visible(self):
        assert profile_for("summarize") == Profile.USER_VISIBLE

    def test_relationship_analysis_escalated_to_user_visible(self):
        """Per Architect Q6 pushback (transitive visibility) — KG content
        surfaces back to users via downstream queries."""
        assert profile_for("relationship_analysis") == Profile.USER_VISIBLE

    def test_slot_extraction_escalated_to_user_visible(self):
        """Slot values get echoed in confirmation prompts."""
        assert profile_for("slot_extraction") == Profile.USER_VISIBLE

    def test_work_item_extraction_escalated_to_user_visible(self):
        """Output becomes GitHub issue body — user-visible eventually."""
        assert profile_for("work_item_extraction") == Profile.USER_VISIBLE

    def test_intent_classification_stays_internal(self):
        """Output parsed into structured Intent; not echoed verbatim."""
        assert profile_for("intent_classification") == Profile.INTERNAL

    def test_general_falls_to_user_visible(self):
        """`general` mapped to mixed → user_visible (fail-closed)."""
        assert profile_for("general") == Profile.USER_VISIBLE

    def test_unknown_task_type_falls_to_user_visible(self):
        """Unknown task_types default to user_visible (fail-closed)."""
        assert profile_for("brand_new_task_type") == Profile.USER_VISIBLE


# ============================================================================
# Tier 1 — PII rules
# ============================================================================


class TestApplyPiiRules:
    def test_empty_string_passes_through(self):
        filtered, result = apply_pii_rules("")
        assert filtered == ""
        assert result.redactions_count == 0
        assert result.matched_rules == []

    def test_no_pii_passes_through(self):
        content = "The quick brown fox jumps over the lazy dog."
        filtered, result = apply_pii_rules(content)
        assert filtered == content
        assert result.redactions_count == 0

    def test_redacts_email(self):
        content = "Please reach out to alice@example.com for details."
        filtered, result = apply_pii_rules(content)
        assert "alice@example.com" not in filtered
        assert REDACTED_TOKEN in filtered
        assert "pii:email" in result.matched_rules
        assert result.redactions_count == 1

    def test_redacts_ssn(self):
        content = "SSN on file: 123-45-6789"
        filtered, result = apply_pii_rules(content)
        assert "123-45-6789" not in filtered
        assert "pii:ssn" in result.matched_rules

    def test_redacts_phone_hyphen(self):
        content = "Call 555-123-4567 anytime."
        filtered, result = apply_pii_rules(content)
        assert "555-123-4567" not in filtered
        assert "pii:phone_hyphen" in result.matched_rules

    def test_redacts_phone_paren(self):
        content = "Call (555) 123-4567 anytime."
        filtered, result = apply_pii_rules(content)
        assert "(555) 123-4567" not in filtered
        assert "pii:phone_paren" in result.matched_rules

    def test_redacts_credit_card(self):
        content = "Card: 4111-1111-1111-1111"
        filtered, result = apply_pii_rules(content)
        assert "4111-1111-1111-1111" not in filtered
        assert "pii:credit_card" in result.matched_rules

    def test_redacts_multiple_pii_in_one_pass(self):
        content = "Email alice@example.com or call 555-123-4567 — SSN 999-12-3456."
        filtered, result = apply_pii_rules(content)
        assert "alice@example.com" not in filtered
        assert "555-123-4567" not in filtered
        assert "999-12-3456" not in filtered
        assert result.redactions_count == 3


# ============================================================================
# Tier 1 — Secret rules
# ============================================================================


class TestApplySecretRules:
    def test_empty_string_passes_through(self):
        filtered, result = apply_secret_rules("")
        assert filtered == ""
        assert result.redactions_count == 0

    def test_redacts_openai_key(self):
        content = "Use sk-proj-AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH for the API."
        filtered, result = apply_secret_rules(content)
        assert "sk-proj-AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH" not in filtered
        assert "secret:openai_key" in result.matched_rules

    def test_redacts_github_token(self):
        content = "Token: ghp_AAAAAABBBBBBCCCCCCDDDDDDEEEEEEFFFFFF"
        filtered, result = apply_secret_rules(content)
        assert "ghp_AAAAAABBBBBBCCCCCCDDDDDDEEEEEEFFFFFF" not in filtered
        assert "secret:github_token" in result.matched_rules

    def test_redacts_aws_access_key(self):
        content = "Configured AKIAIOSFODNN7EXAMPLE for AWS."
        filtered, result = apply_secret_rules(content)
        assert "AKIAIOSFODNN7EXAMPLE" not in filtered
        assert "secret:aws_access_key" in result.matched_rules

    def test_redacts_bearer_token(self):
        content = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        filtered, result = apply_secret_rules(content)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in filtered
        assert "secret:bearer_token" in result.matched_rules

    def test_redacts_url_with_credentials(self):
        content = "Endpoint: https://user:p4ssw0rd@db.example.com/path"
        filtered, result = apply_secret_rules(content)
        assert "user:p4ssw0rd" not in filtered
        assert "secret:url_credentials" in result.matched_rules

    def test_no_secret_passes_through(self):
        content = "Just regular text with no credentials."
        filtered, result = apply_secret_rules(content)
        assert filtered == content
        assert result.redactions_count == 0


# ============================================================================
# Tier 2 — Boundary rules (mocked)
# ============================================================================


@dataclass
class _MockBoundaryDecision:
    is_violation: bool = False
    violation_type: str = ""


class _MockBoundaryEnforcer:
    def __init__(self, will_flag: bool = False, violation_type: str = "harassment"):
        self._will_flag = will_flag
        self._violation_type = violation_type
        self.calls = 0

    async def enforce_boundaries(self, message, context=None, session_id=None):
        self.calls += 1
        return _MockBoundaryDecision(
            is_violation=self._will_flag, violation_type=self._violation_type
        )


class TestApplyBoundaryRules:
    @pytest.mark.asyncio
    async def test_no_enforcer_returns_clean(self):
        result = await apply_boundary_rules("some text", boundary_enforcer=None)
        assert result.is_violation is False
        assert result.matched_rules == []

    @pytest.mark.asyncio
    async def test_enforcer_passes_clean_content(self):
        enforcer = _MockBoundaryEnforcer(will_flag=False)
        result = await apply_boundary_rules("clean text", enforcer)
        assert result.is_violation is False
        assert enforcer.calls == 1

    @pytest.mark.asyncio
    async def test_enforcer_flags_violation(self):
        enforcer = _MockBoundaryEnforcer(will_flag=True, violation_type="harassment")
        result = await apply_boundary_rules("something bad", enforcer)
        assert result.is_violation is True
        assert "boundary:harassment" in result.matched_rules


# ============================================================================
# OutputFilter integration
# ============================================================================


class TestOutputFilter:
    @pytest.mark.asyncio
    async def test_internal_profile_passes_through(self):
        of = OutputFilter()
        result = await of.filter(
            content="Email leak: alice@example.com",
            task_type="intent_classification",
        )
        # Internal profile = log-only, no transform; PII NOT redacted here.
        assert result.filtered_content == "Email leak: alice@example.com"
        assert result.is_violation is False
        assert result.decision.action_taken == Action.PASSTHROUGH
        assert result.decision.profile_applied == Profile.INTERNAL

    @pytest.mark.asyncio
    async def test_user_visible_pii_redacts(self):
        of = OutputFilter()
        result = await of.filter(
            content="Contact alice@example.com please.",
            task_type="conversation",
        )
        assert "alice@example.com" not in result.filtered_content
        assert REDACTED_TOKEN in result.filtered_content
        assert result.is_violation is False  # PII redact is not "violation"
        assert result.decision.action_taken == Action.REDACT_IN_PLACE
        assert result.decision.severity == Severity.MEDIUM
        assert result.decision.redactions_count == 1

    @pytest.mark.asyncio
    async def test_user_visible_secret_redacts_high_severity(self):
        of = OutputFilter()
        result = await of.filter(
            content="Your key is sk-proj-AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH",
            task_type="conversation",
        )
        assert "sk-proj-AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH" not in result.filtered_content
        assert result.decision.action_taken == Action.REDACT_IN_PLACE
        assert result.decision.severity == Severity.HIGH

    @pytest.mark.asyncio
    async def test_user_visible_clean_content_passes_through(self):
        of = OutputFilter()
        result = await of.filter(
            content="The roadmap looks healthy this week.",
            task_type="conversation",
        )
        assert result.filtered_content == "The roadmap looks healthy this week."
        assert result.is_violation is False
        assert result.decision.action_taken == Action.PASSTHROUGH

    @pytest.mark.asyncio
    async def test_boundary_violation_drops_to_canned(self):
        enforcer = _MockBoundaryEnforcer(will_flag=True, violation_type="harassment")
        of = OutputFilter(boundary_enforcer=enforcer)
        result = await of.filter(
            content="LLM emitted something inappropriate here.",
            task_type="conversation",
        )
        assert result.is_violation is True
        assert result.filtered_content == CANNED_VIOLATION_RESPONSE
        assert result.decision.action_taken == Action.CANNED_SUBSTITUTE
        assert result.decision.severity == Severity.CRITICAL
        assert "boundary:harassment" in result.decision.matched_rules

    @pytest.mark.asyncio
    async def test_audit_envelope_stores_hashes_not_raw(self):
        """Critical invariant: audit log gets hashes, never raw content."""
        of = OutputFilter()
        result = await of.filter(
            content="Contact alice@example.com please.",
            task_type="conversation",
            user_id="user-1",
            session_id="sess-1",
        )
        decision = result.decision
        # Hashes are present
        assert len(decision.original_content_hash) == 64  # sha256 hex
        assert len(decision.filtered_content_hash) == 64
        # Original and filtered hashes differ (redaction happened)
        assert decision.original_content_hash != decision.filtered_content_hash
        # Raw content NOT serialized in audit_metadata
        for value in decision.audit_metadata.values():
            assert "alice@example.com" not in str(value)
        # to_dict() doesn't leak raw content either
        as_dict = decision.to_dict()
        assert "alice@example.com" not in str(as_dict)

    @pytest.mark.asyncio
    async def test_attempt_number_chain_captured(self):
        """Regenerate-trigger chain fields propagate into decision."""
        of = OutputFilter()
        result = await of.filter(
            content="Clean content.",
            task_type="conversation",
            attempt_number=2,
            prior_attempt_decision_id="prior-decision-id",
        )
        assert result.decision.attempt_number == 2
        assert result.decision.prior_attempt_decision_id == "prior-decision-id"

    @pytest.mark.asyncio
    async def test_unknown_task_type_falls_to_user_visible_filtering(self):
        of = OutputFilter()
        result = await of.filter(
            content="Email: bob@example.com",
            task_type="some_new_task_type_we_invented",
        )
        # Fail-closed: unknown task_types get user_visible profile + PII redaction.
        assert REDACTED_TOKEN in result.filtered_content
        assert result.decision.profile_applied == Profile.USER_VISIBLE
