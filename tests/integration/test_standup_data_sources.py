"""
Standup data-source tests — the survivors of the #1642 print-theater ruling.

History: created 2025-09-06 as Phase-0 "connectivity documentation" with deliberate
don't-fail semantics. Arch's #1642 investigation (2026-08-17) found 7 of 9 tests
structurally could not fail — two referenced GitHubAgent, a class that never existed
anywhere; one imported a module path that never existed; the rest swallowed every
exception or asserted nothing. Disposed per the ruling (recoverable at the commit
cited in #1642's closing record). What remains is only what can actually fail:

- test_standup_data_source_fallbacks — kept verbatim; Arch named it the template.
- test_standup_with_disconnected_sources — REWRITTEN: its old mocks patched two
  module paths that don't exist (services.integrations.github.github_agent,
  services.intelligence.document_memory), so patch() itself raised and the swallow
  hid it — the body never ran. Those sources being genuinely absent IS the
  disconnected condition, so the test now just runs the real fallback path and
  lets the assertions gate.
- test_document_memory_integration — kept (its import is real today), converted to
  the template's pytest.fail shape so a regression actually fails.
"""

import sys
from pathlib import Path

import pytest

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestStandupDataSources:
    """Data-source behavior for Morning Standup — every test here can fail."""

    def test_document_memory_integration(self):
        """DocumentService is importable and constructible for standup use."""
        try:
            from services.knowledge_graph.document_service import DocumentService

            doc_service = DocumentService()
        except ImportError as e:
            pytest.fail(f"Document service import failed: {e}")
        except Exception as e:
            pytest.fail(f"Document service initialization failed: {e}")
        assert doc_service is not None

    def test_standup_data_source_fallbacks(self):
        """Graceful fallback when data sources unavailable (#1642: the template)."""
        try:
            from cli.commands.standup import StandupCommand

            standup = StandupCommand()

            assert hasattr(standup, "run_standup"), "run_standup method missing"

            if hasattr(standup, "get_default_content"):
                default_content = standup.get_default_content()
                assert default_content is not None

        except ImportError as e:
            pytest.fail(f"Standup command import failed: {e}")
        except Exception as e:
            pytest.fail(f"Standup command initialization failed: {e}")

    @pytest.mark.asyncio
    async def test_standup_with_disconnected_sources(self):
        """Standup still produces default content with its data sources absent.

        No mocks: the GitHub-agent and document-memory module paths the original
        test patched do not exist, which is a stronger version of the condition
        it meant to simulate. If run_standup can't produce a result under that
        reality, this now FAILS — the assertions are un-swallowed per #1642.
        """
        from cli.commands.standup import StandupCommand

        standup = StandupCommand()
        result = await standup.run_standup()

        assert result is not None
        # Real result shape, pinned 2026-08-17 from an actual run (the original
        # asserted an imagined "time" key — the swallow hid that mismatch for a
        # year; #1642). Default content = the summary skeleton with zero counts.
        assert "execution_time_ms" in result
        assert "blockers" in result
        assert "issues_closed" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
