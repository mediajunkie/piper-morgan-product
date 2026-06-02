"""
Tests for Issue #1030 R4 Step 5: ContextAssembler per-gatherer provenance.

After gather_context() runs, get_last_provenance() returns a map keyed by
domain_context key with source attribution + fetch_timestamp + user-scoping.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler


class _NoOpCache:
    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()

    async def get(self, key):
        return None

    async def set(self, key, value, ttl_seconds):
        return False

    async def invalidate(self, key):
        return False

    async def invalidate_prefix(self, prefix):
        return 0


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


class TestProvenanceAttribution:
    """_attribute_provenance writes per-key source entries."""

    def test_attribute_known_key_uses_KEY_SOURCES(self):
        assembler = ContextAssembler()
        assembler._last_provenance = {}
        assembler._attribute_provenance(["calendar"], user_id="u-test")
        assert "calendar" in assembler._last_provenance
        entry = assembler._last_provenance["calendar"]
        assert entry["source"] == "CalendarIntegrationRouter"
        assert entry["integration"] == "google_calendar"
        assert "fetch_timestamp" in entry
        assert entry["user_id_scoped"] is True

    def test_attribute_unknown_key_uses_fallback(self):
        assembler = ContextAssembler()
        assembler._last_provenance = {}
        assembler._attribute_provenance(["totally_made_up_key"])
        entry = assembler._last_provenance["totally_made_up_key"]
        assert entry["source"] == "ContextAssembler"
        assert "fetch_timestamp" in entry

    def test_attribute_with_extra_metadata(self):
        assembler = ContextAssembler()
        assembler._last_provenance = {}
        assembler._attribute_provenance(
            ["recent_activity"],
            user_id="u-test",
            extra={"dedup_decisions": [{"kept": "github", "dropped": "slack_mention"}]},
        )
        entry = assembler._last_provenance["recent_activity"]
        assert "dedup_decisions" in entry
        assert entry["source"] == "MultiSourceAggregator"

    def test_attribute_no_user_id_skips_scoping_flag(self):
        assembler = ContextAssembler()
        assembler._last_provenance = {}
        assembler._attribute_provenance(["calendar"])
        entry = assembler._last_provenance["calendar"]
        assert "user_id_scoped" not in entry


class TestGatherContextResetsProvenance:
    @pytest.mark.asyncio
    async def test_gather_context_resets_provenance_each_call(self):
        """A previous call's provenance must not bleed into the next."""
        assembler = ContextAssembler()
        # Seed stale provenance from imagined prior call
        assembler._last_provenance = {"stale_key": {"source": "Stale"}}
        with patch.object(
            assembler,
            "_gather_identity_context",
            AsyncMock(return_value={}),
        ):
            await assembler.gather_context(
                intent_category="IDENTITY", user_id="u-test"
            )
        # stale_key should be gone after the new gather
        assert "stale_key" not in assembler._last_provenance

    @pytest.mark.asyncio
    async def test_gather_context_attributes_keys_from_each_branch(self):
        """Each gather branch's returned keys get provenance entries."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_trust_context",
            AsyncMock(return_value={"trust_profile": {"stage": 2}}),
        ):
            await assembler.gather_context(
                intent_category="TRUST", user_id="u-test"
            )
        prov = assembler.get_last_provenance()
        assert "trust_profile" in prov
        assert prov["trust_profile"]["source"] == "UserTrustProfileRepository"

    @pytest.mark.asyncio
    async def test_get_last_provenance_for_insight_pull(self):
        """MEMORY/pull_insights path attributes insights key correctly."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_insight_pull_context",
            AsyncMock(
                return_value={
                    "insights": {"high_confidence": [], "is_empty": True}
                }
            ),
        ):
            await assembler.gather_context(
                intent_category="MEMORY",
                intent_action="pull_insights",
                user_id="u-test",
            )
        prov = assembler.get_last_provenance()
        assert "insights" in prov
        assert prov["insights"]["source"] == "InsightRepository"

    @pytest.mark.asyncio
    async def test_current_time_has_no_provenance_entry(self):
        """current_time is always-available system value; deliberately not
        attributed (avoid 'why did you mention 10am' becoming a clock citation)."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_trust_context",
            AsyncMock(return_value={"trust_profile": {"stage": 2}}),
        ):
            context = await assembler.gather_context(
                intent_category="TRUST", user_id="u-test"
            )
        assert "current_time" in context  # ALWAYS set
        prov = assembler.get_last_provenance()
        assert "current_time" not in prov  # but NOT in provenance

    @pytest.mark.asyncio
    async def test_get_last_provenance_returns_empty_dict_when_unset(self):
        assembler = ContextAssembler()
        # No gather call yet
        assert assembler.get_last_provenance() == {}
