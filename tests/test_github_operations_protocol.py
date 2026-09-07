"""#1723 — the GitHubOperations contract ratchet.

The chokepoint move applied to code (Exec ruling, PM-ratified 2026-09-06): before
this test, a router method written against a method neither backing class defines
failed only when someone finally called it in the wild (#892 ``create_issue``,
#1709 ``get_recent_activity``). Now the build fails, listing every missing method
at once.

Same shrink-only idiom as ``MAX_DISPATCH_SITES`` in test_architecture_enforcement:
``KNOWN_MISSING`` may only shrink. When you implement one of its members on the
MCP adapter, REMOVE it from the set in the same commit.
"""

import inspect

from services.integrations.github.github_operations_protocol import GitHubOperations

# Live-called operations the MCP adapter does not yet implement, each with its
# tracking issue. Shrink-only: implementing one without removing it here fails
# the build, and adding a new one is the drift this ratchet exists to block.
KNOWN_MISSING = {
    "get_issue_by_url": "#1723",
    "parse_github_url": "#1723",
}


def _protocol_members():
    return [
        name
        for name, member in inspect.getmembers(GitHubOperations)
        if not name.startswith("_") and callable(member)
    ]


def _adapter_class():
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return GitHubMCPSpatialAdapter


class TestGitHubOperationsContractRatchet:
    def test_every_protocol_member_backed_or_tracked(self):
        """Every GitHubOperations member exists on the MCP adapter or is in
        KNOWN_MISSING with a tracking issue. Fails listing ALL gaps at once —
        that is the point (one pass, not nine debugging sessions)."""
        adapter = _adapter_class()
        gaps = [
            name
            for name in _protocol_members()
            if not hasattr(adapter, name) and name not in KNOWN_MISSING
        ]
        assert not gaps, (
            f"GitHubOperations members with NO backing on GitHubMCPSpatialAdapter "
            f"and NO KNOWN_MISSING entry: {gaps}. Either implement them on the "
            f"adapter or file a tracking issue and add them to KNOWN_MISSING "
            f"(tests/test_github_operations_protocol.py) in this commit."
        )

    def test_known_missing_only_shrinks(self):
        """A KNOWN_MISSING entry whose method now exists on the adapter must be
        removed — the ratchet only goes down."""
        adapter = _adapter_class()
        stale = [name for name in KNOWN_MISSING if hasattr(adapter, name)]
        assert not stale, (
            f"KNOWN_MISSING entries now implemented on the adapter: {stale}. "
            f"Remove them from KNOWN_MISSING in this commit — the set is "
            f"shrink-only."
        )

    def test_known_missing_members_are_real_protocol_members(self):
        """KNOWN_MISSING must stay a subset of the Protocol — a deleted or
        renamed operation must not linger here looking load-bearing."""
        members = set(_protocol_members())
        phantom = [name for name in KNOWN_MISSING if name not in members]
        assert not phantom, (
            f"KNOWN_MISSING entries that are not GitHubOperations members: "
            f"{phantom}. Remove them."
        )

    def test_router_dispatch_surface_is_protocol_or_tracked(self):
        """Every method name the router dispatches through _get_integration()
        must be a Protocol member — the contract and the dispatch surface may
        not drift apart again. (get_integration_status is exempt by design:
        introspective, hasattr-guarded, not routed through _get_integration.)"""
        import re

        source = inspect.getsource(
            __import__(
                "services.integrations.github.github_integration_router",
                fromlist=["GitHubIntegrationRouter"],
            ).GitHubIntegrationRouter
        )
        dispatched = set(re.findall(r'_get_integration\(\s*"([a-z_]+)"\s*\)', source))
        members = set(_protocol_members())
        undeclared = dispatched - members
        assert not undeclared, (
            f"Router dispatches operations not declared in GitHubOperations: "
            f"{sorted(undeclared)}. Add them to the Protocol (and to "
            f"KNOWN_MISSING if unimplemented) — the -> Any era is over (#1723)."
        )
