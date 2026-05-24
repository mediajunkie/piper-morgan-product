"""Tests for `KnowledgeGraphService.create_node` privacy-level filtering — #1089 Phase 0 increment 2.

Covers the three-level privacy semantics ratified during the 2026-05-17
Phase 0 design substrate:

- PUBLIC: no checks, no audit, no redaction
- STANDARD (default): flagged content redacted to `[FILTERED]` + metadata
  flags + filter event logged
- STRICT: flagged content REJECTED with `PrivacyFilterRejectedError`

Test matrix: 3 levels × {clean / harassment-flagged / inappropriate-flagged}.
Plus default-level inference + helper-function unit tests.

Mocks `BoundaryEnforcer` so test execution doesn't depend on the live
ethics-detector configuration. Mocks `KnowledgeGraphRepository.create_node`
so tests don't touch the database.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import KnowledgeNode
from services.ethics.privacy_types import (
    FilterReason,
    PrivacyFilterRejectedError,
    PrivacyLevel,
)
from services.knowledge.knowledge_graph_service import (
    _FILTERED_MARKER,
    KnowledgeGraphService,
)
from services.shared_types import NodeType


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------


def _make_service(
    *,
    harassment_match: bool = False,
    inappropriate_match: bool = False,
) -> KnowledgeGraphService:
    """Construct a KnowledgeGraphService with mocked dependencies.

    `harassment_match` / `inappropriate_match` configure what the
    mocked `BoundaryEnforcer` predicates return — drives the filter
    decision branches without exercising the real detector.

    Repository `create_node` is mocked as a passthrough — returns the
    KnowledgeNode it was called with so tests can assert on the
    eventually-saved content.
    """
    repo = MagicMock()
    repo.create_node = AsyncMock(side_effect=lambda node: node)

    enforcer = MagicMock()
    enforcer.check_harassment_patterns = AsyncMock(return_value=harassment_match)
    enforcer.check_inappropriate_content = AsyncMock(return_value=inappropriate_match)

    return KnowledgeGraphService(
        knowledge_graph_repository=repo,
        ethics_boundary_enforcer=enforcer,
    )


# -------------------------------------------------------------------
# PUBLIC level — no checks regardless of content
# -------------------------------------------------------------------


class TestCreateNodePublicLevel:
    """PUBLIC bypasses content checks entirely (system-trusted source)."""

    @pytest.mark.asyncio
    async def test_clean_content_saved_as_is(self):
        svc = _make_service(harassment_match=False, inappropriate_match=False)
        node = await svc.create_node(
            name="customer", node_type=NodeType.CONCEPT, description="enterprise client",
            privacy_level=PrivacyLevel.PUBLIC,
        )
        assert node.name == "customer"
        assert node.description == "enterprise client"
        assert "is_filtered" not in node.metadata

    @pytest.mark.asyncio
    async def test_flagged_content_NOT_checked(self):
        """Even with predicates matching, PUBLIC skips the check entirely —
        important property: PUBLIC is for known-clean sources, not a backdoor."""
        svc = _make_service(harassment_match=True, inappropriate_match=True)
        node = await svc.create_node(
            name="harass-trigger", node_type=NodeType.CONCEPT, description="bully",
            privacy_level=PrivacyLevel.PUBLIC,
        )
        # Content preserved (no redaction)
        assert node.name == "harass-trigger"
        assert node.description == "bully"
        # Predicates were NEVER called
        svc.ethics_boundary_enforcer.check_harassment_patterns.assert_not_called()
        svc.ethics_boundary_enforcer.check_inappropriate_content.assert_not_called()


# -------------------------------------------------------------------
# STANDARD level — redact + flag + save
# -------------------------------------------------------------------


class TestCreateNodeStandardLevel:
    """STANDARD checks content; flagged matches are redacted + saved."""

    @pytest.mark.asyncio
    async def test_clean_content_saved_as_is(self):
        svc = _make_service(harassment_match=False, inappropriate_match=False)
        node = await svc.create_node(
            name="customer", node_type=NodeType.CONCEPT, description="enterprise client",
            privacy_level=PrivacyLevel.STANDARD,
        )
        assert node.name == "customer"
        assert node.description == "enterprise client"
        assert "is_filtered" not in node.metadata

    @pytest.mark.asyncio
    async def test_harassment_match_redacts_and_flags(self):
        svc = _make_service(harassment_match=True, inappropriate_match=False)
        node = await svc.create_node(
            name="harass me", node_type=NodeType.CONCEPT, description="bully content",
            privacy_level=PrivacyLevel.STANDARD,
        )
        # Content redacted
        assert node.name == _FILTERED_MARKER
        assert node.description == _FILTERED_MARKER
        # Metadata carries the filter signal
        assert node.metadata["is_filtered"] is True
        assert node.metadata["filter_reason"] == "harassment_pattern_matched"
        # Node-type + structural fields preserved
        assert node.node_type == NodeType.CONCEPT

    @pytest.mark.asyncio
    async def test_inappropriate_match_redacts_with_correct_reason(self):
        svc = _make_service(harassment_match=False, inappropriate_match=True)
        node = await svc.create_node(
            name="bad", node_type=NodeType.CONCEPT, description="off content",
            privacy_level=PrivacyLevel.STANDARD,
        )
        assert node.name == _FILTERED_MARKER
        assert node.metadata["filter_reason"] == "inappropriate_content_matched"

    @pytest.mark.asyncio
    async def test_harassment_priority_over_inappropriate(self):
        """When BOTH predicates match, harassment wins (HOST Q2 severity priority)."""
        svc = _make_service(harassment_match=True, inappropriate_match=True)
        node = await svc.create_node(
            name="x", node_type=NodeType.CONCEPT, description="y",
            privacy_level=PrivacyLevel.STANDARD,
        )
        assert node.metadata["filter_reason"] == "harassment_pattern_matched"
        # Only harassment predicate consulted (short-circuit on first match)
        svc.ethics_boundary_enforcer.check_inappropriate_content.assert_not_called()

    @pytest.mark.asyncio
    async def test_existing_metadata_preserved_when_filtered(self):
        """Caller-supplied metadata keys survive the redaction merge."""
        svc = _make_service(harassment_match=True)
        node = await svc.create_node(
            name="harass", node_type=NodeType.CONCEPT, description="bully",
            metadata={"source": "test", "version": 3},
            privacy_level=PrivacyLevel.STANDARD,
        )
        assert node.metadata["source"] == "test"
        assert node.metadata["version"] == 3
        assert node.metadata["is_filtered"] is True
        assert node.metadata["filter_reason"] == "harassment_pattern_matched"


# -------------------------------------------------------------------
# STRICT level — reject with exception
# -------------------------------------------------------------------


class TestCreateNodeStrictLevel:
    """STRICT checks content; flagged matches RAISE + don't save."""

    @pytest.mark.asyncio
    async def test_clean_content_saved_as_is(self):
        svc = _make_service(harassment_match=False, inappropriate_match=False)
        node = await svc.create_node(
            name="customer", node_type=NodeType.CONCEPT, description="enterprise client",
            privacy_level=PrivacyLevel.STRICT,
        )
        assert node.name == "customer"
        assert "is_filtered" not in node.metadata
        svc.repo.create_node.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_harassment_match_raises_and_does_not_save(self):
        svc = _make_service(harassment_match=True, inappropriate_match=False)
        with pytest.raises(PrivacyFilterRejectedError) as exc_info:
            await svc.create_node(
                name="harass", node_type=NodeType.CONCEPT, description="bully",
                privacy_level=PrivacyLevel.STRICT,
            )
        assert exc_info.value.filter_reason is FilterReason.HARASSMENT_PATTERN_MATCHED
        # Repository NEVER called on STRICT rejection
        svc.repo.create_node.assert_not_called()

    @pytest.mark.asyncio
    async def test_inappropriate_match_raises_with_correct_reason(self):
        svc = _make_service(harassment_match=False, inappropriate_match=True)
        with pytest.raises(PrivacyFilterRejectedError) as exc_info:
            await svc.create_node(
                name="bad", node_type=NodeType.CONCEPT, description="off",
                privacy_level=PrivacyLevel.STRICT,
            )
        assert exc_info.value.filter_reason is FilterReason.INAPPROPRIATE_CONTENT_MATCHED
        svc.repo.create_node.assert_not_called()


# -------------------------------------------------------------------
# Default level + helpers
# -------------------------------------------------------------------


class TestDefaultPrivacyLevel:
    """`privacy_level` defaults to STANDARD when caller doesn't pass it."""

    @pytest.mark.asyncio
    async def test_default_is_standard_on_flagged_content(self):
        """Flagged write without explicit level should redact (STANDARD behavior),
        not reject (STRICT) and not bypass (PUBLIC)."""
        svc = _make_service(harassment_match=True)
        node = await svc.create_node(
            name="harass", node_type=NodeType.CONCEPT, description="bully",
            # privacy_level intentionally omitted
        )
        assert node.name == _FILTERED_MARKER
        assert node.metadata["is_filtered"] is True


class TestCheckContentHelper:
    """Direct tests for `_check_content_for_filtering` helper."""

    @pytest.mark.asyncio
    async def test_empty_content_returns_none_without_calling_predicates(self):
        """Whitespace-only content is treated as clean — no predicate calls."""
        svc = _make_service(harassment_match=True, inappropriate_match=True)
        result = await svc._check_content_for_filtering(name="", description="")
        assert result is None
        svc.ethics_boundary_enforcer.check_harassment_patterns.assert_not_called()
        svc.ethics_boundary_enforcer.check_inappropriate_content.assert_not_called()

    @pytest.mark.asyncio
    async def test_clean_content_returns_none(self):
        svc = _make_service(harassment_match=False, inappropriate_match=False)
        result = await svc._check_content_for_filtering(name="ok", description="fine")
        assert result is None

    @pytest.mark.asyncio
    async def test_harassment_match_returns_harassment_reason(self):
        svc = _make_service(harassment_match=True, inappropriate_match=False)
        result = await svc._check_content_for_filtering(name="x", description="y")
        assert result is FilterReason.HARASSMENT_PATTERN_MATCHED

    @pytest.mark.asyncio
    async def test_inappropriate_match_returns_inappropriate_reason(self):
        svc = _make_service(harassment_match=False, inappropriate_match=True)
        result = await svc._check_content_for_filtering(name="x", description="y")
        assert result is FilterReason.INAPPROPRIATE_CONTENT_MATCHED


class TestRedactNodeContentHelper:
    """Direct tests for `_redact_node_content` helper."""

    def test_returns_filtered_markers_and_metadata_flags(self):
        svc = _make_service()
        name, desc, meta = svc._redact_node_content(
            filter_reason=FilterReason.HARASSMENT_PATTERN_MATCHED,
            original_metadata=None,
        )
        assert name == _FILTERED_MARKER
        assert desc == _FILTERED_MARKER
        assert meta == {
            "is_filtered": True,
            "filter_reason": "harassment_pattern_matched",
        }

    def test_preserves_caller_metadata_keys(self):
        svc = _make_service()
        _, _, meta = svc._redact_node_content(
            filter_reason=FilterReason.INAPPROPRIATE_CONTENT_MATCHED,
            original_metadata={"author": "alice", "ttl": 90},
        )
        assert meta["author"] == "alice"
        assert meta["ttl"] == 90
        assert meta["is_filtered"] is True
        assert meta["filter_reason"] == "inappropriate_content_matched"

    def test_does_not_mutate_caller_metadata(self):
        """Caller's dict is NOT modified in place — copy-on-write semantics."""
        svc = _make_service()
        caller_meta = {"key": "value"}
        svc._redact_node_content(
            filter_reason=FilterReason.HARASSMENT_PATTERN_MATCHED,
            original_metadata=caller_meta,
        )
        # Caller dict untouched
        assert caller_meta == {"key": "value"}
        assert "is_filtered" not in caller_meta


# -------------------------------------------------------------------
# Increment 3: read-path privacy filtering
# -------------------------------------------------------------------


def _make_clean_node(name: str = "ok", node_id: str = "n-clean") -> KnowledgeNode:
    """KnowledgeNode unflagged by the write path (no is_filtered metadata)."""
    return KnowledgeNode(
        id=node_id,
        name=name,
        node_type=NodeType.CONCEPT,
        description=f"{name}-desc",
        metadata={},
    )


def _make_filtered_node(node_id: str = "n-flagged") -> KnowledgeNode:
    """KnowledgeNode that was flagged + redacted by the write path."""
    return KnowledgeNode(
        id=node_id,
        name=_FILTERED_MARKER,
        node_type=NodeType.CONCEPT,
        description=_FILTERED_MARKER,
        metadata={
            "is_filtered": True,
            "filter_reason": FilterReason.HARASSMENT_PATTERN_MATCHED.value,
        },
    )


class TestIsNodeFilteredHelper:
    """Direct tests for `_is_node_filtered` predicate."""

    def test_node_with_is_filtered_true_returns_true(self):
        svc = _make_service()
        assert svc._is_node_filtered(_make_filtered_node()) is True

    def test_node_with_is_filtered_false_returns_false(self):
        svc = _make_service()
        node = _make_clean_node()
        node.metadata["is_filtered"] = False
        assert svc._is_node_filtered(node) is False

    def test_node_missing_is_filtered_key_returns_false(self):
        """Legacy node without the metadata key is treated as unflagged."""
        svc = _make_service()
        assert svc._is_node_filtered(_make_clean_node()) is False


class TestGetNodePrivacyLevel:
    """`get_node` per-level read semantics."""

    @pytest.mark.asyncio
    async def test_public_returns_unfiltered_node(self):
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_clean_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.PUBLIC)
        assert result is not None
        assert result.name == "ok"

    @pytest.mark.asyncio
    async def test_public_returns_filtered_node(self):
        """PUBLIC ignores filter flag — used for admin / audit surfaces."""
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_filtered_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.PUBLIC)
        assert result is not None
        assert result.metadata["is_filtered"] is True

    @pytest.mark.asyncio
    async def test_standard_returns_unfiltered_node(self):
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_clean_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.STANDARD)
        assert result is not None

    @pytest.mark.asyncio
    async def test_standard_returns_filtered_node_with_redacted_content(self):
        """STANDARD returns the node — content already `[FILTERED]` from write path."""
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_filtered_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.STANDARD)
        assert result is not None
        assert result.name == _FILTERED_MARKER
        assert result.description == _FILTERED_MARKER
        assert result.metadata["is_filtered"] is True

    @pytest.mark.asyncio
    async def test_strict_returns_unfiltered_node(self):
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_clean_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.STRICT)
        assert result is not None

    @pytest.mark.asyncio
    async def test_strict_excludes_filtered_node(self):
        """STRICT returns None for flagged nodes — structural absence."""
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_filtered_node())
        result = await svc.get_node("n-1", privacy_level=PrivacyLevel.STRICT)
        assert result is None

    @pytest.mark.asyncio
    async def test_repo_returns_none_passthrough(self):
        """Node not found at repo: None regardless of privacy_level."""
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=None)
        for level in PrivacyLevel:
            result = await svc.get_node("missing", privacy_level=level)
            assert result is None

    @pytest.mark.asyncio
    async def test_default_level_is_standard(self):
        """Omitting privacy_level uses STANDARD (returns filtered nodes with redacted content)."""
        svc = _make_service()
        svc.repo.get_node_by_id = AsyncMock(return_value=_make_filtered_node())
        result = await svc.get_node("n-1")  # no privacy_level
        assert result is not None
        assert result.name == _FILTERED_MARKER


class TestGetNodesByTypePrivacyLevel:
    """`get_nodes_by_type` per-level read semantics."""

    @pytest.mark.asyncio
    async def test_public_returns_all_including_filtered(self):
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("a", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.get_nodes_by_type(NodeType.CONCEPT, privacy_level=PrivacyLevel.PUBLIC)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_standard_returns_all_including_filtered(self):
        """STANDARD returns flagged nodes (with their already-redacted content)."""
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("a", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.get_nodes_by_type(NodeType.CONCEPT, privacy_level=PrivacyLevel.STANDARD)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_strict_excludes_filtered(self):
        svc = _make_service()
        nodes_in_repo = [
            _make_clean_node("a", "n1"),
            _make_filtered_node("n2"),
            _make_clean_node("b", "n3"),
        ]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.get_nodes_by_type(NodeType.CONCEPT, privacy_level=PrivacyLevel.STRICT)
        assert len(result) == 2
        assert all(not n.metadata.get("is_filtered") for n in result)
        assert {n.id for n in result} == {"n1", "n3"}

    @pytest.mark.asyncio
    async def test_default_level_is_standard(self):
        """Omitting privacy_level uses STANDARD — flagged nodes included."""
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("a", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.get_nodes_by_type(NodeType.CONCEPT)  # no privacy_level
        assert len(result) == 2


class TestSearchNodesPrivacyLevel:
    """`search_nodes` per-level read semantics — strict-exclude after search match."""

    @pytest.mark.asyncio
    async def test_public_returns_all_including_filtered(self):
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("hello", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.search_nodes(
            node_type=NodeType.CONCEPT, privacy_level=PrivacyLevel.PUBLIC, limit=10
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_standard_returns_all_including_filtered(self):
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("hello", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.search_nodes(
            node_type=NodeType.CONCEPT, privacy_level=PrivacyLevel.STANDARD, limit=10
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_strict_excludes_filtered(self):
        svc = _make_service()
        nodes_in_repo = [
            _make_clean_node("hello", "n1"),
            _make_filtered_node("n2"),
            _make_clean_node("world", "n3"),
        ]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.search_nodes(
            node_type=NodeType.CONCEPT, privacy_level=PrivacyLevel.STRICT, limit=10
        )
        assert {n.id for n in result} == {"n1", "n3"}

    @pytest.mark.asyncio
    async def test_strict_combined_with_search_term(self):
        """STRICT-exclusion stacks correctly with search_term — both filters apply."""
        svc = _make_service()
        nodes_in_repo = [
            _make_clean_node("hello", "n1"),       # matches 'hello'
            _make_filtered_node("n2"),              # FILTERED markers don't match 'hello'
            _make_clean_node("world", "n3"),       # doesn't match 'hello'
        ]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.search_nodes(
            node_type=NodeType.CONCEPT,
            search_term="hello",
            privacy_level=PrivacyLevel.STRICT,
            limit=10,
        )
        assert len(result) == 1
        assert result[0].id == "n1"

    @pytest.mark.asyncio
    async def test_default_level_is_standard(self):
        """Omitting privacy_level uses STANDARD — flagged nodes included."""
        svc = _make_service()
        nodes_in_repo = [_make_clean_node("hello", "n1"), _make_filtered_node("n2")]
        svc.repo.get_nodes_by_type = AsyncMock(return_value=nodes_in_repo)
        result = await svc.search_nodes(node_type=NodeType.CONCEPT, limit=10)  # no privacy_level
        assert len(result) == 2
