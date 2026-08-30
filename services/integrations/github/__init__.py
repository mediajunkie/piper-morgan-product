# GitHub integration exports
# Legacy GitHubAgent removed in Week 4 of deprecation timeline (CORE-INT #109)
# Use GitHubIntegrationRouter for all GitHub operations
#
# The Issue-621 grammar-conscious triplet (narrative_bridge / narrative_helpers /
# response_context) was disposed 2026-08-30 in the Batch-2 census-dead-family
# disposal — loaded-only, zero call sites. Retrievable by commit hash via the
# disposal record in decisions.log. Submodules (github_integration_router,
# repo_resolver, ...) import directly, e.g.
# `from services.integrations.github import repo_resolver`.

__all__: list[str] = []
