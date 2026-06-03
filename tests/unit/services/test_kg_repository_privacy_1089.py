"""Tests for `KnowledgeGraphRepository` privacy safety net — #1089 Phase 0 increment 4.

Repository-layer defense-in-depth per Architect Q3 disposition 2026-05-17:
slim flag-word check fires when a direct repo write contains trivially-
detectable patterns AND lacks the `is_filtered` flag from the service-
layer write path. Catches future bypasses where a new service writes
directly to `KnowledgeGraphRepository` instead of through
`KnowledgeGraphService.create_node`.

Tests exercise `_privacy_safety_check` in isolation (no DB needed) — the
method is a synchronous predicate that raises on violation. End-to-end
create_node testing happens via the existing
`tests/integration/test_knowledge_graph_enhancement.py` suite (which
continues to pass after this change since legitimate KG nodes don't
contain the safety-net patterns).
"""

from unittest.mock import MagicMock

import pytest

from services.database.repositories import (
    _REPO_SAFETY_NET_PATTERNS,
    KnowledgeGraphRepository,
)
from services.domain.models import KnowledgeNode
from services.ethics.privacy_types import FilterReason, PrivacyFilterRejectedError
from services.shared_types import NodeType


# -------------------------------------------------------------------
# Fixtures / helpers
# -------------------------------------------------------------------


def _make_repo() -> KnowledgeGraphRepository:
    """Construct a repo with a mocked session — `_privacy_safety_check`
    doesn't touch the session, so this is enough for unit testing the
    predicate in isolation."""
    fake_session = MagicMock()
    return KnowledgeGraphRepository(fake_session)


def _make_node(
    name: str,
    description: str = "",
    is_filtered: bool = False,
) -> KnowledgeNode:
    """Construct a KnowledgeNode for the safety-net check.

    `is_filtered=True` adds the metadata flag the service-layer write
    path sets when it redacts content. The safety net consults this
    flag to decide whether to skip the check (already-filtered content
    is trusted)."""
    metadata = {}
    if is_filtered:
        metadata["is_filtered"] = True
    return KnowledgeNode(
        id="n-test",
        name=name,
        node_type=NodeType.CONCEPT,
        description=description,
        metadata=metadata,
    )


# -------------------------------------------------------------------
# Safety net pattern list — sanity
# -------------------------------------------------------------------


class TestRepoSafetyNetPatternList:
    """The `_REPO_SAFETY_NET_PATTERNS` constant should stay narrow per
    the Architect Q3 design — false positives on legitimate writes
    matter more than completeness here."""

    def test_pattern_list_is_a_tuple(self):
        """Module-level constant, immutable tuple (not a list)."""
        assert isinstance(_REPO_SAFETY_NET_PATTERNS, tuple)

    def test_pattern_list_is_narrow(self):
        """Stay deliberately narrow. If this assertion fires, the list
        grew past its "trivially-detectable" mandate — review whether
        each addition is warranted."""
        assert len(_REPO_SAFETY_NET_PATTERNS) <= 5

    def test_patterns_are_all_lowercase(self):
        """Check logic lowercases content + patterns are pre-lowered;
        if a pattern has uppercase, the check silently misses it."""
        for pattern in _REPO_SAFETY_NET_PATTERNS:
            assert pattern == pattern.lower()

    def test_patterns_are_non_empty_strings(self):
        """Empty-string patterns would match everything — silent footgun."""
        for pattern in _REPO_SAFETY_NET_PATTERNS:
            assert isinstance(pattern, str) and len(pattern) > 0


# -------------------------------------------------------------------
# _privacy_safety_check — predicate behavior
# -------------------------------------------------------------------


class TestPrivacySafetyCheckClean:
    """Clean content passes; no raise."""

    def test_empty_content(self):
        repo = _make_repo()
        node = _make_node(name="", description="")
        repo._privacy_safety_check(node)  # no raise

    def test_neutral_words(self):
        repo = _make_repo()
        node = _make_node(name="customer", description="enterprise account")
        repo._privacy_safety_check(node)  # no raise

    def test_content_without_safety_net_words(self):
        """Words that flag the FULL boundary enforcer at the service
        layer (e.g., "inappropriate", "threaten") aren't necessarily in
        the SLIM repo safety net — repo passes them through (defense-
        in-depth is the slim layer, not full-redundant coverage)."""
        repo = _make_repo()
        node = _make_node(name="threaten alarm", description="intimidate scenario")
        # The slim list (harass, bully) doesn't include these — pass.
        # If a flag word IS later added to the slim list, this test
        # documents the expected current scope.
        for pattern in _REPO_SAFETY_NET_PATTERNS:
            assert pattern not in "threaten alarm intimidate scenario".lower()
        repo._privacy_safety_check(node)


# -------------------------------------------------------------------
# _privacy_safety_check — fires on each pattern
# -------------------------------------------------------------------


class TestPrivacySafetyCheckFires:
    """Flag words in unfiltered content trigger the raise."""

    @pytest.mark.parametrize("pattern", _REPO_SAFETY_NET_PATTERNS)
    def test_raises_on_each_pattern_in_name(self, pattern):
        repo = _make_repo()
        node = _make_node(name=f"some {pattern} text", description="")
        with pytest.raises(PrivacyFilterRejectedError):
            repo._privacy_safety_check(node)

    @pytest.mark.parametrize("pattern", _REPO_SAFETY_NET_PATTERNS)
    def test_raises_on_each_pattern_in_description(self, pattern):
        repo = _make_repo()
        node = _make_node(name="ok", description=f"content with {pattern}")
        with pytest.raises(PrivacyFilterRejectedError):
            repo._privacy_safety_check(node)

    @pytest.mark.parametrize("pattern", _REPO_SAFETY_NET_PATTERNS)
    def test_case_insensitive_match(self, pattern):
        """Patterns are lowercased; content is lowercased — uppercase
        flag words still match (avoids trivial bypass-by-casing)."""
        repo = _make_repo()
        upper_pattern = pattern.upper()
        node = _make_node(name=f"text {upper_pattern} more", description="")
        with pytest.raises(PrivacyFilterRejectedError):
            repo._privacy_safety_check(node)


# -------------------------------------------------------------------
# _privacy_safety_check — is_filtered flag skips the check
# -------------------------------------------------------------------


class TestPrivacySafetyCheckSkippedWhenFiltered:
    """`metadata.is_filtered=True` signals service-layer pre-filtering;
    repo trusts the flag and skips its own check."""

    @pytest.mark.parametrize("pattern", _REPO_SAFETY_NET_PATTERNS)
    def test_skips_when_is_filtered_true_even_with_pattern(self, pattern):
        """Service-layer's STANDARD redaction sets is_filtered=True and
        replaces content with `[FILTERED]` — but to test the SKIP
        semantics independently, we include both the flag AND the
        pattern. The skip should win (the service vouched)."""
        repo = _make_repo()
        node = _make_node(
            name=f"contains {pattern}",
            description="real content",
            is_filtered=True,  # service-layer set this
        )
        repo._privacy_safety_check(node)  # no raise

    def test_no_skip_when_is_filtered_explicitly_false(self):
        """Only `True` skips. False-or-missing means service didn't
        vouch — run the check."""
        repo = _make_repo()
        node = KnowledgeNode(
            id="n-1",
            name="harass text",  # contains a slim-list pattern
            node_type=NodeType.CONCEPT,
            description="",
            metadata={"is_filtered": False},
        )
        with pytest.raises(PrivacyFilterRejectedError):
            repo._privacy_safety_check(node)


# -------------------------------------------------------------------
# Exception details
# -------------------------------------------------------------------


class TestPrivacySafetyCheckException:
    """Verify the raised exception carries useful context."""

    def test_filter_reason_is_harassment(self):
        """Repo-layer fires with HARASSMENT_PATTERN_MATCHED for the
        current slim list (harassment-leaning words). When the list
        expands to include inappropriate-content patterns, this test
        + the safety-check code will need to differentiate."""
        repo = _make_repo()
        node = _make_node(name="harass content", description="")
        with pytest.raises(PrivacyFilterRejectedError) as exc_info:
            repo._privacy_safety_check(node)
        assert exc_info.value.filter_reason is FilterReason.HARASSMENT_PATTERN_MATCHED

    def test_message_includes_matched_pattern(self):
        """The error message should name the pattern + recommend the
        proper service-layer path. Helps debug accidental bypasses."""
        repo = _make_repo()
        node = _make_node(name="bully content", description="")
        with pytest.raises(PrivacyFilterRejectedError) as exc_info:
            repo._privacy_safety_check(node)
        msg = str(exc_info.value)
        assert "bully" in msg
        assert "KnowledgeGraphService" in msg  # nudge toward proper path
