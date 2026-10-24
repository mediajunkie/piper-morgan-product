"""
Architecture Enforcement Tests - Phase 4A
Prevents regression to direct GitHubAgent imports
"""

import ast
import glob
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List

import pytest
import yaml

from services.process.registry import ProcessType


class TestGitHubArchitectureEnforcement:
    """
    Comprehensive architectural enforcement for GitHub integration router pattern.

    These tests ensure that:
    1. Services never import GitHubAgent directly
    2. Services use GitHubIntegrationRouter instead
    3. The router architecture remains intact as code evolves
    """

    def test_no_direct_github_agent_imports(self):
        """
        CRITICAL: Prevent services from importing GitHubAgent directly.

        This test fails if any service bypasses the router architecture.
        Direct imports are prohibited to maintain feature flag control
        and spatial intelligence capabilities.
        """

        # Find all Python files in services directory
        service_files = glob.glob("services/**/*.py", recursive=True)

        # Files that are allowed to import GitHubAgent directly
        allowed_files = [
            "services/integrations/github/github_agent.py",  # The agent itself
            "services/integrations/github/github_integration_router.py",  # Router needs it for delegation
            "services/integrations/github/__init__.py",  # Module exports
        ]

        violations = []

        for file_path in service_files:
            # Skip test files and cache (specific patterns only)
            if file_path.startswith("tests/") or "__pycache__" in file_path:
                continue

            # Skip explicitly allowed files
            if any(allowed in file_path for allowed in allowed_files):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Skip binary files
                continue

            # Check for direct imports (multiple patterns)
            direct_import_patterns = [
                "from .github_agent import GitHubAgent",
                "from github_agent import GitHubAgent",
                "import services.integrations.github.github_agent",
            ]

            for pattern in direct_import_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: Direct GitHubAgent import found - '{pattern}'")

        if violations:
            violation_message = self._format_violation_message(violations)
            pytest.fail(violation_message)

    def test_services_use_router(self):
        """
        CRITICAL: Verify domain layer services use GitHubIntegrationRouter.

        Domain services that need GitHub functionality must use the router
        to ensure feature flag control and spatial intelligence work correctly.

        Per ADR-029: Orchestration/feature layers use domain services, not routers.
        """

        # Services that were converted in Phase 2A and must use router
        # NOTE: Orchestration services (like standup_orchestration_service.py) use
        # GitHubDomainService per ADR-029, not the router directly
        required_router_services = [
            "services/domain/github_domain_service.py",
            "services/domain/pm_number_manager.py",
            # REMOVED: "services/domain/standup_orchestration_service.py" - uses GitHubDomainService per ADR-029
            # REMOVED 2026-05-24 (#694): "services/integrations/github/issue_analyzer.py"
            #   — orphan in production (no callers of GitHubIssueAnalyzer.analyze_issue_by_url),
            #   file deleted along with companion issue_generator.py + content_generator.py.
            # REMOVED 2026-05-24 (#1114): "services/orchestration/engine.py"
            #   — deleted in #1094 (Architect-ratified γ-preserve, commit 92617bab1, 2026-05-15);
            #   the OrchestrationEngine class is gone, replaced by direct IntentService dispatch.
            #   This allowlist entry was stale ever since.
        ]

        missing_router_imports = []

        for file_path in required_router_services:
            if not os.path.exists(file_path):
                missing_router_imports.append(f"{file_path}: File not found")
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                missing_router_imports.append(f"{file_path}: Cannot read file")
                continue

            # Check for router import and usage
            if "GitHubIntegrationRouter" not in content:
                missing_router_imports.append(f"{file_path}: Missing GitHubIntegrationRouter usage")
            elif (
                "from services.integrations.github.github_integration_router import GitHubIntegrationRouter"
                not in content
            ):
                missing_router_imports.append(
                    f"{file_path}: Router imported but incorrect import statement"
                )

        if missing_router_imports:
            failure_message = self._format_router_missing_message(missing_router_imports)
            pytest.fail(failure_message)

    def test_router_architectural_integrity(self):
        """
        CRITICAL: Verify router maintains proper architectural patterns.

        UPDATED (Sprint A4): Supports two architectures:
        - Week 4: Spatial-only with _get_integration() delegation
        - ADR-013 Phase 2: MCP+Spatial with adapter methods

        Both patterns maintain spatial intelligence and proper error handling.
        """

        router_file = "services/integrations/github/github_integration_router.py"

        if not os.path.exists(router_file):
            pytest.fail(f"Router file not found: {router_file}")

        with open(router_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if router is in ADR-013 Phase 2 migration
        is_mcp_phase2 = self._is_mcp_migration_phase2(content)

        if is_mcp_phase2:
            # ADR-013 Phase 2 required patterns
            required_patterns = [
                "GitHubMCPSpatialAdapter",  # MCP integration
                "GitHubSpatialIntelligence",  # Spatial fallback
                "self.mcp_adapter",  # MCP adapter instance
                "self.spatial_github",  # Spatial instance
                "async def initialize(",  # Async initialization
                "self._initialized",  # Lazy init flag
                "raise RuntimeError",  # Proper error handling
            ]
        else:
            # Week 4 spatial-only patterns
            required_patterns = [
                "_get_integration",  # Simplified delegation method
                "FeatureFlags.should_use_spatial_github",  # Feature flags
                "GitHubSpatialIntelligence",  # Spatial integration
                "raise RuntimeError",  # Proper error handling
            ]

        # Patterns that MUST NOT exist (both architectures)
        forbidden_patterns = [
            "_get_preferred_integration",  # Old delegation method (removed Week 4)
            "GitHubAgent",  # Legacy integration (removed Week 4)
            "_warn_deprecation_if_needed",  # Deprecation warnings (no longer needed)
        ]

        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)

        present_forbidden = []
        for pattern in forbidden_patterns:
            if pattern in content:
                present_forbidden.append(pattern)

        errors = []
        architecture_type = (
            "ADR-013 Phase 2 (MCP+Spatial)" if is_mcp_phase2 else "Week 4 (Spatial-only)"
        )

        if missing_patterns:
            errors.append(f"Missing required patterns for {architecture_type}: {missing_patterns}")
        if present_forbidden:
            errors.append(f"Legacy patterns still present (should be removed): {present_forbidden}")

        if errors:
            pytest.fail(f"Router architectural integrity violated. {' | '.join(errors)}")

    def test_critical_methods_preserved(self):
        """
        CRITICAL: Verify all critical GitHub methods remain available in router.

        These 5 methods were verified in Phase 3A and must remain available
        to prevent service functionality regression.
        """

        try:
            # Import with minimal environment impact
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )
        except ImportError as e:
            pytest.fail(f"Cannot import GitHubIntegrationRouter: {e}")

        # Critical methods that services depend on
        critical_methods = [
            "get_open_issues",  # Used by domain service & PM manager
            "get_recent_issues",  # Used by domain service
            "get_recent_activity",  # Used by standup orchestration
            "list_repositories",  # Used by domain service
        ]

        missing_methods = []
        try:
            router = GitHubIntegrationRouter()
            for method_name in critical_methods:
                if not hasattr(router, method_name):
                    missing_methods.append(method_name)
        except Exception as e:
            pytest.fail(f"Router initialization failed: {e}")

        if missing_methods:
            pytest.fail(f"Critical methods missing from router: {missing_methods}")

    def test_feature_flag_integration_preserved(self):
        """
        CRITICAL: Verify feature flag system integration remains functional.

        The router must continue to respect USE_SPATIAL_GITHUB and other
        feature flags to maintain spatial intelligence capabilities.
        """

        try:
            from services.infrastructure.config.feature_flags import FeatureFlags
        except ImportError as e:
            pytest.fail(f"Cannot import FeatureFlags: {e}")

        # Critical feature flag methods
        required_flag_methods = [
            "should_use_spatial_github",
            "is_legacy_github_allowed",
            "should_warn_github_deprecation",
        ]

        missing_flag_methods = []
        for method_name in required_flag_methods:
            if not hasattr(FeatureFlags, method_name):
                missing_flag_methods.append(method_name)

        if missing_flag_methods:
            pytest.fail(f"Feature flag methods missing: {missing_flag_methods}")

    def _format_violation_message(self, violations: List[str]) -> str:
        """Format architectural violation message for clarity"""
        return "\n".join(
            [
                "🚨 ARCHITECTURAL VIOLATION: Direct GitHubAgent imports found!",
                "",
                "The router architecture has been bypassed. Services must use",
                "GitHubIntegrationRouter to maintain feature flag control and",
                "spatial intelligence capabilities.",
                "",
                "Violations found:",
            ]
            + [f"  ❌ {v}" for v in violations]
            + [
                "",
                "🔧 How to fix:",
                "  Replace:",
                "  With:",
                "    from services.integrations.github.github_integration_router import GitHubIntegrationRouter",
                "",
                "📖 See: archive/docs-architecture-2025/github-integration-router.md",
                "🐛 Issue: GitHub #193 - CORE-GREAT-2",
            ]
        )

    def _format_router_missing_message(self, missing: List[str]) -> str:
        """Format missing router usage message for clarity"""
        return "\n".join(
            [
                "🚨 ARCHITECTURAL VIOLATION: Services not using GitHubIntegrationRouter!",
                "",
                "These services were converted in Phase 2A and must use the router",
                "to ensure feature flag control and spatial intelligence work correctly.",
                "",
                "Missing router usage:",
            ]
            + [f"  ❌ {m}" for m in missing]
            + [
                "",
                "🔧 Services must import and use GitHubIntegrationRouter instead of GitHubAgent",
                "📖 See: archive/docs-architecture-2025/github-integration-router.md",
                "🐛 Issue: GitHub #193 - CORE-GREAT-2",
            ]
        )

    def _is_mcp_migration_phase2(self, content: str) -> bool:
        """
        Check if router is in ADR-013 Phase 2 migration.

        Phase 2 indicators:
        - Has MCP spatial adapter (GitHubMCPSpatialAdapter, mcp_adapter)
        - Has lazy initialization pattern (self._initialized, initialize())
        - Adapter methods that delegate directly to MCP
        """
        mcp_indicators = [
            "MCPSpatialAdapter",
            "self.mcp_adapter",
            "self._initialized",
            "async def initialize(",
        ]

        return any(indicator in content for indicator in mcp_indicators)


class TestArchitecturalRegression:
    """
    Additional regression tests to catch common architectural violations.

    These tests catch subtle ways the architecture could be compromised
    beyond direct import violations.
    """

    def test_no_github_agent_instantiation(self):
        """
        Detect GitHubAgent() instantiation even without direct imports.

        Catches cases where GitHubAgent might be imported indirectly
        and then instantiated, bypassing the router.
        """

        service_files = glob.glob("services/**/*.py", recursive=True)

        # Files allowed to instantiate GitHubAgent
        allowed_files = [
            "services/integrations/github/github_agent.py",
            "services/integrations/github/github_integration_router.py",
        ]

        violations = []

        for file_path in service_files:
            if file_path.startswith("tests/") or "__pycache__" in file_path:
                continue

            if any(allowed in file_path for allowed in allowed_files):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            # Look for GitHubAgent instantiation patterns
            instantiation_patterns = [
                "GitHubAgent()",
                "github_agent = GitHubAgent",
                "= GitHubAgent(",
            ]

            for pattern in instantiation_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: GitHubAgent instantiation found - '{pattern}'")

        if violations:
            pytest.fail(
                f"GitHubAgent instantiation found (should use GitHubIntegrationRouter): {violations}"
            )

    def test_router_delegation_pattern_preserved(self):
        """
        Verify router maintains proper delegation pattern.

        UPDATED (Sprint A4): Supports two patterns:
        - Week 4 pattern: _get_integration() for spatial-only delegation
        - ADR-013 Phase 2: Adapter methods that delegate to mcp_adapter

        ADR-013 Phase 2 Migration Pattern:
        - Router has adapter methods (get_recent_issues, get_issue, etc.)
        - Methods delegate directly to self.mcp_adapter or self.spatial_github
        - Uses lazy initialization (await self.initialize())
        - Backward-compatible interface with MCP+Spatial implementation
        """

        router_file = "services/integrations/github/github_integration_router.py"

        with open(router_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if router is in ADR-013 Phase 2 migration
        is_mcp_phase2 = self._is_mcp_migration_phase2(content)

        # Count methods that should follow delegation pattern
        import re

        method_matches = re.findall(
            r"def (get_\w+|create_\w+|list_\w+|parse_\w+|test_\w+)\(", content
        )

        # Exclude router-specific methods and module-level functions
        excluded_methods = [
            "get_integration_status",  # Special status method
            "get_deprecation_week",  # Timeline helper
            "create_github_integration",  # Factory function
            "get_integration",  # Internal delegation method itself
            "get_boolean_flag",  # Helper method
            "get_authentication_token",  # Config method
        ]
        delegation_methods = [m for m in method_matches if m not in excluded_methods]

        pattern_violations = []
        for method in delegation_methods:
            # #1115 fix: terminate at next def-keyword (not substring match
            # inside identifiers like `_resolve_default_repo`). Use word
            # boundary + match the indentation pattern Python methods follow.
            method_pattern = (
                rf"def {re.escape(method)}\([^)]*\).*?" rf"(?=\n    (?:async )?def\b|\n\nclass |\Z)"
            )
            method_match = re.search(method_pattern, content, re.DOTALL)

            if method_match:
                method_body = method_match.group(0)

                if is_mcp_phase2:
                    # ADR-013 Phase 2: Allow adapter methods OR _get_integration pattern
                    has_adapter_delegation = (
                        "self.mcp_adapter" in method_body or "self.spatial_github" in method_body
                    )
                    has_get_integration = "_get_integration(" in method_body

                    if not (has_adapter_delegation or has_get_integration):
                        pattern_violations.append(
                            f"Method {method} missing delegation (Phase 2 requires: "
                            "self.mcp_adapter/self.spatial_github OR _get_integration)"
                        )
                else:
                    # Week 4 pattern: Requires _get_integration() call
                    if "_get_integration(" not in method_body:
                        pattern_violations.append(
                            f"Method {method} missing _get_integration() call (Week 4 pattern)"
                        )

                # Forbid old complex routing patterns (both patterns)
                forbidden_patterns = [
                    "_get_preferred_integration(",  # Old pattern
                    "_warn_deprecation_if_needed(",  # No longer needed
                ]
                for forbidden in forbidden_patterns:
                    if forbidden in method_body:
                        pattern_violations.append(
                            f"Method {method} contains legacy pattern: {forbidden}"
                        )

        if pattern_violations:
            pytest.fail(f"Router delegation pattern violations: {pattern_violations}")

    def _is_mcp_migration_phase2(self, content: str) -> bool:
        """
        Check if router is in ADR-013 Phase 2 migration.

        Phase 2 indicators:
        - Has MCP spatial adapter (GitHubMCPSpatialAdapter, mcp_adapter)
        - Has lazy initialization pattern (self._initialized, initialize())
        - Adapter methods that delegate directly to MCP
        """
        mcp_indicators = [
            "MCPSpatialAdapter",
            "self.mcp_adapter",
            "self._initialized",
            "async def initialize(",
        ]

        return any(indicator in content for indicator in mcp_indicators)


class TestPreFloorDispatchSiteRatchet:
    """#1124 Phase 4 — architectural enforcement for the pre-floor-handler migration.

    `intent_service.py` historically routed actions through hand-coded
    `if/elif intent.action in [...]` chains that bypass the workflow-dispatcher
    rail (ADR-059). #1124 is migrating these onto the rail one cohort at a time.

    This test is a RATCHET: it counts the remaining hand-coded action-dispatch
    sites and fails if the count GROWS. When a migration lands, lower
    ``MAX_DISPATCH_SITES`` to the new count in the same commit (never raise it). A
    new handler must be added as a workflow-dispatcher entry
    (``workflow_entries.py`` + ``action_triggered=True``), not a new
    ``elif intent.action`` branch.

    Counts both ``if`` and ``elif``: a new handler can regress the architecture by
    extending a chain (``elif``) OR opening a fresh chain (``if intent.action``);
    an elif-only count would miss the latter.
    """

    # Ratchet target — hand-coded action-dispatch sites remaining in
    # intent_service.py. LOWER as #1124 migrations land; NEVER raise.
    # 2026-06-10: 0 — every `if/elif intent.action in [...]` dispatch site in
    # intent_service.py is migrated onto the action-dispatch rail (#1124 fully done).
    # The final 3 (analyze_document, strategic_planning, learn_pattern category
    # if-heads) landed this pass. Trajectory: 28 (audit baseline 2026-05-25) → 15
    # (cohort-1) → 12 (analysis) → 10 (synthesis) → 3 (QUERY cohort) → 0. The ratchet
    # now blocks ANY new hand-coded action-dispatch branch — all handlers register a
    # workflow-dispatcher entry instead.
    MAX_DISPATCH_SITES = 0

    DISPATCH_RE = re.compile(r"^[ \t]*(?:if|elif) intent\.action in \[", re.MULTILINE)

    def _count_dispatch_sites(self) -> int:
        with open("services/intent/intent_service.py", encoding="utf-8") as fh:
            content = fh.read()
        return len(self.DISPATCH_RE.findall(content))

    def test_no_new_pre_floor_dispatch_sites(self):
        """Fails if a new hand-coded `if/elif intent.action in [...]` site is added.

        New action handlers MUST register a workflow-dispatcher entry instead
        (services/intent_service/workflow_entries.py). If you just migrated a
        handler onto the rail, LOWER MAX_DISPATCH_SITES to the new count here.
        """
        count = self._count_dispatch_sites()
        assert count <= self.MAX_DISPATCH_SITES, (
            f"intent_service.py has {count} hand-coded `if/elif intent.action in [...]` "
            f"dispatch sites, exceeding the #1124 ratchet target of "
            f"{self.MAX_DISPATCH_SITES}. New action handlers must use the "
            f"workflow-dispatcher rail (workflow_entries.py + action_triggered=True), "
            f"not a new elif branch. The #1124 direction is DOWN."
        )

    def test_ratchet_target_stays_tight(self):
        """The target must equal the actual count, not sit loosely above it — a loose
        target silently permits regressions up to the slack. When a migration lowers
        the real count, lower MAX_DISPATCH_SITES to match in the same commit."""
        count = self._count_dispatch_sites()
        assert count == self.MAX_DISPATCH_SITES, (
            f"Ratchet drift: actual dispatch-site count is {count} but "
            f"MAX_DISPATCH_SITES is {self.MAX_DISPATCH_SITES}. If a migration just "
            f"lowered the count, set MAX_DISPATCH_SITES = {count} in this commit so "
            f"the ratchet stays tight (no silent regression slack)."
        )


class TestSessionScopeCommitContract:
    """#1193 guard (m-41): `session_scope()` MUST commit on clean exit.

    The docstring always promised "automatic commit"; the implementation didn't
    commit, so writes through it were flushed then silently discarded on close.
    That silent-write-loss trap bit twice independently (#1079 standup, #1143
    composting — plus user corrections via web/api/routes/insights.py) before a
    133-call-site audit (2026-06-12) confirmed zero callers depend on no-commit
    semantics and the behavior was conformed to the spec (Arch-ratified Option A,
    Pattern-073). This guard fails the build if the commit is ever removed —
    without it, the next "cleanup" resurrects the trap invisibly.
    """

    _FACTORY = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "services",
        "database",
        "session_factory.py",
    )

    def _session_scope_source(self) -> str:
        import ast

        with open(self._FACTORY) as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "session_scope":
                lines = source.splitlines()
                return "\n".join(lines[node.lineno - 1 : node.end_lineno])
        raise AssertionError("session_scope() not found in session_factory.py")

    def test_session_scope_commits_on_clean_exit(self):
        src = self._session_scope_source()
        yield_idx = src.find("yield session")
        commit_idx = src.find("await session.commit()")
        assert yield_idx != -1, "session_scope() no longer yields a session?"
        assert commit_idx != -1, (
            "#1193 REGRESSION: session_scope() no longer commits on clean exit. "
            "Its docstring contract promises automatic commit; removing the commit "
            "resurrects the silent-write-loss trap (writes flushed then discarded "
            "on close — see #1079, #1143, #1193). Restore `await session.commit()` "
            "after the yield, or coordinate an Arch-level contract change."
        )
        assert commit_idx > yield_idx, (
            "session_scope() must commit AFTER the yield (on the caller's clean "
            "exit), not before it."
        )

    def test_session_scope_docstring_states_contract(self):
        src = self._session_scope_source()
        docstring = src.split('"""')[1] if '"""' in src else ""
        assert "commit" in docstring.lower(), (
            "session_scope()'s docstring must state the commit contract — the "
            "doc/behavior drift is how #1193 happened."
        )


class TestModelMigrationCoverage:
    """#1267 / ADR-071 D5 extension (m-41): every ORM model table MUST have an
    ``op.create_table`` migration.

    ``project_integrations`` had only ALTER migrations (``4d1e2c3b5f7a`` owner_id,
    ``d73b3722eb03`` timestamptz) and NO create migration. Both alters are
    IF-EXISTS-defensive, so a fresh ``alembic upgrade head`` ran clean, SILENTLY
    skipped the never-created table, and the Projects API 500'd on the missing
    relation (#1267). That silent-skip is why the gap is invisible at upgrade time.

    A STRUCTURAL guard (not a runtime ``upgrade head`` test) is the durable catch:
    a dev/test DB that already has the table via ``Base.metadata.create_all()`` (the
    test-only path) would FALSE-PASS a runtime check while a true fresh-alembic DB
    stays broken. The structural check can't be fooled by a polluted DB.

    Ratchet-with-baseline: ``KNOWN_UNMIGRATED`` holds pre-existing create_all-era
    model tables that still lack a create migration. LOWER it as those migrations
    land; NEVER add to it — a new model table ships with its create migration.
    #1267 removes ``project_integrations`` from the uncovered set.
    """

    # create_all-era gaps still lacking a create migration. #1267 fixed
    # project_integrations (a1267projintegrations); #1273 (a1273coretables) backfilled
    # intents/stakeholders/tasks/workflows → the set is now EMPTY: every ORM model
    # table has a create migration. Do NOT add to this set — a new model table must
    # ship with its create migration. It only shrinks.
    KNOWN_UNMIGRATED = frozenset()

    _CREATE_TABLE_RE = re.compile(r"""create_table\(\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']""")
    _TABLENAME_RE = re.compile(r"""__tablename__\s*=\s*["']([a-zA-Z_][a-zA-Z0-9_]*)["']""")

    def _repo_root(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _migrated_tables(self) -> set:
        tables: set = set()
        for path in glob.glob(os.path.join(self._repo_root(), "alembic", "versions", "*.py")):
            with open(path, encoding="utf-8") as fh:
                tables.update(self._CREATE_TABLE_RE.findall(fh.read()))
        return tables

    def _model_tables(self) -> set:
        tables: set = set()
        pattern = os.path.join(self._repo_root(), "services", "**", "*.py")
        for path in glob.glob(pattern, recursive=True):
            with open(path, encoding="utf-8") as fh:
                tables.update(self._TABLENAME_RE.findall(fh.read()))
        return tables

    def test_project_integrations_has_create_migration(self):
        """#1267 regression: the table whose absence 500'd the Projects API on
        every pure-alembic DB. Fails until a create_table migration exists."""
        assert "project_integrations" in self._migrated_tables(), (
            "project_integrations has no `op.create_table` migration. Its only "
            "migrations are IF-EXISTS-defensive ALTERs, so a fresh "
            "`alembic upgrade head` silently skips it → table absent → Projects API "
            "500 (#1267). Add an idempotent create_table head migration."
        )

    def test_no_unmigrated_model_tables_beyond_baseline(self):
        """Every ORM model ``__tablename__`` has a create migration, except the
        documented create_all-era baseline. A NEW model table without a create
        migration — or project_integrations before its fix — fails here."""
        uncovered = self._model_tables() - self._migrated_tables() - self.KNOWN_UNMIGRATED
        assert not uncovered, (
            f"ORM model tables with no `op.create_table` migration: {sorted(uncovered)}. "
            f"A model table must ship with its create migration (a fresh "
            f"`alembic upgrade head` won't create it otherwise — #1267). Add the "
            f"migration; do NOT add the table to KNOWN_UNMIGRATED."
        )

    def test_baseline_stays_tight(self):
        """KNOWN_UNMIGRATED must not list a table that already HAS a create
        migration — a stale baseline hides the next regression. It only shrinks."""
        stale = self.KNOWN_UNMIGRATED & self._migrated_tables()
        assert not stale, (
            f"KNOWN_UNMIGRATED lists tables that now HAVE a create migration: "
            f"{sorted(stale)}. Remove them from the baseline (it only shrinks)."
        )


class TestGitHubDefaultRepoScopingEnforcement:
    """#1366 Component A — architectural enforcement for the default-repo scoping fix.

    ``piper_config_loader.load_github_config()`` reads ONE file at server-instance
    level with zero user-scoping. Its ``.default_repository``/``.owner`` fields are
    safe only in a single-user prototype; on a shared instance (alpha.pipermorgan.ai
    is one today) they would hand every user PM's own default GitHub repo. The
    per-user, DB-backed source of truth is ``get_user_default_repo(user_id)``
    (services/integrations/github/repo_resolver.py), which reads
    ``ConnectorConfigService`` (ADR-070 D4).

    Scope, per Arch's ratification note (memo 2026-07-06,
    "1366-componentA-proceed-plus-lint-scoping"): this targets ONLY the repo-fields
    (``default_repository``/``owner``) read via the ``github_config`` variable that
    ``load_github_config()`` conventionally gets assigned to — NOT every
    ``load_github_config()`` call (``pm_prefix``/``pm_start``/``pm_padding``/
    ``default_labels``/``api_base`` are a different, legitimately-still-file-backed
    concern) and NOT ``load_pm_identity_config()``/``resolve_pm_owner_id()``
    (#1260's Component-C PM-identity path — a structurally separate method, a
    different field, a non-per-user CLI-ingestion path, legitimate until Component
    B lands per ADR-071-D1's PM-owner distinction).

    Same family as the #1283 reachability lint and the #1307 exempt-list lint:
    impossible-by-construction, not vigilance. Zero tolerance, not a ratchet —
    there is no legitimate reason for any file to read the repo-fields off the
    unscoped loader, so unlike TestPreFloorDispatchSiteRatchet this has no
    declining-target track; the allowed count is always 0.
    """

    # Files structurally exempt because they ARE the loader/type definition, not
    # callers — reading/assigning the field here is the implementation, not a leak.
    ALLOWED_FILES = [
        "services/configuration/piper_config_loader.py",  # loader builds the value
        "services/config/github_config.py",  # GitHubConfig dataclass itself
    ]

    UNSCOPED_READ_RE = re.compile(r"\bgithub_config\.(default_repository|owner)\b")

    def test_no_unscoped_default_repository_reads(self):
        """Fails if any caller reads `.default_repository`/`.owner` off a config
        object sourced from the unscoped `load_github_config()` loader.

        Fix: repoint onto `get_user_default_repo(user_id)`
        (services/integrations/github/repo_resolver.py) — see
        services/intent_service/canonical_handlers.py and
        services/intent/intent_service.py for the #1366 reference fix.
        """
        service_files = glob.glob("services/**/*.py", recursive=True) + glob.glob(
            "web/**/*.py", recursive=True
        )

        violations = []

        # Vacuity guard (Arch checker 2026-08-04): this scan DERIVES its input;
        # an empty derivation must fail loudly, never pass as "no violations".
        assert (
            len(service_files) >= 100
        ), f"unscoped-read scan found only {len(service_files)} files — detection broken"
        for file_path in service_files:
            if "__pycache__" in file_path:
                continue
            if any(allowed in file_path for allowed in self.ALLOWED_FILES):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            if self.UNSCOPED_READ_RE.search(content):
                violations.append(file_path)

        assert not violations, (
            f"Unscoped `.default_repository`/`.owner` read(s) found in: "
            f"{violations}. On a shared instance this leaks PM's own default "
            f"GitHub repo to every user (#1366). Use "
            f"`get_user_default_repo(user_id)` "
            f"(services/integrations/github/repo_resolver.py) instead of "
            f"`piper_config_loader.load_github_config().default_repository`."
        )


class TestPersonalizationScopingEnforcement:
    """ADR-075 D5 — architectural enforcement for the Component B personalization fix.

    ``piper_config_loader.get_system_prompt()`` reads ONE file at server-instance
    level with zero user-scoping. Category-1 personalization (ADR-075 D1: name/
    role/timezone/style/focus/portfolio/standing-priorities) must resolve through
    ``PersonalizationService`` (owner_id-scoped, D2/D4) — never call the raw
    loader directly on a request path, or every user gets PM's own context
    (the #1366 leak this component closes).

    Same family as #1283 (reachability) / #1307 (exempt-list) / Component A's
    ``TestGitHubDefaultRepoScopingEnforcement``: impossible-by-construction, not
    vigilance. Zero tolerance — there is no legitimate reason for a request-path
    file to call the raw loader for the system prompt.
    """

    # Files structurally exempt because they ARE the loader, or the ONE
    # sanctioned caller of it (PersonalizationService's own D3/PM-fallback
    # path — the whole point of the service is to be the single seam between
    # "unscoped file" and "scoped per-user"), or a CLI/batch tool that is NOT
    # a request path (same category ADR-075 D6 already rules for Component C's
    # #1260 CLI-ingestion path — DocumentIngester has no web/request caller,
    # confirmed by direct search, only scripts/validate_322_multiworker.py).
    ALLOWED_FILES = [
        "services/configuration/piper_config_loader.py",
        "services/configuration/personalization_service.py",
        "services/knowledge_graph/ingestion.py",
    ]

    UNSCOPED_READ_RE = re.compile(r"\bpiper_config_loader\.get_system_prompt\(\)")

    def test_no_unscoped_system_prompt_reads(self):
        """Fails if any caller invokes `piper_config_loader.get_system_prompt()`
        directly instead of resolving through `PersonalizationService`.

        Fix: repoint onto `personalization_service.resolve_system_prompt(user_id,
        session)` (or `resolve_system_prompt_standalone(user_id)` if no session is
        already in scope) — see services/intent_service/conversational_floor.py,
        services/intent_service/classifier.py for the #1366/ADR-075 Component B
        reference fix (llm_classifier.py deleted 2026-08-02, #1432).
        """
        service_files = glob.glob("services/**/*.py", recursive=True) + glob.glob(
            "web/**/*.py", recursive=True
        )

        violations = []

        # Vacuity guard (Arch checker 2026-08-04): this scan DERIVES its input;
        # an empty derivation must fail loudly, never pass as "no violations".
        assert (
            len(service_files) >= 100
        ), f"unscoped-read scan found only {len(service_files)} files — detection broken"
        for file_path in service_files:
            if "__pycache__" in file_path:
                continue
            if any(allowed in file_path for allowed in self.ALLOWED_FILES):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            if self.UNSCOPED_READ_RE.search(content):
                violations.append(file_path)

        assert not violations, (
            f"Unscoped `piper_config_loader.get_system_prompt()` call(s) found in: "
            f"{violations}. On a shared instance this leaks PM's own personalization "
            f"context to every user (#1366/ADR-075). Use "
            f"`personalization_service.resolve_system_prompt(user_id, session)` "
            f"instead."
        )


if __name__ == "__main__":
    # Allow running tests directly for verification
    pytest.main([__file__, "-v"])


class TestUploadedFileByteSeamEnforcement:
    """#1306 (Arch-ratified condition): uploaded-file bytes are touched ONLY via
    the storage seam (write_file_to_storage / read_file_from_storage in
    services/file_context/storage.py). This guard makes the un-routed access
    hard to express: any file that works with uploaded-file storage paths AND
    does raw byte IO fails the build. The 2026-07-08 inventory routed 7 sites
    (3 in document_handlers, 1 in document_analyzer, 3 in files.py — including
    the upload route's bypass write the design memo missed); this keeps the
    seam count at exactly one in each direction.
    """

    ALLOWED_FILES = [
        "services/file_context/storage.py",  # THE seam
        "scripts/backfill_encrypt_files_1306.py",  # converts legacy files, raw by design
    ]

    _RAW_BYTE_IO = re.compile(r"\.read_bytes\(\)|open\([^)\n]*,\s*[\"'][rwa]b[\"']")
    _UPLOAD_TOKENS = re.compile(r"storage_path|[\"']uploads[\"']|Path\([\"']uploads[\"']\)")

    def _scan(self):
        offenders = []
        for root in ("services", "web"):
            for path in glob.glob(os.path.join(root, "**", "*.py"), recursive=True):
                rel = path.replace(os.sep, "/")
                if rel in self.ALLOWED_FILES:
                    continue
                with open(path, encoding="utf-8", errors="ignore") as f:
                    src = f.read()
                if self._UPLOAD_TOKENS.search(src) and self._RAW_BYTE_IO.search(src):
                    hits = [
                        f"{rel}:{i}"
                        for i, line in enumerate(src.splitlines(), 1)
                        if self._RAW_BYTE_IO.search(line)
                    ]
                    offenders.append((rel, hits))
        return offenders

    def test_no_raw_byte_io_outside_the_storage_seam(self):
        offenders = self._scan()
        assert not offenders, (
            "#1306 SEAM VIOLATION: uploaded-file bytes must flow through "
            "read_file_from_storage/write_file_to_storage (services/file_context/"
            "storage.py) — a raw byte read/write in a storage-path-handling file "
            "bypasses encrypt-at-rest (writes plaintext or reads ciphertext as "
            f"content). Offenders: {offenders}. Route through the seam, or if a "
            "file's byte IO is genuinely unrelated to uploaded files, refactor so "
            "the guard's upload-token heuristic no longer matches (or justify an "
            "ALLOWED_FILES entry in review)."
        )


# ============================================================================
# #1433 — CHAT_POINTERS product-surface reachability ratchet
# (Arch-ratified design 2026-08-02:
#  docs/internal/architecture/current/chat-pointers-reachability-ratchet-design-1433.md)
#
# The #1283/ADR-077 lint checks registry-OUTWARD (every registry canonical is
# dispatchable). NOTHING checked product-INWARD — which is how integrations-
# connect ×4, file-upload, api-keys, lists and work-items could all be
# chat-unreachable (or falsely denied, #1426) without any test noticing
# (census D, 2026-07-16). This ratchet closes that half:
#
#   1. The must-be-covered surface set is DERIVED at collection time (pages
#      from ui.py, connectable integrations from settings_integrations.py,
#      capabilities named in decline copy). A new surface with no ledger row
#      FAILS the build — membership by existing (ADR-072/ADR-079 precedent).
#   2. Every POINTER utterance must resolve DETERMINISTICALLY — the harness
#      runs the real pre-classifier + rail/registry/action-mapper resolution
#      with NO LLM call and NO network, and asserts BOTH the destination AND
#      the RESOLUTION PATH (Arch's required addition: "routed deterministically"
#      and "routed somehow" must never produce identical output — the m-44
#      guard applied to the check itself). Keyless in gating CI by construction.
#      Immune to the #1395/Q22 oscillation class: borderline LLM classification
#      is sampled; static pre-classifier + action-mapping resolution is
#      deterministic by construction (which is what the no-LLM constraint buys).
#   3. CHAT_INVISIBLE entries carry a STRUCTURED citation (issue=N or
#      ref="ADR-/PDR-..."), enforced below — free-text reason = fail. The set
#      may only SHRINK (count ceiling in scripts/ratchet_ceilings.json).
#   4. Decline-copy freshness (#1426 structural half): UNWIRED_WRITE_DECLINES
#      keys and _get_contextual_fallback's denial rows must stay disjoint from
#      the reachable-action set — shipping a capability forces its stale
#      denial out of the build in the same commit.
#
# SINGLE SOURCE (#1428, design §6 step 3): the ledger itself (POINTER,
# CHAT_INVISIBLE, UNTRACKED_BASELINE, CHAT_POINTERS) lives in
# services/intent_service/chat_pointers.py, imported here AND by the product's
# "what can you do?" answer path (context_assembler._gather_identity_context
# via capability_answer_lines). This class still gates the ledger identically;
# a POINTER row is simultaneously a verified-reachable claim (enforced here)
# and a user-facing capability offer (surfaced there) — so the answer can
# never claim what the ratchet hasn't verified, and a new capability joins
# the answer by getting a ledger row.
# ============================================================================

from services.intent_service.chat_pointers import (  # noqa: E402
    CHAT_INVISIBLE,
    CHAT_POINTERS,
    POINTER,
    UNTRACKED_BASELINE,
)

# _get_contextual_fallback denial rows — the curated bridge between the
# denial STRINGS in services/intent/intent_service.py and the capability
# ACTION tokens whose shipping would make each denial stale. Two-directionally
# enforced below: a NEW "I can't ..." denial in the function without a row
# here fails; a row whose snippet no longer appears in the source fails
# (capability shipped → remove the row + its ledger surface in the same
# commit).
CONTEXTUAL_FALLBACK_DENIALS = {
    "capability:create_calendar_event": {
        "snippet": "can't create calendar events",
        "actions": {"create_calendar_event", "schedule_meeting", "create_meeting", "book_meeting"},
    },
    "capability:create_document": {
        "snippet": "can't create documents",
        "actions": {"create_document", "create_doc", "make_document"},
    },
    "capability:batch_create_issues": {
        "snippet": "can't batch-create issues",
        "actions": {"batch_create_issues", "create_issues_from_meeting", "batch_create"},
    },
    "capability:post_to_slack": {
        "snippet": "can't post to Slack channels",
        "actions": {"post_to_slack", "send_slack_message", "post_to_channel"},
    },
}


@pytest.mark.smoke
class TestChatPointersReachabilityRatchet:
    """#1433 — the product-inward reachability ratchet (see block comment above)."""

    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _UI_PY = os.path.join(_ROOT, "web", "api", "routes", "ui.py")
    _SETTINGS_INTEGRATIONS_PY = os.path.join(
        _ROOT, "web", "api", "routes", "settings_integrations.py"
    )
    _INTENT_SERVICE_PY = os.path.join(_ROOT, "services", "intent", "intent_service.py")
    _CEILINGS_JSON = os.path.join(_ROOT, "scripts", "ratchet_ceilings.json")

    # ---- derived enumeration (membership by existing) ----

    def _page_paths(self) -> set:
        """Every ui.py page route path, from the @router.get decorators (AST —
        idiom-change makes this fail LOUDLY, the safe direction). API routes
        (/api/...) are not pages and are excluded."""
        import ast

        with open(self._UI_PY, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        paths = set()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if (
                    isinstance(dec, ast.Call)
                    and isinstance(dec.func, ast.Attribute)
                    and dec.func.attr == "get"
                    and isinstance(dec.func.value, ast.Name)
                    and dec.func.value.id == "router"
                    and dec.args
                    and isinstance(dec.args[0], ast.Constant)
                    and isinstance(dec.args[0].value, str)
                    and not dec.args[0].value.startswith("/api/")
                ):
                    paths.add(dec.args[0].value)
        return paths

    def _connectable_integrations(self) -> set:
        """The connectable-integration set, derived from settings_integrations'
        route surface: a provider is connectable iff it has a /{name}/connect
        (OAuth) or /{name}/save (API-key) route."""
        with open(self._SETTINGS_INTEGRATIONS_PY, encoding="utf-8") as fh:
            src = fh.read()
        connect = set(re.findall(r'@router\.get\("/([a-z_]+)/connect"\)', src))
        save = set(re.findall(r'@router\.post\("/([a-z_]+)/save"\)', src))
        return connect | save

    def _fallback_denial_fragments(self) -> list:
        """Every STRING CONSTANT inside _get_contextual_fallback that denies a
        capability (contains \"can't\"). AST-derived so comments (which quote
        the #1426 pre-fix denials as history) never count; affirmative
        redirects (\"I can set reminders\", \"You can upload files\")
        deliberately don't match."""
        import ast

        with open(self._INTENT_SERVICE_PY, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "_get_contextual_fallback":
                return [
                    const.value
                    for const in ast.walk(node)
                    if isinstance(const, ast.Constant)
                    and isinstance(const.value, str)
                    and "can't" in const.value
                ]
        raise AssertionError(
            "_get_contextual_fallback not found in intent_service.py — the "
            "extraction idiom changed; fix _fallback_denial_fragments()."
        )

    def _derived_surfaces(self) -> set:
        from services.intent_service.unwired_writes import UNWIRED_WRITE_DECLINES

        surfaces = {f"page:{p}" for p in self._page_paths()}
        surfaces |= {f"integration:{i}" for i in self._connectable_integrations()}
        surfaces |= {f"capability:{a}" for a in UNWIRED_WRITE_DECLINES}
        surfaces |= set(CONTEXTUAL_FALLBACK_DENIALS)
        return surfaces

    # ---- static resolution harness (NO LLM, NO network) ----

    def _rail(self) -> set:
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        return set(get_action_workflows().keys())

    def _elif_tokens(self) -> set:
        """The EXECUTION elif-dispatched tokens (same derivation as
        TestForwardGuardExecutionCohort in test_routing_vocabulary_1283)."""
        with open(self._INTENT_SERVICE_PY, encoding="utf-8") as fh:
            src = fh.read()
        eq = set(re.findall(r'mapped_action\s*==\s*"([a-z_]+)"', src))
        for group in re.findall(r"mapped_action\s+in\s+\[([^\]]+)\]", src):
            eq |= set(re.findall(r'"([a-z_]+)"', group))
        return eq

    # The deterministic resolver set (Arch's required addition). Stage 1 is
    # ALWAYS the pre-classifier (a POINTER whose utterance needs the LLM
    # classifier fails at authoring time); stage 2 is the deterministic
    # dispatch surface for the emitted action:
    #   rail-key            — process_intent's action rail (dict lookup)
    #   registry-CANONICAL  — CanonicalHandlers fast path
    #   registry-FLOOR      — deliberate floor routing with context assembly
    #   action-mapper-elif  — the EXECUTION cohort (ActionMapper dict + elif;
    #                         the forward-guard D4-bridge, Arch 2026-07-16 §A)
    DETERMINISTIC_RESOLVERS = frozenset(
        {
            "pre-classifier→rail-key",
            "pre-classifier→registry-CANONICAL",
            "pre-classifier→registry-FLOOR",
            "pre-classifier→action-mapper-elif",
            # #1595 Phase 3 (2026-09-27): a pattern list's literals were
            # deleted under the reviewed, gated deletion ratchet — the
            # resolution moved from a regex to the ledger's re-verified
            # evidence (real corpus row + real router-report verdict,
            # re-checked every run). Still zero LLM calls at resolve time.
            "phase3-deletion-ledger",
        }
    )

    def _static_resolve(self, utterance: str) -> tuple:
        """Resolve `utterance` through the static routing surfaces only.

        Returns (destination, resolver) where destination is the
        (category, action) the deterministic chain emits (None if the
        utterance would need the LLM classifier) and resolver names the
        resolution path — recorded so a failure message shows WHICH surface
        resolved (or failed to resolve) the pointer.
        """
        from services.intent_service.action_registry import (
            ACTION_REGISTRY,
            ActionDisposition,
        )
        from services.intent_service.pre_classifier import PreClassifier

        intent = PreClassifier.pre_classify(utterance)
        if intent is None:
            ledger_destination = self._phase3_ledger_resolve(utterance)
            if ledger_destination is not None:
                return ledger_destination, "phase3-deletion-ledger"
            return None, "LLM-classifier-required (pre-classifier returned None)"

        category = intent.category.value
        action = intent.action
        destination = (category, action)

        if action in self._rail():
            return destination, "pre-classifier→rail-key"

        disposition = ACTION_REGISTRY.get((category.upper(), action))
        if disposition is ActionDisposition.CANONICAL:
            return destination, "pre-classifier→registry-CANONICAL"
        if disposition is ActionDisposition.FLOOR:
            return destination, "pre-classifier→registry-FLOOR"

        if category == "execution":
            from services.intent_service.action_mapper import ActionMapper

            if ActionMapper.map_action(action) in self._elif_tokens():
                return destination, "pre-classifier→action-mapper-elif"

        return destination, (
            f"UNDISPATCHED (pre-classifier emitted {destination} but it is not "
            f"a rail key, its registry disposition is {disposition}, and it is "
            f"not action-mapper-elif dispatched)"
        )

    def _phase3_ledger_resolve(self, utterance: str):
        """#1595 Phase 3 deletion ledger fallback — NO LLM call.

        A `*_PATTERNS` list deliberately deleted from the pre-classifier
        (scripts/inversion_phase3_deleted_patterns.json) no longer claims
        its rows at surface 1 BY DESIGN: the deletion gate only licenses a
        deletion when every claimed row is MATCH/agreeing-REVIEW against a
        real router report, or the row's expected action is already
        live-flag-routable (docs/internal/architecture/current/
        intent-routing-stack.md, "Phase 3 — deletion gate"). A POINTER
        whose utterance is one of a ledgered entry's verified
        ``rows_claimed_at_deletion``, re-checked against that SAME evidence
        every run via ``check_deleted_entry_non_regression`` (real corpus
        row + real router-report verdict — no LLM call here, ever), still
        resolves deterministically: the resolution path just moved from a
        regex to the reviewed, gated, re-verified ledger. Returns the
        (category, action) destination, or None if no ledgered entry
        covers this utterance (or its own non-regression check fails —
        then it is honestly unresolved, never silently claimed).
        """
        import sys

        sys.path.insert(0, os.path.join(self._ROOT, "scripts"))
        import inversion_phase0_baseline as p0
        import inversion_phase3_deletion_gate as gate

        from services.intent_service.action_registry import ACTION_REGISTRY

        category_by_action = {action: cat for (cat, action) in ACTION_REGISTRY}
        corpus_by_phrase = {r["phrase"]: r for r in p0.load_corpus()}

        for entry in gate.load_deleted_pattern_lists():
            if utterance not in entry.get("rows_claimed_at_deletion", []):
                continue
            # Per-phrase resolution (#1595 Phase 3 second deletion,
            # TODO_QUERY_PATTERNS): an entry's expected_ops may name MORE
            # than one destination once it deletes a heterogeneous list —
            # gate.expected_op_for_phrase resolves THIS utterance's own
            # target from its corpus row / the entry's expected_op_by_phrase
            # map, never "any op the entry has ever routed to". None means
            # genuinely ambiguous for this phrase — don't guess.
            action = gate.expected_op_for_phrase(entry, utterance, corpus_by_phrase.get(utterance))
            if action is None:
                continue
            category = category_by_action.get(action)
            if category is None:
                # A rail key with no registry row (show_standup, the GitHub
                # listings …) is dispatched by the live consult with the
                # grammar's category for the op, else QUERY — the same rule
                # inversion_live applies (its "QUERY is the honest value"
                # branch). Mirror it; never invent a category.
                from services.intent_service.inversion_live import _category_by_operation
                from services.intent_service.inversion_router import derive_routing_grammar
                from services.intent_service.workflow_dispatcher import get_action_workflows
                from services.intent_service.workflow_entries import register_default_workflows

                register_default_workflows()
                if action in get_action_workflows():
                    category = (
                        _category_by_operation(derive_routing_grammar()).get(action) or "QUERY"
                    )
            if category is None:
                continue
            # #1595 Phase 3 fourth deletion (2026-10-01): an entry can carry a
            # MISMATCH-but-live-route row (TEMPORAL_PATTERNS' "what is on my
            # calendar", reabsorbed from CALENDAR_QUERY_PATTERNS) that needs
            # the live-flag's routable set to pass non-regression — cats=None
            # (the "deployment unknown" strictest reading) would fail the
            # WHOLE entry non-regression check over ONE row having nothing to
            # do with THIS utterance, blocking every other phrase in the same
            # entry from resolving here too. This ratchet exists to confirm a
            # chat pointer resolves the way PRODUCTION resolves it, and
            # production's live flag does carry gate.CURRENT_LIVE_CATEGORIES
            # (dispatch-verified throughout this epic) — so that is the
            # correct set to check against, not "unknown".
            ok, _problems = gate.check_deleted_entry_non_regression(
                entry, cats=gate.CURRENT_LIVE_CATEGORIES
            )
            if not ok:
                continue
            return (category.lower(), action)
        return None

    def _reachable_actions(self) -> set:
        """The reachable-action denominator for decline-copy freshness.

        Per the ratified design §3 (Arch refinement 3, denominator named):
        this reachable set covers POINTER-resolved + registry-wired paths
        (registry actions, rail keys, pre-classifier emissions, the EXECUTION
        elif tokens and the ActionMapper variants that canonicalize onto them)
        and does NOT cover capabilities reachable by paths outside both
        (believed empty today) — carried as this comment so "complete for the
        space it searched" stays visible.
        """
        from services.intent_service.action_mapper import ActionMapper
        from services.intent_service.action_registry import ACTION_REGISTRY

        rail = self._rail()
        elif_tokens = self._elif_tokens()

        with open(
            os.path.join(self._ROOT, "services", "intent_service", "pre_classifier.py"),
            encoding="utf-8",
        ) as fh:
            pre_src = fh.read()
        pre_surface = set(re.findall(r'action="([a-z_]+)"', pre_src)) | set(
            re.findall(r'IntentCategory\.\w+,\s*"([a-z_]+)"', pre_src)
        )

        pointer_resolved = set()
        for row in CHAT_POINTERS.values():
            if isinstance(row, POINTER):
                destination, _resolver = self._static_resolve(row.utterance)
                if destination:
                    pointer_resolved.add(destination[1])

        dispatched = elif_tokens | rail
        mapper_variants = {k for k, v in ActionMapper.ACTION_MAPPING.items() if v in dispatched}
        return (
            pointer_resolved
            | {action for (_cat, action) in ACTION_REGISTRY}
            | rail
            | pre_surface
            | elif_tokens
            | mapper_variants
        )

    # ---- the tests ----

    def test_every_derived_surface_has_a_ledger_row(self):
        """Membership by existing: a new page route, connectable integration,
        or decline-copy capability joins the contract by existing — the build
        fails until it gets a ledger row (POINTER or justified CHAT_INVISIBLE).
        Both directions: a ledger row whose surface no longer exists is stale
        and must be removed (the CHAT_INVISIBLE set only shrinks)."""
        derived = self._derived_surfaces()
        ledgered = set(CHAT_POINTERS)
        # #1521: "pin:" rows are regression pins, not derived surfaces — they
        # keep a once-misrouted natural phrasing under
        # test_every_pointer_resolves_deterministically forever (the #1471
        # precedent, generalized for capabilities with no surface of their
        # own). Exempt from surface derivation ONLY; a pin must be a POINTER
        # (a CHAT_INVISIBLE pin would assert nothing).
        pins = {k for k in ledgered if k.startswith("pin:")}
        non_pointer_pins = sorted(k for k in pins if not isinstance(CHAT_POINTERS[k], POINTER))
        assert not non_pointer_pins, (
            f"pin: rows must be POINTERs (they exist to be resolution-tested): "
            f"{non_pointer_pins}"
        )
        missing = derived - ledgered
        stale = ledgered - derived - pins
        assert not missing, (
            f"Product surfaces with NO CHAT_POINTERS ledger row: {sorted(missing)}. "
            f"Add a POINTER (a canonical utterance that resolves deterministically) "
            f"or a justified CHAT_INVISIBLE(issue=N | ref='ADR-...') row in "
            f"tests/test_architecture_enforcement.py (#1433)."
        )
        assert not stale, (
            f"CHAT_POINTERS rows for surfaces that no longer exist: {sorted(stale)}. "
            f"Remove the row (and if CHAT_INVISIBLE, lower the chat_invisible "
            f"ceiling in scripts/ratchet_ceilings.json in this same commit)."
        )

    def test_chat_invisible_citations_are_structured(self):
        """Free-text reason = fail (Arch refinement 2). Every CHAT_INVISIBLE
        names a tracked issue (issue=N) or a ratified ADR/PDR (ref='ADR-NNN'),
        or sits in the frozen 2026-08-02 UNTRACKED_BASELINE."""
        bad = []
        for surface, row in CHAT_POINTERS.items():
            if not isinstance(row, CHAT_INVISIBLE):
                continue
            citations = [
                row.issue is not None,
                row.ref is not None,
                bool(row.untracked),
            ]
            if sum(citations) != 1:
                bad.append(f"{surface}: exactly ONE of issue=/ref=/untracked= required")
                continue
            if row.issue is not None and not isinstance(row.issue, int):
                bad.append(f"{surface}: issue= must be an int issue number, got {row.issue!r}")
            if row.ref is not None and not re.fullmatch(r"(ADR|PDR)-\d+", str(row.ref)):
                bad.append(f"{surface}: ref= must look like 'ADR-063'/'PDR-006', got {row.ref!r}")
            if row.untracked and surface not in UNTRACKED_BASELINE:
                bad.append(
                    f"{surface}: untracked=True is baseline-only — file a tracking "
                    f"issue and cite it (never grow UNTRACKED_BASELINE)"
                )
        assert not bad, "CHAT_INVISIBLE citation violations:\n  " + "\n  ".join(bad)

    def test_untracked_baseline_stays_tight(self):
        """A baseline entry whose row now cites a real issue/ref (or is now a
        POINTER, or is gone) is stale — remove it; the baseline only shrinks."""
        still_untracked = {
            surface
            for surface, row in CHAT_POINTERS.items()
            if isinstance(row, CHAT_INVISIBLE) and row.untracked
        }
        stale = UNTRACKED_BASELINE - still_untracked
        assert not stale, (
            f"UNTRACKED_BASELINE entries no longer untracked: {sorted(stale)}. "
            f"Remove them from the baseline (it only shrinks)."
        )

    def test_every_pointer_resolves_deterministically(self):
        """The Arch-required resolver-path assertion: each POINTER's utterance
        must reach its expected destination through the deterministic set —
        never via LLM luck. The failure message records which surface resolved
        (or failed to resolve) each pointer."""
        failures = []
        for surface, row in CHAT_POINTERS.items():
            if not isinstance(row, POINTER):
                continue
            destination, resolver = self._static_resolve(row.utterance)
            expected = (row.expects[0].lower(), row.expects[1])
            if destination != expected:
                failures.append(
                    f"{surface}: {row.utterance!r} resolved to {destination} "
                    f"via [{resolver}], expected {expected}"
                )
            elif resolver not in self.DETERMINISTIC_RESOLVERS:
                failures.append(
                    f"{surface}: {row.utterance!r} reached {destination} but via "
                    f"[{resolver}], which is NOT in the deterministic set "
                    f"{sorted(self.DETERMINISTIC_RESOLVERS)} — a POINTER that "
                    f"only works via the LLM classifier fails at authoring time"
                )
        assert not failures, "POINTER resolution failures (#1433):\n  " + "\n  ".join(failures)

    def test_chat_invisible_ceiling(self):
        """Shrink-lock: the CHAT_INVISIBLE count is frozen in
        scripts/ratchet_ceilings.json ('chat_invisible') and may only go DOWN —
        both directions, per the #1424 ratchet discipline (a count below the
        ceiling must lower the ceiling in the same commit)."""
        import json

        with open(self._CEILINGS_JSON, encoding="utf-8") as fh:
            ceiling = json.load(fh)["chat_invisible"]
        count = sum(1 for row in CHAT_POINTERS.values() if isinstance(row, CHAT_INVISIBLE))
        assert count <= ceiling, (
            f"chat_invisible: count {count} exceeds frozen ceiling {ceiling} (#1433). "
            f"A new chat-invisible surface may not ship silently — give it a POINTER, "
            f"or (for a deliberate web-only surface) cite the ruling AND raise the "
            f"question with Arch; the ledger's CHAT_INVISIBLE set only shrinks."
        )
        assert count == ceiling, (
            f"chat_invisible: count {count} is BELOW ceiling {ceiling} — a surface "
            f"became reachable. Lower the ceiling to {count} in "
            f"scripts/ratchet_ceilings.json in this same commit to lock it in."
        )

    def test_unwired_write_declines_stay_fresh(self):
        """#1426 structural half: UNWIRED_WRITE_DECLINES keys ∩ reachable
        actions == ∅. Shipping a capability (rail entry, mapper mapping, elif
        branch, registry entry, or a POINTER that resolves to it) forces its
        stale denial copy out of the build in the same commit.

        Denominator (design §3, Arch refinement 3): `reachable` covers
        POINTER-resolved + registry-wired paths and does NOT cover
        capabilities reachable by paths outside both (believed empty today) —
        stated here so "complete for the space it searched" stays visible."""
        from services.intent_service.unwired_writes import UNWIRED_WRITE_DECLINES

        reachable = self._reachable_actions()
        # Vacuity guard (Arch checker 2026-08-04): the reachable set is DERIVED;
        # empty means the derivation broke, not "nothing is reachable".
        assert (
            len(reachable) >= 20
        ), f"reachable-actions derivation returned only {len(reachable)} — detection broken"
        stale = set(UNWIRED_WRITE_DECLINES) & reachable
        assert not stale, (
            f"UNWIRED_WRITE_DECLINES lists actions that are now REACHABLE: "
            f"{sorted(stale)}. The capability shipped — remove its decline copy "
            f"from services/intent_service/unwired_writes.py (and its "
            f"capability: ledger row + the chat_invisible ceiling) in this same "
            f"commit, or Piper denies a capability it has (#1426's false-denial "
            f"class)."
        )

    def test_contextual_fallback_denials_stay_fresh(self):
        """The _get_contextual_fallback keyword→copy table gets the same
        treatment (string-match on its denial keys, per the ratified design):

        (a) every "I can't ..." denial string in the function must map to a
            CONTEXTUAL_FALLBACK_DENIALS row (a NEW denial without a row fails);
        (b) every row's snippet must still appear in the function (capability
            shipped → denial removed → remove the row + ledger surface);
        (c) no row's capability-action tokens may be reachable."""
        fragments = self._fallback_denial_fragments()
        snippets = {surface: row["snippet"] for surface, row in CONTEXTUAL_FALLBACK_DENIALS.items()}

        uncovered = [
            frag for frag in fragments if not any(snip in frag for snip in snippets.values())
        ]
        assert not uncovered, (
            f"NEW capability denial(s) in _get_contextual_fallback with no "
            f"CONTEXTUAL_FALLBACK_DENIALS row: {uncovered}. Add a row (snippet + "
            f"capability-action tokens) and a capability: ledger surface in this "
            f"same commit — an unledgered denial is exactly how #1426's false "
            f"denials went unnoticed."
        )

        denial_text = "\n".join(fragments)
        vanished = [
            f"{surface} (snippet {snip!r})"
            for surface, snip in snippets.items()
            if snip not in denial_text
        ]
        assert not vanished, (
            f"CONTEXTUAL_FALLBACK_DENIALS rows whose denial no longer exists in "
            f"_get_contextual_fallback: {vanished}. The capability shipped (or the "
            f"copy moved) — remove the row and its capability: ledger surface, and "
            f"lower the chat_invisible ceiling, in this same commit."
        )

        reachable = self._reachable_actions()
        stale = [
            f"{surface}: {sorted(set(row['actions']) & reachable)}"
            for surface, row in CONTEXTUAL_FALLBACK_DENIALS.items()
            if set(row["actions"]) & reachable
        ]
        assert not stale, (
            f"_get_contextual_fallback still DENIES capabilities that are now "
            f"reachable: {stale}. Remove/replace the stale denial copy in "
            f"intent_service.py (point at the real capability instead) in this "
            f"same commit (#1426)."
        )

    def test_derivations_are_alive(self):
        """Canaries for the extractors (the #1283 idiom): if an idiom changes,
        the derivation must fail LOUDLY here, never silently shrink coverage."""
        pages = self._page_paths()
        assert len(pages) >= 20, (
            f"ui.py page-route derivation returned only {len(pages)} paths — "
            f"the decorator idiom likely changed; fix _page_paths()."
        )
        integrations = self._connectable_integrations()
        assert integrations >= {"github", "slack", "calendar", "notion"}, (
            f"connectable-integration derivation returned {sorted(integrations)} — "
            f"the /connect|/save route idiom likely changed; fix "
            f"_connectable_integrations()."
        )
        assert len(self._fallback_denial_fragments()) >= 4, (
            "_get_contextual_fallback denial derivation collapsed — the string "
            "idiom likely changed; fix _fallback_denial_fragments()."
        )
        assert len(self._elif_tokens()) >= 5, (
            "EXECUTION elif-token derivation collapsed — idiom changed; fix " "_elif_tokens()."
        )


class TestSingleDeclarativeBase:
    """#1312 (Arch invariant, ruled 2026-06-25 + re-confirmed 2026-07-08): ONE
    declarative Base per physical database. A second declarative_base() creates a
    parallel metadata invisible to alembic's target_metadata — its tables silently
    fall out of autogenerate and drift unchecked (services/personality/models.py
    did exactly this for a year before deletion). Only services/database/connection.py
    may call declarative_base()."""

    ALLOWED = {os.path.join("services", "database", "connection.py")}

    def test_only_connection_py_creates_a_base(self):
        offenders = []
        files_scanned = 0
        for root, _dirs, files in os.walk("services"):
            if "__pycache__" in root:
                continue
            for f in files:
                files_scanned += 1
                if not f.endswith(".py"):
                    continue
                path = os.path.join(root, f)
                rel = os.path.relpath(path)
                if rel in self.ALLOWED:
                    continue
                src = open(path, encoding="utf-8", errors="ignore").read()
                if re.search(r"^\s*Base\s*=\s*declarative_base\(\)", src, re.M):
                    offenders.append(rel)
        assert (
            files_scanned >= 100
        ), f"Base-scan walked only {files_scanned} files — detection broken (vacuity guard)"
        assert not offenders, (
            f"Second declarative Base created in: {offenders} — one Base per DB "
            "(Arch invariant, #1312). Register models on "
            "services.database.connection.Base instead."
        )


class TestNoRawTodoEnumComparisons1472:
    """#1472 — raw TodoStatus/TodoPriority members must never appear in a
    comparison: `todo_items.status`/`priority` are String columns ("Changed
    from Enum to String"), so binding a raw enum member raises asyncpg
    DataError ("expected str, got TodoStatus") at execution time — which every
    call site's try/except turns into a silent degraded lookup (#1425 None
    sentinel). The class stayed latent because the broken filters were only
    reachable through gates that were dead until #1460 revived them.

    Rule enforced (AST, whole services/ tree): an attribute of the bare name
    `TodoStatus`/`TodoPriority` (i.e. an enum MEMBER, not `.value` on one) may
    not be an operand of a comparison (`==`, `!=`, etc.) nor an element of a
    list/tuple/set passed to SQLAlchemy's `.in_()`/`.notin_()`. Passing a
    member as a typed argument (e.g. `get_todos_by_owner(status=TodoStatus.
    PENDING)`) stays legal — the repository normalizes via `.value`; that
    parameter-shaped half of the class is pinned by bind-type tests in
    tests/unit/services/repositories/test_todo_repository_enum_filters_1472.py.
    """

    _ENUM_NAMES = {"TodoStatus", "TodoPriority"}

    @classmethod
    def _is_raw_member(cls, node) -> bool:
        """`TodoStatus.COMPLETED` — but NOT `TodoStatus.COMPLETED.value`
        (there the operand's .value attr chain bottoms out in an Attribute,
        not a bare enum Name)."""
        import ast

        return (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in cls._ENUM_NAMES
        )

    def test_no_raw_enum_members_compared_or_in_listed(self):
        import ast

        violations = []
        files_scanned = 0
        for path in glob.glob("services/**/*.py", recursive=True):
            if "__pycache__" in path:
                continue
            files_scanned += 1
            try:
                tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    operands = [node.left, *node.comparators]
                    if any(self._is_raw_member(op) for op in operands):
                        violations.append(f"{path}:{node.lineno} (comparison)")
                elif (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in ("in_", "notin_")
                ):
                    for arg in node.args:
                        if isinstance(arg, (ast.List, ast.Tuple, ast.Set)) and any(
                            self._is_raw_member(el) for el in arg.elts
                        ):
                            violations.append(f"{path}:{node.lineno} (.in_ list)")

        # m-44 denominator: the scan must actually have covered the tree.
        # 526 files at time of writing; floor set with slack for deletions.
        assert files_scanned >= 400, (
            f"enum-comparison scan walked only {files_scanned} services/ files "
            f"— detection broken (vacuity guard); expected >= 400"
        )
        assert not violations, (
            f"Raw TodoStatus/TodoPriority member used in a comparison against "
            f"String-typed columns (asyncpg DataError -> silent degraded "
            f"lookup, #1472). Compare `.value` instead. Sites: {violations} "
            f"(scanned {files_scanned} files)"
        )


class TestPrincipalThreadingGuards1532:
    """#1532 — the three guards from the principal-dropping audit
    (docs/internal/operations/principal-dropping-audit-2026-08-08.md §Guards).

    The class being guarded: state keyed by ``{user_id or 'anonymous'}:...``
    read WITHOUT the principal — every authenticated user silently gets the
    anonymous key's (empty or wrong) data. #1394 (floor history), F1 (agenda
    todos read with owner_id=session_id), F2 (priorities read session-only)
    and F3 (conversation persistence had no ownership check) were all this
    one shape. These guards make the shape a test failure instead of an audit
    finding.

    Guard 1 is a RATCHET like TestPreFloorDispatchSiteRatchet: the allowlist
    is exact (tight, no slack) and may only SHRINK. When you thread a
    principal through an allowlisted site, remove its entry in the same
    commit. NEVER add an entry — thread the principal (or recover it via
    ``_principal_from_intent(intent)``, the sanctioned recovery idiom the
    guard recognizes) instead.
    """

    # Functions whose results are principal-keyed (the audit's reader set that
    # is callable across modules; the three F3 persistence readers are covered
    # structurally by Guard 3 + their own ownership tests).
    PRINCIPAL_KEYED_READERS = {
        "get_or_create_context",  # in-memory discourse state (#817 key)
        "get_user_context",  # user prefs/projects (F2's reader)
        "build_recent_history",  # prompt-shaped history (#1394's reader)
        # #1501 reader-set extension (2026-08-09): project reads are
        # owner-keyed. These names cover ProjectQueryService, PortfolioService
        # AND ProjectRepository call sites alike (matching is by attr name) —
        # an unthreaded call to any of them is the global cross-tenant read
        # #1501 fixed. The principal here is `owner_id` or `user_id` (kwarg);
        # _passes_principal recognizes both.
        "list_active_projects",
        "find_project_by_name",
        "count_active_projects",
    }

    # Demo-only surface (audit §INERT / by-design): excluded, not allowlisted,
    # so its churn can never consume the ratchet budget.
    EXCLUDED_FILES = {
        os.path.join("services", "conversation", "context_tracker.py"),
    }

    # Guard 1 baseline — audit-validated: exactly ONE unthreaded site remained
    # (classify_conscious's anonymous-keyed context read — zero production
    # callers; delete-candidate with the #1526 class; F2 was fixed 2026-08-08).
    # The #1501 reader-set extension re-validated the baseline and surfaced
    # ONE more site (two calls): ProjectContext.resolve_project's bare
    # repo.list_active_projects() reads — a class with NO principal in scope
    # and zero production callers (#1421 census B item 31). Allowlisted as the
    # extension's validated baseline, NOT as budget: fixing means threading an
    # owner or deleting the class. Direction is DOWN: as those die, so do
    # their rows. 2026-08-30: services/project_context/ WAS deleted (Batch-2
    # census-dead-family disposal) — its tuple and both counted call sites
    # left the set exactly as this comment predicted (3 → 1).
    # 2026-09-12 (#1768): classify_conscious WAS deleted — its tuple, the last
    # allowlisted exemption, leaves the set (1 → 0). The gate is now fully
    # tight: EVERY principal-keyed read must thread a principal. Never re-seed
    # this set — fix the site instead.
    ALLOWED_UNTHREADED: set = set()
    MAX_UNTHREADED_PRINCIPAL_READS = 0

    @staticmethod
    def _call_name(call) -> str:
        import ast

        func = call.func
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
        return ""

    @staticmethod
    def _passes_principal(call) -> bool:
        """A reader call is threaded if it passes a user_id or owner_id
        (#1501 readers name the principal owner_id) that is not the literal
        None — as keyword, or as the 2nd positional arg (the original three
        readers and find_project_by_name take the principal as parameter #2;
        the single-parameter #1501 readers should pass it as a keyword)."""
        import ast

        for kw in call.keywords:
            if kw.arg in ("user_id", "owner_id"):
                return not (isinstance(kw.value, ast.Constant) and kw.value.value is None)
        if len(call.args) >= 2:
            a = call.args[1]
            return not (isinstance(a, ast.Constant) and a.value is None)
        return False

    def _scan_files(self):
        import ast

        for base in ("services", "web"):
            for root, _dirs, files in os.walk(base):
                if "__pycache__" in root:
                    continue
                for f in sorted(files):
                    if not f.endswith(".py"):
                        continue
                    rel = os.path.relpath(os.path.join(root, f))
                    src = open(rel, encoding="utf-8", errors="ignore").read()
                    yield rel, ast.parse(src)

    def _unthreaded_reader_sites(self):
        """(rel_path, enclosing_function, reader) for every principal-keyed
        reader call that neither threads a principal nor sits in a function
        using the ``_principal_from_intent`` recovery idiom."""
        import ast

        violations = []
        reader_calls_seen = 0
        files_scanned = 0

        for rel, tree in self._scan_files():
            files_scanned += 1
            if rel in self.EXCLUDED_FILES:
                continue

            def walk(node, enclosing):
                nonlocal reader_calls_seen
                for child in ast.iter_child_nodes(node):
                    child_enclosing = enclosing
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        child_enclosing = child
                    if (
                        isinstance(child, ast.Call)
                        and self._call_name(child) in self.PRINCIPAL_KEYED_READERS
                    ):
                        reader_calls_seen += 1
                        if not self._passes_principal(child):
                            recovered = enclosing is not None and any(
                                isinstance(n, ast.Name) and n.id == "_principal_from_intent"
                                for n in ast.walk(enclosing)
                            )
                            if not recovered:
                                violations.append(
                                    (
                                        rel,
                                        enclosing.name if enclosing else "<module>",
                                        self._call_name(child),
                                    )
                                )
                    walk(child, child_enclosing)

            walk(tree, None)

        return violations, reader_calls_seen, files_scanned

    def test_guard1_no_unthreaded_principal_keyed_reads(self):
        """Guard 1: every principal-keyed read passes a non-None user_id (or
        recovers it via _principal_from_intent). Tight ratchet — the violation
        set must EQUAL the allowlist, so fixes shrink it in the same commit
        and new drops fail immediately."""
        violations, reader_calls_seen, files_scanned = self._unthreaded_reader_sites()

        # Vacuity guards (m-44): prove the scan actually measured something.
        assert (
            files_scanned >= 100
        ), f"principal-reader scan walked only {files_scanned} files — detection broken"
        assert reader_calls_seen >= 15, (
            f"principal-reader scan matched only {reader_calls_seen} reader calls — "
            "detection broken (the tree has dozens)"
        )

        assert len(violations) <= self.MAX_UNTHREADED_PRINCIPAL_READS, (
            f"NEW unthreaded principal-keyed read(s): "
            f"{sorted(set(violations) - self.ALLOWED_UNTHREADED)} — this is the #1394/F1/F2 "
            "shape (authenticated users silently served the anonymous key's data). Thread "
            "user_id through, or recover it with _principal_from_intent(intent). Do NOT "
            "extend the allowlist."
        )
        assert set(violations) == self.ALLOWED_UNTHREADED, (
            f"Guard-1 ratchet drift: actual={sorted(set(violations))} vs "
            f"allowlist={sorted(self.ALLOWED_UNTHREADED)}. If you just threaded/deleted an "
            "allowlisted site, shrink ALLOWED_UNTHREADED (and "
            "MAX_UNTHREADED_PRINCIPAL_READS) in this commit; if a new site appears, fix the "
            "site, never the list."
        )

    def test_guard2_session_id_is_never_an_owner(self):
        """Guard 2: no call anywhere passes owner_id=<session-derived value>.
        F1's exact bug (todos read with owner_id=session_id while writes used
        owner_id=user_id → structurally empty for every authenticated user).
        Zero baseline — F1 is fixed; any hit is a regression."""
        import ast

        violations = []
        owner_kwargs_seen = 0

        for rel, tree in self._scan_files():
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                for kw in node.keywords:
                    if kw.arg != "owner_id":
                        continue
                    owner_kwargs_seen += 1
                    idents = {n.id for n in ast.walk(kw.value) if isinstance(n, ast.Name)} | {
                        n.attr for n in ast.walk(kw.value) if isinstance(n, ast.Attribute)
                    }
                    session_like = {i for i in idents if i == "session" or i.startswith("session_")}
                    if session_like:
                        violations.append((rel, node.lineno, sorted(session_like)))

        assert (
            owner_kwargs_seen >= 10
        ), f"owner_id scan matched only {owner_kwargs_seen} keyword sites — detection broken"
        assert not violations, (
            f"owner_id passed a session-derived value at: {violations} — a session id is "
            "NEVER an owner (F1, #1532 audit). Owners are principals (user_id); thread the "
            "user's id instead."
        )

    def test_guard3_f3_persistence_readers_accept_principal(self):
        """Guard 3: the three F3 conversation-persistence readers keep their
        principal parameter (ownership contract pinned behaviorally in
        test_conversation_ownership_1532.py; this pins the signatures so a
        refactor can't silently drop the parameter again)."""
        import inspect

        from services.conversation.conversation_manager import ConversationManager
        from services.intent_service.conversation_context import hydrate_turns_from_db

        for func, name in [
            (ConversationManager.get_recent_turns, "ConversationManager.get_recent_turns"),
            (ConversationManager.load_context_state, "ConversationManager.load_context_state"),
            (hydrate_turns_from_db, "hydrate_turns_from_db"),
        ]:
            assert "user_id" in inspect.signature(func).parameters, (
                f"{name} lost its user_id (principal) parameter — the F3 ownership check "
                "cannot be threaded without it (#1532)."
            )


# ============================================================================
# #1547 — status-truth: the plugin registry is NOT a configuration source
# ============================================================================


class TestRegistryConfiguredReadRatchet:
    """#1547 (status-truth audit 2026-08-09) — architectural enforcement for the
    canonical-status migration.

    All four real integration plugins hardcode ``is_configured() -> False``
    (#784 — the plugin interface has no user, and integration truth is
    user-scoped), so any surface reading
    ``PluginRegistry.get_status_all()[...]["configured"]`` reports every real
    integration never-connected — the mechanism behind 6 of the audit's 10
    findings (#1534, the blind floor, the constant degrade nudges, ...).

    The canonical source is
    ``services/integrations/integration_status_service.py``
    (user-scoped, binding-first). This test is a RATCHET: it counts remaining
    non-test ``get_status_all()`` consumer sites and fails if the count GROWS.
    When a migration lands, LOWER ``MAX_REGISTRY_STATUS_CONSUMERS`` in the same
    commit (never raise it). New status-consuming surfaces must read the
    canonical service.
    """

    # Ratchet target — non-test get_status_all() consumer sites remaining.
    # 2026-08-09 (#1547): 1 — the Slack-help capability enumeration in
    # canonical_handlers._get_dynamic_capabilities (audit F6, a separate slice).
    # Trajectory: 4 (audit baseline) → 1 (F1 guidance, F2 identity context +
    # github flag migrated this pass). LOWER as F6 lands; NEVER raise.
    MAX_REGISTRY_STATUS_CONSUMERS = 1

    # Where consumers could live (m-44: name the denominator — this is the
    # scanned space, and the guard test below asserts it's actually populated).
    SCAN_GLOBS = ("services/**/*.py", "web/**/*.py", "main.py")

    # The definition site itself (and this test) are not consumers.
    DEFINITION_FILE = "services/plugins/plugin_registry.py"

    CALL_RE = re.compile(r"get_status_all\s*\(")

    def _consumer_sites(self):
        sites = []
        scanned = 0
        for pattern in self.SCAN_GLOBS:
            for path in glob.glob(pattern, recursive=True):
                if os.path.normpath(path) == os.path.normpath(self.DEFINITION_FILE):
                    continue
                scanned += 1
                with open(path, encoding="utf-8") as fh:
                    for lineno, line in enumerate(fh, start=1):
                        if self.CALL_RE.search(line):
                            sites.append(f"{path}:{lineno}")
        return sites, scanned

    def test_denominator_guard_scan_space_is_populated(self):
        """m-44: an empty glob would make the ratchet pass by measuring nothing.
        Assert the scan actually covered the production tree."""
        _sites, scanned = self._consumer_sites()
        assert scanned >= 300, (
            f"Scan space collapsed: only {scanned} files scanned — the ratchet "
            "below would be vacuous. Check SCAN_GLOBS / working directory."
        )

    def test_no_new_registry_configured_readers(self):
        """Fails if a new non-test surface starts consuming registry status.
        New surfaces must read IntegrationStatusService (user-scoped,
        binding-first) — the registry's 'configured' bit is structurally
        unknowable (#784)."""
        sites, _scanned = self._consumer_sites()
        assert len(sites) <= self.MAX_REGISTRY_STATUS_CONSUMERS, (
            f"{len(sites)} non-test get_status_all() consumer sites found "
            f"({sites}), exceeding the #1547 ratchet target of "
            f"{self.MAX_REGISTRY_STATUS_CONSUMERS}. The registry cannot report "
            "per-user configuration — read "
            "services/integrations/integration_status_service.py instead."
        )

    def test_ratchet_target_stays_tight(self):
        """The target must equal the actual count — a loose target silently
        permits regressions up to the slack. When F6 migrates, lower
        MAX_REGISTRY_STATUS_CONSUMERS to 0 in the same commit."""
        sites, _scanned = self._consumer_sites()
        assert len(sites) == self.MAX_REGISTRY_STATUS_CONSUMERS, (
            f"Ratchet drift: actual consumer-site count is {len(sites)} "
            f"({sites}) but MAX_REGISTRY_STATUS_CONSUMERS is "
            f"{self.MAX_REGISTRY_STATUS_CONSUMERS}. If a migration just landed, "
            "lower the target in the same commit."
        )

    def test_real_plugins_do_not_fabricate_configured(self):
        """The lying source stays retired: no real plugin's get_status() may
        emit a boolean 'configured' again (None + note is the contract; demo is
        env-fed and exempt)."""
        plugin_files = [
            "services/integrations/github/github_plugin.py",
            "services/integrations/slack/slack_plugin.py",
            "services/integrations/calendar/calendar_plugin.py",
            "services/integrations/notion/notion_plugin.py",
        ]
        offenders = []
        for path in plugin_files:
            assert os.path.exists(path), (
                f"Denominator guard: {path} missing — the fabrication check "
                "would be vacuous. Update the list if plugins moved."
            )
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            if re.search(r"\"configured\"\s*:\s*self\.is_configured\(\)", content):
                offenders.append(path)
        assert not offenders, (
            f"{offenders} reintroduced 'configured': self.is_configured() — "
            "that bit is hardcoded False without user context (#784) and every "
            "registry consumer inherits the lie (#1547)."
        )


class TestWorkflowEffectDeclaration:
    """Arch ruling 2026-08-09 (building on PDR-006 condition 2, ruled 2026-08-04):
    every ``WorkflowEntry`` must DECLARE its effect — a required, DEFAULTLESS,
    ordered enum (``EffectClass``: READ < WRITE < DESTRUCTIVE; destructive is a
    subset of write).

    Why defaultless is load-bearing (Arch, decisions.log 2026-08-04): 4 of
    WorkflowEntry's 5 prior fields are defaulted, so a defaulted effect field
    would let every future entry silently inherit a value nobody chose. The
    construction-site break IS THE FEATURE — you cannot register a handler
    without saying whether it writes.

    Why an enum, not a boolean (Arch 2026-08-09): four consumers (capability
    legibility #1509, destructive-mutation gate #1190, consent gate #1509, MCP
    readOnlyHint/destructiveHint annotations per PDR-006 §30) each derive a
    DIFFERENT predicate from the one declared value. A boolean ``mutates``
    would force #1190 and MCP annotations to re-derive destructiveness —
    recreating the inference problem one level down.

    Effect is a fact about what the operation does IN THE WORLD — it is not
    computable from the entry point, signature, or description. Declare once at
    the source; derive everything else (read_only_hint / destructive_hint /
    needs_consent / needs_confirm properties on WorkflowEntry).
    """

    def test_effect_is_required_at_construction(self):
        """Constructing a WorkflowEntry without effect must raise — the
        construction-site break at every registration is the enforcement
        mechanism the ruling asks for."""
        from unittest.mock import AsyncMock

        from services.intent_service.workflow_dispatcher import WorkflowEntry

        with pytest.raises(TypeError):
            WorkflowEntry(entry_point=AsyncMock(), description="no effect declared")

    def test_effect_field_is_defaultless_in_the_dataclass_definition(self):
        """The field must carry NO default and NO default_factory — a later
        'convenience' default would silently reintroduce inherited-value drift
        for every future entry (the exact failure the 08-04 ruling names)."""
        import dataclasses

        from services.intent_service.workflow_dispatcher import WorkflowEntry

        effect_fields = [f for f in dataclasses.fields(WorkflowEntry) if f.name == "effect"]
        assert len(effect_fields) == 1, (
            "WorkflowEntry must declare an `effect` field (Arch ruling "
            "2026-08-09 / PDR-006 condition 2)."
        )
        f = effect_fields[0]
        assert f.default is dataclasses.MISSING, (
            "WorkflowEntry.effect has a default value. The ruling requires it "
            "DEFAULTLESS: a defaulted effect lets new entries silently inherit "
            "a mutation-semantics value nobody chose."
        )
        assert f.default_factory is dataclasses.MISSING, (
            "WorkflowEntry.effect has a default_factory — same defect as a "
            "default value; remove it."
        )

    def test_effect_enum_is_ordered_read_write_destructive(self):
        """Consumers gate on ordered comparison (needs_consent = effect >=
        WRITE), so the ordering READ < WRITE < DESTRUCTIVE is contract, not
        style. Destructive ⊂ write: you cannot destroy without writing."""
        from services.shared_types import EffectClass

        assert EffectClass.READ < EffectClass.WRITE < EffectClass.DESTRUCTIVE
        # The consent predicate the #1509 gate derives:
        assert not (EffectClass.READ >= EffectClass.WRITE)
        assert EffectClass.WRITE >= EffectClass.WRITE
        assert EffectClass.DESTRUCTIVE >= EffectClass.WRITE

    def test_every_registered_default_entry_declares_a_real_effect(self):
        """Denominator guard (m-44): assert the registry is non-empty AND every
        registered entry's effect is an EffectClass member — a registry the
        default registration never populated would make this check vacuous."""
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import (
            register_default_workflows,
        )
        from services.shared_types import EffectClass

        saved = dict(WORKFLOW_REGISTRY)
        try:
            register_default_workflows()
            assert len(WORKFLOW_REGISTRY) >= 30, (
                f"Denominator guard: only {len(WORKFLOW_REGISTRY)} workflows "
                "registered — expected the full default set (~80 alias keys). "
                "If the default set legitimately shrank, update this floor."
            )
            offenders = {
                key: getattr(entry, "effect", None)
                for key, entry in WORKFLOW_REGISTRY.items()
                if not isinstance(getattr(entry, "effect", None), EffectClass)
            }
            assert not offenders, (
                f"Registered workflows without a declared EffectClass effect: " f"{offenders}"
            )
        finally:
            WORKFLOW_REGISTRY.clear()
            WORKFLOW_REGISTRY.update(saved)

    # ── Ratchet: no name-based effect inference in production code ─────────
    # Now that the effect is DECLARED on WorkflowEntry, production code must
    # never re-derive read/write-ness from action NAMES, key prefixes, or
    # descriptions — that inference is exactly what the declared field
    # retires (PA's evidence: `prioritization` sounds like a bulk-write and
    # writes nothing; guess and fact pointed opposite ways). Hand-maintained
    # read/write action lists are the greppable signature of that inference.
    INFERENCE_LIST_RE = re.compile(
        r"^\s*(?:READ|WRITE|MUTATING|READONLY|READ_ONLY|DESTRUCTIVE)"
        r"[A-Z_]*_(?:ACTIONS|WORKFLOWS|KEYS)\s*[:=]",
        re.MULTILINE,
    )
    MAX_INFERENCE_SITES = 0  # Ratchet: never raise.

    def test_no_name_based_effect_inference_in_production_code(self):
        """Fails if production code (services/, web/) introduces a
        hand-maintained read/write/destructive action list — the field on
        WorkflowEntry is the single source of effect truth; consumers derive
        via entry.effect / the derivation properties, never via name lists."""
        offenders: List[str] = []
        for root in ("services", "web"):
            for path in glob.glob(f"{root}/**/*.py", recursive=True):
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
                if self.INFERENCE_LIST_RE.search(content):
                    offenders.append(path)
        assert len(offenders) <= self.MAX_INFERENCE_SITES, (
            f"Hand-maintained effect-classification lists found in production "
            f"code: {offenders}. Effect is DECLARED on WorkflowEntry "
            f"(entry.effect: EffectClass) — derive predicates from it "
            f"(read_only_hint / destructive_hint / needs_consent / "
            f"needs_confirm); never re-infer from names (Arch ruling "
            f"2026-08-09)."
        )


def _execute_re_alternative_count() -> int:
    """Top-level alternatives of ``collaboration_gate._EXECUTE_RE``, read from
    the compiled pattern's own parse tree (never its source text): the
    head-verb group's alternatives (create|file|…|start) plus one per non-verb
    anchor ("don't let me forget", "need to remember", "i'm done with").
    A nested alternation INSIDE an anchor ("i(?:'m| am)") is one anchor, not two."""
    try:
        import re._parser as sre_parse  # Python 3.11+
    except ImportError:  # pragma: no cover
        import sre_parse  # type: ignore[no-redef]

    from services.intent_service.collaboration_gate import _EXECUTE_RE

    tree = sre_parse.parse(_EXECUTE_RE.pattern, _EXECUTE_RE.flags)
    op, av = list(tree)[-1]
    assert str(op) == "BRANCH", f"_EXECUTE_RE's last element is {op}, not the alternation"
    branches = av[1]
    head = list(branches[0])
    verbs = None
    for o, a in head:
        if str(o) == "BRANCH":  # a non-capturing group parses as a bare BRANCH
            verbs = a[1]
            break
        if str(o) == "SUBPATTERN":
            for o2, a2 in a[-1]:
                if str(o2) == "BRANCH":
                    verbs = a2[1]
            break
    assert verbs, "_EXECUTE_RE's first branch is no longer the head-verb group"
    return len(verbs) + (len(branches) - 1)


class TestExecuteVocabRatchet:
    """#1970 (Arch's ruling 2026-10-10, option c; ADR-080 open questions):
    ``_EXECUTE_RE`` is a CONSERVATIVE CONSENT DETECTOR (D3/D4 side), and its
    error leans toward asking, the safe direction. Router framing is deferred
    because the router's error leans toward acting ("My default repo should
    be X" read execute @0.99). The regex stays, but its growth is ratcheted
    in the ``MAX_DISPATCH_SITES`` shape, with a JUSTIFIED-BUMP rule:

    - ``MAX_EXECUTE_ALTERNATIVES`` is the count on 2026-10-10 (39 = 36
      head verbs + 3 anchors). It never rises by editing this number.
    - The ceiling rises only by appending to ``JUSTIFIED_BUMPS``, in the same
      commit that adds the alternative AND the corpus row
      ``TestExecuteVocabCoverage`` demands for it. Each entry is that row's
      exact phrase, and must be a real corpus row the regex reads EXECUTE.
    - When an alternative is removed, lower ``MAX_EXECUTE_ALTERNATIVES`` in
      that commit.

    Retry trigger for router framing (recorded on #1970): every
    ``framing: declarative|question`` corpus row reads ambiguous at N=5 on
    the served model, AND the full-run operation diff shows no
    ×6-attributed regression."""

    MAX_EXECUTE_ALTERNATIVES = 39
    JUSTIFIED_BUMPS: List[str] = []

    def test_execute_alternatives_do_not_grow_unjustified(self):
        count = _execute_re_alternative_count()
        ceiling = self.MAX_EXECUTE_ALTERNATIVES + len(self.JUSTIFIED_BUMPS)
        assert count <= ceiling, (
            f"_EXECUTE_RE has {count} alternatives, ceiling {ceiling} "
            f"({self.MAX_EXECUTE_ALTERNATIVES} + {len(self.JUSTIFIED_BUMPS)} justified). "
            "A new imperative verb needs its corpus row first, then one JUSTIFIED_BUMPS "
            "entry naming that row, in the same commit (#1970, Arch 2026-10-10)."
        )

    def test_each_justified_bump_names_a_real_execute_corpus_row(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
        from inversion_phase0_baseline import load_corpus  # noqa: E402

        from services.intent_service.collaboration_gate import (
            FRAMING_EXECUTE,
            classify_framing,
        )

        phrases = {row["phrase"] for row in load_corpus()}
        for phrase in self.JUSTIFIED_BUMPS:
            assert phrase in phrases, f"justified bump {phrase!r} is not a corpus row"
            assert (
                classify_framing(phrase) == FRAMING_EXECUTE
            ), f"justified bump {phrase!r} does not read EXECUTE"

    def test_counter_reads_todays_shape(self):
        # Pins the counter itself: the head-verb group and the three anchors
        # as of 2026-10-10. If the regex is restructured, update this pin and
        # the counter together. Never loosen the ratchet to make it pass.
        assert _execute_re_alternative_count() == 39


class TestExecuteVocabCoverage:
    """#1595 Phase 3 (Arch ruling 2026-10-04, in-reply-to ask-lead-to-arch-
    cc-cxo-ppm-complete-todo-entry-parked-write-consent-gate-holds-plain-
    completions-2026-10-04.md): mechanical coverage so the
    ``collaboration_gate._EXECUTE_RE`` vocabulary gap that blocked
    ``complete_todo`` (plain "complete todo 1" read AMBIGUOUS, arming a
    consent "shall I?" instead of executing) cannot recur silently.

    The contract, verbatim from ``_EXECUTE_RE``'s own #1509 comment: the
    gate "covers EVERY WRITE-effect rail action", so the imperative verb
    list must carry every WRITE (or allowlisted-DESTRUCTIVE, #1677) rail
    entry's verb-initial shape. This test DERIVES the check from the
    registry + rail (``get_action_workflows()`` + ``action_registry.
    get_verb``) — never a hand list — so link-repo / archive / restore
    (Arch's own named examples of what will hit this next) fail the build
    the moment they register without vocabulary, no second manual audit
    required.

    Scope (Arch's exact words): every rail entry with ``EffectClass.WRITE``,
    OR ``EffectClass.DESTRUCTIVE`` AND allowlisted in ``FLIP_WRITE_ALLOWLIST``
    (#1677). A non-allowlisted DESTRUCTIVE entry (``close_issue``,
    ``reopen_issue`` today) is OUT OF SCOPE: ``consent_gate.decide_consent``
    returns CONFIRM for DESTRUCTIVE in every framing/mode cell, so framing
    vocabulary cannot affect its consent outcome — nothing to ratchet.

    EXEMPTIONS (named, reasoned, never silent — per this unit's own HARD
    RULES): ``delete_todo``'s verb ("delete") is NOT currently in
    ``_EXECUTE_RE`` — discovered BUILDING this test, not before (Arch's
    memo did not re-run it). Exempted rather than vocabulary-patched: it is
    the one allowlisted DESTRUCTIVE entry today, and
    ``consent_gate.decide_consent``'s own matrix/docstring (PRIVATE/OUTWARD
    x DESTRUCTIVE: CONFIRM in every cell, every framing, every mode) means
    ``_EXECUTE_RE``'s classification of a delete_todo message has ZERO
    effect on its consent outcome — the #1509 contract ``_EXECUTE_RE``'s
    own comment states scopes coverage to "EVERY WRITE-effect rail
    action", not DESTRUCTIVE. If delete_todo (or a future DESTRUCTIVE
    allowlist entry) ever becomes framing-sensitive, remove the exemption
    and add its verb instead of widening this comment.
    """

    # Named, reasoned exemptions from the EXECUTE-classification assertion
    # (test_every_qualifying_verb_classifies_execute below). Every key here
    # MUST be re-verified by test_exemption_list_stays_accurate on every run
    # — a stale exemption (gap fixed, or entry retired) is a silent no-op,
    # not a safety net, and must be removed in the same commit it goes stale.
    EXEMPT_ALLOWLISTED_DESTRUCTIVE = {
        "delete_todo": (
            "DESTRUCTIVE effect is CONFIRM in every framing/mode cell "
            "(consent_gate.decide_consent's matrix) — _EXECUTE_RE's own "
            "contract comment scopes coverage to WRITE-effect actions; a "
            "missing verb here cannot change delete_todo's consent outcome."
        ),
        # #1926 / #1595 Phase 3 (2026-10-04): unlink_repo — the second
        # allowlisted DESTRUCTIVE entry, same reasoning as delete_todo above
        # (discovered applying this test's own precedent, not re-derived):
        # "unlink" is not in _EXECUTE_RE's verb list, but
        # consent_gate.decide_consent's matrix returns CONFIRM for
        # DESTRUCTIVE in every framing/mode cell, so _EXECUTE_RE's missing
        # verb cannot change unlink_repo's consent outcome either.
        "unlink_repo": (
            "DESTRUCTIVE effect is CONFIRM in every framing/mode cell "
            "(consent_gate.decide_consent's matrix) — _EXECUTE_RE's own "
            "contract comment scopes coverage to WRITE-effect actions; a "
            "missing verb here cannot change unlink_repo's consent outcome."
        ),
    }

    def _qualifying_entries(self):
        """Return ``{canonical_action_name: (entry, verb_or_None)}`` for
        every DISTINCT rail entry in scope (see class docstring),
        deduplicated by object identity since one entry often serves a
        whole alias family (e.g. complete_todo/finish_todo/mark_complete/
        mark_done share ONE WorkflowEntry object)."""
        from services.intent_service.action_registry import get_verb
        from services.intent_service.workflow_dispatcher import (
            FLIP_WRITE_ALLOWLIST,
            WORKFLOW_REGISTRY,
            get_action_workflows,
        )
        from services.intent_service.workflow_entries import (
            register_default_workflows,
        )
        from services.shared_types import EffectClass

        saved = dict(WORKFLOW_REGISTRY)
        try:
            register_default_workflows()
            workflows = get_action_workflows()
        finally:
            WORKFLOW_REGISTRY.clear()
            WORKFLOW_REGISTRY.update(saved)

        seen_ids = set()
        result = {}
        for key, entry in workflows.items():
            if id(entry) in seen_ids:
                continue
            in_scope = entry.effect == EffectClass.WRITE or (
                entry.effect == EffectClass.DESTRUCTIVE
                and entry.flip_write_allowlist_key in FLIP_WRITE_ALLOWLIST
            )
            if not in_scope:
                continue
            seen_ids.add(id(entry))
            # Prefer the declared allowlist key — by the allowlist's own
            # construction-site convention it IS the canonical registry
            # name — else scan this entry's alias keys for one ACTION_TO_VERB
            # recognizes.
            canonical = entry.flip_write_allowlist_key
            verb = get_verb(canonical) if canonical else None
            if verb is None:
                for alias_key, alias_entry in workflows.items():
                    if alias_entry is entry:
                        verb = get_verb(alias_key)
                        if verb is not None:
                            canonical = alias_key
                            break
            result[canonical or key] = (entry, verb)
        return result

    def test_denominator_is_nonempty_and_known(self):
        """Vacuity guard (m-44): the scan must find the known current
        members, or the collection logic broke silently. The set GROWS as
        link/archive/restore register (Arch's memo names them) — this is a
        FLOOR, never an exact-count ratchet; lower it only if an entry was
        deliberately retired, and say why in the same commit."""
        qualifying = self._qualifying_entries()
        names = set(qualifying)
        expected_floor = {
            "update_document_query",
            "comment_issue_query",
            "update_issue",
            "create_issue",
            "create_reminder",
            "create_todo",
            "complete_todo",
            "set_default_repo",
            "set_timezone",
            "delete_todo",
        }
        missing = expected_floor - names
        assert not missing, (
            f"Expected WRITE/allowlisted-DESTRUCTIVE rail entries missing "
            f"from the scan: {missing}. Either the collection logic broke, "
            f"or one of these entries was deliberately retired (update this "
            f"floor in the same commit if so)."
        )

    def test_every_write_or_allowlisted_destructive_entry_has_a_verb(self):
        """A qualifying entry with NO registered Verb cannot be checked at
        all — that is a coverage gap in ``ACTION_TO_VERB``
        (``action_registry.validate_verb_coverage``'s OWN scope), never a
        reason to work around it here."""
        qualifying = self._qualifying_entries()
        unverbed = {
            name: entry.effect.name for name, (entry, verb) in qualifying.items() if verb is None
        }
        assert not unverbed, (
            f"WRITE/allowlisted-DESTRUCTIVE rail entries with no registered "
            f"Verb (action_registry.ACTION_TO_VERB): {unverbed}. Add the "
            f"verb mapping there — this test cannot evaluate _EXECUTE_RE "
            f"coverage without one."
        )

    def test_every_qualifying_verb_classifies_execute(self):
        """THE mechanical ratchet Arch's ruling asked for: every WRITE (or
        allowlisted DESTRUCTIVE) rail entry's registry verb, said as a bare
        imperative, must classify EXECUTE through the REAL gate classifier
        — never a hand list. A future WRITE entry (link_repo,
        archive_project, restore_project — Arch's own named examples)
        registering without its verb in ``_EXECUTE_RE`` fails HERE, at the
        moment it is added, not after a live phrasing regression ships
        (``complete_todo``'s own history, this unit)."""
        from services.intent_service.collaboration_gate import (
            FRAMING_EXECUTE,
            classify_framing,
        )

        qualifying = self._qualifying_entries()
        failures = {}
        for name, (entry, verb) in qualifying.items():
            if verb is None:
                continue  # reported as its own failure by the sibling test above
            if name in self.EXEMPT_ALLOWLISTED_DESTRUCTIVE:
                continue
            phrase = f"{verb.value} the item"
            framing = classify_framing(phrase)
            if framing != FRAMING_EXECUTE:
                failures[name] = (verb.value, phrase, framing)
        assert not failures, (
            f"WRITE/allowlisted-DESTRUCTIVE rail entries whose registry verb "
            f"does not classify EXECUTE via "
            f"collaboration_gate.classify_framing: {failures}. Add the verb "
            f"to _EXECUTE_RE (collaboration_gate.py), or add a NAMED, "
            f"REASONED exemption to EXEMPT_ALLOWLISTED_DESTRUCTIVE above "
            f"ONLY if Arch's framing-invariant DESTRUCTIVE contract "
            f"(consent_gate.decide_consent) supports it — never silently "
            f"skip."
        )

    def test_exemption_list_stays_accurate(self):
        """The exemption dict must name entries that (a) actually exist in
        scope and (b) actually still fail the classify-EXECUTE check — a
        stale exemption (the underlying gap got fixed, or the entry was
        retired) would hide nothing real and must be removed in the same
        commit it goes stale."""
        from services.intent_service.collaboration_gate import (
            FRAMING_EXECUTE,
            classify_framing,
        )

        qualifying = self._qualifying_entries()
        for name in self.EXEMPT_ALLOWLISTED_DESTRUCTIVE:
            assert name in qualifying, (
                f"EXEMPT_ALLOWLISTED_DESTRUCTIVE names {name!r}, which is no "
                f"longer in scope — remove the stale exemption."
            )
            entry, verb = qualifying[name]
            assert verb is not None, f"{name} has no verb — its exemption is moot."
            phrase = f"{verb.value} the item"
            assert classify_framing(phrase) != FRAMING_EXECUTE, (
                f"{name}'s verb {verb.value!r} now classifies EXECUTE — the "
                f"gap this exemption documented is FIXED. Remove the "
                f"exemption from EXEMPT_ALLOWLISTED_DESTRUCTIVE in the same "
                f"commit."
            )

    # ------------------------------------------------------------------
    # Corpus-driven coverage (Arch's 2026-10-04 ruling §2, in-reply-to
    # ask-lead-to-arch-cc-cxo-cio-exec-unlink-repoint-claim-connect-corpus-
    # coverage-health-gate-inert-2026-10-04.md): "A registry-verb check
    # can't see aliases, and adding 'connect' by hand is how this recurs.
    # Extend the coverage test: for every corpus row whose expected op is a
    # rail WRITE (or allowlisted DESTRUCTIVE), classify_framing(phrase) must
    # be EXECUTE, unless the row is explicitly marked as a question/compose
    # framing. The corpus already carries the vocabulary users actually
    # use. Then add connect because the test demands it, not by
    # inspection."
    #
    # test_every_qualifying_verb_classifies_execute (above) only probes ONE
    # synthetic phrase per rail entry (f"{verb} the item") — it cannot see
    # that a REAL corpus phrase for the SAME operation uses a different
    # verb. This walks tests/fixtures/inversion_corpus_phase0.yaml instead.
    #
    # Resolution (the "resolve aliases the way the gate does" the ask named):
    # same alias map scripts/inversion_phase3_deletion_gate.py's own
    # ``expected_action_is_live`` uses (``derive_routing_grammar().
    # alias_to_canonical`` + ``get_action_workflows()``), WITH ONE NAMED
    # EXCEPTION: the legacy composite action ``manage_repos`` (Issue #862,
    # not yet re-pointed to its list_repos/link_repo/unlink_repo split —
    # Arch's 2026-10-04 §1 ruling: "Don't re-point link or list yet") has NO
    # alias entry at all (it is its own standalone ACTION_REGISTRY action,
    # CANONICAL-dispositioned, never a WORKFLOW_REGISTRY key), so it resolves
    # to itself and is invisible to a bare alias lookup — exactly the
    # "registry-verb check can't see aliases" gap this unit exists to close.
    # REPO_MANAGEMENT_PATTERNS (pre_classifier.py, Issue #862) already splits
    # into two sub-families by its OWN "# Link operations" / "# List
    # operations" comments (the third, "# Unlink operations", was carved out
    # into REPO_UNLINK_PATTERNS by this same ruling's §1 — see
    # REPO_UNLINK_PATTERNS above); a corpus row claiming manage_repos is
    # resolved to list_repos (READ, out of scope) if it matches one of the
    # 3 list literals, else link_repo (WRITE, in scope) — never re-matched
    # by a second hand-written regex, but READ via identity against the
    # production list itself (vacuity-asserted below), so a future change to
    # that list's shape fails loud here rather than drifting silently.
    def _repo_management_list_literals(self):
        """The 1 LIST-shaped literal inside REPO_MANAGEMENT_PATTERNS,
        pointed at by IDENTITY (list membership), not copied/re-derived.

        Re-derived 2026-10-09 (#1595 Phase 3, twenty-third deletion plus a
        same-day SECOND pass, rule 10): the list went 9 -> 4 -> 3. First
        pass deleted the three owner/repo link forms and the
        connect-repository form. Second pass deleted the generic
        "show|list|view|which repos" list form (its own corpus row,
        "list my repos on github", scored a plain live MATCH). Kept: 2
        link-shaped (link/add a repo to) + 1 list-shaped
        (which-repos-are-linked).

        2026-10-10 (#1973-shape restore, Lead): the connect-repository form
        is BACK (WRITE row, link_repo), so the list is 4 literals: 3
        link-shaped (link / connect / add a repo to) + 1 list-shaped."""
        from services.intent_service.pre_classifier import PreClassifier

        literals = list(PreClassifier.REPO_MANAGEMENT_PATTERNS)
        assert len(literals) == 4, (
            f"REPO_MANAGEMENT_PATTERNS has {len(literals)} literals, expected "
            f"4 (3 link-shaped + 1 list-shaped) after the 2026-10-09 rule-10 "
            f"partial deletion plus the 2026-10-10 connect restore — the link/list sub-split below "
            f"assumes this shape; update it in the same commit as whatever "
            f"changed the list."
        )
        link_literals, list_literals = literals[:3], literals[-1:]
        for lit in link_literals:
            assert "repo(?:sitory)" in lit and (
                "link" in lit or "add" in lit or "connect" in lit
            ), (
                f"REPO_MANAGEMENT_PATTERNS' first 3 literals no longer look "
                f"link-shaped ({lit!r}) — re-derive the split, don't just "
                f"update this assertion."
            )
        for expect_fragment in ("linked|connected",):
            assert any(expect_fragment in lit for lit in list_literals), (
                f"REPO_MANAGEMENT_PATTERNS' last literal no longer looks "
                f"list-shaped (missing {expect_fragment!r}) — the positional "
                f"link/list split this unit assumes has drifted; re-derive "
                f"the split, don't just update this assertion."
            )
        return list_literals

    def _corpus_rows(self):
        """Rows of ``tests/fixtures/inversion_corpus_phase0.yaml`` via
        ``yaml.safe_load``. #2073 (Arch, 2026-10-17): the builder emits
        strict YAML (every string scalar JSON-quoted) and every loader reads
        it with ``safe_load``; the regex line parser this replaced only
        unescaped ``\\"`` in the phrase. Still duplicated rather than importing
        ``scripts/`` into ``tests/`` (no shared import boundary for it).
        ``framing:`` rides the row when the builder emits it.
        """
        root = os.path.dirname(os.path.abspath(__file__))
        corpus_path = Path(root) / "fixtures" / "inversion_corpus_phase0.yaml"
        rows = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))["corpus"]
        assert len(rows) >= 400, (
            f"corpus parse found only {len(rows)} rows (expected >= 400) — "
            f"the fixture collapsed or the builder's `corpus:` shape changed; "
            f"fix the builder, don't trust a collapsed count."
        )
        return rows

    def _write_or_allowlisted_destructive_corpus_rows(self):
        """Every corpus row whose ``expected:`` field names an action that
        resolves (see class docstring above) to a rail entry with
        ``EffectClass.WRITE``, or ``EffectClass.DESTRUCTIVE`` AND
        allowlisted via ``FLIP_WRITE_ALLOWLIST`` (#1677) — Arch's §2 scope,
        verbatim. Returns a list of ``(row, canonical_name, entry)``."""
        from services.intent_service.inversion_router import derive_routing_grammar
        from services.intent_service.workflow_dispatcher import (
            FLIP_WRITE_ALLOWLIST,
            WORKFLOW_REGISTRY,
            get_action_workflows,
        )
        from services.intent_service.workflow_entries import (
            register_default_workflows,
        )
        from services.shared_types import EffectClass

        saved = dict(WORKFLOW_REGISTRY)
        try:
            register_default_workflows()
            grammar = derive_routing_grammar()
            workflows = get_action_workflows()
        finally:
            WORKFLOW_REGISTRY.clear()
            WORKFLOW_REGISTRY.update(saved)

        list_literals = self._repo_management_list_literals()

        def _in_scope(entry) -> bool:
            return entry.effect == EffectClass.WRITE or (
                entry.effect == EffectClass.DESTRUCTIVE
                and entry.flip_write_allowlist_key in FLIP_WRITE_ALLOWLIST
            )

        qualifying = []
        for row in self._corpus_rows():
            expected = row.get("expected", "")
            if not expected.startswith("action:"):
                continue
            action = expected.split(":", 1)[1]
            if action == "manage_repos":
                # The ONE named exception: resolve via the production
                # list/link sub-split (see class docstring), never a second
                # hand-matched regex copy.
                from services.intent_service.pre_classifier import PreClassifier

                is_list_shaped = PreClassifier._matches_patterns(
                    row["phrase"].lower(), list_literals
                )
                canonical = "list_repos" if is_list_shaped else "link_repo"
            else:
                canonical = grammar.alias_to_canonical.get(action, action)
            entry = workflows.get(canonical)
            if entry is None or not _in_scope(entry):
                continue
            qualifying.append((row, canonical, entry))
        return qualifying

    def test_corpus_scope_denominator_is_known(self):
        """m-44: name what this scan covers out of the corpus's total, and
        fail loud if either count collapses (parser/resolution broke)."""
        rows = self._corpus_rows()
        qualifying = self._write_or_allowlisted_destructive_corpus_rows()
        assert len(qualifying) >= 10, (
            f"only {len(qualifying)} of {len(rows)} corpus rows resolved to "
            f"a WRITE/allowlisted-DESTRUCTIVE rail entry — expected at "
            f"least 10 known members (create_reminder/create_todo/"
            f"link_repo/unlink_repo/...one each from the corpus's own "
            f"known rows); the alias-resolution scan likely broke."
        )

    def test_every_corpus_write_phrase_classifies_execute(self):
        """THE corpus-driven ratchet Arch's §2 ruling asked for. Every
        qualifying row (see _write_or_allowlisted_destructive_corpus_rows)
        must classify EXECUTE through the REAL gate classifier, unless:

        - its resolved entry is DESTRUCTIVE (CONFIRM in every framing/mode
          cell per consent_gate.decide_consent's matrix — framing cannot
          change its outcome; same reasoning as
          EXEMPT_ALLOWLISTED_DESTRUCTIVE above, applied honestly here
          rather than re-derived), or
        - the row is marked ``framing: declarative`` — then it is ASSERTED to
          read NOT-EXECUTE instead (Arch 2026-10-09; pins #1960), or
        - the row is explicitly marked ``framing: question`` (a literal
          question is legitimately AMBIGUOUS/COLLABORATE — not this
          ratchet's business; none of today's qualifying rows need this
          marker, but the field is read for the next one that does).
        """
        from services.intent_service.collaboration_gate import (
            FRAMING_EXECUTE,
            classify_framing,
        )
        from services.shared_types import EffectClass

        failures = {}
        declarative_executes = {}
        for row, canonical, entry in self._write_or_allowlisted_destructive_corpus_rows():
            if entry.effect == EffectClass.DESTRUCTIVE:
                continue
            if row.get("framing") == "question":
                continue
            phrase = row["phrase"]
            framing = classify_framing(phrase)
            if row.get("framing") == "declarative":
                # Arch 2026-10-09: a declarative / first-person-wish row is ASSERTED,
                # not exempted — it must read NOT-EXECUTE, which pins #1960's ruling
                # (ambiguous -> COLLABORATE asks first). A later vocabulary change
                # that makes it read EXECUTE fails here instead of passing silently.
                if framing == FRAMING_EXECUTE:
                    declarative_executes[phrase] = canonical
                continue
            if framing != FRAMING_EXECUTE:
                failures[phrase] = (canonical, framing)
        assert not declarative_executes, (
            f"Corpus rows marked `framing: declarative` now classify EXECUTE: "
            f"{declarative_executes}. That would skip the consent ask #1960 ruled "
            f"correct for declaratives — narrow _EXECUTE_RE, don't drop the marker."
        )
        assert not failures, (
            f"Corpus phrases resolving to a WRITE rail action that do NOT "
            f"classify EXECUTE: {failures}. Add the missing vocabulary to "
            f"_EXECUTE_RE (collaboration_gate.py), or — ONLY if the row is "
            f"genuinely phrased as a question — add `framing: question` to "
            f"the corpus row with a reason."
        )

    def test_destructive_corpus_rows_are_named_exemptions(self):
        """Every DESTRUCTIVE-resolved qualifying row's canonical action must
        be a NAMED entry in EXEMPT_ALLOWLISTED_DESTRUCTIVE (reused from the
        registry-driven tests above, never a second parallel exemption
        dict) — a new allowlisted DESTRUCTIVE action appearing in the
        corpus without a reviewed exemption is a silent gap, not a pass."""
        from services.shared_types import EffectClass

        unnamed = {
            canonical
            for _row, canonical, entry in self._write_or_allowlisted_destructive_corpus_rows()
            if entry.effect == EffectClass.DESTRUCTIVE
            and canonical not in self.EXEMPT_ALLOWLISTED_DESTRUCTIVE
        }
        assert not unnamed, (
            f"DESTRUCTIVE corpus-resolved actions with no reviewed exemption "
            f"in EXEMPT_ALLOWLISTED_DESTRUCTIVE: {unnamed}. Add a named, "
            f"reasoned entry there (or fix the gap) before this can pass."
        )


class TestInversionShadowNoExecutionBoundary:
    """#1595 Phase 1 — the SHADOW-ONLY property, enforced structurally.

    The inversion router's decision must be un-consumable by dispatch: no
    production code path may execute (or even see) a ``RoutingDecision``.
    Enforcement is an import boundary — the ONLY production module allowed to
    reference ``inversion_router`` / ``RoutingDecision`` is the async shadow
    observer ``services/intent_service/inversion_shadow.py`` (whose coroutine
    returns None and whose only side effect is a log line). The dispatch layer
    (``services/intent/intent_service.py``) may reference ONLY the observer's
    scheduler.

    Phase 2 (per-category flip) will deliberately relax this test — that
    relaxation is the reviewable act of wiring the router into dispatch.

    ⚠️ RELAXED ONCE, 2026-08-19 (#1595 Phase 2.2 flip-1 — the reviewed act
    this docstring promised): ``services/intent_service/inversion_live.py``
    joins the allowlist as the ONE live-consult module. Named file, never a
    pattern — every future consumer is its own reviewed amendment. The
    boundary's core property survives intact: the dispatch layer
    (``services/intent/intent_service.py``) still may not reference the
    router or its decision type — it consumes ``consult_inversion_live``,
    which returns a plain ``Intent`` (or None) that flows into the SAME
    action rail a classified intent uses. The decision type remains
    un-importable from dispatch code; what changed is that exactly one
    module may now translate a decision into an Intent, behind the
    DEFAULT-EMPTY ``PIPER_INVERSION_LIVE_CATEGORIES`` flag set with a
    declared-READ rail-entry guard (see inversion_live.py's docstring for
    the four dispatch conditions).
    """

    ROUTER_TOKENS_RE = re.compile(r"\binversion_router\b|\bRoutingDecision\b")
    ALLOWED_REFERRERS = {
        os.path.normpath("services/intent_service/inversion_router.py"),
        os.path.normpath("services/intent_service/inversion_shadow.py"),
        # #1595 Phase 2.2 flip-1 (2026-08-19): the sanctioned live-routing
        # consult — the single production module allowed to consume a
        # RoutingDecision and re-express it as an Intent for the existing
        # rail. Kept to EXACTLY one named module; do not widen by pattern.
        os.path.normpath("services/intent_service/inversion_live.py"),
        # Pre-claim shadow probe (2026-09-02): the #1668 mirror — an OBSERVER
        # like inversion_shadow.py (its coroutine returns None; the decision
        # is logged and dropped, never dispatched). Measurement backbone for
        # the PM-ratified 2026-08-29 pre-classifier narrowing schedule.
        # Named file, never a pattern.
        os.path.normpath("services/intent_service/preclaim_shadow.py"),
        # #1886(b) (Arch's binding ruling, 2026-10-07): the SHARED,
        # stateless armed-turn consult used by both the #1886 add-project
        # name carrier and the reminder-task carrier to decide release vs.
        # bind vs. confirm on an armed turn's answer. It calls ``route()``
        # directly (the same stateless call shape ``inversion_live.
        # read_op_claims_turn`` already uses) and NEVER dispatches — the
        # consult's result is data (``ArmedReplyOutcome``), never a
        # ``RoutingDecision`` or ``Intent`` reaching the rail from this
        # module. Named file, never a pattern, same as inversion_live.py.
        os.path.normpath("services/intent_service/armed_turn_consult.py"),
    }

    def _referrers(self):
        files_scanned = 0
        referrers = []
        for root in ("services", "web"):
            for path in glob.glob(f"{root}/**/*.py", recursive=True):
                files_scanned += 1
                with open(path, encoding="utf-8") as fh:
                    content = fh.read()
                if self.ROUTER_TOKENS_RE.search(content):
                    referrers.append(os.path.normpath(path))
        return referrers, files_scanned

    def test_only_the_shadow_observer_may_import_the_router(self):
        referrers, files_scanned = self._referrers()
        # Vacuity guards (m-44): the scan measured something, and the boundary
        # protects a module that actually exists and is actually consumed.
        assert (
            files_scanned >= 100
        ), f"boundary scan walked only {files_scanned} files — detection broken"
        assert (
            os.path.normpath("services/intent_service/inversion_router.py") in referrers
        ), "inversion_router.py missing — the boundary would be vacuously green"
        assert os.path.normpath("services/intent_service/inversion_shadow.py") in referrers, (
            "inversion_shadow.py no longer references the router — the shadow "
            "lane is dead, and this boundary test is guarding nothing (m-44)"
        )
        assert os.path.normpath("services/intent_service/inversion_live.py") in referrers, (
            "inversion_live.py no longer references the router — the Phase 2.2 "
            "live-consult lane is dead while its allowlist entry survives; "
            "either the flip was removed (then shrink ALLOWED_REFERRERS in the "
            "same commit) or the consult broke silently (m-44)"
        )
        assert os.path.normpath("services/intent_service/preclaim_shadow.py") in referrers, (
            "preclaim_shadow.py no longer references the router — the "
            "pre-claim probe lane is dead while its allowlist entry survives; "
            "either the probe was removed (then shrink ALLOWED_REFERRERS in "
            "the same commit) or it broke silently (m-44)"
        )
        offenders = sorted(set(referrers) - self.ALLOWED_REFERRERS)
        assert not offenders, (
            f"Production code outside the shadow observer references the "
            f"inversion router: {offenders}. Phase 1 is SHADOW-ONLY — routes "
            f"are logged, never executed (#1595; Arch ratification 2026-08-09). "
            f"If this is the deliberate Phase-2 flip, relax ALLOWED_REFERRERS "
            f"in the same reviewed commit that wires the dispatch."
        )

    def test_dispatch_layer_sees_scheduler_only(self):
        """intent_service.py calls the fire-and-forget scheduler (shadow) and
        the live consult (flip-1) and must be blind to the decision type: no
        router import, no awaiting the shadow task. Unchanged by the Phase-2.2
        relaxation — the consult module returns Intent-or-None, so the
        dispatch layer still never sees a RoutingDecision."""
        path = os.path.normpath("services/intent/intent_service.py")
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "maybe_schedule_shadow_check" in content, (
            "the standing shadow-check hook is gone from process_intent — "
            "the continuous falsifiability property (#1595 point 3) is dead"
        )
        assert "consult_inversion_live" in content, (
            "the #1595 Phase 2.2 flip-1 consult is gone from process_intent — "
            "the live lane's allowlist entry is guarding nothing (m-44); "
            "remove services/intent_service/inversion_live.py from "
            "ALLOWED_REFERRERS in the same commit if the flip was withdrawn"
        )
        assert not self.ROUTER_TOKENS_RE.search(content), (
            "intent_service.py references inversion_router/RoutingDecision — "
            "the dispatch layer must consume NOTHING from the router directly; "
            "only inversion_live.py may translate decisions into Intents"
        )
        assert "await maybe_schedule_shadow_check" not in content, (
            "the shadow check must be fire-and-forget — awaiting it puts the "
            "router's latency on the user's turn"
        )


class TestExtractionPatternRatchet:
    """PM-ratified 2026-08-29 (live round, in-conversation): NO MORE
    EXTRACTION-PATTERN WHACK-A-MOLE.

    The interpretation-by-pattern surfaces below have grown one regex at a
    time, each patching one live phrasing miss (#1490, #1543, #1649, #1693,
    ...). Every added pattern is a new hand-maintained micro-parser branch —
    the same architectural smell the #1124 dispatch ratchet closed for
    `elif intent.action` chains, one layer down. PM's ruling: that failure
    class becomes CORPUS DEPOSITS; argument extraction moves into the
    Inversion router's slot emission.

    ⚠️ THE DEFAULT ANSWER TO A NEW FAILING PHRASING IS A CORPUS ROW, NOT A
    PATTERN. ADDING A PATTERN REQUIRES lowering something else, or a REVIEWED
    ceiling raise WITH a corpus-deposit justification recorded in the same
    commit (why a deposit could not cover it). If you hit this ratchet while
    fixing a live phrasing miss, that is the ratchet WORKING: deposit the
    phrasing in the corpus and let the Inversion slot-emission lane learn it.

    Mechanism (mirrors TestPreFloorDispatchSiteRatchet): each named span's
    source is located by AST and its regex literals counted — list elements
    of any `*pattern*`-named list literal, plus every `re`/`_re` call whose
    pattern argument is inline (not a bare name), plus 1 for a named pattern
    CONSTANT. Ceilings are frozen at counts MEASURED 2026-08-29. LOWER them
    as extraction migrates onto the router; never raise without the review
    above.

    Vacuity guard: a named function/constant that disappears FAILS the count
    (AssertionError in the locator), so a refactor cannot silently unhook a
    surface from the ratchet.
    """

    # Frozen ceilings — MEASURED 2026-08-29 (see class docstring; the
    # tightness test below keeps these exactly equal to the actual counts,
    # so drift in either direction is loud).
    CEILINGS = {
        # Floor-internal binders (Arch 2026-10-05) — MEASURED 2026-10-05 by this
        # class's own counter; down only as #1943's router-arg flips land.
        # 9 -> 8 (2026-10-08, #1943 step 6): the #1914 ordinal binder (_ORDINAL_SHAPE_RE) retired
        # now that complete_todo is live and the router names targets.
        "todo-floor-binding": 8,
        "reminder-clear-binding": 17,
        "todo-create": 11,  # 5 + _extract_completion_text's 6, frozen at measured value 2026-09-01
        "reminder-extraction": 11,
        "issue-slot-extraction": 15,
        # 567 -> 558 (2026-09-27, #1595 Phase 3 first deletion): REMINDER_PATTERNS
        # (5 literals) + REMINDER_QUERY_PATTERNS (4 literals) emptied to []
        # (kept as tombstones — see scripts/inversion_phase3_deleted_patterns.json).
        # 567 - 5 - 4 = 558.
        # 558 -> 548 (2026-09-27, #1595 Phase 3 second deletion): TODO_QUERY_PATTERNS
        # (10 literals) emptied to [] (same tombstone form; ledger entry appended).
        # 558 - 10 = 548.
        # 548 -> 496 (2026-10-01, #1595 Phase 3 third deletion): CALENDAR_QUERY_PATTERNS
        # (52 literals) emptied to [] (same tombstone form; ledger entry appended,
        # incl. 19 documented TEMPORAL_PATTERNS known_reabsorptions, all disagreeing).
        # 548 - 52 = 496.
        # 496 -> 440 (2026-10-01, #1595 Phase 3 fourth deletion): TEMPORAL_PATTERNS
        # (56 literals) emptied to [] (same tombstone form; ledger entry appended,
        # incl. the 19 CALENDAR_QUERY_PATTERNS known_reabsorptions it claimed now
        # marked resolved, since the reclaiming list itself is gone).
        # 496 - 56 = 440.
        # 440 -> 376 (2026-10-02, #1595 Phase 3 fifth deletion): GITHUB_QUERY_PATTERNS
        # (64 literals) emptied to [] (same tombstone form; ledger entry appended,
        # incl. 1 documented STATUS_PATTERNS known_reabsorption — agreeing — for
        # "any update on the next milestone", reclaimed by STATUS_PATTERNS's
        # pre-existing \bnext milestone\b literal, previously shadowed).
        # 440 - 64 = 376.
        # 376 -> 329 (2026-10-02, #1595 Phase 3 sixth deletion): PRIORITY_PATTERNS
        # (47 literals) emptied to [] (same tombstone form; ledger entry appended,
        # incl. 2 documented misserved_at_deletion rows and — a new shape — 2
        # documented surface2_verified_at_deletion rows, Arch's condition (d): a
        # frozen N=5 surface-2 probe shows the LLM classifier reaching the same
        # FLOOR-disposition destination (get_top_priority) by category on every
        # sample, so the pattern was never load-bearing for those two phrases. 0
        # reabsorptions found post-deletion (STATUS/GUIDANCE/TODO_COMPLETE/
        # ANALYSIS patterns all checked, none reclaim).
        # 376 - 47 = 329.
        # 329 -> 277 (2026-10-02, #1595 Phase 3 seventh deletion): STATUS_PATTERNS
        # (56 literals) PARTIALLY emptied — 52 literals go, 4 SURVIVE
        # (`\bcurrent work\b`, `\bproject overview\b`, `\bproject landscape\b`,
        # `\bnext milestone\b`): the FIRST partial deletion in this epic. The
        # gate found 4 claimed rows FAIL (each a MATCH on a non-live op where a
        # frozen N=5 surface-2 probe does NOT show the LLM classifier landing
        # in STATUS on every sample), so those 4 literals' own rows stay
        # load-bearing and the literals survive; the other 52 (0 of which were
        # independently load-bearing) are deleted. Ledger entry appended with
        # `partial: true`, `surviving_literals`, and `surface2_verified_at_deletion`
        # for the 0 cross-list-shadowed rows the gate credited via a probe
        # (the 3 cross-list-shadowed unexercised literals — byte-identical
        # duplicates of the inline, non-class-attribute
        # MILESTONE_STATUS_INLINE_PATTERNS list, checked before STATUS_PATTERNS
        # — go to `shadowed_literals`, not `surface2_verified_at_deletion`: they
        # were never reachable via STATUS_PATTERNS at all, probe or no probe).
        # 329 - 52 = 277.
        # 277 -> 259 (2026-10-02, #1595 Phase 3 eighth deletion): GUIDANCE_PATTERNS
        # (21 literals) PARTIALLY emptied — 18 literals go, 3 SURVIVE
        # (`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`):
        # the SECOND partial deletion in this epic. The gate found 3 claimed rows
        # FAIL (each a MATCH on a non-live op where a frozen N=5 surface-2 probe
        # shows the LLM classifier landing EXECUTION 10/10, never GUIDANCE), so
        # those 3 literals' own rows stay load-bearing and survive; the other 18
        # (all exercised 1:1 by a claimed row, no cross-list shadowing, 17
        # surface-2-verified into GUIDANCE, 1 misserved — `\bgetting started\b`
        # vs. ruled action:greeting) are deleted. Zero reabsorptions post-deletion
        # across all 18 deleted-literal rows (checked both entry surfaces via
        # claim_for_phrase); all 3 survivor rows remain claimed by
        # GUIDANCE_PATTERNS itself. A prior same-day attempt at a FULL deletion of
        # this list had STOPPED on a disagreeing reabsorption via
        # STATUS_PATTERNS's then-live `\bmy projects\b`/`\bmy portfolio\b`
        # literals; STATUS_PATTERNS's own seventh deletion has since removed both
        # literals, and this partial additionally keeps the collision's load-
        # bearing literals alive regardless.
        # 277 - 18 = 259.
        # 259 -> 240 (2026-10-03, #1595 Phase 3 ninth deletion): DISCOVERY_PATTERNS
        # (20 literals) PARTIALLY emptied — 19 literals go, 1 SURVIVES
        # (`\bneed\s*help\b`): the THIRD partial deletion in this epic. The gate
        # found 1 claimed row FAIL (a MISMATCH where the router declines with
        # CLARIFY@0.6 and a frozen N=10 surface-2 probe shows the LLM classifier
        # landing get_capabilities 0/10 samples), so that literal's own row stays
        # load-bearing and survives; the other 19 (all exercised 1:1 by a claimed
        # row — 0 unexercised, no shadowed_literals, no corpus deposits needed)
        # are deleted. Zero reabsorptions post-deletion across all 19
        # deleted-literal rows (checked both entry surfaces via claim_for_phrase);
        # the survivor row remains claimed by DISCOVERY_PATTERNS itself.
        # 259 - 19 = 240.
        # 240 -> 225 (2026-10-03, #1595 Phase 3 tenth deletion): TRUST_PATTERNS
        # (16 literals) PARTIALLY emptied — 15 literals go, 1 SURVIVES
        # (`\bwhy can'?t you\b`): the FOURTH partial deletion in this epic. The
        # gate found 1 claimed row FAIL (a REVIEW-disagrees row — the router
        # names get_capabilities@0.9, a live op, but the expected destination is
        # REVIEW/not-action-shaped), so that literal's own row stays load-bearing
        # and survives; the other 15 (all exercised 1:1 by a claimed row — 0
        # unexercised, no shadowed_literals, no corpus deposits needed) are
        # deleted: 14 via a plain live MATCH, 1 ("why are you always cautious
        # about this suggestion") via the mis-serve escape (TRUST_PATTERNS claims
        # explain_trust, disagreeing with the ruled action:explain_suggestion;
        # the router independently reaches explain_suggestion@0.95 live, and a
        # frozen N=10 surface-2 probe does NOT show the LLM classifier landing
        # PROVENANCE on every sample, but the mismatch is deletable regardless —
        # deleting a deterministically-wrong fallback cannot regress the row).
        # Zero reabsorptions post-deletion across all 15 deleted-literal rows
        # (checked both entry surfaces via claim_for_phrase); the survivor row
        # remains claimed by TRUST_PATTERNS itself.
        # 240 - 15 = 225.
        # 225 -> 213 (2026-10-03, #1595 Phase 3 eleventh deletion):
        # MEMORY_PATTERNS (15 literals) PARTIALLY emptied — 12 literals go, 3
        # SURVIVE (`\b(my|our) (conversation )?history\b`, `\bsearch (my
        # |our )?(conversation )?history\b`, `\bwhat (i|we)
        # (said|talked|discussed)\b`): the FIFTH partial deletion in this
        # epic. The gate found 3 claimed rows FAIL (each a row with no live
        # fallback naming the same op — "our history together has been
        # good" router=NONE, "search history for that conversation topic"
        # router=CLARIFY@0.4, "what we discussed yesterday was helpful"
        # router=NONE), so those 3 literals stay load-bearing and survive;
        # the other 11 claimed rows pass (10 via a plain live MATCH, 1
        # ("remember when we shipped the last release?") via the mis-serve
        # escape — MEMORY_PATTERNS claims get_memory, disagreeing with the
        # ruled action:check_completion_status; the router independently
        # MATCHes check_completion_status@0.85 on a non-live op, and a
        # frozen N=10 surface-2 probe does NOT show the LLM classifier
        # landing STATUS on every sample, but the mismatch is deletable
        # regardless). 1 of the 12 deleted literals
        # (`\bhow (much|far back) do you remember\b`) was UNEXERCISED by any
        # claimed row and is PROVABLY SHADOWED within this same list by its
        # own earlier sibling `\bdo you remember\b` (also deleted here, not
        # a survivor) — confirmed via PreClassifier.pre_classify_with_pattern_list
        # against candidate phrasings, never claimed by the shadowed
        # literal; no corpus deposit was needed. Post-deletion, 1 of the 11
        # deleted-literal rows is an AGREEING reabsorption ("can you show my
        # conversation history" reclaimed by the surviving `\b(my|our)
        # (conversation )?history\b` literal); the other 10 plus both of the
        # shadowed literal's candidate phrasings are genuinely UNCLAIMED
        # (checked both entry surfaces via claim_for_phrase); the 3 survivor
        # rows remain claimed by MEMORY_PATTERNS itself.
        # 225 - 12 = 213.
        # 213 -> 201 (2026-10-03, #1595 Phase 3 twelfth deletion):
        # ANALYSIS_PATTERNS (16 literals) PARTIALLY emptied — 12 literals go, 4
        # SURVIVE (`\bwhat.*obstacle\b`, `\bwhat'?s in the way\b`, `\banalyze.*
        # (?:risk|impact|blocker|bottleneck)\b`, `\bimpact analysis\b`): the
        # SIXTH partial deletion in this epic. The gate found 4 claimed rows
        # FAIL (each a MISMATCH where the router declines with CLARIFY@0.4 and
        # the pattern is the only live path: "what's the main obstacle here",
        # "what's in the way of finishing this", "let's analyze the risk
        # here", "can you run an impact analysis on this change"), so those 4
        # literals stay load-bearing and survive; the other 12 claimed rows
        # pass (11 via a plain live MATCH/REVIEW-agrees, 1 ("is there a
        # bottleneck analysis available") via the ordinary live-group MATCH
        # branch even though ANALYSIS_PATTERNS's own claim (analyze_blockers)
        # disagrees with the ruled destination (action:get_capabilities) — the
        # router independently MATCHes get_capabilities@0.92 live, so deleting
        # the pattern cannot regress a row it already mis-serves). 0 of the 16
        # literals were UNEXERCISED by any claimed corpus row — confirmed via
        # unexercised_literals("ANALYSIS_PATTERNS", lv.rows) — so no shadowing
        # audit was needed. Post-deletion, all 12 deleted-literal rows are
        # genuinely UNCLAIMED (checked both entry surfaces via
        # claim_for_phrase; zero reabsorptions); the 4 survivor rows remain
        # claimed by ANALYSIS_PATTERNS itself.
        # 213 - 12 = 201.
        # 201 -> 188 (2026-10-03, #1595 Phase 3 thirteenth deletion):
        # CONTEXTUAL_QUERY_PATTERNS (13 literals) emptied to [] (FULL
        # deletion, same tombstone form as the first seven FULL deletions).
        # The gate found 13/13 claimed rows MATCH (expected action live via
        # group -- changes_query/attention_query are both WORKFLOW-
        # disposition rail ops, live under this epic's --live set). 0 of the
        # 13 literals were UNEXERCISED by any claimed corpus row -- the
        # 2026-10-03 six-list deposits lane had already deposited a row for
        # every literal that lacked one. Zero reabsorptions post-deletion
        # across all 13 deleted-literal rows (checked both entry surfaces
        # via claim_for_phrase).
        # 201 - 13 = 188.
        # 188 -> 182 (2026-10-03, #1595 Phase 3 fourteenth deletion):
        # SESSION_ACTIVITY_QUERY_PATTERNS (6 literals) emptied to [] (FULL
        # deletion). The gate found 6/6 claimed rows MATCH or an agreeing
        # REVIEW (expected action live via group -- session_activity_query
        # is a WORKFLOW-disposition rail op, live under read_status). 0 of
        # the 6 literals were UNEXERCISED (the 2026-10-03 six-list deposits
        # lane had already filled the one gap). Zero reabsorptions
        # post-deletion across all 6 deleted-literal rows (checked both
        # entry surfaces via claim_for_phrase).
        # 188 - 6 = 182.
        # 182 -> 175 (2026-10-03, #1595 Phase 3 fifteenth deletion):
        # INSIGHT_PULL_PATTERNS (7 literals) emptied to [] (FULL deletion).
        # The gate found 8/8 claimed rows MATCH or an agreeing REVIEW
        # (expected action live via group -- pull_insights is FLOOR-
        # disposition with no WorkflowEntry, live here only because
        # READ_FLOOR itself joined CURRENT_LIVE_CATEGORIES on 2026-10-03).
        # 0 of the 7 literals were UNEXERCISED. ONE disagreeing reabsorption
        # found post-deletion ("what insights do you have about my
        # productivity" reclaimed by PRODUCTIVITY_QUERY_PATTERNS as
        # productivity_query) -- temporary and self-resolving: PRODUCTIVITY_
        # QUERY_PATTERNS is itself deleted as this same batch's seventeenth
        # deletion; the row's own frozen router evidence (MATCH@0.95, live)
        # independently proves it safe regardless. See the ledger's
        # known_reabsorptions for full detail.
        # 182 - 7 = 175.
        # 175 -> 170 (2026-10-03, #1595 Phase 3 sixteenth deletion):
        # GET_DEFAULT_REPO_PATTERNS (5 literals) emptied to [] (FULL
        # deletion). The gate found 5/5 claimed rows MATCH or an agreeing
        # REVIEW (expected action live via group -- get_default_repo is a
        # WORKFLOW rail op, live). 1 of the 5 literals (\bwhat\s+default\s+
        # repo(?:sitory)?\b) was UNEXERCISED and PROVABLY SHADOWED by its
        # own earlier sibling -- the shadower is deleted alongside it (both
        # go together), no corpus deposit needed. Zero reabsorptions
        # post-deletion across all 5 deleted-literal rows.
        # 175 - 5 = 170.
        # 170 -> 166 (2026-10-03, #1595 Phase 3 seventeenth deletion):
        # PRODUCTIVITY_QUERY_PATTERNS (4 literals) emptied to [] (FULL
        # deletion). The gate found 5/5 claimed rows MATCH or an agreeing
        # REVIEW (expected action live via group -- productivity_query is a
        # WORKFLOW rail op, live). One row ("what insights do you have
        # about my productivity") is a mis-serve (this list's own claim
        # disagrees with the ruled pull_insights destination) -- the SAME
        # phrase the fifteenth deletion flagged as a temporary disagreeing
        # reabsorption onto this list; deleting this list RESOLVES it (both
        # phrases now genuinely unclaimed). Zero reabsorptions post-deletion
        # across all 5 deleted-literal rows.
        # 170 - 4 = 166.
        # 166 -> 155 (2026-10-03, #1595 Phase 3 eighteenth deletion):
        # LOCAL_GIT_STATUS_PATTERNS (12 literals) PARTIALLY emptied — 11
        # literals go, 1 SURVIVES (`\bbehind (?:main|origin|upstream|
        # master)\b`): the SEVENTH partial deletion in this epic. The gate
        # found 1 claimed row FAIL (a MISMATCH where the router names
        # analyze_blockers@0.72, below the 0.8 dispatch threshold, so the
        # consult stands down: "are we behind upstream at all"), so that
        # literal's own row stays load-bearing and survives; the other 11
        # (all exercised 1:1 by a claimed row — 0 unexercised, no
        # shadowed_literals) are deleted: 10 via a plain live MATCH, 1 via
        # an agreeing REVIEW. Zero reabsorptions post-deletion across all
        # 11 deleted-literal rows (checked both entry surfaces via
        # claim_for_phrase); the survivor row remains claimed by
        # LOCAL_GIT_STATUS_PATTERNS itself. This is the final list in
        # #1595 Phase 3's 2026-10-03 thirteenth-through-eighteenth dispatch
        # batch.
        # 166 - 11 = 155.
        # 155 -> 149 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # IDENTITY_PATTERNS (6 literals) emptied to [] (FULL deletion, same
        # tombstone form). Gate (--list IDENTITY_PATTERNS --live
        # read_status,read_referent,read_synthesis,create_todo,
        # create_reminder,read_strategic,read_temporal,delete_todo,
        # read_floor,read_floor_2,read_canonical,read_portfolio,
        # complete_todo): GO, 6/6 corpus rows claimed, all [OK] -- 1
        # pre-existing probe row ("who are you?", REVIEW-agrees) plus 5 rows
        # from the same-day rule-10 corpus deposit (PPM-ruled, scored on the
        # served model), 4 via a plain live MATCH and 1 ("what do you do")
        # via a MISMATCH whose router route (get_capabilities) is itself
        # live via the same read_floor_2 group. 0 unexercised literals
        # (rule 10 satisfied). Zero reabsorptions post-deletion.
        # 155 - 6 = 149.
        # 149 -> 143 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # FEATURE_INFO_PATTERNS (6 literals) emptied to [] (FULL deletion,
        # same tombstone form). Gate: GO, 6/6 corpus rows claimed, all [OK]
        # -- 1 pre-existing probe row ("tell me more about the github
        # integration", REVIEW-agrees) plus 5 rows from the same-day
        # rule-10 corpus deposit, all via a plain live MATCH -- expected
        # action live via the same read_floor_2 group IDENTITY_PATTERNS'
        # deletion also relies on (get_feature_info's rail entry). 0
        # unexercised literals. Zero reabsorptions post-deletion.
        # 149 - 6 = 143.
        # 143 -> 140 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # STAKEHOLDER_UPDATE_PATTERNS (4 literals) PARTIALLY emptied -- 3 of
        # 4 literals deleted, 1 load-bearing literal SURVIVES (`\bwrite\s+
        # (?:me\s+)?(?:a|an)?\s*(?:\w+\s+){0,3}update\s+for\b`). BEFORE gate
        # read GO (full, 5/5 claimed rows [OK]) -- but a non-corpus
        # end-to-end regression test (test_pre_classifier_stakeholder_
        # update_1256.py::test_judge_experiment_query_routes_to_
        # stakeholder_update) FAILED when the "write ... update for"
        # literal was emptied: the phrase mis-routed to
        # update_document_query (DOCUMENT_QUERY_PATTERNS' loose "update ...
        # with" regex re-claimed it), reopening the original #1256
        # production bug. Rule 10(B): that literal RESTORED (and only it),
        # converting the deletion from FULL to PARTIAL. The other 3
        # literals deleted (own corpus rows score MATCH live via
        # read_floor_2, no end-to-end test depends on them).
        # 143 - 3 = 140.
        # 140 -> 135 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # REPO_MANAGEMENT_PATTERNS (9 literals) PARTIALLY emptied -- 5 of 9
        # literals deleted, 4 load-bearing literals SURVIVE (the bare
        # "repo(sitory)" link/add forms and both list forms). BEFORE gate
        # read GO (partial): 3 of the 5 deleted rows pass via the
        # mis-serve escape (claim manage_repos disagrees with ruled
        # link_repo; link_repo has no live token, surface-2 probe shows no
        # WRITE/DESTRUCTIVE op), 1 via a live-group MISMATCH
        # (get_contextual_guidance, live via read_canonical), 1 via a
        # plain live MATCH (list_repos, live via read_portfolio). 0
        # unexercised literals. No rule-10(B) restores needed -- all 7
        # affected test assertions converted cleanly under rule 10(A),
        # every decline confirmed empirically (no reabsorption, no
        # production misroute).
        # 140 - 5 = 135.
        # 135 -> 132 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # PROVENANCE_PATTERNS (8 literals) PARTIALLY emptied -- 3 of 8
        # literals deleted, 5 load-bearing literals SURVIVE (the
        # "where did...", "how did you know...", "why.*on list/radar/
        # mind", and both "based on" literals). BEFORE gate read GO
        # (partial): 4 claimed rows FAIL (each a MISMATCH where the
        # router declines CLARIFY -- the pattern is the live path), so
        # those literals stay load-bearing. Of the 3 deleted rows: 1 is a
        # pre-existing probe row (REVIEW-agrees, live via read_floor_2), 2
        # are the same-day rule-10 deposit (1 plain live MATCH, 1
        # live-group MISMATCH where the router's own route, explain_trust,
        # is live via the same group). 0 unexercised literals. No
        # rule-10(B) restores needed -- every affected test assertion
        # converted cleanly under rule 10(A).
        # 135 - 3 = 132.
        # 132 -> 130 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # TODO_COMPLETE_PATTERNS (7 literals) PARTIALLY emptied -- 2 of 7
        # literals deleted ("finish todo\b" and "complete todo\b", the
        # bare "todo-immediately-after-the-verb" forms), 5 load-bearing
        # literals SURVIVE. BEFORE gate read GO (partial): 11 claimed rows
        # FAIL (mostly UNSCORED multi-item/clear-family phrasings), all
        # claiming the 5 survivors. Both deleted literals' own rows
        # ("finish todo about deployment", "complete todo for the deploy
        # checklist", both today's rule-10 deposit) MATCH live via the
        # complete_todo operation directly. 0 unexercised literals. No
        # rule-10(B) restores needed.
        # 132 - 2 = 130.
        # 130 -> 129 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion):
        # PORTFOLIO_PATTERNS (16 literals) PARTIALLY emptied -- 1 of 16
        # literals deleted (the "search projects for Y" form), 15
        # load-bearing literals SURVIVE. Per PM/PPM ruling, delete/remove/
        # get-rid-of are named survivors until #1935 regardless of the
        # gate's own per-literal verdict; hide/put-away/add/new-project
        # are held or survivors per the gate's own read. The ONLY
        # deletable literal's own corpus row ("search projects for
        # budget", today's rule-10 deposit) is a plain live MATCH
        # (search_projects, live via read_portfolio). 0 unexercised
        # literals. No rule-10(B) restores needed.
        # 130 - 1 = 129.
        # 129 -> 125 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion,
        # second pass): the completion-pattern list (Issue #904, Query #55
        # in pre_classifier.py) PARTIALLY emptied further -- 4 MORE of its
        # remaining 5 literals deleted, 1 load-bearing literal SURVIVES
        # ("mark done"). Lead's same-day score of the 12 previously-
        # UNSCORED claimed rows (12/12 MATCH, served model, per-row,
        # inversion-phase3-unscored-rows-score-2026-10-09-anthropic.md)
        # licensed this pass. BEFORE gate read GO (partial): 14/15 claimed
        # rows OK, 1 FAIL (the survivor's own row, router declines
        # CLARIFY). All 14 newly-licensed rows MATCH or agreeing-REVIEW,
        # live via the complete_todo operation directly. 0 unexercised
        # literals. No rule-10(B) restores needed.
        # 129 - 4 = 125.
        # 125 -> 124 (2026-10-09, #1595 Phase 3, rule-10-licensed deletion,
        # second pass): REPO_MANAGEMENT_PATTERNS (Issue #862) PARTIALLY
        # emptied further -- 1 MORE of the remaining 4 literals deleted
        # (the "show/list/view/which repos" form), 3 load-bearing literals
        # SURVIVE. Lead's same-day score of the 12 previously-UNSCORED
        # claimed rows licensed this pass: BEFORE gate read GO (partial),
        # 2/5 claimed rows OK, 3 FAIL (the 3 remaining survivors' own
        # rows). The deleted literal's own row ("list my repos on
        # github") is a plain live MATCH, live via read_portfolio
        # (list_repos' own rail entry). 0 unexercised literals. No
        # rule-10(B) restore needed. A SEPARATE attempt this same day to
        # delete STAKEHOLDER_UPDATE_PATTERNS' sole remaining literal
        # ("write ... update for") was ALSO licensed by the gate (its own
        # #1256 phrase scored MATCH@0.95 as its own corpus row) but
        # EMPIRICALLY reopened the original #1256 production bug when
        # tried (PreClassifier.pre_classify on the exact #1256 phrase
        # returned update_document_query, not write_stakeholder_update) --
        # restored unchanged, filed as discovered work (GH #1971): the
        # gate's per-row score cannot see a DIFFERENT pre-classifier list
        # intercepting the phrase first. STAKEHOLDER_UPDATE_PATTERNS'
        # ceiling contribution is UNCHANGED by this (no literal removed).
        # 125 - 1 = 124.
        #
        # 2026-10-09: GUIDANCE_PATTERNS' 3 eighth-deletion survivors
        # (`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*
        # portfolio\b`) tombstoned FULL under rule 10 — the 3 own rows plus 6
        # rule-10 pin-phrasing rows all scored MATCH get_contextual_guidance
        # 0.85-0.95 (inversion-phase3-guidance-pin-rows-score-2026-10-09-
        # anthropic.md, inversion-phase3-rule11-sweep-rows-score-2026-10-09-
        # anthropic.md). 124 - 3 = 121.
        #
        # 121 -> 127 (2026-10-10, Lead): six #1973-shape restores (Arch's
        # ruling, issue 1973 comment 6091429803), each a deleted literal put
        # back verbatim: REMINDER_PATTERNS `\\bset\\s+(?:a\\s+)?reminder\\b`
        # ("set a reminder for the dentist appointment"), PRIORITY_PATTERNS
        # `\\bwhere.*focus\\b` ("where should my focus be today"),
        # STATUS_PATTERNS `\\bupcoming milestones?\\b` ("any upcoming milestones
        # for this project") and `\\bstatus report\\b` ("I need a status
        # report"), CONTEXTUAL_QUERY_PATTERNS `\\bneeds my attention\\b` ("this
        # project needs my attention today"), REPO_MANAGEMENT_PATTERNS
        # `\\bconnect\\s+...repo...\\s+(?:to\\s+)` ("connect my repository to the
        # project"). Report: inversion-week-calendar-description-full-score-
        # 2026-10-10-anthropic.md. 121 + 6 = 127.
        #
        # 127 -> 124 (2026-10-11): COMPLETION_HISTORY partial (3 of 5).
        # 124 -> 122 (2026-10-11): STATUS partial, `\\bproject landscape\\b` and
        # `\\bupcoming milestones?\\b` (the latter under misserved_at_deletion).
        #
        # 122 -> 121 (2026-10-11): PRIORITY `\\bwhere.*focus\\b` re-deleted under
        # misserved_at_deletion (CXO withdrew the survivor status).
        #
        # 121 -> 120 (2026-10-11): PORTFOLIO partial, the show/list/view-projects
        # literal (PORTFOLIO_LIST_PATTERN constant removed with it).
        #
        # 120 -> 90 (2026-10-13, Arch decisions.log 4905a9d746): FILE_REFERENCE_PATTERNS
        # (30 literals) DELETED outright — not a routing claim (no corpus licence,
        # no ledger entry): its one reader produced a context flag and a recent-
        # uploads string that no caller consumed (no classify call site passes a
        # session; no constructor passes an event_bus). List, both helpers, the
        # classifier read and tests/domain/test_file_reference_detection.py removed;
        # the deletion gate's NOT_ROUTING dict is now empty by name.
        "pre-classifier": 90,
    }

    # The named interpretation-by-pattern spans, per surface: (file, symbols).
    SURFACE_SPANS = {
        # Arch's ruling 2026-10-05 (after PM's live round: "first three" bound
        # one item; a verb answer carrying the list fell to complete_todo('it')):
        # the FLOOR-INTERNAL interpretation regexes — the binders that decide
        # WHICH things an already-chosen action applies to — join the ratchet,
        # frozen at today's measured count, down only. Otherwise the surface-1
        # deletions just move the regexes inward. The LLM decides meaning (the
        # router's args, #1943); these shrink as those flips land.
        "todo-floor-binding": [
            (
                "services/intent_service/todo_handlers.py",
                [
                    "_QUOTE_SPAN_RE",
                    "_CLAUSE_JOINER_RE",
                    "_REMINDER_RESTATEMENT_RE",
                    "_split_completion_clause",  # 0 literals (uses the constants) — existence is the guard
                    "_extract_todo_id",
                    "_meaningful_words",
                    "_reminder_saved_message",
                    "handle_reminder_task_turn",
                ],
            ),
        ],
        "reminder-clear-binding": [
            (
                "services/intent_service/reminder_clear.py",
                [
                    "_REMINDER_NOUN_RE",
                    "_TODO_NOUN_RE",
                    "_EXPLICIT_VERB_RE",
                    "_EXCEPTION_RE",
                    "_BULK_REMINDER_PLURAL_RE",
                    "_BULK_TODO_PLURAL_RE",
                    "_QUOTED_TARGET_RE",
                    "_THE_X_TARGET_RE",
                    "_DIFFERENT_ANSWER_RE",
                    "_USUAL_ANSWER_RE",
                    "_COMPLETE_ANSWER_RE",
                    "_NEGATED_DELETE_RE",
                    "_CORRECTION_CLAIM_RE",
                    "_ORDINAL_WORD_RE",
                    "_NUMERIC_ORDINAL_RE",
                    "_OVERDUE_WORD_RE",
                    "_WORD_RE",
                    "detect_clear_family_ask",  # 0 literals — existence guards
                    "_extract_named_target",
                    "_ordinal_index",
                    "_name_index",
                    "_resolve_pick_target",
                ],
            ),
        ],
        "todo-create": [
            (
                "services/intent_service/todo_handlers.py",
                # _extract_completion_text added 2026-09-01 (coverage gap flagged by the
                # 1527 named-target lane: complete_todo's extraction was outside the frozen
                # surfaces while its siblings were ratcheted).
                [
                    "_extract_todo_text",
                    "_TODO_TOKEN",
                    "_TODO_SEP",
                    "_extract_completion_text",
                    "_extract_priority",  # #1758: word-set match, 0 regex literals — tracked, ceiling unchanged
                ],
            ),
        ],
        "reminder-extraction": [
            (
                "services/intent_service/todo_handlers.py",
                [
                    "_extract_reminder_text",
                    "_strip_trailing_time_expressions",
                    "_is_pure_time_expression",
                    "_has_time_signal",
                ],
            ),
        ],
        "issue-slot-extraction": [
            (
                "services/intent_service/drafted_issue.py",
                [
                    "_ANSWER_QSPAN",
                    "_ANSWER_MARKER_QUOTED_RE",
                    "_ANSWER_BARE_QUOTED_RE",
                    "_ANSWER_MARKER_UNQUOTED_RE",
                    "_ANSWER_METACOMMENT_RE",
                    "extract_title_answer",  # count may be 0; existence is the guard
                ],
            ),
            (
                "services/intent/intent_service.py",
                ["_slotfill_issue_request"],  # _qspan + the marker patterns live here
            ),
        ],
    }

    _PRE_CLASSIFIER_PY = "services/intent_service/pre_classifier.py"
    # Vacuity floor for the pre-classifier scan: the class held 35 `*PATTERNS`
    # lists at freeze time; a scan finding far fewer means the derivation
    # broke (renamed class / moved lists), not that patterns went away.
    _MIN_PATTERN_LISTS = 30

    _RE_METHODS = frozenset(
        {"search", "match", "fullmatch", "sub", "subn", "split", "findall", "finditer", "compile"}
    )

    # ---- counting mechanism ----

    def _find_named_node(self, tree, name):
        import ast

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                return node
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == name:
                        return node
        return None

    def _count_regex_literals(self, node) -> int:
        import ast

        count = 0
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assign):
                for target in sub.targets:
                    if (
                        isinstance(target, ast.Name)
                        and "pattern" in target.id.lower()
                        and isinstance(sub.value, (ast.List, ast.Tuple))
                    ):
                        count += len(sub.value.elts)
            elif isinstance(sub, ast.Call):
                func = sub.func
                if (
                    isinstance(func, ast.Attribute)
                    and func.attr in self._RE_METHODS
                    and isinstance(func.value, ast.Name)
                    and func.value.id in ("re", "_re")
                    and sub.args
                    and not isinstance(sub.args[0], ast.Name)
                ):
                    count += 1
        if count == 0 and isinstance(node, ast.Assign):
            # A named pattern CONSTANT (_TODO_TOKEN, _ANSWER_QSPAN, ...): the
            # assignment itself is one pattern literal.
            count = 1
        return count

    def _surface_count(self, surface: str) -> int:
        import ast

        total = 0
        for file_path, symbols in self.SURFACE_SPANS[surface]:
            with open(file_path, encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            for name in symbols:
                node = self._find_named_node(tree, name)
                assert node is not None, (
                    f"VACUITY: named extraction span `{name}` not found in "
                    f"{file_path} — a refactor moved/renamed it without "
                    f"re-pointing TestExtractionPatternRatchet. Update "
                    f"SURFACE_SPANS (and re-measure the ceiling) in the same "
                    f"commit; the ratchet must never silently unhook a surface."
                )
                total += self._count_regex_literals(node)
        return total

    def _pre_classifier_count(self) -> int:
        """Delegates to ``scripts/pattern_literal_counts.py`` (factored out
        2026-09-27, #1595 Phase 3) so this ratchet and the deletion-gate
        instrument (``scripts/inversion_phase3_deletion_gate.py``) share ONE
        per-list counting derivation instead of two copies drifting apart —
        the AST walk, the vacuity guard, and the ≥30-list floor are
        byte-identical to the pre-factor inline scan."""
        import sys

        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, _root)
        sys.path.insert(0, os.path.join(_root, "scripts"))
        import pattern_literal_counts

        assert pattern_literal_counts.MIN_PATTERN_LISTS == self._MIN_PATTERN_LISTS, (
            "pattern_literal_counts.MIN_PATTERN_LISTS drifted from "
            "TestExtractionPatternRatchet._MIN_PATTERN_LISTS — keep them equal."
        )
        # module's own default path resolution (REPO_ROOT from its __file__)
        # points at the same file self._PRE_CLASSIFIER_PY names relatively —
        # pass it explicitly so a worktree-relative cwd never causes drift.
        return pattern_literal_counts.total_literal_count(Path(_root) / self._PRE_CLASSIFIER_PY)

    def _all_counts(self) -> dict:
        counts = {surface: self._surface_count(surface) for surface in self.SURFACE_SPANS}
        counts["pre-classifier"] = self._pre_classifier_count()
        return counts

    # ---- the tests ----

    def test_no_new_extraction_patterns(self):
        """Fails if any interpretation-by-pattern surface GREW.

        The default answer to a new failing phrasing is a CORPUS ROW (the
        Inversion router's slot emission learns it), not a new regex here.
        A ceiling raise requires review + a corpus-deposit justification in
        the same commit (PM-ratified 2026-08-29).
        """
        counts = self._all_counts()
        over = {s: (n, self.CEILINGS[s]) for s, n in counts.items() if n > self.CEILINGS[s]}
        assert not over, (
            f"Extraction-pattern ratchet exceeded: "
            f"{ {s: f'{n} > ceiling {c}' for s, (n, c) in over.items()} }. "
            f"A new regex pattern in an interpretation surface is the "
            f"whack-a-mole class PM retired 2026-08-29: deposit the failing "
            f"phrasing as a corpus row and let the Inversion slot-emission "
            f"lane cover it. If a pattern is genuinely unavoidable, lower "
            f"another surface or raise the ceiling in a REVIEWED commit that "
            f"records why a corpus deposit could not cover it."
        )

    def test_extraction_ratchet_stays_tight(self):
        """Ceilings must equal actual counts — a loose ceiling silently
        permits regressions up to the slack (same rule as
        TestPreFloorDispatchSiteRatchet.test_ratchet_target_stays_tight).
        When migration onto the router lowers a real count, lower the
        CEILINGS entry to match in the same commit."""
        counts = self._all_counts()
        drift = {s: (n, self.CEILINGS[s]) for s, n in counts.items() if n != self.CEILINGS[s]}
        assert not drift, (
            f"Ratchet drift: actual vs frozen ceiling differs: "
            f"{ {s: f'actual {n}, ceiling {c}' for s, (n, c) in drift.items()} }. "
            f"If a migration just LOWERED a count, set the CEILINGS entry to "
            f"the new number in this commit so the ratchet stays tight."
        )

    def test_named_spans_still_exist(self):
        """Explicit vacuity check: every named span resolves. (The counters
        assert this too; this test makes a disappeared symbol fail with its
        own name in the test report rather than inside a count.)"""
        import ast

        missing = []
        for surface, spans in self.SURFACE_SPANS.items():
            for file_path, symbols in spans:
                with open(file_path, encoding="utf-8") as fh:
                    tree = ast.parse(fh.read())
                for name in symbols:
                    if self._find_named_node(tree, name) is None:
                        missing.append(f"{surface}: {name} ({file_path})")
        assert not missing, (
            f"Named extraction spans no longer resolve: {missing}. Update "
            f"SURFACE_SPANS + re-measure ceilings in the same commit — the "
            f"ratchet must never silently unhook a surface."
        )


class TestAcceptanceContractRatchet:
    """#1739 — THE acceptance contract's adoption ratchet (Arch condition (c)).

    Arch ruling 2026-09-09: "Enumerate the armed seams; each is either
    predicate-consulting or in the set with its tracking issue; the set only
    shrinks, and any NEW seam with bespoke acceptance logic fails the build
    listing itself. Without this, the contract is a convention — and a
    convention is not a model (m-53): skipping the predicate must break the
    build visibly, or adoption will decay per-seam the way every bolt-on
    does."

    THE MECHANISM: an acceptance consultation is detectable at two
    signatures —

    1. a CALL to a legacy detector (``detect_offer_response(`` /
       ``detect_confirm_response(``) outside their definition/alias module
       (``soft_invocation.py``). Every such (file, detector) pair must be in
       ``KNOWN_UNADOPTED_DETECTOR_SITES``.
    2. a REFERENCE to the acceptance vocabulary (``ACCEPT_PATTERNS`` /
       ``DECLINE_PATTERNS`` / ``CONFIRM_ACCEPT_RE`` / ``_CONFIRM_ACCEPT_WORD``)
       outside the two contract modules (``soft_invocation.py`` declares it,
       ``acceptance.py`` composes it) — a bespoke regex copy or a private
       vocabulary. Every such file must be in
       ``KNOWN_BESPOKE_VOCABULARY_FILES``.

    Both baselines are SHRINK-ONLY (the KNOWN_UNMIGRATED / MAX_DISPATCH_SITES
    idiom): migrate a seam onto ``acceptance.evaluate_acceptance`` and remove
    its row in the same commit; never add a row.

    ADOPTION STATUS TABLE (#1739, updated 2026-09-10 — the bookkeeping Arch
    asked for; per-seam, most seams below are file-granular here because the
    scan is file-granular):

    ============================================  ======  ==========  =======================
    seam                                          tier    status      input-adequacy (#1665)
    ============================================  ======  ==========  =======================
    standup REFINING tail (conversation_handler)  READ    ADOPTED     asks stored + det. default
    generic offer seam, READ kinds (intent_svc)   READ    ADOPTED     "question" on the record
    contextual last_offer binding (intent_svc)    READ    ADOPTED     LastOffer.offer_text
    soft-offer arm site (intent_svc)              READ    ADOPTED     "question" added 09-09
    confirm-workflow seam (intent_svc)            DESTR   ADOPTED     "question" threaded 09-10
    destructive_confirm module residues           DESTR   ADOPTED     (via the confirm seam)
    drafted_issue file-confirm decision           W/OUT   ADOPTED     "question" threaded 09-10
    repo_clarification accept/decline decision    W/OUT   ADOPTED     "question" threaded 09-10
    standup overdue-todo offer answers (int_svc)  W/PRIV  ADOPTED     "question" on the record
    #1591 interview-invitation answers (int_svc)  W/PRIV  ADOPTED     "question" on the record
    #1591 mode read-back answers (int_svc)        W/PRIV  ADOPTED     "question" on the record
    reminder_clear verb/correction turns          READ*   ADOPTED     "question" threaded 09-12
    reminder time/task turns (todo_handlers)      READ    ADOPTED     "question" threaded 09-12
    resume-offer seam, #889 mechanic (int_svc)    W/PRIV  ADOPTED     "question" threaded 09-12
    capped-list remainder seam (int_svc)          READ    ADOPTED     offer_text stored 09-13
    generic offer seam, other non-READ kinds      W/PRIV  UNADOPTED   blocked: LOW-tier vocab
    FTUX interview turn (first_contact)           READ    UNADOPTED   holds
    verified_inference meta/decline seam          WRITE   UNADOPTED   holds (prose opt-out)
    onboarding portfolio_handler (own vocab)      WRITE   UNADOPTED   onboarding on ice
    ============================================  ======  ==========  =======================

    2026-09-10 (DESTRUCTIVE-adjacent adoption, Arch condition (b) complete
    for the CONFIRM carrier): the confirm-workflow seam, drafted_issue's
    file-confirm, and repo_clarification's accept/decline all consult
    ``evaluate_acceptance`` directly, threading registry-declared axes and
    the arm-site's stored ask; ``detect_confirm_response`` has NO production
    callers left (it survives in soft_invocation.py as the tested
    compatibility alias only). The rows still listed for drafted_issue /
    repo_clarification / intent_service under ``detect_offer_response`` are
    NOT acceptance decisions: drafted_issue's are vocabulary SHAPE reads
    (near-accept / near-miss re-ask discrimination — they pick between
    re-ask copies, nothing fires off them), repo_clarification's is the
    ``allow_bare_token`` shape read, and intent_service's is the non-READ
    generic-kind residue whose adoption is BLOCKED on the LOW-tier greedy-row
    vocabulary tightening (CXO-owned; see
    test_low_tier_keeps_the_generic_vocabulary_including_its_greedy_residue).
    READ* = the generic-branch residue of those kinds IS adopted; the
    kind-specific handlers' own detector calls are not (reminder_clear's
    kind-specific turns adopted 2026-09-12, #1653; the todo_handlers turns
    adopted the same day, #1654 — both see below).

    2026-09-11 (PM live PARTIAL on #1617's contract behavior, v71 06:54:
    "are we done with that standup?" against the armed overdue-todo offer
    released to the classifier and fuzzy-matched as a completion attempt):
    the ``standup_complete_todo`` kind adopted at the generic seam.
    Tier judgment recorded there and here: adopted at its DECLARED axes
    (WRITE×PRIVATE → LOW_CEREMONY), NOT the stricter escape hatch for the
    blocked LOW vocabulary — the NAMED_OBJECT bar cannot parse the
    #1651-pinned verbatim acceptance "Yes mark the overdue todo done." and
    refusing it would re-release that turn to the fuzzy classifier (the
    original #1651 harm). The greedy residue the seam inherits is
    byte-identical to the legacy detector it replaced, so the accept surface
    widened by nothing; the kind inherits the CXO-owned LOW-tier tightening
    automatically when it lands. The intent_service.py
    ``detect_offer_response`` baseline row REMAINS: the OTHER non-READ /
    axis-less generic kinds still take the legacy branch — the row states
    the true remaining debt (m-44).

    2026-09-12 (#1652, the offer-flag gap's consume half): the
    ``verify_inference`` and ``standup_interview`` kinds adopted at the
    generic seam, at their DECLARED axes (WRITE×PRIVATE → LOW_CEREMONY —
    the standup_complete_todo tier judgment and zero-widening argument
    apply verbatim; the invitation's own copy teaches "just say yes", so
    the bare-affirmative bar is contract axis (b), not a loosening). Arm
    survival is the SILENT LOW-tier form (§5a): these asks hold no bound
    object, so normal processing answers their state questions correctly —
    unlike the todo kind's visible form, whose questions the classifier
    demonstrably misread. Remaining on the intent_service.py legacy branch:
    ftux and unregistered workflow types. The arm half of #1652 is
    flag-stamping only (``standup_interview_invitation_pending`` /
    ``verify_inference_read_back_pending`` join ``_apply_soft_offer``'s
    ``_pending_flags``), covering all three #1591 arm sites incl. PPM's
    empty lead.

    2026-09-12 (#1653, the confirm-greed residue's OTHER site): the
    reminder_clear kind-specific turns adopted. The verb-answer turn
    consults the predicate at the SEAM's declared axes
    (clarify_reminder_clear_verb: READ×PRIVATE → LOW_CEREMONY) with the
    arm-site's stored ask threaded; STATE_QUESTION falls through to the
    generic READ branch's SILENT §5a re-arm (stated in-branch: nothing can
    fire from the survived arm — the delete path still runs through the
    #1190 NAMED_OBJECT confirm). The verb CLAIMS are judged at their TARGET
    action's axes: delete → clear_reminders_delete (DESTRUCTIVE×PRIVATE →
    NAMED_OBJECT) takes the #1650 anchored crisp bar — the SAME
    ``_CORRECTION_CLAIM_RE``, reused, replacing the unanchored
    ``_DELETE_ANSWER_RE`` residue that let PM's live aside store a wrong
    sticky verb default; complete → complete_todo (WRITE×PRIVATE →
    LOW_CEREMONY) keeps word-level detection behind the prose floor (axis
    (c)). The correction window gets the same axis-(a) STATE_QUESTION gate
    ("delete them?" no longer arms the confirm off a question). The
    reminder_clear.py ``detect_offer_response`` row REMAINS below: its one
    call is ``_reask_verb_question_if_unrecognized``'s DEFERRAL shape read
    (returns None so the generic seam decides accepts/declines — the
    drafted_issue/repo_clarification row rationale, not an acceptance
    decision). Echo-answers at the armed delete confirm ("yes, delete
    them") stay deliberately non-firing (issue #1653 note 2; evidence-gated
    to change).

    2026-09-12 (#1654, the orphaned-clarify class's consume half): BOTH
    todo_handlers kind-specific turns adopted — the row SHRANK OUT (no
    legacy detector calls remain in the file). Each seam consults the
    predicate at its REGISTRY-DECLARED axes (clarify_reminder_task /
    clarify_reminder_time: READ×PRIVATE → LOW_CEREMONY) with the arm-site's
    stored ask threaded (#1665). STATE_QUESTION falls through to the
    generic READ branch's SILENT §5a re-arm (stated in-branch: nothing can
    fire from the survived arm — the REAL save runs only off a fresh
    answer turn). The load-bearing axis-(a) gains, all reproduced red
    first: a question the pre-classifier couldn't claim BOUND AS THE TASK
    ("what do you mean?" → "Got it — **what do you mean**"); a
    time-bearing state question SAVED A REMINDER ("did I say 3pm?" parsed
    and wrote a row); a plain question at the time seam got the re-ask
    copy instead of an answer. Zero-widening: ACCEPT at both seams only
    ever re-asks (never fires), and the crisp CONFIRM superset it adds
    used to BIND as the task text ("confirm" became a reminder), so the
    wider accept surface is a strict improvement. Question-suffixed time
    answers ("tomorrow at 9?") now cost a turn, not an action — the §5b
    trade, pinned deliberately.

    Arm-survival semantics as adopted (CXO ruling 2026-09-10, contract doc
    §5a/§5b — docs/internal/design/acceptance-contract-user-facing-2026-09-10.md):
    READ-tier arms survive a state question SILENTLY (re-armed, normal
    processing answers). CONFIRM-tier arms NEVER survive silently — a state
    question is answered by normal processing with the stored ask RE-RENDERED
    in one clause appended to the reply; the re-render is itself a new ask,
    so it arms, and the next "yes" binds to an ask the user saw THIS turn.
    No stored ask → nothing to restate → the pop stands. The
    standup_complete_todo kind (LOW tier by axes) deliberately takes the
    VISIBLE form, stated per the ruling's survival-must-be-stated clause:
    silent survival delegates the ANSWER to normal processing, and PM's live
    turn is the proof normal processing misreads this kind's state question
    as a completion attempt — questions naming the offer's referents are
    answered at the seam (standup_todo_offer.state_question_reply) with the
    ask re-rendered in the same reply; other questions re-arm with the
    confirm-style "Still pending:" suffix.

    2026-09-12 (#1753, the survival ruling's soft-offer corollary): a
    survived arm must also outlive the SAME TURN's soft-offer application.
    Survival turns compose their result in normal processing, so the
    ``_apply_soft_offer`` ``_pending_flags`` belt (which reads only
    ``result.intent_data``) structurally cannot cover them; the guard now
    also PEEKS THE STORE (read-only, #1595) before setting — any entry
    present at apply time was armed or survival-re-armed this turn (the
    store is popped before classification, #1529), so the soft offer is
    skipped honestly instead of replacing the arm in the one-slot #846
    store. The flag belt remains (#1652 pins stand). Regression:
    ``test_soft_offer_survival_clobber_1753.py``.

    2026-09-12 (#1769, the seam BOTH scans structurally missed): the
    resume-offer seam (``_check_pending_resume_offer``, the #889 mechanic)
    adopted. Its four bespoke inline word-sets called no legacy detector and
    referenced no shared vocabulary name — the stated boundary of this
    class's file scans (name-based detection cannot see inline set
    literals), found by the #1766 census build. The seam consults THE
    predicate at registry-declared axes (standup_interview: WRITE×PRIVATE →
    LOW_CEREMONY — accepting re-enters the SAME flow that entry declares;
    declining transitions the same private row to ABANDONED) with the
    arm-site's stored ask threaded (#1665, `resume_offer_question` from the
    one-turn last_offer rail). The #1529 explicit-anytime commands
    ("resume", "start over", …) became TAUGHT vocabulary threaded into the
    predicate — `taught_declines` added to `evaluate_acceptance` for the
    decline half (full-message, LOW tier only, symmetric with
    `taught_accepts`); with no offer pending the seam consults the predicate
    DIFFERENTIALLY (taught-vs-bare) so only flow-naming commands act — no
    local matcher survives. STATE_QUESTION never fires the resume; the arm
    survives in the SILENT §5a form (re-armed on the last_offer rail; the
    #1753-shape clobber residue at THIS rail is filed on #1769). NOT
    zero-widening, stated honestly: the legacy sets were exact-match, so the
    LOW-tier vocabulary (greedy residue included) widens both surfaces while
    armed — pinned deliberately in test_resume_offer_acceptance_1769.py
    (recoverable re-entry; inherits the CXO-owned tightening); "n"/"yea"
    narrowed out (bespoke-only tokens; a PASS leaves the flow suspended for
    greeting re-entry). Arm half: both #1766 census rows for this seam's ask
    sites shrank out in the same commit.

    2026-09-12 (#1770, the #1753 corollary at the SECOND one-slot store):
    the clobber residue #1769 filed is discharged. The cohort's other
    one-slot arm rail — the #852/#1529 one-turn ``last_offer`` field, where
    the resume survival re-arms — is now covered by the SAME apply-seam
    guard: ``_apply_soft_offer`` peeks BOTH stores (one block, one skip log
    naming the store), and the canonical ``offer_hint`` write is
    first-arm-wins. Same soundness argument as #1753: the rail is
    always-cleared at turn start (the #852 invariant, before every
    apply-seam call site), so any value present at either guard site was
    armed or survival-re-armed THIS turn; a stale prior-turn arm cannot
    reach the guards (no-over-block pinned). Regression:
    ``test_soft_offer_last_offer_clobber_1770.py``.

    2026-09-13 (#1762 epic 6, the FIRST seam with a PERSISTING arm): the
    capped-list remainder seam (``_check_pending_list_remainder``) adopted.
    A GitHub listing that caps its render now stores the unrendered tail
    (GatherOutcome §5b: "…and N more" is a claim the assistant must be able
    to CASH) and "show me the rest" consumes it through THE predicate at the
    arming action's REGISTRY-DECLARED axes (all six ``_READ_QUERY_COHORT``
    listings declare ``EffectClass.READ``, PRIVATE → LOW_CEREMONY), with the
    arm-site's rendered offer threaded as the stored ask (#1665). The offer's
    own copy teaches "the rest" via ``taught_accepts`` — ADDITIVE over the
    shared vocabulary, never a substitute, because CXO §5b-i decision 2 is
    that the affordance must not become a syntax (a bare "yes" still cashes;
    pinned parametrically).

    ⭐ ARM SURVIVAL, STATED — and this one is the NON-default form, so it is
    spelled out rather than inherited (the ruling's survival-must-be-stated
    clause). **PERSISTING**, not the §5a silent re-arm: a STATE_QUESTION *or
    a PASS* leaves the remainder in place, and it stays in place across
    arbitrary intervening turns. CXO's reason, which is the whole shape of
    this build: *a capped-list offer is exactly the kind a user answers
    LATE — they read the five, think, and come back*, and an acceptance test
    of "immediate next turn asks" passes without exercising the property that
    actually fails. Her tier ruling licenses it (COLLABORATE/READ arms MAY
    survive; only CONFIRM must not) and what makes it safe is that NOTHING
    CAN FIRE from it — cashing prints lines already gathered, touches no
    state, and issues no request. Bounded by: cashed, declined, replaced by a
    newer capped list, or stale past ``REMAINDER_MAX_AGE_MINUTES``.

    The store is DELIBERATELY not one of the two one-slot rails, and
    therefore deliberately NOT in the ``_apply_soft_offer`` store peek above:
    peeking a store that lives 30 minutes would suppress every soft offer for
    that whole window, which is the over-block the #1753/#1770 soundness
    argument exists to avoid. The arm TURN is covered the ordinary way, by a
    ``list_remainder_offer_pending`` flag in ``_pending_flags``. Precedence
    is explicit: the seam runs AFTER the ``last_offer`` pop and the #889
    resume check and only when neither bound, so a fresher arm always wins.

    Honest boundary, pinned rather than papered over: contract axis (a)
    means an interrogative REQUEST ("can I see the rest?") is a
    STATE_QUESTION, not an accept — the arm survives and normal processing
    answers, so nothing is lost, but it is the #1579 shape and the CONTRACT
    is where it would change, not this seam. Regression:
    ``test_cashable_list_remainder_1762.py``.
    """

    _CONTRACT_MODULES = (
        os.path.join("services", "intent_service", "soft_invocation.py"),
        os.path.join("services", "intent_service", "acceptance.py"),
    )

    # Legacy detector CALL sites: (relpath, detector) pairs. SHRINK-ONLY —
    # migrate the seam to acceptance.evaluate_acceptance (threading its
    # declared axes + stored ask), then remove its row in the same commit.
    # Tracking issue for every row: #1739.
    KNOWN_UNADOPTED_DETECTOR_SITES = frozenset(
        {
            # 2026-09-10: the three detect_confirm_response rows (this file,
            # drafted_issue, repo_clarification) shrank out — the
            # DESTRUCTIVE-adjacent adoption. The remaining
            # detect_offer_response rows for those files are documented in
            # the class docstring: shape reads + the blocked non-READ
            # generic residue, not acceptance decisions.
            ("services/intent/intent_service.py", "detect_offer_response"),
            ("services/intent_service/repo_clarification.py", "detect_offer_response"),
            ("services/intent_service/drafted_issue.py", "detect_offer_response"),
            # 2026-09-12: the todo_handlers row shrank out (#1654) — both
            # reminder question turns consult the predicate directly.
            ("services/intent_service/reminder_clear.py", "detect_offer_response"),
            ("services/intent_service/first_contact.py", "detect_offer_response"),
            ("services/intent_service/verified_inference.py", "detect_offer_response"),
        }
    )

    # Files with a PRIVATE acceptance vocabulary (bespoke regex lists) —
    # the un-modeled-noun failure profile itself. SHRINK-ONLY. Tracking: #1739
    # (portfolio onboarding is on ice per ADR-059; its vocabulary migrates or
    # dies with it).
    KNOWN_BESPOKE_VOCABULARY_FILES = frozenset(
        {
            "services/onboarding/portfolio_handler.py",
        }
    )

    _DETECTOR_CALL_RE = re.compile(r"\b(detect_offer_response|detect_confirm_response)\s*\(")
    _VOCABULARY_REF_RE = re.compile(
        r"\b(ACCEPT_PATTERNS|DECLINE_PATTERNS|CONFIRM_ACCEPT_RE|_CONFIRM_ACCEPT_WORD)\b"
    )

    def _repo_root(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _production_files(self):
        root = self._repo_root()
        for top in ("services", "web"):
            for path in glob.glob(os.path.join(root, top, "**", "*.py"), recursive=True):
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                yield rel, path

    def _detector_call_sites(self) -> set:
        found = set()
        skip = {p.replace(os.sep, "/") for p in self._CONTRACT_MODULES}
        for rel, path in self._production_files():
            if rel in skip:
                continue
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for name in set(self._DETECTOR_CALL_RE.findall(text)):
                found.add((rel, name))
        return found

    def _bespoke_vocabulary_files(self) -> set:
        found = set()
        skip = {p.replace(os.sep, "/") for p in self._CONTRACT_MODULES}
        for rel, path in self._production_files():
            if rel in skip:
                continue
            with open(path, encoding="utf-8") as fh:
                # Comment lines may NAME the vocabulary (e.g.
                # destructive_confirm.py's "#1650 rationale" note); only code
                # references are a bespoke implementation.
                code = "\n".join(
                    line for line in fh.read().splitlines() if not line.lstrip().startswith("#")
                )
            if self._VOCABULARY_REF_RE.search(code):
                found.add(rel)
        return found

    def test_scan_space_is_populated(self):
        """Vacuity guard (m-44): the scan must actually see the known world —
        an empty result set is indistinguishable from a broken scanner."""
        sites = self._detector_call_sites()
        assert ("services/intent/intent_service.py", "detect_offer_response") in sites, (
            "The detector-call scan no longer finds the generic offer seam "
            "(intent_service.py) — the scanner is measuring nothing. Fix the "
            "scan before trusting any of this class's other results."
        )

    def test_no_new_unadopted_acceptance_seams(self):
        """Arch condition (c): a NEW seam with bespoke acceptance logic fails
        the build listing itself. Consult acceptance.evaluate_acceptance
        (threading the seam's declared EffectClass + Outwardness and its
        arm-site's stored ask) instead of calling the legacy detectors."""
        new_sites = self._detector_call_sites() - self.KNOWN_UNADOPTED_DETECTOR_SITES
        assert not new_sites, (
            f"NEW legacy acceptance-detector call sites: {sorted(new_sites)}. "
            f"#1739: every armed seam consults THE acceptance predicate "
            f"(services/intent_service/acceptance.py, evaluate_acceptance) with "
            f"its declared axes and stored ask. Do NOT add rows to "
            f"KNOWN_UNADOPTED_DETECTOR_SITES — it only shrinks."
        )

    def test_no_new_bespoke_acceptance_vocabulary(self):
        """A private accept/decline vocabulary outside the contract modules is
        a bespoke acceptance implementation — the exact failure profile #1739
        exists to end (N seams, N rules)."""
        new_files = self._bespoke_vocabulary_files() - self.KNOWN_BESPOKE_VOCABULARY_FILES
        assert not new_files, (
            f"NEW bespoke acceptance-vocabulary files: {sorted(new_files)}. "
            f"The acceptance vocabularies live in soft_invocation.py and are "
            f"composed ONLY by acceptance.evaluate_acceptance (#1739). Do NOT "
            f"add rows to KNOWN_BESPOKE_VOCABULARY_FILES — it only shrinks."
        )

    def test_unadopted_baseline_stays_tight(self):
        """Shrink-only, enforced: a baseline row whose seam no longer calls a
        legacy detector is STALE — remove it in the migrating commit, so the
        baseline always states the true remaining adoption debt (m-44: the
        denominator must be real)."""
        sites = self._detector_call_sites()
        stale = self.KNOWN_UNADOPTED_DETECTOR_SITES - sites
        assert not stale, (
            f"KNOWN_UNADOPTED_DETECTOR_SITES lists seams that no longer call a "
            f"legacy detector: {sorted(stale)}. Remove the rows (the set only "
            f"shrinks)."
        )
        stale_vocab = self.KNOWN_BESPOKE_VOCABULARY_FILES - self._bespoke_vocabulary_files()
        assert not stale_vocab, (
            f"KNOWN_BESPOKE_VOCABULARY_FILES lists files with no bespoke "
            f"vocabulary left: {sorted(stale_vocab)}. Remove the rows."
        )

    def test_adopted_seams_do_not_regress(self):
        """A regressed adoption fails loudly (Arch's red-proof requirement):
        the migrated seams must still consult the predicate, and the #1617
        substring word-list must never come back."""
        root = self._repo_root()
        standup = os.path.join(root, "services", "standup", "conversation_handler.py")
        with open(standup, encoding="utf-8") as fh:
            standup_src = fh.read()
        assert "evaluate_acceptance" in standup_src, (
            "services/standup/conversation_handler.py no longer consults "
            "acceptance.evaluate_acceptance — the #1617 seam regressed off the "
            "#1739 contract (PM's live 'are we done with that standup?' fired "
            "on exactly this seam's bespoke logic)."
        )
        assert "acceptance_words" not in standup_src, (
            "The #1617 substring acceptance word-list is back in "
            "conversation_handler.py — that list is the mechanism that fired a "
            "state change on PM's question. The predicate is the only "
            "acceptance authority (#1739)."
        )
        intent_svc = os.path.join(root, "services", "intent", "intent_service.py")
        with open(intent_svc, encoding="utf-8") as fh:
            intent_src = fh.read()
        assert "evaluate_acceptance" in intent_src, (
            "services/intent/intent_service.py no longer consults "
            "acceptance.evaluate_acceptance — the READ-tier offer-seam "
            "adoption (#1739) regressed."
        )
        assert "detect_confirm_response" not in intent_src, (
            "services/intent/intent_service.py calls detect_confirm_response "
            "again — the DESTRUCTIVE-adjacent confirm-seam adoption "
            "(#1739, 2026-09-10) regressed off the predicate."
        )
        for rel in (
            os.path.join("services", "intent_service", "drafted_issue.py"),
            os.path.join("services", "intent_service", "repo_clarification.py"),
        ):
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                src = fh.read()
            assert "evaluate_acceptance" in src, (
                f"{rel} no longer consults acceptance.evaluate_acceptance — "
                "the DESTRUCTIVE-adjacent adoption (#1739, 2026-09-10) "
                "regressed."
            )
            assert "detect_confirm_response(" not in src, (
                f"{rel} calls detect_confirm_response again — its acceptance "
                "decision must route through the predicate (#1739)."
            )


class TestUnarmedAskSiteRatchet:
    """#1766 — ask-only-when-armed enforcement for the #1730 Gap-2 ruling
    (Lead proposed + Arch concurred 2026-09-12): every question-emitting site
    arms through the one-slot store (#846) or doesn't ask.

    THE CENSUS PREDICATE (Arch's ratification condition: derived MECHANICALLY,
    visible here so its coverage is arguable — a new question-emitting site
    fails the build BY BEING FOUND, never by someone remembering a table):

    Scope (#2011, Arch 2026-10-14 — widened from the two intent packages):
    every ``*.py`` under ``services/`` RECURSIVELY, minus, each BY NAME with
    its reason (never by leaving a package out of the glob):

    - ``services/intent_service/soft_invocation.py`` — the arming rail
      itself: every offer template it declares reaches the user only
      through the apply path that records + ``set_pending_offer``-arms it
      by construction;
    - ``services/standup/`` — its conversation machine arms via its own
      adopted state rail, not the one-slot store (#1739 table);
    - ``services/onboarding/`` — on ice (ADR-059);
    - ``services/consciousness/{auth,cli}_consciousness.py`` — NON-CHAT
      surfaces (#2011 call 4, Arch 2026-10-14): the login/session routes
      and terminal output (``ui_consciousness`` was ruled a third, then
      found dead and deleted, Arch round 2). The one-slot store is a
      chat mechanism. Each exclusion is held true by a CONSUMER TRIPWIRE
      (``test_2011_non_chat_surface_consumers``) pinning its measured
      importer set; a chat-path importer fails the build.

    An INTERROGATIVE LITERAL is any string constant or f-string (constant
    parts joined with ``{}`` placeholders) in which some line, after
    stripping trailing whitespace and markdown closers (``*_)`]``), ends
    with ``?`` — minimum 8 chars and containing a space (drops bare-token
    matches). NOT counted (each rule earned by a measured false-positive
    class, 2026-09-12 iteration):

    - docstrings;
    - operands of comparisons, dict KEYS, ``raise`` messages, and arguments
      to string-matcher/regex/logging calls (``endswith``/``strip``/
      ``re.search``/``logger.*`` etc.) — input matching, not emission;
    - strings flowing into an ``utterance`` parameter (kwarg ``utterance=``,
      or any argument of a corpus callable whose FIRST parameter is
      ``utterance``, e.g. ``POINTER(...)``) — sample USER phrasings;
    - holders named ``*EXAMPLE*`` (sample user messages, e.g.
      ``ACTION_EXAMPLES``) or ``*PROMPT*`` (LLM-facing template constants);
    - holders whose own name says ``question`` (``open_repo_question``,
      ``FTUX_INTERVIEW_QUESTION``, ...) — ask-copy DEFINITIONS whose
      emission lives at their consumers; every current consumer verified
      arming at freeze time (they thread the copy as the stored
      ``question=`` — itself an arm signal);
    - #2011 calibration (2026-10-14), three classes measured in the newly
      scanned packages, each a false-positive SHAPE, never a site:
      (a) strings in an ``examples=`` kwarg (any kwarg named ``*example*``)
          — sample USER phrasings, the kwarg form of the ``*EXAMPLE*``
          holder rule (e.g. ``commands/definitions.py`` IDENTITY_COMMAND
          ``examples=["who are you?", "what's your name?"]``);
      (b) strings in an ``original_message=`` kwarg — a synthesized USER
          message handed to a handler, the same class as ``utterance=``
          (e.g. ``integrations/slack/webhook_router.py``
          ``_handle_priority_subcommand``: ``Intent(...,
          original_message="what's my top priority?")``);
      (c) strings inside a container whose OWN name says ``question`` —
          an instance-attribute assignment target (``self.*question*``)
          or a dict value under a ``*question*`` key — the container form
          of the ``*question*``-named holder rule (e.g.
          ``intelligence/clarifying_questions.py``
          ``ClarifyingQuestionGenerator.__init__``:
          ``self.question_templates = {...: ["How urgent is this
          issue?", ...]}``). Local variables do NOT qualify: a local
          ``question = "…?"`` returned unarmed stays counted;
    - #2011 call 5 (Arch 2026-10-14) — OPEN INVITATIONS, a CLASS: a literal
      every one of whose question sentences is a closed-set invitation
      shape (what can I help (you) with · anything else I can help with /
      you need · what's on your mind · how does that sound · does that
      help · what would you like to work on / focus on · need anything
      else; optionally + today / now / this morning|afternoon|evening),
      carrying NO action offer (want me to · should I · shall I|we ·
      would you|you'd like me to). Any reply to such a question is a fresh
      request, so nothing needs binding. Measured both ways: EXEMPT
      ``home_state_service`` "Welcome. What can I help you with?"; COUNTED
      "How does that sound? Anything you'd like me to adjust?" (the same
      literal offers an action; measured 2026-10-14 in
      consciousness/templates.py DIALOGUE_INVITATION, the only measured
      literal of that kind, and deleted the same day with that unreachable
      module — the pin keeps its text). A
      second question of any other shape — a slot request — keeps the
      literal counted;
    - literals carrying an ``# ask-census: <reason>`` marker on their own
      line or the line directly above — the residual hand-annotation lives
      AT the site, never in this table, and the marker count is ceilinged
      below.

    A HOLDER is the enclosing function/method (qualname), or the target
    name of a module/class-level assignment (copy constants/containers).
    A holder ARMS iff its OWN body (nested defs excluded) does any of:
    call ``set_pending_offer``; pass a ``question=`` kwarg or build a dict
    with a ``"question"`` key (the #1665 stored-ask idiom); mention a
    string ending ``_pending`` (the no-clobber flag stamp); or construct a
    ``LastOffer(...)`` (#2011 calibration: the #852/#1529 one-turn
    ``last_offer`` rail, the SECOND one-slot arm store per #1770 — e.g.
    ``conversation/conversation_handler.py``
    ``ConversationHandler._check_suspended_session_reentry`` stores its
    "Welcome back! … Would you like to continue, or start fresh?" as
    ``LastOffer(offer_type="process_resume", offer_text=resume_message)``,
    the same holder that renders it); or call ``_track_offer_hint(`` (#2010
    signal (i), Arch 2026-10-15: it converts an ``offer_hint`` into that same
    ``LastOffer`` — the call is the arm); or build an ``"offer_hint"`` key, as
    a dict-literal key or ``x["offer_hint"] = …`` (#2010 signal (ii): the
    #852 idiom, which ``_track_offer_hint`` turns into ``LastOffer`` at the
    seam the result reaches). Signal (ii) has two conditions: REACH — it is
    credited only in ``_OFFER_HINT_BUILDER_MODULES``
    (``canonical_handlers.py``), whose builders were measured to reach a
    tracking seam (``CanonicalHandlers.handle`` dispatch, tracked in
    ``_process_intent_internal``, or a pinned rail adapter returning
    through ``_finalize_canonical_rail_result``); a new builder module, or a
    new external caller of a builder or of any in-class method that
    transitively reaches one (#2024 (b)), fails
    ``test_2010_offer_hint_reach_tripwire``.
    ADEQUACY (#1739 (a)) — the judge reads ``offer_text`` as the held
    question, so a holder armed by (ii) alone has its row removed only if
    every question sentence its literals render is verbatim a question
    sentence of an ``offer_text`` it builds; otherwise the row stays and the
    mismatch is reported in ``stats["offer_text_mismatch"]``. And an
    ``offer_text`` must itself be a question (#2024 (a), Arch 2026-10-15: an
    offer is ONE yes/no question; a directive or statement binds no "yes"):
    a non-question constant fails ``test_2024_offer_text_is_a_question``,
    naming holder and line. A function
    consumer-armed (below) through a (ii)-only caller is pinned and audited
    in ``test_2010_offer_hint_consumer_adequacy``. Or assign
    ``<x>.filling_state = SlotFillingState.PROMPTING|CONFIRMING`` (#2011
    call 2, Arch 2026-10-14: the slot-filling machine's transition into an
    answer-binding state — the next reply is routed by that state to the
    handler that binds it; terminal COMPLETE/CANCELLED are not arms, so
    ``_SLOT_MESSAGES``' post-terminal "wrapped up! Want to start a new
    one?" stays counted). CONSUMER-ARMED (one hop, #2011 call 2; four
    bounds blessed by Arch round 2, each pinned in
    test_2011_one_hop_bounds): a MODULE-LEVEL function is treated as
    arming iff (1) at least one caller exists and EVERY caller arms by its
    own body; (2) callers are searched across ``services/**``, ``web/**``
    and ``main.py`` — a caller in an excluded package still counts; (3)
    test callers count neither way; (4) a function referenced other than
    by a direct call (callback, dict value, getattr) has unknown callers
    and is NOT armed; one hop only, never transitive. Measured:
    ``slot_prompts.format_final_confirmation`` (called only by
    ``_determine_next_step`` / ``_handle_confirming``, which enter/hold
    CONFIRMING). The census is every
    holder with >= 1 interrogative literal that does not arm.

    KNOWN_UNARMED_ASK_SITES starts at the census MEASURED 2026-09-12
    (measured, never base-minus-predicted) and is SHRINK-ONLY — the
    KNOWN_UNADOPTED_DETECTOR_SITES / KNOWN_UNMIGRATED mechanics. Arm a
    site (store the rendered ask + arm the one-slot store, or delete the
    ask) and remove its row in the same commit. A row is
    (file, holder, literal-count, fingerprint): copy edits or NEW ask copy
    inside an already-listed holder change the row and fail the tightness
    test — an unarmed site's ask copy cannot drift silently.

    PRESENT-NOT-ENFORCED BOUNDARY (requirement 3, stated honestly — the
    predicate is fully mechanical over its scope; these are the edges of
    that scope, each carried here so "complete for the space it searched"
    stays visible, m-44):

    1. SCOPE: ``services/**`` (#2011). Question-emitting code elsewhere is
       not censused: ``services/standup/`` (its conversation machine arms
       via its own adopted state rail, not the one-slot store — #1739
       table), onboarding (on ice, ADR-059), the two non-chat
       consciousness modules (tripwired, #2011 call 4), web templates, ``web/`` and
       ``main.py``, and above all LLM FREE TEXT — the conversational floor can generate
       a question in prose at runtime; no static census can see it. Those
       surfaces' ask-only-when-armed compliance is Present, not Enforced.
    2. GRANULARITY: holder-level. A holder that arms on one path is
       treated as arming all its asks — a mixed function with an armed ask
       on path A and an unarmed ask on path B under-reports B (this is the
       same granularity the acceptance-contract file scan accepts).
    3. The ``*question*``-named copy-helper exemption trusts the consumer:
       a FUTURE consumer that emits such a helper's copy without arming
       holds no literal of its own and escapes the census.
    4. FIRST-ARM-WINS (#2010 signal (ii), Arch 2026-10-15): under #1770,
       ``_track_offer_hint`` SKIPS the hint on a turn where a live same-turn
       arm already holds the one-turn rail. The census still reads the
       builder holder as armed, but on that turn its question renders
       unbound. Rare (it needs a surviving arm plus a canonical answer);
       the same holder-level granularity as item 2.
    """

    # #2011 (Arch, 2026-10-14): was services/intent_service/*.py +
    # services/intent/*.py only; 67 holder sites in packages it neither
    # scanned nor named escaped it. Recursive over all of services/ now.
    _SCAN_GLOBS = (os.path.join("services", "**", "*.py"),)

    _EXCLUDED_MODULES = frozenset(
        {
            "services/intent_service/soft_invocation.py",
            # #2011 call 4 (Arch 2026-10-14): NON-CHAT SURFACES, excluded by
            # name. The one-slot store is a chat mechanism; these modules'
            # copy never reaches a chat reply. Each exclusion is held TRUE by
            # a consumer tripwire (test_2011_non_chat_surface_consumers): if a
            # chat path ever imports one, the build fails and the exclusion
            # must be re-ruled.
            #  (ui_consciousness was a third, until Arch's round-2 correction:
            #  its template mentions were Jinja comments — it was dead, and
            #  was deleted.)
            #  - auth_consciousness: login/session pages (web/api/routes/auth.py);
            #  - cli_consciousness: terminal output of main.py.
            "services/consciousness/auth_consciousness.py",
            "services/consciousness/cli_consciousness.py",
        }
    )

    # #2011 call 4: the measured importer set per excluded non-chat module
    # (production code only — tests/ and dev/ excluded). `git grep` 2026-10-14.
    _NON_CHAT_SURFACE_IMPORTERS = {
        "auth_consciousness": frozenset(
            {"services/consciousness/__init__.py", "web/api/routes/auth.py"}
        ),
        "cli_consciousness": frozenset({"services/consciousness/__init__.py", "main.py"}),
    }

    # #2011 call 2: SlotFillingState members whose assignment arms (the reply
    # is bound by the PROMPTING/CONFIRMING handler).
    _SLOT_ARM_STATES = frozenset({"PROMPTING", "CONFIRMING"})

    # #2010 signal (ii) (Arch 2026-10-15, condition 1): a built "offer_hint"
    # key arms only in the modules whose builders were MEASURED to reach a
    # tracking seam (CanonicalHandlers.handle dispatch, tracked in
    # IntentService._process_intent_internal, or a rail adapter returning
    # through _finalize_canonical_rail_result). Held true by
    # test_2010_offer_hint_reach_tripwire.
    _OFFER_HINT_BUILDER_MODULES = frozenset({"services/intent_service/canonical_handlers.py"})
    # The measured EXTERNAL referrers (outside the builder modules) of every
    # builder holder AND of every in-class method that TRANSITIVELY reaches
    # one (#2024 hardening (b), Arch 2026-10-15). Measured 2026-10-15 after
    # #2024 dropped the archive/restore/search not-found hints (those three
    # adapters were the #2010 set and are no longer builders' callers): one
    # referrer, the read_canonical string table, whose
    # "_handle_guidance_query" reaches _format_project_setup_guidance,
    # _handle_project_setup_request and _format_integration_setup_guidance
    # in-class. Its adapter getattr-dispatches the name and returns through
    # _finalize_canonical_rail_result (check (c)).
    _OFFER_HINT_EXTERNAL_CALLERS = frozenset(
        {
            ("services/intent_service/workflow_entries.py", "_READ_CANONICAL_MEMBERS"),
        }
    )
    # A pinned referrer that is a NAME TABLE (strings dispatched by getattr)
    # maps to the adapter holder that dispatches it; (c) checks that adapter.
    _OFFER_HINT_TABLE_ADAPTERS = {
        (
            "services/intent_service/workflow_entries.py",
            "_READ_CANONICAL_MEMBERS",
        ): "_make_read_canonical_entry_point.run_read_canonical_workflow",
    }
    # The internal seam: CanonicalHandlers.handle reaches every builder by
    # dispatch, and its tracked dispatch site is pinned by check (d). It is
    # left out of the by-NAME external match ("handle" is a common attribute
    # across services/; matching it by name would pin unrelated code).
    _OFFER_HINT_SEAM_METHODS = frozenset({"handle"})
    # #2030 (Arch's ruling, issuecomment-6203827433, item 5): check (d) pins
    # the CanonicalHandlers.handle dispatch sites BY HOLDER, not by receiver
    # name. A receiver is a CanonicalHandlers when it is named
    # ``canonical_handlers`` or is a ``self.<attr>`` its module binds from a
    # ``CanonicalHandlers(...)`` construction or from a ``canonical_handlers``
    # name/attribute (the orchestrator's ``self._handlers``). Each holder
    # either ARMS (calls _track_offer_hint itself) or CARRIES (puts
    # ``offer_hint=`` on its result, and the holder that runs the plan arms
    # the picked ``armed_offer_hint`` through _track_offer_hint before its
    # _apply_soft_offer). A third dispatch site fails the build.
    _CANONICAL_DISPATCH_HOLDERS = {
        ("services/intent/intent_service.py", "IntentService._process_intent_internal"): "arms",
        (
            "services/intent_service/orchestrator.py",
            "IntentOrchestrator._execute_single",
        ): "carries",
    }

    # #2011 call 5 (Arch 2026-10-14): OPEN INVITATIONS — a CLOSED word-set of
    # invitation shapes whose any reply is a fresh request (nothing to bind).
    # A literal is in the class iff EVERY question sentence in it is one of
    # these shapes (optionally followed by a time phrase) AND it carries no
    # action offer. A second question of any other shape (a slot request, an
    # adjust-offer) keeps the whole literal counted.
    _OPEN_INVITATION_RE = re.compile(
        r"(?i)^(?:"
        r"what can i help(?: you)? with"
        r"|anything else (?:i can help(?: you)? with|you need)"
        r"|what['’]?s on your mind"
        r"|how does that sound"
        r"|does that help"
        r"|what would you like to (?:work on|focus on)"
        r"|need anything else"
        r")(?: today| now| this (?:morning|afternoon|evening))?\?$"
    )
    _ACTION_OFFER_RE = re.compile(
        r"(?i)\b(?:want me to|should i|shall i|shall we|(?:would you|you'd|you would) like me to)\b"
    )
    _QUESTION_SENTENCE_RE = re.compile(r"[^.!?\n]*\?")

    # Excluded BY NAME, each with its reason (class docstring, Scope).
    _EXCLUDED_PACKAGES = ("services/standup/", "services/onboarding/")

    # #2011 calibration (a)/(b): kwargs whose value is sample/synthesized
    # USER text, not a Piper ask.
    _USER_TEXT_KWARGS = frozenset({"utterance", "original_message"})
    _EXAMPLE_NAME_RE = re.compile(r"(?i)example")

    _MATCHER_ATTRS = frozenset(
        {
            "endswith",
            "startswith",
            "strip",
            "lstrip",
            "rstrip",
            "split",
            "rsplit",
            "removeprefix",
            "removesuffix",
            "count",
            "find",
            "rfind",
            "index",
            "replace",
            "search",
            "match",
            "fullmatch",
            "sub",
            "subn",
            "findall",
            "finditer",
            "compile",
        }
    )

    _TRAILING_CLOSERS = " \t\n*_)`]"
    _QUESTION_NAME_RE = re.compile(r"(?i)question")
    _MARKER_RE = re.compile(r"ask-census:\s*\S")

    # In-source marker exemptions, MEASURED 2026-09-12 and kept tight below:
    # a marker is the sanctioned residual annotation (it lives AT the site,
    # with its reason); this ceiling keeps it an exception, not an exit.
    #   1. IntentService._generate_feature_request_template — GitHub
    #      issue-template body; its '?' lines are template section prose.
    #   2. todo_handlers.handle_reminder_time_turn — the re-ask copy is
    #      emitted AFTER _rearm_time_question() re-armed the store with
    #      this same stored ask (#1654); the arm lives in the callee, out
    #      of the holder-local scan's sight.
    #   3–6. MEASURED 2026-10-12 under the widened predicate (#2000): four
    #      module-level copy constants the mid-line rule now sees, each
    #      classified by reading its consumer —
    #      add_project_clarify._NAME_REASK_TAIL (stored as the ask:
    #      `pending_offer["question"] = _NAME_REASK_TAIL` in _name_reask),
    #      standup_preferences._TEACHING_LINE and INVITE_EMPTY_LEAD (both
    #      reach the user only through build_interview_invitation, which
    #      stores `"question": question`; #2076 moved INVITE_EMPTY_LEAD's
    #      marker to _EMPTY_OFFER_ASK, the question both empty leads
    #      interpolate, so the count is unchanged), conversational_floor
    #      .FLOOR_FALLBACK_TRANSIENT ("Could you try again in a moment?" is
    #      error copy asking for a retry; it binds no answer).
    #   7–10. #2011 call 1 (Arch 2026-10-14; CXO's deliberate list
    #      2026-10-14 15:35): a question answered by its own directive on
    #      the same line, nothing waits for a reply — api/errors.py
    #      ERROR_MESSAGES ×3 ("Need help? Check our …", "Did you mean to
    #      '…'? For more examples, see …"), ui_messages
    #      UserFriendlyErrorService.__init__ ×1 ("Need help? Check our
    #      examples."). CXO's templates.py TEMPORAL_GREETINGS ×3 were NOT
    #      marked: the module was unreachable and deleted (Arch 14:2x).
    #      6 -> 10, the measured count.
    MAX_MARKER_EXEMPTIONS = 10

    # THE RATCHET TABLE — census MEASURED 2026-09-12 (predicate above, run
    # over the scope above). SHRINK-ONLY: arm the site through the one-slot
    # store (storing the rendered ask, #1665) or delete the ask, then remove
    # the row in the same commit. NEVER add a row — a new unarmed ask site
    # must arm instead. Row = (file, holder, literal-count, fingerprint:
    # first 60 chars of the lexicographically-first whitespace-normalized
    # interrogative literal).
    KNOWN_UNARMED_ASK_SITES = frozenset(
        {
            (
                "services/intent/intent_service.py",
                "IntentService._get_contextual_fallback",
                5,  # 4 → 5 on 2026-10-12: the widened predicate (#2000) sees "…? Say 'close issue #…'"
                "I can close issues! Just tell me the issue number, like 'clo",
            ),
            (
                "services/intent/intent_service.py",
                "IntentService._handle_close_issue_query",
                # 2 -> 1 (2026-10-06, CXO 10-05 flag): the multi-match "Which one would
                # you like to ...?" became a declarative "Say '... issue #N' with the
                # number you mean." The confirm literal below remains.
                # 1 -> 2 (2026-10-12, #2000): the widened predicate now sees
                # that declarative's "…? Say 'close issue #N'…" hint line.
                2,
                "Are you sure you want to close issue #{}: **{}**? Say 'yes, ",
            ),
            (
                "services/intent/intent_service.py",
                "IntentService._handle_reopen_issue_query",
                # 2 -> 1 (2026-10-06, CXO 10-05 flag): the multi-match "Which one would
                # you like to ...?" became a declarative "Say '... issue #N' with the
                # number you mean." The confirm literal below remains.
                # 1 -> 2 (2026-10-12, #2000): same hint line as close; the
                # "Did you mean" literal now sorts first, so the fingerprint moved.
                2,
                "Did you mean issue #{}: {}? Say 'reopen issue #{}' to confir",
            ),
            # 2026-09-12 (#1769): the _resume_suspended_standup and
            # _start_standup_conversation rows shrank out — both ask sites
            # now arm the one-turn process-resume offer with their rendered
            # ask threaded as question= (_arm_resume_offer).
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._format_general_setup_guidance",
                1,
                "I'd be happy to help you get set up with Piper! **Getting St",
            ),
            # 2026-10-15 (#2010, Arch's offer_hint ruling): the
            # _format_integration_setup_guidance and _handle_project_setup_request
            # rows shrank out — each builds an "offer_hint" whose offer_text is,
            # verbatim, the question it renders (signal (ii), condition 2 audit
            # PASS, measured by the census). _format_project_setup_guidance
            # FAILED that audit (its offer_text held only the first half of
            # "…, or are you ready to set up your first project?") and stayed.
            # 2026-10-15 (#2024, CXO copy): its either/or became the single
            # question "Are you ready to set up your first project?", armed
            # verbatim as offer_text; its row (2 literals) left BY MEASUREMENT
            # (census 34 rows / 57 literals -> 33 / 55).
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_portfolio_query",
                # 12 → 11: #1856 DELETED an ask. "I'd be happy to help you add
                # a new project! What would you like to call it?" was an open
                # question off a flow that could not hear the answer (the
                # onboarding adapter is unregistered, ADR-059), which is how
                # PM got the identical line twice on 2026-09-23. Its
                # replacement in _handle_add_project is imperative copy that
                # states what to type, so it is not an ask at all — the
                # shrink is a real deletion, not a re-housing.
                # 11 → 7 (2026-10-04, #1595 Phase 3, Arch's manage_portfolio
                # WRITE split §2): the ARCHIVE/RESTORE branches' "I couldn't
                # find a project called '…'. Would you like me to list your
                # [archived] projects?" messages + their offer_hint
                # offer_text literals (4 occurrences total) were hoisted into
                # NEW methods (_handle_archive_project/_handle_restore_
                # project). Re-housing them unchanged would have registered
                # TWO new unarmed-ask holders (forbidden — "NEVER add a row");
                # rewritten as imperative, non-interrogative copy in both new
                # methods instead (the SAME #1856 fix applied again), so they
                # are REMOVED from the census entirely, not re-housed. This
                # holder's own fingerprint/text is unchanged — only the count
                # shrinks, from the deletion.
                # 7 → 5 (2026-10-04, #1595 Phase 3, Arch's manage_portfolio
                # READ split §1, "add search_projects to read_portfolio"):
                # the SEARCH branch's "I couldn't find any projects matching
                # '…'. Would you like to see all your projects?" message +
                # its offer_hint offer_text literal (2 occurrences) were
                # hoisted into a NEW method (_handle_search_projects), same
                # shape as the archive/restore hoist directly above —
                # rewritten as imperative, non-interrogative copy there
                # instead of re-housed unchanged (which would have
                # registered a new unarmed-ask holder). REMOVED from the
                # census entirely, not re-housed. This holder's own
                # fingerprint/text is unchanged (the surviving 5 literals'
                # alphabetically-first, "I can help you manage…", was
                # already first among the 7 — the two removed texts start
                # "I couldn't find any projects matching", which sorts
                # after "I can help...").
                # 5 → 3 (#2010): the list branch's empty-state message and its
                # offer_hint now come from empty_projects_message() /
                # empty_projects_offer_hint() (files_consciousness.py, one
                # source; consumer-armed, every caller arms); both literals
                # leave this holder.
                # Stays at 3 under the #2010 offer_hint signal (ii) (Arch
                # 2026-10-15): condition-2 audit FAIL — the fallback menu's
                # "What would you like to do?" is bound by no offer_text (the
                # delete-not-found "Would you like me to list your projects?"
                # matches its offer_text and would pass on its own).
                # Stays at 3 under #2035 (measured): the empty-state offer now
                # rides "write_offer" from empty_projects_offer() (a #846
                # record built by a self-arming helper), deliberately NOT a
                # question= kwarg in this holder, which would credit the
                # whole holder and hide the unarmed fallback menu.
                3,
                "I can help you manage your projects. You can ask me to: - Sh",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_priority_query",
                2,
                "I'm having trouble accessing your configuration right now. Y",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_provenance_query",
                1,
                "I ran into a snag retrieving what I was drawing on for that.",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_spatial_project_list",
                1,
                "You don't have any active projects configured in your PIPER.",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_status_query",
                1,
                "I'm having trouble accessing your configuration right now. Y",
            ),
            (
                "services/intent_service/conversational_floor.py",
                "_SCAFFOLDING_ONLY_FALLBACK",
                1,
                "I don't have that information in front of me right now — cou",
            ),
            (
                "services/intent_service/first_contact.py",
                "render_first_contact_block",
                1,
                "You don't need to hold this list — I've got it. Want to dig ",
            ),
            (
                "services/intent_service/todo_handlers.py",
                "TodoIntentHandlers.handle_create_todo",
                1,
                "I didn't catch what you'd like me to add. Could you try: 'ad",
            ),
            (
                "services/intent_service/workflow_entries.py",
                "run_summarize_document_workflow",
                1,
                "You've uploaded a few files and I'm not sure which one you m",
            ),
            # ---- MEASURED 2026-10-12 under the widened predicate (#2000, Arch):
            # a measurement change, not new debt — these asks were always
            # unarmed; the old predicate could not see a '?' followed by a
            # same-line hint ("…? Try …", "…? Say …", "…? Tell …"). Each
            # classified by reading its holder: none arms. SHRINK-ONLY from
            # here, same as every row above. #1987 (Arch's condition, met
            # 2026-10-13): handle_delete_todo's ask now lists the numbered
            # candidates and arms through the #846 store
            # (delete_todo_pick.arm_delete_pick); its row shrank out. The
            # handler's unarmable fallback is an instruction, not a question.
            (
                "services/intent/intent_service.py",
                "IntentService._handle_set_timezone",
                1,
                '"{}" matches more than one timezone — did you mean {}? Tell ',
            ),
            (
                "services/intent/intent_service.py",
                "IntentService._resume_suspended_onboarding",
                1,
                "I couldn't find the paused setup. Want to start fresh? Just ",
            ),
            (
                "services/intent_service/calendar_offer_policy.py",
                "OFFER_TEXT",
                1,
                "I noticed your calendar isn't connected yet — would you like",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_link_repo",
                2,
                "Which project should I link {} to? Please tell me the projec",
            ),
            (
                "services/intent_service/todo_handlers.py",
                "TodoIntentHandlers.handle_complete_todo",
                2,
                "I found {} todos matching '{}': {}. Which one should I compl",
            ),
            # ---- MEASURED 2026-10-14 under the #2011 widening (Arch): scope
            # services/** minus standup/onboarding by name, after the #2011
            # calibration (classes (a)-(c) + the LastOffer arm signal, class
            # docstring). A measurement change, not new debt: these asks were
            # always there, unscanned. Each read at its holder: none arms in
            # the holder. SHRINK-ONLY from here, same as every row above —
            # #2010's two questions were format_projects_conscious's 2 literals
            # (rendered by IntentService._handle_projects_query, which did not
            # arm); that row left when #2010 landed (2026-10-15: the empty
            # state moved to empty_projects_message(), rendered and armed by
            # its callers; the list ends with no question). Holders per package:
            # consciousness 34 · slot_filling 3 · trust 3 · integrations 2 · memory 2 · mux 2 · api 1 · conversation 1 · home 1 · mcp 1 · personality 1 · process 1 · ui_messages 1 (total 53).
            # RE-SHAPED 2026-10-14 per Arch's five calls (#2011), re-measured:
            # 53 -> 34 holders. Call 1: literals marked deliberate at their
            # sites (CXO) — api ERROR_MESSAGES, ui_messages and (until its
            # module was deleted, below) TEMPORAL_GREETINGS leave. Call 2: the slot-filling transition arm + one-hop
            # consumer-armed rule — slot_prompts.format_final_confirmation
            # leaves. Call 3: has_suspended_session's question moved to its
            # arming caller — leaves. Call 4: ui/auth/cli excluded by name —
            # 7 holders leave (toast formatters deleted). Call 5: the open-
            # invitation class — 15 literals; 7 holders leave, 3 shrink.
            # Holders per package now: consciousness 23 · trust 3 ·
            # slot_filling 2 · integrations 2 · mux 2 · mcp 1 · memory 1 (34).
            # 34 -> 28 (2026-10-14, Arch 14:2x): consciousness/templates.py +
            # injection.py had no consumer outside the package (no served
            # path rendered them); deleted, their 6 holders with them
            # (ACCOMPLISHMENT_RECOGNITION, DIALOGUE_INVITATION, GENTLE_FLAGGING,
            # MISSING_DATA_EXPLANATION, PRIORITY_FRAMING, injection.fix_mvc_gaps).
            # 28 -> 22 (2026-10-14, T2 per CXO): search ×3 and learning's
            # format_patterns_learned_conscious offer became statements (CXO
            # verbatim); format_project_detail_conscious,
            # format_learning_event_conscious, format_preference_saved_conscious
            # deleted (no consumer beyond the package re-export). todo
            # _build_closing re-measured (CXO 265; 268's reprioritize claim
            # dropped — no op changes a todo's priority).
            # 22 -> 20 (2026-10-14, T4 per CXO): error_consciousness
            # format_error_conscious + _add_dialogue_invitation + _fix_mvc_gaps
            # deleted (no consumer beyond the package re-export). Line 124's
            # live retry offer stays: CXO's replacement doubles the recovery
            # text it follows (sent back to CXO). Loading copy is unreachable
            # (web/utils/streaming_responses has no importer) but its modules
            # are not ruled for deletion: rows stay.
            # 20 -> 17 (2026-10-14, Arch round 2 Rule-0 GO): the loading
            # chain (loading_consciousness -> ui_messages/loading_states ->
            # web/utils/streaming_responses) and slot_prompts
            # .format_confirmation deleted — CONSCIOUS_LOADING_MESSAGES,
            # _get_generic_conscious_message and format_confirmation leave.
            # 17 -> 16 (2026-10-14, CXO 16:10): format_conversational_error_
            # conscious drops its ERROR/CRITICAL invitation (the recovery
            # already says what to do) — its row leaves.
            # -- services/consciousness/ (5; format_projects_conscious left, #2010)
            (
                "services/consciousness/files_consciousness.py",
                "_fix_mvc_gaps",
                1,
                "Want me to tell you more about any of these?",
            ),
            (
                "services/consciousness/learning_consciousness.py",
                "format_patterns_learned_conscious",
                1,
                "I looked through {} items but didn't spot any clear patterns",
            ),
            (
                "services/consciousness/todo_consciousness.py",
                "_build_closing",
                3,
                "How would you like to tackle these?",
            ),
            (
                "services/consciousness/todo_consciousness.py",
                "_fix_mvc_gaps",
                1,
                ". Anything you'd like me to adjust?",
            ),
            (
                "services/consciousness/todo_consciousness.py",
                "format_next_todo_conscious",
                1,
                "Does that priority feel right?",
            ),
            # -- services/integrations/ (2)
            (
                "services/integrations/slack/response_handler.py",
                "SlackResponseHandler._generate_query_response",
                1,
                "🤖 I'm Piper Morgan, your AI Product Management Assistant. Ho",
            ),
            (
                "services/integrations/slack/socket_mode_runner.py",
                "SlackSocketModeRunner._handle_event",
                2,
                "I heard you, but couldn't form a response — try me again?",
            ),
            # -- services/mcp/ (1)
            (
                "services/mcp/consumer/github_adapter.py",
                "GitHubMCPSpatialAdapter.degrade",
                1,
                "Which repo? I couldn't tell which repository you mean — name",
            ),
            # -- services/memory/ (1)
            (
                "services/memory/greeting_context.py",
                "GREETING_APPROACHES",
                4,
                "Back already! We were working on {topic}—continue?",
            ),
            # -- services/mux/ (2)
            (
                "services/mux/premonition.py",
                "SURFACING_FRAMES",
                1,
                "Can I share something that might help?",
            ),
            (
                "services/mux/pull_mode.py",
                "CORRECTION_INVITATION",
                1,
                "Would you like me to explain any of these, or correct someth",
            ),
            # -- services/slot_filling/ (1)
            (
                "services/slot_filling/slot_filling_manager.py",
                "_SLOT_MESSAGES",
                3,
                "I lost track of what we were setting up — could you start ag",
            ),
            # -- services/trust/ (3)
            (
                "services/trust/delegation.py",
                "DELEGATION_PATTERNS",
                1,
                "Would you like me to {action}?",
            ),
            (
                "services/trust/trust_explainer.py",
                "TrustExplainer.explain_proactive_action",
                1,
                "Can you tell me more about what happened?",
            ),
            (
                "services/trust/trust_explainer.py",
                "TrustExplainer.get_followup_offer",
                4,
                "Does this way of working together feel right to you?",
            ),
        }
    )

    # ---- census machinery (the predicate, executably) ----

    def _repo_root(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # #2000 (Arch, 2026-10-12): an ask followed by an instructional hint on
    # the same line ("Which todo should I remove? Try: 'delete todo
    # [number]'") used to be invisible — the predicate only saw a line that
    # ENDS in '?'. A '?' followed by whitespace and a capital letter is a
    # question mark closing a sentence mid-line; count it too.
    _MIDLINE_QUESTION_RE = re.compile(r"\?[ \t]+[A-Z]")

    @staticmethod
    def _interrogative(text: str) -> bool:
        if len(text) < 8 or " " not in text:
            return False
        return any(
            line.rstrip(TestUnarmedAskSiteRatchet._TRAILING_CLOSERS).endswith("?")
            or TestUnarmedAskSiteRatchet._MIDLINE_QUESTION_RE.search(line) is not None
            for line in text.splitlines()
        )

    def test_2000_predicate_sees_a_question_closed_mid_line(self):
        """#2000: the delete ask was invisible because its line ends in a
        hint, not a '?'. A '?' + whitespace + capital counts; a '?' followed
        by lowercase does not; the length/space floors still apply."""
        p = TestUnarmedAskSiteRatchet._interrogative
        assert p("Which todo should I remove? Try: 'delete todo [number]'")
        assert p("Want the guided version instead? Say 'my standup interview'.")
        assert p("Did you mean tomorrow?**")  # trailing closers still stripped, unchanged
        assert not p("the '?' character is not a question here")
        assert not p("what? no, not that one")  # '?' + lowercase
        assert not p("ok?")  # below the length floor

    def test_2011_calibration_classes(self):
        """#2011: the three false-positive classes and the LastOffer arm
        signal, pinned on minimal shapes (each mirrors its measured example
        in the class docstring); a local ``question`` variable stays
        counted."""
        import ast

        cls = TestUnarmedAskSiteRatchet

        def excluded_texts(code):
            tree = ast.parse(code)
            ids = cls._excluded_string_ids(tree, set())
            return {
                n.value
                for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) in ids
            }

        assert "who are you?" in excluded_texts('C(examples=["who are you?"])')  # (a)
        assert "what is my top priority?" in excluded_texts(
            'Intent(original_message="what is my top priority?")'
        )  # (b)
        assert "How urgent is this issue?" in excluded_texts(
            'self.question_templates = {1: ["How urgent is this issue?"]}'
        )  # (c) attribute
        assert "What day is it?" in excluded_texts(
            'cfg = {"questions": ["What day is it?"]}'
        )  # (c) dict key
        assert "Which project do you mean?" not in excluded_texts(
            'question = "Which project do you mean?"'
        )  # a local stays counted
        assert cls._holder_arms(
            list(ast.walk(ast.parse('ctx.last_offer = LastOffer(offer_text="x")')))
        )

    @classmethod
    def _open_invitation(cls, text: str) -> bool:
        """#2011 call 5: True iff every question sentence in ``text`` is a
        closed-set open invitation and ``text`` offers no action."""
        if cls._ACTION_OFFER_RE.search(text):
            return False
        questions = [q.strip() for q in cls._QUESTION_SENTENCE_RE.findall(text)]
        questions = [q for q in questions if q]
        return bool(questions) and all(cls._OPEN_INVITATION_RE.match(q) for q in questions)

    def test_2011_reshape_call2_call5(self):
        """#2011 calls 2 and 5 (Arch 2026-10-14), pinned on measured
        literals: the slot-filling transition arms (terminal states do not),
        and the open-invitation class exempts a closed-set invitation but
        not one that also carries an offer."""
        import ast

        cls = TestUnarmedAskSiteRatchet

        def arms(code):
            return cls._holder_arms(list(ast.walk(ast.parse(code))))

        # call 2: transition INTO an answer-binding state arms ...
        assert arms("session.filling_state = SlotFillingState.CONFIRMING")
        assert arms("session.filling_state = SlotFillingState.PROMPTING")
        # ... a terminal state does not (the post-terminal "wrapped up! Want
        # to start a new one?" in _SLOT_MESSAGES stays counted).
        assert not arms("session.filling_state = SlotFillingState.COMPLETE")
        assert not arms("session.filling_state = SlotFillingState.CANCELLED")

        # call 5, measured both ways:
        # EXEMPT — home_state_service.HomeStateService._generate_greeting.
        assert cls._open_invitation("Welcome. What can I help you with?")
        # COUNTED — measured in templates.DIALOGUE_INVITATION (since deleted,
        # unreachable): an invitation shape, but the same literal offers an
        # action ("you'd like me to adjust").
        assert not cls._open_invitation("How does that sound? Anything you'd like me to adjust?")
        # an offer anywhere disqualifies; a non-shape question (a slot
        # request) disqualifies.
        assert not cls._open_invitation("Does that help? Want me to try again?")
        assert not cls._open_invitation("What can I help you with? Which repo do you mean?")
        assert not cls._open_invitation("Want me to try again?")

    def test_2011_one_hop_bounds(self):
        """#2011 call 2 one-hop CONSUMER-ARMED rule — Arch's four bounds
        (round 2, 2026-10-14), each pinned on a minimal fixture (the house
        idiom of this class's self-tests) and anchored on real measurement."""
        import ast

        cls = TestUnarmedAskSiteRatchet

        def idx(files):
            return cls._caller_index([(r, ast.parse(c)) for r, c in files.items()])

        fmt = {"svc/f.py": "def fmt():\n    return 'Shall I go ahead?'\n"}
        arm = {
            "svc/a.py": "def h(s):\n"
            "    s.filling_state = SlotFillingState.CONFIRMING\n"
            "    return fmt()\n"
        }
        noarm = {"svc/b.py": "def g():\n    return fmt()\n"}

        def armed(files):
            return cls._consumer_armed("svc/f.py", "fmt", idx(files))

        # Bound 1: >= 1 caller AND every caller arms.
        assert not armed({**fmt})  # zero callers: dead copy stays counted
        assert armed({**fmt, **arm})
        assert not armed({**fmt, **arm, **noarm})
        # Bound 2: a caller in a census-EXCLUDED package still counts.
        assert not armed({**fmt, **arm, "services/standup/x.py": noarm["svc/b.py"]})
        # Bound 4: referenced other than by a direct call -> unknown callers.
        assert not armed({**fmt, **arm, "svc/c.py": "HANDLERS = {'x': fmt}\n"})
        assert not armed({**fmt, **arm, "svc/c.py": "def k():\n    register(fmt)\n"})
        assert not armed({**fmt, **arm, "svc/c.py": "def k(m):\n    return getattr(m, 'fmt')()\n"})
        # Bound 4: one hop only — mid() is consumer-armed by top(); fmt(),
        # called only by mid(), is NOT (never transitive).
        chain = idx(
            {
                **fmt,
                "svc/m.py": "def mid():\n    return fmt()\n",
                "svc/t.py": "def top(s):\n"
                "    s.filling_state = SlotFillingState.PROMPTING\n"
                "    return mid()\n",
            }
        )
        assert cls._consumer_armed("svc/m.py", "mid", chain)
        assert not cls._consumer_armed("svc/f.py", "fmt", chain)

        # Real measurement. Bound 2: the caller roots reach web/, main.py
        # and the census-excluded services/standup/. Bound 3: never tests/.
        rels = {rel for rel, _tree in self._caller_trees()}
        assert "main.py" in rels
        assert any(r.startswith("web/") for r in rels)
        assert any(r.startswith("services/standup/") for r in rels)
        assert not any(r.startswith("tests/") for r in rels)
        # Bound 1 + 3, measured: format_final_confirmation's production
        # callers (_determine_next_step, _handle_confirming) all arm; its
        # non-arming TEST callers (test_slot_prompts.py) count neither way.
        _rows, stats = self._census()
        assert (
            "services/slot_filling/slot_prompts.py",
            "format_final_confirmation",
        ) in stats["consumer_armed"]

    def test_2011_non_chat_surface_consumers(self):
        """#2011 call 4 TRIPWIRE: each non-chat module excluded by name in
        _EXCLUDED_MODULES is imported by EXACTLY its measured consumer set
        (production code; tests/ and dev/ not counted) — directly, or by
        importing one of its names through the ``services.consciousness``
        package. A new importer (above all a chat path) fails here, and the
        exclusion must be re-ruled instead of silently going false."""
        import ast

        root = self._repo_root()
        mods = self._NON_CHAT_SURFACE_IMPORTERS
        public = {}
        for mod in mods:
            with open(os.path.join(root, "services", "consciousness", f"{mod}.py")) as fh:
                tree = ast.parse(fh.read())
            public[mod] = {
                n.name
                for n in tree.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not n.name.startswith("_")
            } | {
                t.id
                for n in tree.body
                if isinstance(n, ast.Assign)
                for t in n.targets
                if isinstance(t, ast.Name)
            }
        found = {mod: set() for mod in mods}
        paths = [os.path.join(root, "main.py"), os.path.join(root, "main_mcp.py")]
        for top in ("services", "web", "cli", "scripts", "shared", "tools", "config"):
            paths += glob.glob(os.path.join(root, top, "**", "*.py"), recursive=True)
        scanned = 0
        for path in paths:
            if not os.path.isfile(path):
                continue
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            with open(path, encoding="utf-8") as fh:
                src = fh.read()
            if "consciousness" not in src:
                continue
            scanned += 1
            for node in ast.walk(ast.parse(src)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    for mod in mods:
                        full = f"services.consciousness.{mod}"
                        if node.module == full or (
                            node.module == "services.consciousness"
                            and any(a.name in (mod, *public[mod]) for a in node.names)
                        ):
                            found[mod].add(rel)
                elif isinstance(node, ast.Import):
                    for mod in mods:
                        if any(a.name == f"services.consciousness.{mod}" for a in node.names):
                            found[mod].add(rel)
        assert scanned >= 10, f"tripwire scanned only {scanned} files — the walk broke"
        for mod, expected in mods.items():
            assert found[mod] - {
                "services/consciousness/__init__.py"
            }, f"{mod}: its measured surface consumer vanished — re-measure"
            assert found[mod] == set(expected), (
                f"#2011 call 4 tripwire: {mod} is excluded from the unarmed-ask "
                f"census as a NON-CHAT surface, measured importers "
                f"{sorted(expected)}; now imported by {sorted(found[mod])}. "
                f"If a chat path now renders its copy, the exclusion is false: "
                f"remove it from _EXCLUDED_MODULES and census its asks."
            )

    def test_2010_offer_hint_signal(self):
        """#2010 (Arch 2026-10-15): signal (i) ``_track_offer_hint(`` arms
        anywhere; signal (ii), a built ``"offer_hint"`` key (dict-literal or
        subscript assignment), arms only inside _OFFER_HINT_BUILDER_MODULES;
        offer_text resolves within the holder; the condition-2 adequacy rule
        covers a rendered question only by a verbatim offer_text question."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        scoped = next(iter(cls._OFFER_HINT_BUILDER_MODULES))

        def nodes(code):
            return list(ast.walk(ast.parse(code)))

        # (i): the call is the arm, in any module.
        track = "self._track_offer_hint(result, session_id, user_id)"
        assert cls._holder_arms(nodes(track))
        assert cls._holder_arms(nodes(track), "services/anywhere.py")
        # (ii): both build forms, reach-scoped by module.
        lit = (
            'r = {"message": m, "offer_hint": {"continuation_hint": "c", "offer_text": "Shall I?"}}'
        )
        sub = 'r["offer_hint"] = {"continuation_hint": "c", "offer_text": "Shall I?"}'
        for code in (lit, sub):
            assert cls._holder_arms(nodes(code), scoped)
            assert not cls._holder_arms(nodes(code), "services/elsewhere.py")
            assert not cls._holder_arms(nodes(code))
        # reading a hint is not building one.
        assert not cls._holder_arms(nodes('h = r.get("offer_hint")'), scoped)
        # offer_text resolution: a local name, a hint dict bound to a name,
        # and a hint built elsewhere (a call) — which resolves to nothing.
        assert cls._offer_texts(
            nodes('outro = "Want X?"\nr = {"offer_hint": {"offer_text": outro}}')
        ) == {"Want X?"}
        assert cls._offer_texts(nodes('h = {"offer_text": "Want X?"}\nr = {"offer_hint": h}')) == {
            "Want X?"
        }
        assert cls._offer_texts(nodes('r["offer_hint"] = make_hint()')) == set()
        # adequacy, on the measured pre-#2024 2383 shape (FAIL) and a verbatim match.
        held = {"Would you like me to explain more about how Piper uses project context?"}
        assert not cls._offer_text_covers(
            "Would you like me to explain more about how Piper uses project "
            "context, or are you ready to set up your first project?",
            held,
        )
        assert cls._offer_text_covers(
            "Steps above. Would you like me to explain more about how Piper "
            "uses project context?",
            held,
        )
        # a directive offer_text binds no question.
        assert not cls._offer_text_covers(
            "Would you like me to list your projects?",
            {"Say 'list my projects' to see what you have."},
        )

    def test_2010_offer_hint_reach_tripwire(self):
        """#2010 condition 1 TRIPWIRE (Arch 2026-10-15): signal (ii) is
        credible only because every builder's result reaches a tracking
        seam — a fact about CALLERS, not the holder body. Measured over
        services/**, web/** and main.py:
        (a) every holder that builds an "offer_hint" without tracking it
            itself lives in _OFFER_HINT_BUILDER_MODULES (a new builder
            module fails here until it is shown to reach a seam);
        (b) the EXTERNAL referrers of every builder AND of every in-class
            method that transitively reaches one (#2024 hardening (b): the
            ``ast`` call graph inside each builder-module class, closed
            backwards from the builders) are exactly the pinned set (a new
            external caller of any reaching method fails here);
        (c) each pinned referrer returns the builder's result through
            _finalize_canonical_rail_result, which calls _track_offer_hint
            (a pinned NAME TABLE is checked at its getattr adapter);
        (d) the CanonicalHandlers.handle dispatch sites are exactly the
            pinned HOLDERS (#2030: _process_intent_internal, which arms, and
            IntentOrchestrator._execute_single, which carries the hint to the
            plan-running holder's _track_offer_hint), found by receiver
            binding, not receiver name."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        trees = self._caller_trees()
        reach = cls._offer_hint_reach(trees)
        builders = reach["builders"]

        # (a) builder modules
        modules = {rel for rel, _qual in builders}
        assert modules == set(cls._OFFER_HINT_BUILDER_MODULES), (
            f"#2010 reach tripwire: offer_hint builders that do not track "
            f"themselves now live in {sorted(modules)}; measured scope "
            f"{sorted(cls._OFFER_HINT_BUILDER_MODULES)}. A builder's hint "
            f"arms only if its result reaches _track_offer_hint: show the "
            f"seam, then re-rule the scope (or call _track_offer_hint)."
        )
        # vacuity: Arch measured 7 builder holders 2026-10-15; #2024 dropped
        # the archive/restore/search not-found hints -> 4, measured. #2035
        # moved the two project-setup write offers to the #846 store
        # ("write_offer") -> 2, measured (_format_integration_setup_guidance,
        # _handle_portfolio_query's delete-not-found).
        assert len(builders) >= 2, f"only {len(builders)} builders found — the scan broke"

        # (b) external referrers of every builder AND every in-class method
        # that transitively reaches one (#2024 hardening (b)).
        cls._assert_offer_hint_reach_pinned(reach)
        # vacuity: 21 external entry points into the builder-module classes
        # measured 2026-10-15 (the seam ``handle`` and dunders not counted).
        assert len(reach["entry_points"]) >= 18, (
            f"only {len(reach['entry_points'])} external entry points found — "
            f"the referrer scan broke"
        )
        names = reach["reaching"]

        # (c) each adapter returns the builder's result through the seam.
        index = dict(trees)
        cls._assert_referrers_return_through_finalize(
            index, cls._OFFER_HINT_EXTERNAL_CALLERS, cls._OFFER_HINT_TABLE_ADAPTERS, names, "#2010"
        )
        finalize = next(
            n
            for n in index["services/intent_service/workflow_entries.py"].body
            if isinstance(n, ast.AsyncFunctionDef) and n.name == "_finalize_canonical_rail_result"
        )
        assert cls._holder_arms(
            list(cls._own_nodes(finalize))
        ), "_finalize_canonical_rail_result no longer calls _track_offer_hint"

        # (d) the internal route: CanonicalHandlers.handle's dispatch sites,
        # pinned by holder (#2030).
        cls._assert_canonical_dispatch_reaches_seam(trees)

    @classmethod
    def _assert_referrers_return_through_finalize(
        cls, index, pinned, table_adapters, names, label
    ) -> None:
        """#2010 check (c), shared with #2035's write_offer tripwire: each
        pinned external referrer (a NAME TABLE checked at its getattr
        adapter) binds the result of a reaching method and returns it only
        through ``_finalize_canonical_rail_result``."""
        import ast

        for rel, name in sorted(pinned):
            target = table_adapters.get((rel, name), name)
            fn = cls._find_def(index[rel], target)
            assert fn is not None, f"pinned referrer {rel}::{target} not found"
            produced = set()
            getattr_bound = {
                t.id
                for n in ast.walk(fn)
                if isinstance(n, ast.Assign)
                and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Name)
                and n.value.func.id == "getattr"
                for t in n.targets
                if isinstance(t, ast.Name)
            }
            for n in ast.walk(fn):
                if (
                    isinstance(n, ast.Assign)
                    and isinstance(n.value, ast.Await)
                    and isinstance(n.value.value, ast.Call)
                    and (
                        (
                            isinstance(n.value.value.func, ast.Attribute)
                            and n.value.value.func.attr in names
                        )
                        or (
                            isinstance(n.value.value.func, ast.Name)
                            and n.value.value.func.id in getattr_bound
                        )
                    )
                ):
                    produced |= {t.id for t in n.targets if isinstance(t, ast.Name)}
            through, other = [], []
            for r in (n for n in ast.walk(fn) if isinstance(n, ast.Return)):
                v = r.value
                if v is None or (isinstance(v, ast.Constant) and v.value is None):
                    continue  # missing-context exit: no result, no offer
                if (
                    isinstance(v, ast.Await)
                    and isinstance(v.value, ast.Call)
                    and isinstance(v.value.func, ast.Name)
                    and v.value.func.id == "_finalize_canonical_rail_result"
                    and produced & {a.id for a in v.value.args if isinstance(a, ast.Name)}
                ):
                    through.append(r)
                else:
                    other.append(r)
            assert produced and through and not other, (
                f"{label} reach tripwire: {target} must return its builder result "
                f"through _finalize_canonical_rail_result (the arming seam); "
                f"{len(other)} return(s) bypass it"
            )

    @staticmethod
    def _canonical_receivers(tree) -> set:
        """#2030: the ``self.<attr>`` names a module binds to a
        CanonicalHandlers: from a ``CanonicalHandlers(...)`` construction or
        from a ``canonical_handlers`` name/attribute (an alias of one)."""
        import ast

        out = {"canonical_handlers"}
        for n in ast.walk(tree):
            if not isinstance(n, (ast.Assign, ast.AnnAssign)) or n.value is None:
                continue
            v = n.value
            if (
                (
                    isinstance(v, ast.Call)
                    and isinstance(v.func, ast.Name)
                    and v.func.id == "CanonicalHandlers"
                )
                or (isinstance(v, ast.Name) and v.id == "canonical_handlers")
                or (isinstance(v, ast.Attribute) and v.attr == "canonical_handlers")
            ):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                out |= {
                    t.attr
                    for t in targets
                    if isinstance(t, ast.Attribute)
                    and isinstance(t.value, ast.Name)
                    and t.value.id == "self"
                }
        return out

    @classmethod
    def _canonical_dispatch_holders(cls, trees) -> dict:
        """#2030: (rel, holder) -> (own nodes, names bound from the call's
        result), for every holder that calls ``<CanonicalHandlers>.handle(``
        (receiver resolved by binding)."""
        import ast

        found = {}
        for rel, tree in trees:
            receivers = cls._canonical_receivers(tree)
            for qual, nodes in cls._collect_holders(tree):
                dispatches = set()
                for sub in nodes:
                    if not (
                        isinstance(sub, ast.Call)
                        and isinstance(sub.func, ast.Attribute)
                        and sub.func.attr == "handle"
                    ):
                        continue
                    recv = sub.func.value
                    name = (
                        recv.attr
                        if isinstance(recv, ast.Attribute)
                        else (recv.id if isinstance(recv, ast.Name) else None)
                    )
                    if name in receivers:
                        dispatches.add(id(sub))
                if not dispatches:
                    continue
                produced = {
                    t.id
                    for n in nodes
                    if isinstance(n, ast.Assign)
                    and isinstance(n.value, ast.Await)
                    and id(n.value.value) in dispatches
                    for t in n.targets
                    if isinstance(t, ast.Name)
                }
                found[(rel, qual)] = (nodes, produced)
        return found

    @staticmethod
    def _carries_offer_hint(nodes, produced, kwarg="offer_hint") -> bool:
        """#2030: the holder puts ``offer_hint=`` on a result it builds, its
        value read from the dispatch's result (a name in ``produced``).
        #2041: the same for ``write_offer=`` (``kwarg``)."""
        import ast

        return any(
            isinstance(n, ast.Call)
            and any(
                kw.arg == kwarg
                and any(isinstance(v, ast.Name) and v.id in produced for v in ast.walk(kw.value))
                for kw in n.keywords
            )
            for n in nodes
        )

    @classmethod
    def _plan_arm_holders(
        cls, trees, arm="_track_offer_hint", attr="armed_offer_hint", before=()
    ) -> list:
        """#2030: (rel, holder, problem) for every holder that runs a plan
        (``.execute_plan(``). ``problem`` is None when the holder passes the
        picked ``<x>.armed_offer_hint`` to ``_track_offer_hint`` after the
        plan runs and before its next ``_apply_soft_offer`` call (#1770: the
        live arm then suppresses a second, soft ask). #2041: the same for
        ``<x>.armed_write_offer`` -> ``_arm_write_offer`` (``arm``/``attr``),
        which must ALSO come before the next call of each name in ``before``
        (``_track_offer_hint``: a write offer outranks a hint)."""
        import ast

        out = []
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                calls = [
                    n
                    for n in nodes
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                ]
                plans = [c.lineno for c in calls if c.func.attr == "execute_plan"]
                if not plans:
                    continue
                arms = [
                    c.lineno
                    for c in calls
                    if c.func.attr == arm
                    and any(
                        isinstance(a, ast.Attribute) and a.attr == attr
                        for arg in c.args
                        for a in ast.walk(arg)
                    )
                ]
                plan = min(plans)
                first = min((a for a in arms if a > plan), default=None)
                problem = None
                if first is None:
                    problem = f"never passes {attr} to {arm}"
                else:
                    for later in ("_apply_soft_offer", *before):
                        nxt = min(
                            (c.lineno for c in calls if c.func.attr == later and c.lineno > plan),
                            default=None,
                        )
                        if nxt is not None and nxt < first:
                            problem = f"arms {attr} AFTER {later}" + (
                                " (#1770)" if later == "_apply_soft_offer" else ""
                            )
                            break
                out.append((rel, qual, problem))
        return out

    @classmethod
    def _assert_canonical_dispatch_reaches_seam(cls, trees) -> None:
        """#2010 check (d), by holder (#2030): the dispatch holders are
        exactly ``_CANONICAL_DISPATCH_HOLDERS``; an "arms" holder calls
        _track_offer_hint; a "carries" holder puts ``offer_hint=`` on its
        result AND every plan-running holder arms the picked hint before
        its soft offer."""
        found = cls._canonical_dispatch_holders(trees)
        assert set(found) == set(cls._CANONICAL_DISPATCH_HOLDERS), (
            f"#2030 check (d): CanonicalHandlers.handle dispatch holders are "
            f"{sorted(found)}; pinned {sorted(cls._CANONICAL_DISPATCH_HOLDERS)}. "
            f"A new dispatch site must arm (_track_offer_hint) or carry the "
            f"offer_hint to a holder that does; show it, then pin it."
        )
        import ast

        for key, mode in sorted(cls._CANONICAL_DISPATCH_HOLDERS.items()):
            rel, qual = key
            nodes, produced = found[key]
            if mode == "arms":
                # the dispatch's OWN result reaches _track_offer_hint (a
                # different call in the same holder, e.g. the multi-intent
                # arm, does not count).
                arms_result = any(
                    isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute)
                    and n.func.attr == "_track_offer_hint"
                    and produced & {a.id for a in n.args if isinstance(a, ast.Name)}
                    for n in nodes
                )
                assert produced and arms_result, (
                    f"#2030 check (d): {rel}::{qual} dispatches "
                    f"CanonicalHandlers.handle but its result no longer reaches "
                    f"_track_offer_hint"
                )
            else:
                assert cls._carries_offer_hint(nodes, produced), (
                    f"#2030 check (d): {rel}::{qual} dispatches "
                    f"CanonicalHandlers.handle but its result no longer carries offer_hint"
                )
                plan_arms = cls._plan_arm_holders(trees)
                assert plan_arms, (
                    f"#2030 check (d): {rel}::{qual} carries offer_hint but no "
                    f"holder runs a plan (.execute_plan) and arms it"
                )
                bad = [(r, q, p) for r, q, p in plan_arms if p is not None]
                assert not bad, (
                    f"#2030 check (d): the carried offer_hint does not reach "
                    f"_track_offer_hint: {bad}"
                )

    @staticmethod
    def _find_def(tree, qual):
        """The def node at dotted ``qual`` (nested defs allowed), or None."""
        import ast

        node = tree
        for part in qual.split("."):
            node = next(
                (
                    n
                    for n in ast.iter_child_nodes(node)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                    and n.name == part
                ),
                None,
            )
            if node is None:
                return None
        return node

    @staticmethod
    def _class_call_graph(cls_node) -> dict:
        """#2024 (b): method -> the methods of the same class it references
        (``self.x`` / ``cls.x`` / ``ClassName.x``, or a string constant naming
        one, e.g. a getattr target or a dispatch table). Conservative: a
        reference is an edge whether or not it is called."""
        import ast

        methods = {
            n.name for n in cls_node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        graph = {}
        for fn in cls_node.body:
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            refs = set()
            for sub in ast.walk(fn):
                if (
                    isinstance(sub, ast.Attribute)
                    and isinstance(sub.value, ast.Name)
                    and sub.value.id in ("self", "cls", cls_node.name)
                ):
                    refs.add(sub.attr)
                elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    refs.add(sub.value)
            graph[fn.name] = (refs & methods) - {fn.name}
        return graph

    @classmethod
    def _offer_hint_reach(cls, trees) -> dict:
        """#2010 condition 1 + #2024 hardening (b), measured over ``trees``:

        - ``builders``: (rel, qual) holders that build an ``"offer_hint"``
          and do not track it themselves;
        - ``reaching``: simple names of the builders plus every method of a
          builder-module class whose in-class call graph reaches a builder
          (transitive closure), minus the pinned seam (``handle``, check (d));
        - ``entry_points``: method name -> {(rel, qual)} referrers OUTSIDE the
          builder modules (attribute, name, or string constant naming it), for
          every method of a builder-module class (dunders and the seam not
          counted);
        - ``external``: the referrers of any ``reaching`` name."""
        import ast

        builders = set()
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                if cls._builds_offer_hint(nodes) and not cls._holder_arms(nodes):
                    builders.add((rel, qual))
        return cls._builder_reach(
            trees, builders, cls._OFFER_HINT_BUILDER_MODULES, cls._OFFER_HINT_SEAM_METHODS
        )

    @classmethod
    def _builder_reach(cls, trees, builders, builder_modules, seam_methods) -> dict:
        """The reach closure shared by the #2010 offer_hint and #2035
        write_offer tripwires (see ``_offer_hint_reach`` for the keys):
        ``builders`` are (rel, qual) holders; ``reaching`` closes them
        backwards over each builder-module class's in-class call graph;
        ``entry_points`` are referrers OUTSIDE ``builder_modules``."""
        import ast

        builder_names = {qual.rsplit(".", 1)[-1] for _rel, qual in builders}
        reaching = set(builder_names)
        universe = set(builder_names)
        for rel, tree in trees:
            if rel not in builder_modules:
                continue
            for cls_node in (n for n in tree.body if isinstance(n, ast.ClassDef)):
                graph = cls._class_call_graph(cls_node)
                universe |= set(graph)
                own = {
                    q.rsplit(".", 1)[-1]
                    for r, q in builders
                    if r == rel and q.startswith(cls_node.name + ".")
                }
                closed = set(own)
                grew = True
                while grew:
                    grew = False
                    for m, refs in graph.items():
                        if m not in closed and refs & closed:
                            closed.add(m)
                            grew = True
                reaching |= closed
        excluded = set(seam_methods)
        reaching -= excluded
        universe = {n for n in universe - excluded if not n.startswith("__")}
        entry_points = {}
        for rel, tree in trees:
            if rel in builder_modules:
                continue
            for qual, nodes in cls._collect_holders(tree):
                for sub in nodes:
                    if isinstance(sub, ast.Attribute):
                        ref = sub.attr
                    elif isinstance(sub, ast.Name):
                        ref = sub.id
                    elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        ref = sub.value
                    else:
                        continue
                    if ref in universe:
                        entry_points.setdefault(ref, set()).add((rel, qual))
        external = set()
        for name in reaching & set(entry_points):
            external |= entry_points[name]
        return {
            "builders": builders,
            "reaching": reaching,
            "entry_points": entry_points,
            "external": external,
        }

    @classmethod
    def _assert_offer_hint_reach_pinned(cls, reach) -> None:
        """#2024 hardening (b): fail if any external referrer reaches a
        builder (directly or through the in-class closure) unless pinned."""
        reaching_entries = sorted(n for n in reach["entry_points"] if n in reach["reaching"])
        assert reach["external"] == set(cls._OFFER_HINT_EXTERNAL_CALLERS), (
            f"#2010/#2024 reach tripwire: the offer_hint builders and the "
            f"in-class methods that reach them {sorted(reach['reaching'])} are "
            f"now referenced outside {sorted(cls._OFFER_HINT_BUILDER_MODULES)} "
            f"by {sorted(reach['external'])} (via {reaching_entries}); measured "
            f"{sorted(cls._OFFER_HINT_EXTERNAL_CALLERS)}. Show the new caller "
            f"hands the result to _track_offer_hint, then pin it."
        )

    def test_2024_reach_closure_catches_an_indirect_caller(self):
        """#2024 hardening (b), fed a fake in memory: an external caller of a
        method that reaches a builder only THROUGH another in-class method
        fails the pin; a caller of a method that reaches none does not."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        mod = next(iter(cls._OFFER_HINT_BUILDER_MODULES))
        fake_builder = ast.parse(
            "class CanonicalHandlers:\n"
            "    async def handle(self, intent):\n"
            "        return await self._entry(intent)\n"
            "    async def _builder(self):\n"
            '        return {"message": "m", "offer_hint": {"offer_text": "Want X?"}}\n'
            "    async def _mid(self):\n"
            "        return await self._builder()\n"
            "    async def _entry(self, intent):\n"
            "        return await self._mid()\n"
            "    async def _other(self):\n"
            '        return {"message": "no offer"}\n'
        )
        indirect = ast.parse("async def caller(ch):\n    return await ch._entry(None)\n")
        unrelated = ast.parse("async def other_caller(ch):\n    return await ch._other()\n")
        reach = cls._offer_hint_reach(
            [(mod, fake_builder), ("services/x.py", indirect), ("services/y.py", unrelated)]
        )
        assert {"_builder", "_mid", "_entry"} <= reach["reaching"]
        assert "_other" not in reach["reaching"]
        assert "handle" not in reach["reaching"]  # the seam, pinned by (d)
        assert reach["external"] == {("services/x.py", "caller")}
        with pytest.raises(AssertionError, match="services/x.py"):
            cls._assert_offer_hint_reach_pinned(reach)
        # the unrelated caller alone reaches nothing: the pin's set-equality
        # then fails only on the real pinned referrer being absent.
        quiet = cls._offer_hint_reach([(mod, fake_builder), ("services/y.py", unrelated)])
        assert quiet["external"] == set()
        assert set(quiet["entry_points"]) == {"_other"}

    # ---- #2035 write_offer reach tripwire (Arch's rule item 2, 2026-10-15) ----
    # A yes/no offer whose "yes" leads to a WRITE is a #846 one-slot record
    # (Arch's #2035 rule), built by a FACTORY (add_project_clarify
    # .build_add_project_offer, files_consciousness.empty_projects_offer). The
    # census credits those holders by the #1665 stored-ask idiom (the
    # factory's ``question=`` kwarg / ``"question"`` key), and credits
    # empty_projects_message through its arming callers. That credit is true
    # only if every record REACHES a #846 arming point: ``set_pending_offer``
    # directly, or the ``"write_offer"`` result key that
    # IntentService._arm_write_offer reads at the two seams a canonical dict
    # reaches (the canonical dispatch in _process_intent_internal, and
    # _finalize_canonical_rail_result). MEASURED 2026-10-15 on main
    # 2cf001266f (c726ce5d35 + copy follow-ups).
    _WRITE_OFFER_BUILDER_MODULES = frozenset({"services/intent_service/canonical_handlers.py"})
    # The holders that put a factory's record on a result's "write_offer"
    # (they have no offer-store access). A NEW builder fails until it is
    # shown to reach an arming point and pinned here.
    _WRITE_OFFER_BUILDERS = frozenset(
        {
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._format_project_setup_guidance",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_project_setup_request",
            ),
            (
                "services/intent_service/canonical_handlers.py",
                "CanonicalHandlers._handle_portfolio_query",
            ),
        }
    )
    # The EXTERNAL referrers of every builder and of every in-class method
    # that transitively reaches one (the #2024 (b) closure), measured: the
    # read_canonical name table, whose "_handle_guidance_query" reaches both
    # setup-guidance builders; its adapter returns through
    # _finalize_canonical_rail_result (check (c)). _handle_portfolio_query
    # has no external referrer: it is reached only through the
    # CanonicalHandlers.handle seam (check (d)).
    _WRITE_OFFER_EXTERNAL_CALLERS = frozenset(
        {
            ("services/intent_service/workflow_entries.py", "_READ_CANONICAL_MEMBERS"),
        }
    )
    _WRITE_OFFER_TABLE_ADAPTERS = {
        (
            "services/intent_service/workflow_entries.py",
            "_READ_CANONICAL_MEMBERS",
        ): "_make_read_canonical_entry_point.run_read_canonical_workflow",
    }
    # The #846 record factories whose result rides "write_offer", derived
    # (callees in a "write_offer" value, closed over module-level functions
    # that return a factory's call) and pinned.
    _WRITE_OFFER_FACTORIES = frozenset(
        {
            ("services/intent_service/add_project_clarify.py", "build_add_project_offer"),
            ("services/consciousness/files_consciousness.py", "empty_projects_offer"),
            # #2048 follow-up (Arch's D4 ruling, 2026-10-16): the adopted-write
            # confirm. Its one caller, CanonicalHandlers._handle_portfolio_query
            # (a pinned builder above), puts it on "write_offer", which the
            # canonical dispatch seam arms (_arm_write_offer). Pinned by
            # test_adopted_category_reads_only_2048.py (armed + yes executes).
            (
                "services/intent_service/adopted_category_reads_only.py",
                "build_adopted_write_confirm_offer",
            ),
        }
    )
    # Check (d): the CanonicalHandlers.handle dispatch holders (found by
    # receiver binding, the #2030 helper) and what each does with the
    # result's "write_offer". "arms": the dispatch result reaches
    # _arm_write_offer. "carries" (#2041, Arch's ruling 2026-10-15; was the
    # pinned "drops" gap measured 2026-10-15): the holder puts
    # ``write_offer=`` on its result, and every holder that runs a plan
    # passes the picked ``armed_write_offer`` to _arm_write_offer after the
    # plan and before both _track_offer_hint and _apply_soft_offer (a write
    # offer outranks a hint; #1770 first-arm-wins then holds the slot).
    _WRITE_OFFER_DISPATCH_HOLDERS = {
        ("services/intent/intent_service.py", "IntentService._process_intent_internal"): "arms",
        (
            "services/intent_service/orchestrator.py",
            "IntentOrchestrator._execute_single",
        ): "carries",
    }

    @staticmethod
    def _callee_name(call):
        import ast

        f = call.func
        if isinstance(f, ast.Attribute):
            return f.attr
        if isinstance(f, ast.Name):
            return f.id
        return None

    @staticmethod
    def _local_bindings(nodes) -> dict:
        """local name -> value expressions assigned to it in the holder."""
        import ast

        out = {}
        for sub in nodes:
            if isinstance(sub, ast.Assign):
                for t in sub.targets:
                    if isinstance(t, ast.Name):
                        out.setdefault(t.id, []).append(sub.value)
            elif (
                isinstance(sub, ast.AnnAssign)
                and sub.value is not None
                and isinstance(sub.target, ast.Name)
            ):
                out.setdefault(sub.target.id, []).append(sub.value)
        return out

    @classmethod
    def _write_offer_reach(cls, trees, builder_modules=None) -> dict:
        """#2035: the ``_builder_reach`` closure for holders that build a
        ``"write_offer"`` key and do not arm it themselves
        (``set_pending_offer``)."""
        import ast

        builders = set()
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                if cls._built_key_values(nodes, "write_offer") and not any(
                    isinstance(n, ast.Call) and cls._callee_name(n) == "set_pending_offer"
                    for n in nodes
                ):
                    builders.add((rel, qual))
        return cls._builder_reach(
            trees,
            builders,
            cls._WRITE_OFFER_BUILDER_MODULES if builder_modules is None else builder_modules,
            cls._OFFER_HINT_SEAM_METHODS,
        )

    @classmethod
    def _assert_write_offer_reach_pinned(
        cls, reach, builders=None, external=None, modules=None
    ) -> None:
        """#2035 checks (a) and (b): the builders and the external referrers
        of every method that reaches one are exactly the pinned sets."""
        builders = cls._WRITE_OFFER_BUILDERS if builders is None else builders
        external = cls._WRITE_OFFER_EXTERNAL_CALLERS if external is None else external
        modules = cls._WRITE_OFFER_BUILDER_MODULES if modules is None else modules
        found_modules = {rel for rel, _q in reach["builders"]}
        assert found_modules <= set(modules), (
            f"#2035 write_offer reach tripwire: write_offer builders now live in "
            f"{sorted(found_modules)}; measured scope {sorted(modules)}. A builder's "
            f"record arms only if its result reaches IntentService._arm_write_offer "
            f"(or set_pending_offer): show the seam, then re-rule the scope."
        )
        assert reach["builders"] == set(builders), (
            f"#2035 write_offer reach tripwire: write_offer builders are "
            f"{sorted(reach['builders'])}; pinned {sorted(builders)}. A new builder "
            f"must be shown to reach a #846 arming point, then pinned."
        )
        reaching_entries = sorted(n for n in reach["entry_points"] if n in reach["reaching"])
        assert reach["external"] == set(external), (
            f"#2035 write_offer reach tripwire: the write_offer builders and the "
            f"in-class methods that reach them {sorted(reach['reaching'])} are "
            f"referenced outside {sorted(modules)} by {sorted(reach['external'])} "
            f"(via {reaching_entries}); pinned {sorted(external)}. Show the new "
            f"caller hands the result to _arm_write_offer "
            f"(_finalize_canonical_rail_result), then pin it."
        )

    @classmethod
    def _write_offer_factories(cls, trees) -> set:
        """#2035: (rel, qual) of every def whose call result rides a
        ``"write_offer"`` value (directly or through a local name), closed
        over defs that RETURN a factory's call."""
        import ast

        names = set()
        for _rel, tree in trees:
            for _qual, nodes in cls._collect_holders(tree):
                bound = cls._local_bindings(nodes)
                for v in cls._built_key_values(nodes, "write_offer"):
                    for e in bound.get(v.id, []) if isinstance(v, ast.Name) else [v]:
                        if isinstance(e, ast.Call) and cls._callee_name(e):
                            names.add(cls._callee_name(e))
        defs = [
            (rel, qual, nodes)
            for rel, tree in trees
            for qual, nodes in cls._collect_holders(tree)
            if any(isinstance(n, ast.Return) for n in nodes)
        ]
        grew = True
        while grew:
            grew = False
            for _rel, qual, nodes in defs:
                simple = qual.rsplit(".", 1)[-1]
                if simple in names:
                    continue
                if any(
                    isinstance(n, ast.Return)
                    and isinstance(n.value, ast.Call)
                    and cls._callee_name(n.value) in names
                    for n in nodes
                ):
                    names.add(simple)
                    grew = True
        return {(rel, qual) for rel, qual, _n in defs if qual.rsplit(".", 1)[-1] in names}

    @classmethod
    def _write_offer_factory_violations(cls, trees, factories) -> list:
        """#2035 check (e): (rel, holder, line) for every call of a factory
        whose record reaches NO #846 arming point in the calling holder: it
        must be an argument of ``set_pending_offer``, or a ``"write_offer"``
        value (directly or through a local name bound to the call). A
        factory's own call to another factory (it returns it) is exempt."""
        import ast

        names = {q.rsplit(".", 1)[-1] for _r, q in factories}
        out = []
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                if (rel, qual) in factories:
                    continue
                calls = [
                    n for n in nodes if isinstance(n, ast.Call) and cls._callee_name(n) in names
                ]
                if not calls:
                    continue
                sinks = list(cls._built_key_values(nodes, "write_offer"))
                for n in nodes:
                    if isinstance(n, ast.Call) and cls._callee_name(n) == "set_pending_offer":
                        sinks += list(n.args) + [kw.value for kw in n.keywords]
                sink_ids = {id(x) for s in sinks for x in ast.walk(s)}
                sink_names = {x.id for s in sinks for x in ast.walk(s) if isinstance(x, ast.Name)}
                for c in calls:
                    if id(c) in sink_ids:
                        continue
                    bound = {
                        t.id
                        for a in nodes
                        if isinstance(a, (ast.Assign, ast.AnnAssign)) and a.value is c
                        for t in (a.targets if isinstance(a, ast.Assign) else [a.target])
                        if isinstance(t, ast.Name)
                    }
                    if bound & sink_names:
                        continue
                    out.append((rel, qual, c.lineno))
        return out

    @classmethod
    def _assert_write_offer_dispatch(cls, trees, pinned=None) -> None:
        """#2035 check (d): the CanonicalHandlers.handle dispatch holders
        are exactly the pinned set; an "arms" holder passes the dispatch
        result to _arm_write_offer; a "carries" holder (#2041) puts
        ``write_offer=`` on its result, read from the dispatch result, AND
        every plan-running holder passes the picked ``armed_write_offer``
        to _arm_write_offer after the plan and before _track_offer_hint and
        _apply_soft_offer."""
        import ast

        pinned = cls._WRITE_OFFER_DISPATCH_HOLDERS if pinned is None else pinned
        found = cls._canonical_dispatch_holders(trees)
        assert set(found) == set(pinned), (
            f"#2035 check (d): CanonicalHandlers.handle dispatch holders are "
            f"{sorted(found)}; pinned {sorted(pinned)}. A new dispatch site must "
            f"hand the result's write_offer to IntentService._arm_write_offer; "
            f"show it, then pin it."
        )
        for key, mode in sorted(pinned.items()):
            rel, qual = key
            nodes, produced = found[key]
            arms = any(
                isinstance(n, ast.Call)
                and cls._callee_name(n) == "_arm_write_offer"
                and produced & {a.id for a in n.args if isinstance(a, ast.Name)}
                for n in nodes
            )
            if mode == "arms":
                assert produced and arms, (
                    f"#2035 check (d): {rel}::{qual} dispatches CanonicalHandlers.handle "
                    f"but its result no longer reaches _arm_write_offer"
                )
                continue
            assert mode == "carries", f"#2035 check (d): unknown pin mode {mode!r}"
            assert cls._carries_offer_hint(nodes, produced, "write_offer"), (
                f"#2041 check (d): {rel}::{qual} dispatches CanonicalHandlers.handle "
                f"but its result no longer carries write_offer"
            )
            plan_arms = cls._plan_arm_holders(
                trees, "_arm_write_offer", "armed_write_offer", ("_track_offer_hint",)
            )
            assert plan_arms, (
                f"#2041 check (d): {rel}::{qual} carries write_offer but no holder "
                f"runs a plan (.execute_plan) and arms it"
            )
            bad = [(r, q, p) for r, q, p in plan_arms if p is not None]
            assert not bad, (
                f"#2041 check (d): the carried write_offer does not reach "
                f"_arm_write_offer: {bad}"
            )

    def test_2035_write_offer_reach_tripwire(self):
        """#2035 (Arch's rule item 2, 2026-10-15), the write_offer sibling of
        test_2010_offer_hint_reach_tripwire, measured over services/**,
        web/** and main.py:
        (a) the holders that build a "write_offer" key (without arming it)
            are exactly _WRITE_OFFER_BUILDERS, in _WRITE_OFFER_BUILDER_MODULES;
        (b) the EXTERNAL referrers of every builder and every in-class method
            that transitively reaches one are exactly the pinned set;
        (c) each pinned referrer returns the result through
            _finalize_canonical_rail_result, which passes it to
            _arm_write_offer, which reads "write_offer" and calls
            set_pending_offer;
        (d) the CanonicalHandlers.handle dispatch holders are pinned with
            what each does with write_offer (the single path arms; #2041:
            the orchestrator carries it to the plan-running holder, which
            arms the picked one before the hint and the soft offer);
        (e) every call of a #846 write-offer factory reaches set_pending_offer
            or a "write_offer" value in its own holder."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        trees = self._caller_trees()
        index = dict(trees)
        reach = cls._write_offer_reach(trees)

        # (a) + (b)
        cls._assert_write_offer_reach_pinned(reach)
        # vacuity: the closure reaches the three builders plus the guidance
        # router (measured 2026-10-15: 4 reaching names).
        assert len(reach["reaching"]) >= 4, f"reach closure broke: {sorted(reach['reaching'])}"

        # (c) the rail adapters and the seam they return through.
        cls._assert_referrers_return_through_finalize(
            index,
            cls._WRITE_OFFER_EXTERNAL_CALLERS,
            cls._WRITE_OFFER_TABLE_ADAPTERS,
            reach["reaching"],
            "#2035 write_offer",
        )
        finalize = cls._find_def(
            index["services/intent_service/workflow_entries.py"], "_finalize_canonical_rail_result"
        )
        assert finalize is not None
        params = {a.arg for a in finalize.args.args}
        assert any(
            isinstance(n, ast.Call)
            and cls._callee_name(n) == "_arm_write_offer"
            and {a.id for a in n.args if isinstance(a, ast.Name)} & params
            for n in cls._own_nodes(finalize)
        ), "_finalize_canonical_rail_result no longer passes its result to _arm_write_offer"
        arm = cls._find_def(
            index["services/intent/intent_service.py"], "IntentService._arm_write_offer"
        )
        assert arm is not None, "IntentService._arm_write_offer not found"
        arm_nodes = list(cls._own_nodes(arm))
        assert any(
            isinstance(n, ast.Constant) and n.value == "write_offer" for n in arm_nodes
        ) and any(
            isinstance(n, ast.Call) and cls._callee_name(n) == "set_pending_offer"
            for n in arm_nodes
        ), "IntentService._arm_write_offer no longer reads write_offer and arms it"

        # (d) the internal route, by holder.
        cls._assert_write_offer_dispatch(trees)

        # (e) the factories, and every call of one reaches an arming point.
        factories = cls._write_offer_factories(trees)
        assert factories == set(cls._WRITE_OFFER_FACTORIES), (
            f"#2035 check (e): write-offer factories are {sorted(factories)}; "
            f"pinned {sorted(cls._WRITE_OFFER_FACTORIES)}. Show the new one's "
            f"callers arm its record, then pin it."
        )
        bad = cls._write_offer_factory_violations(trees, factories)
        assert not bad, (
            f"#2035 check (e): a write-offer record built here reaches no #846 "
            f"arming point (set_pending_offer, or a 'write_offer' result key): {bad}"
        )

    def test_2035_write_offer_reach_tripwire_fails_on_fakes(self):
        """#2035, fed fakes in memory: a new builder, a builder in a new
        module, a new external caller, a dropped factory record and a new
        dispatch holder each fail; the real shapes pass."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        mod = "services/intent_service/canonical_handlers.py"
        handlers = ast.parse(
            "class CanonicalHandlers:\n"
            "    async def handle(self, intent):\n"
            "        return await self._entry(intent)\n"
            "    async def _builder(self):\n"
            "        offer = build_add_project_offer(question='Want to add one?')\n"
            '        return {"message": "m", "write_offer": offer}\n'
            "    async def _entry(self, intent):\n"
            "        return await self._builder()\n"
            "    async def _plain(self):\n"
            '        return {"message": "no offer"}\n'
        )
        factory = ast.parse(
            "def build_add_project_offer(question, user_id=None):\n"
            '    return {"question": question}\n'
        )
        pinned_builders = {(mod, "CanonicalHandlers._builder")}
        base = [(mod, handlers), ("services/f.py", factory)]

        # the fake shapes pass when pinned as measured
        reach = cls._write_offer_reach(base, {mod})
        assert {"_builder", "_entry"} <= reach["reaching"] and "_plain" not in reach["reaching"]
        cls._assert_write_offer_reach_pinned(reach, pinned_builders, set(), {mod})

        # (a) a NEW builder in the pinned module fails
        extra = ast.parse(
            "class CanonicalHandlers:\n"
            "    async def _new_builder(self):\n"
            '        return {"write_offer": build_add_project_offer(question="Q?")}\n'
        )
        reach = cls._write_offer_reach(base + [(mod, extra)], {mod})
        with pytest.raises(AssertionError, match="_new_builder"):
            cls._assert_write_offer_reach_pinned(reach, pinned_builders, set(), {mod})

        # (a) a builder in a NEW module fails
        elsewhere = ast.parse(
            "def build(r):\n" '    r["write_offer"] = build_add_project_offer(question="Q?")\n'
        )
        reach = cls._write_offer_reach(base + [("services/new.py", elsewhere)], {mod})
        with pytest.raises(AssertionError, match="services/new.py"):
            cls._assert_write_offer_reach_pinned(reach, pinned_builders, set(), {mod})

        # (b) a NEW external caller of a reaching method fails (through the
        # in-class closure: _entry reaches _builder)
        caller = ast.parse("async def caller(ch):\n    return await ch._entry(None)\n")
        reach = cls._write_offer_reach(base + [("services/x.py", caller)], {mod})
        assert reach["external"] == {("services/x.py", "caller")}
        with pytest.raises(AssertionError, match="services/x.py"):
            cls._assert_write_offer_reach_pinned(reach, pinned_builders, set(), {mod})

        # (e) a factory record that reaches no arming point fails; one handed
        # to set_pending_offer, or to a write_offer key via a local, passes
        dropped = ast.parse(
            "def render(svc, sid):\n"
            "    offer = build_add_project_offer(question='Q?')\n"
            "    return offer['question']\n"
        )
        armed = ast.parse(
            "def arm(svc, sid):\n"
            "    svc.set_pending_offer(sid, build_add_project_offer(question='Q?'))\n"
        )
        trees = base + [("services/d.py", dropped), ("services/a.py", armed)]
        factories = cls._write_offer_factories(trees)
        assert factories == {("services/f.py", "build_add_project_offer")}
        assert cls._write_offer_factory_violations(trees, factories) == [
            ("services/d.py", "render", 2)
        ]

        # (d) a third CanonicalHandlers.handle dispatch holder fails; an
        # "arms" holder whose result skips _arm_write_offer fails
        arms_ok = ast.parse(
            "async def run(canonical_handlers, svc):\n"
            "    result = await canonical_handlers.handle(None)\n"
            "    svc._arm_write_offer(result, 's')\n"
            "    return result\n"
        )
        arms_bad = ast.parse(
            "async def run(canonical_handlers, svc):\n"
            "    result = await canonical_handlers.handle(None)\n"
            "    return result\n"
        )
        third = ast.parse(
            "async def also(canonical_handlers):\n"
            "    return await canonical_handlers.handle(None)\n"
        )
        cls._assert_write_offer_dispatch(
            [("services/r.py", arms_ok)], {("services/r.py", "run"): "arms"}
        )
        with pytest.raises(AssertionError, match="no longer reaches _arm_write_offer"):
            cls._assert_write_offer_dispatch(
                [("services/r.py", arms_bad)], {("services/r.py", "run"): "arms"}
            )
        with pytest.raises(AssertionError, match="services/t.py"):
            cls._assert_write_offer_dispatch(
                [("services/r.py", arms_ok), ("services/t.py", third)],
                {("services/r.py", "run"): "arms"},
            )
        # #2041: a "carries" holder passes when it carries write_offer AND
        # the plan-running holder arms the picked one before the hint and
        # the soft offer; it fails when it drops write_offer, when no holder
        # arms the picked one, or when the arm comes after the hint or the
        # soft offer.
        carries = ast.parse(
            "async def run(canonical_handlers):\n"
            "    result = await canonical_handlers.handle(None)\n"
            "    return Result(offer_hint=result.get('offer_hint'),\n"
            "                  write_offer=result.get('write_offer'))\n"
        )
        drops = ast.parse(
            "async def run(canonical_handlers):\n"
            "    result = await canonical_handlers.handle(None)\n"
            "    return Result(offer_hint=result.get('offer_hint'))\n"
        )
        plan_ok = (
            "async def go(self, plan):\n"
            "    o = await self.intent_orchestrator.execute_plan(plan)\n"
            "    self._arm_write_offer({'write_offer': o.armed_write_offer}, 's')\n"
            "    self._track_offer_hint({'offer_hint': o.armed_offer_hint}, 's')\n"
            "    return self._apply_soft_offer(o)\n"
        )
        carry_pin = {("services/r.py", "run"): "carries"}

        def _run(holder, plan_src):
            trees = [("services/r.py", holder)]
            if plan_src is not None:
                trees.append(("services/p.py", ast.parse(plan_src)))
            cls._assert_write_offer_dispatch(trees, carry_pin)

        _run(carries, plan_ok)  # the shape as built
        with pytest.raises(AssertionError, match="no longer carries write_offer"):
            _run(drops, plan_ok)
        with pytest.raises(AssertionError, match="no holder runs a plan"):
            _run(carries, None)
        no_arm = plan_ok.replace(
            "    self._arm_write_offer({'write_offer': o.armed_write_offer}, 's')\n", ""
        )
        with pytest.raises(AssertionError, match="never passes armed_write_offer"):
            _run(carries, no_arm)
        arm_line = "    self._arm_write_offer({'write_offer': o.armed_write_offer}, 's')\n"
        hint_line = "    self._track_offer_hint({'offer_hint': o.armed_offer_hint}, 's')\n"
        after_hint = plan_ok.replace(arm_line + hint_line, hint_line + arm_line)
        with pytest.raises(AssertionError, match="AFTER _track_offer_hint"):
            _run(carries, after_hint)
        after_soft = plan_ok.replace(arm_line, "").replace(
            "    return self._apply_soft_offer(o)\n",
            "    r = self._apply_soft_offer(o)\n" + arm_line + "    return r\n",
        )
        with pytest.raises(AssertionError, match="AFTER _apply_soft_offer"):
            _run(carries, after_soft)
        # the real orchestrator source with its write_offer carry removed fails
        orch_rel = "services/intent_service/orchestrator.py"
        index = dict(self._caller_trees())
        real = ast.unparse(index[orch_rel])
        carry = "write_offer=result.get('write_offer') or None"
        assert carry in real, "the orchestrator's write_offer carry moved; update this fake"
        dropped_real = ast.parse(real.replace(carry, "error=None"))
        real_trees = [(r, t) for r, t in index.items() if r != orch_rel]
        cls._assert_write_offer_dispatch(list(index.items()))
        with pytest.raises(AssertionError, match="no longer carries write_offer"):
            cls._assert_write_offer_dispatch(real_trees + [(orch_rel, dropped_real)])

    def test_2030_check_d_pins_dispatch_holders_fed_fakes(self):
        """#2030 (Arch's ruling item 5), check (d) fed fakes in memory: the
        dispatch sites are found by receiver BINDING (the orchestrator's
        ``self._handlers``), and the check fails when either pinned holder
        stops reaching _track_offer_hint, when the plan-running holder arms
        the picked hint after its soft offer (#1770), or when a third
        dispatch site appears."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        svc_rel = "services/intent/intent_service.py"
        orch_rel = "services/intent_service/orchestrator.py"
        svc_ok = (
            "class IntentService:\n"
            "    def __init__(self):\n"
            "        self.canonical_handlers = CanonicalHandlers()\n"
            "    async def _process_intent_internal(self, intent, plan, s, u):\n"
            "        orchestrated = await self.intent_orchestrator.execute_plan(plan, s, u)\n"
            "        self._track_offer_hint({'offer_hint': orchestrated.armed_offer_hint}, s, u)\n"
            "        multi = self._apply_soft_offer(orchestrated)\n"
            "        canonical_result = await self.canonical_handlers.handle(intent, s, u)\n"
            "        self._track_offer_hint(canonical_result, s, u)\n"
            "        return self._apply_soft_offer(canonical_result)\n"
        )
        orch_ok = (
            "class IntentOrchestrator:\n"
            "    def __init__(self, canonical_handlers):\n"
            "        self._handlers = canonical_handlers\n"
            "    async def _execute_single(self, intent, s, u):\n"
            "        result = await self._handlers.handle(intent, s, u)\n"
            "        return IntentExecutionResult(\n"
            "            intent=intent, response=result.get('message', ''),\n"
            "            offer_hint=result.get('offer_hint') or None,\n"
            "        )\n"
        )

        def trees(svc=svc_ok, orch=orch_ok, extra=None):
            out = [(svc_rel, ast.parse(svc)), (orch_rel, ast.parse(orch))]
            if extra is not None:
                out.append(("services/z.py", ast.parse(extra)))
            return out

        cls._assert_canonical_dispatch_reaches_seam(trees())  # the shape as built

        # the orchestrator stops carrying the hint
        dropped = orch_ok.replace("            offer_hint=result.get('offer_hint') or None,\n", "")
        with pytest.raises(AssertionError, match="IntentOrchestrator._execute_single"):
            cls._assert_canonical_dispatch_reaches_seam(trees(orch=dropped))
        # the single path stops arming its own result (the multi arm in the
        # same holder must not mask it)
        unarmed = svc_ok.replace("        self._track_offer_hint(canonical_result, s, u)\n", "")
        with pytest.raises(AssertionError, match="_process_intent_internal"):
            cls._assert_canonical_dispatch_reaches_seam(trees(svc=unarmed))
        # the plan-running holder never arms the picked hint
        no_plan_arm = svc_ok.replace(
            "        self._track_offer_hint({'offer_hint': orchestrated.armed_offer_hint}, s, u)\n",
            "",
        )
        with pytest.raises(AssertionError, match="never passes armed_offer_hint"):
            cls._assert_canonical_dispatch_reaches_seam(trees(svc=no_plan_arm))
        # ... or arms it AFTER the soft offer (#1770 guard cannot see it)
        late = svc_ok.replace(
            "        self._track_offer_hint({'offer_hint': orchestrated.armed_offer_hint}, s, u)\n"
            "        multi = self._apply_soft_offer(orchestrated)\n",
            "        multi = self._apply_soft_offer(orchestrated)\n"
            "        self._track_offer_hint({'offer_hint': orchestrated.armed_offer_hint}, s, u)\n",
        )
        with pytest.raises(AssertionError, match="AFTER _apply_soft_offer"):
            cls._assert_canonical_dispatch_reaches_seam(trees(svc=late))
        # a third dispatch site, under a receiver name nobody pinned
        third = (
            "class Elsewhere:\n"
            "    def __init__(self):\n"
            "        self.ch = CanonicalHandlers()\n"
            "    async def go(self, intent):\n"
            "        r = await self.ch.handle(intent, None, None)\n"
            "        self._track_offer_hint(r, None, None)\n"
            "        return r\n"
        )
        with pytest.raises(AssertionError, match="services/z.py"):
            cls._assert_canonical_dispatch_reaches_seam(trees(extra=third))
        # an unrelated .handle( (not a CanonicalHandlers receiver) is not a site
        unrelated = "async def f(sdk_handler, req):\n    return await sdk_handler.handle(req)\n"
        cls._assert_canonical_dispatch_reaches_seam(trees(extra=unrelated))

    def test_2024_offer_text_is_a_question(self):
        """#2024 hardening (a) (Arch 2026-10-15): a built ``offer_hint``
        whose constant ``offer_text`` resolves to a non-question fails the
        build. A directive or a statement is not an offer: arming one binds
        a "yes" to something the user was never asked."""
        checked = self._assert_offer_texts_are_questions(self._caller_trees())
        # vacuity: 4 constant offer_texts measured 2026-10-15 after #2024
        # (_format_project_setup_guidance, _handle_project_setup_request,
        # _format_integration_setup_guidance, _handle_portfolio_query's
        # delete-not-found); a hint built by a call resolves to none.
        # #2035: the two project-setup offers left the #852 rail for the #846
        # store -> 2, measured.
        assert checked >= 2, f"only {checked} offer_texts resolved — the scan broke"

    def test_2024_offer_text_check_fails_on_a_directive(self):
        """#2024 hardening (a), fed a fake: the directive offer_text the
        archive/restore/search not-found branches carried before #2024
        fails, naming holder and line; a question passes."""
        import ast

        cls = TestUnarmedAskSiteRatchet
        directive = ast.parse(
            "class H:\n"
            "    def not_found(self):\n"
            '        return {"message": "m", "offer_hint": {\n'
            '            "continuation_hint": "list all projects",\n'
            '            "offer_text": "Say \'list my projects\' to see what you have.",\n'
            "        }}\n"
        )
        with pytest.raises(AssertionError, match=r"services/fake\.py:5 H\.not_found"):
            cls._assert_offer_texts_are_questions([("services/fake.py", directive)])
        statement = ast.parse(
            "def f(project_count):\n"
            '    outro = "I can help you add a new project or review your existing portfolio."\n'
            '    r = {"message": outro}\n'
            '    r["offer_hint"] = {"continuation_hint": "c", "offer_text": outro}\n'
            "    return r\n"
        )
        with pytest.raises(AssertionError, match=r"services/fake\.py:2 f"):
            cls._assert_offer_texts_are_questions([("services/fake.py", statement)])
        question = ast.parse(
            "def g():\n" '    return {"offer_hint": {"offer_text": "Want to add another?"}}\n'
        )
        cls._assert_offer_texts_are_questions([("services/fake.py", question)])

    @classmethod
    def _assert_offer_texts_are_questions(cls, trees) -> int:
        """#2024 (a): every resolved constant offer_text of every built
        offer_hint in ``trees`` is interrogative (``_interrogative``, the
        census's own question test); returns how many were checked."""
        bad = []
        checked = 0
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                if not cls._builds_offer_hint(nodes):
                    continue
                for text, node in cls._offer_text_nodes(nodes):
                    checked += 1
                    if not cls._interrogative(text):
                        bad.append(f"{rel}:{getattr(node, 'lineno', '?')} {qual}: {text!r}")
        assert not bad, (
            "#2024 (Arch 2026-10-15): an offer_hint arms only on ONE yes/no "
            "question, and its offer_text is that question as rendered. These "
            "offer_texts are not questions (a directive or a statement binds "
            "no 'yes'; drop the offer_hint or ask): " + "; ".join(sorted(bad))
        )
        return checked

    # #2010: functions consumer-armed (one hop) through at least one caller
    # armed by signal (ii) alone, MEASURED 2026-10-15. The one-hop rule does
    # not check offer_text adequacy for these mechanically (the caller's hint
    # is built by a call); each is audited by hand below.
    _OFFER_HINT_CONSUMER_ARMED = frozenset(
        {
            ("services/consciousness/files_consciousness.py", "empty_projects_message"),
            # #2035: empty_projects_offer_hint deleted; its successor
            # empty_projects_offer arms itself (question= kwarg, #846 record).
        }
    )

    def test_2010_offer_hint_consumer_adequacy(self):
        """#2010 condition 2 for the one-hop route: the functions credited
        through a (ii)-only caller are exactly the measured set, and the
        empty-projects question is verbatim the offer_text its callers arm
        (the judge reads offer_text as the held question). A new function
        credited this way fails here until audited."""
        _rows, stats = self._census()
        assert stats["consumer_armed_via_offer_hint"] == set(self._OFFER_HINT_CONSUMER_ARMED), (
            f"consumer-armed through a signal-(ii) caller: "
            f"{sorted(stats['consumer_armed_via_offer_hint'])}; measured "
            f"{sorted(self._OFFER_HINT_CONSUMER_ARMED)}. Audit the new one's "
            f"question against its callers' offer_text, then pin it."
        )
        from services.consciousness.files_consciousness import (
            empty_projects_message,
            empty_projects_offer,
        )

        # #2035: the empty-projects question is now armed on the #846 store
        # by both callers (empty_projects_offer's stored question), no longer
        # as an offer_hint offer_text. _handle_portfolio_query still reaches
        # this set through its OTHER (ii) builder (the delete-not-found
        # hint), so the one-hop credit is audited against the #846 record.
        assert self._question_sentences(empty_projects_message()) == {
            empty_projects_offer()["question"]
        }

    @staticmethod
    def _joined_text(node) -> str:
        import ast

        return "".join(
            v.value if isinstance(v, ast.Constant) and isinstance(v.value, str) else "{}"
            for v in node.values
        )

    @staticmethod
    def _marker_lines(source: str) -> set:
        import io
        import tokenize

        marked = set()
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT and TestUnarmedAskSiteRatchet._MARKER_RE.search(
                tok.string
            ):
                marked.add(tok.start[0])
        return marked

    @staticmethod
    def _own_nodes(node):
        """Walk a holder body WITHOUT descending into nested defs/classes."""
        import ast

        stack = list(ast.iter_child_nodes(node))
        while stack:
            child = stack.pop()
            yield child
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                stack.extend(ast.iter_child_nodes(child))

    @classmethod
    def _holder_arms(cls, nodes, rel=None) -> bool:
        """True iff the holder's OWN body arms (class docstring). ``rel`` is
        the holder's module: signal (ii), the built ``"offer_hint"`` key, is
        credited only inside ``_OFFER_HINT_BUILDER_MODULES`` (#2010, Arch
        2026-10-15 condition 1); without ``rel`` it is never credited."""
        import ast

        nodes = list(nodes)
        for sub in nodes:
            if isinstance(sub, ast.Call):
                f = sub.func
                attr = (
                    f.attr
                    if isinstance(f, ast.Attribute)
                    else (f.id if isinstance(f, ast.Name) else None)
                )
                # #2010 signal (i): `_track_offer_hint(` converts an
                # offer_hint into LastOffer itself — the call is the arm.
                if attr in ("set_pending_offer", "LastOffer", "_track_offer_hint"):
                    return True
                if any(kw.arg == "question" for kw in sub.keywords):
                    return True
            # #2011 call 2 (Arch 2026-10-14): the slot-filling machine's
            # transition INTO an answer-binding state is an arm — the next
            # reply is routed by `filling_state` to the handler that binds it
            # (slot_filling_manager.handle_turn). Terminal states
            # (COMPLETE/CANCELLED) are NOT arms.
            if isinstance(sub, (ast.Assign, ast.AnnAssign)):
                targets = sub.targets if isinstance(sub, ast.Assign) else [sub.target]
                v = sub.value
                if (
                    any(isinstance(t, ast.Attribute) and t.attr == "filling_state" for t in targets)
                    and isinstance(v, ast.Attribute)
                    and v.attr in cls._SLOT_ARM_STATES
                    and isinstance(v.value, ast.Name)
                    and v.value.id == "SlotFillingState"
                ):
                    return True
            if isinstance(sub, ast.Dict) and any(
                isinstance(k, ast.Constant) and k.value == "question" for k in sub.keys
            ):
                return True
            if (
                isinstance(sub, ast.Constant)
                and isinstance(sub.value, str)
                and sub.value.endswith("_pending")
            ):
                return True
        # #2010 signal (ii), reach-scoped by module (condition 1).
        return rel in cls._OFFER_HINT_BUILDER_MODULES and cls._builds_offer_hint(nodes)

    @classmethod
    def _offer_hint_values(cls, nodes):
        """The value expressions of every ``"offer_hint"`` key the holder
        builds: a dict-literal key, or a subscript assignment
        ``x["offer_hint"] = ...``."""
        return cls._built_key_values(nodes, "offer_hint")

    @staticmethod
    def _built_key_values(nodes, key):
        """The value expressions of every ``key`` the holder builds (a
        dict-literal key, or ``x[key] = ...``); #2010 offer_hint, #2035
        write_offer."""
        import ast

        out = []
        for sub in nodes:
            if isinstance(sub, ast.Dict):
                out.extend(
                    v
                    for k, v in zip(sub.keys, sub.values)
                    if isinstance(k, ast.Constant) and k.value == key
                )
            elif isinstance(sub, (ast.Assign, ast.AnnAssign)) and sub.value is not None:
                targets = sub.targets if isinstance(sub, ast.Assign) else [sub.target]
                if any(
                    isinstance(t, ast.Subscript)
                    and isinstance(t.slice, ast.Constant)
                    and t.slice.value == key
                    for t in targets
                ):
                    out.append(sub.value)
        return out

    @classmethod
    def _builds_offer_hint(cls, nodes) -> bool:
        return bool(cls._offer_hint_values(nodes))

    @classmethod
    def _offer_texts(cls, nodes) -> set:
        """The ``offer_text`` strings the holder's built offer_hints carry,
        resolved within the holder: a literal, an f-string, or a local name
        bound to either (``offer_text: outro``) or to the hint dict itself
        (``"offer_hint": offer_hint``). A value built elsewhere (a call)
        resolves to nothing — its holder's literals then cannot be covered."""
        return {text for text, _node in cls._offer_text_nodes(nodes)}

    @classmethod
    def _offer_text_nodes(cls, nodes) -> list:
        """(text, node) per resolved ``offer_text`` constant (see
        ``_offer_texts``); the node carries the source line (#2024 (a))."""
        import ast

        assigns = {}
        for sub in nodes:
            if isinstance(sub, ast.Assign):
                for t in sub.targets:
                    if isinstance(t, ast.Name):
                        assigns.setdefault(t.id, []).append(sub.value)
            elif (
                isinstance(sub, ast.AnnAssign)
                and sub.value is not None
                and isinstance(sub.target, ast.Name)
            ):
                assigns.setdefault(sub.target.id, []).append(sub.value)

        def resolve(expr):
            if isinstance(expr, ast.Name):
                return assigns.get(expr.id, [])
            return [expr]

        out = []
        for hint in cls._offer_hint_values(nodes):
            for d in resolve(hint):
                if not isinstance(d, ast.Dict):
                    continue
                for k, v in zip(d.keys, d.values):
                    if not (isinstance(k, ast.Constant) and k.value == "offer_text"):
                        continue
                    for e in resolve(v):
                        if isinstance(e, ast.Constant) and isinstance(e.value, str):
                            out.append((e.value, e))
                        elif isinstance(e, ast.JoinedStr):
                            out.append((cls._joined_text(e), e))
        return out

    @classmethod
    def _question_sentences(cls, text: str) -> set:
        return {" ".join(q.split()) for q in cls._QUESTION_SENTENCE_RE.findall(text) if q.strip()}

    @classmethod
    def _offer_text_covers(cls, text: str, offer_texts) -> bool:
        """#2010 condition 2 (#1739 (a)), mechanically: every question
        sentence ``text`` renders is, verbatim (whitespace-normalized), a
        question sentence of an ``offer_text`` the holder arms — the judge
        reads offer_text as the held question."""
        held = set()
        for ot in offer_texts:
            held |= cls._question_sentences(ot)
        asked = cls._question_sentences(text)
        return bool(asked) and asked <= held

    @staticmethod
    def _utterance_ctors(tree) -> set:
        """Corpus callables whose FIRST (non-self) parameter is `utterance` —
        strings passed to them are sample USER phrasings, not Piper asks."""
        import ast

        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                        args = [a.arg for a in item.args.args if a.arg != "self"]
                        if args and args[0] == "utterance":
                            names.add(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
                if args and args[0] == "utterance":
                    names.add(node.name)
        return names

    @classmethod
    def _excluded_string_ids(cls, tree, utterance_ctors) -> set:
        """ids of string nodes in non-emitting contexts (matching, logging,
        raising, comparison, dict keys, utterance corpora)."""
        import ast

        excluded = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                f = node.func
                attr = (
                    f.attr
                    if isinstance(f, ast.Attribute)
                    else (f.id if isinstance(f, ast.Name) else None)
                )
                root = f
                while isinstance(root, ast.Attribute):
                    root = root.value
                root_name = root.id if isinstance(root, ast.Name) else None
                non_emitting = (
                    attr in cls._MATCHER_ATTRS
                    or root_name in ("logger", "logging", "log")
                    or attr in utterance_ctors
                )
                if non_emitting:
                    for arg in node.args:
                        excluded.update(id(s) for s in ast.walk(arg))
                for kw in node.keywords:
                    if (
                        non_emitting
                        or kw.arg in cls._USER_TEXT_KWARGS
                        or (kw.arg is not None and cls._EXAMPLE_NAME_RE.search(kw.arg))
                    ):
                        excluded.update(id(s) for s in ast.walk(kw.value))
            elif isinstance(node, ast.Compare):
                excluded.update(id(s) for s in ast.walk(node))
            elif isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if key is not None:
                        excluded.update(id(s) for s in ast.walk(key))
                        # #2011 (c): value under a *question*-named key.
                        if (
                            isinstance(key, ast.Constant)
                            and isinstance(key.value, str)
                            and cls._QUESTION_NAME_RE.search(key.value)
                        ):
                            excluded.update(id(s) for s in ast.walk(value))
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                # #2011 (c): value assigned to a self.*question* attribute.
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if node.value is not None and any(
                    isinstance(t, ast.Attribute) and cls._QUESTION_NAME_RE.search(t.attr)
                    for t in targets
                ):
                    excluded.update(id(s) for s in ast.walk(node.value))
            elif isinstance(node, ast.Raise):
                excluded.update(id(s) for s in ast.walk(node))
        return excluded

    @staticmethod
    def _docstring_ids(tree) -> set:
        import ast

        ids = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if (
                    body
                    and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                ):
                    ids.add(id(body[0].value))
        return ids

    @staticmethod
    def _collect_holders(tree):
        """(qualname, body-nodes) per holder: every def, plus module/class-
        level assignment targets (copy constants/containers)."""
        import ast

        result = []

        def rec(node, prefix, at_top):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    q = f"{prefix}{child.name}"
                    result.append((q, list(TestUnarmedAskSiteRatchet._own_nodes(child))))
                    rec(child, q + ".", False)
                elif isinstance(child, ast.ClassDef):
                    rec(child, f"{prefix}{child.name}.", True)
                elif (
                    at_top
                    and isinstance(child, ast.Assign)
                    and len(child.targets) == 1
                    and isinstance(child.targets[0], ast.Name)
                ):
                    result.append((f"{prefix}{child.targets[0].id}", list(ast.walk(child.value))))
                elif (
                    at_top
                    and isinstance(child, ast.AnnAssign)
                    and child.value is not None
                    and isinstance(child.target, ast.Name)
                ):
                    result.append((f"{prefix}{child.target.id}", list(ast.walk(child.value))))
                elif at_top:
                    result.append(
                        (
                            f"{prefix}<toplevel>",
                            list(TestUnarmedAskSiteRatchet._own_nodes(child)) + [child],
                        )
                    )

        rec(tree, "", True)
        return result

    # #2011 bound 2: the one-hop caller search spans production code beyond
    # the census scope (an excluded package's caller still counts); bound 3:
    # tests/ is not a root, so a test caller counts neither way.
    _CALLER_ROOTS = (
        os.path.join("services", "**", "*.py"),
        os.path.join("web", "**", "*.py"),
        "main.py",
    )

    def _caller_trees(self):
        """(rel, tree) for every file under _CALLER_ROOTS — no exclusions."""
        import ast

        root = self._repo_root()
        out = []
        for pattern in self._CALLER_ROOTS:
            for path in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                with open(path, encoding="utf-8") as fh:
                    out.append((rel, ast.parse(fh.read())))
        return out

    @classmethod
    def _caller_index(cls, trees):
        """One-hop caller index over ``trees``: (callers, indirect, arming,
        hint_only); hint_only: the arming holders armed by #2010 signal (ii)
        alone.
        callers: simple name -> {(rel, holder)} that CALL it directly.
        indirect: names referenced other than as a call's callee (a Load of
        the name / attribute outside a call position, or a string argument
        to getattr/hasattr) — their callers are unknown (bound 4).
        arming: holders that arm by their OWN body (never consumer-armed —
        one hop only, bound 4)."""
        import ast

        callers, indirect, arming, hint_only = {}, set(), set(), set()
        for rel, tree in trees:
            for qual, nodes in cls._collect_holders(tree):
                if cls._holder_arms(nodes, rel):
                    arming.add((rel, qual))
                    if not cls._holder_arms(nodes):
                        hint_only.add((rel, qual))
                callee_ids = set()
                for sub in nodes:
                    if not isinstance(sub, ast.Call):
                        continue
                    f = sub.func
                    callee_ids.add(id(f))
                    name = (
                        f.attr
                        if isinstance(f, ast.Attribute)
                        else (f.id if isinstance(f, ast.Name) else None)
                    )
                    if name:
                        callers.setdefault(name, set()).add((rel, qual))
                    if name in ("getattr", "hasattr") and len(sub.args) >= 2:
                        a = sub.args[1]
                        if isinstance(a, ast.Constant) and isinstance(a.value, str):
                            indirect.add(a.value)
                for sub in nodes:
                    if id(sub) in callee_ids:
                        continue
                    if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                        indirect.add(sub.id)
                    elif isinstance(sub, ast.Attribute) and isinstance(sub.ctx, ast.Load):
                        indirect.add(sub.attr)
        return callers, indirect, arming, hint_only

    @staticmethod
    def _consumer_armed(rel, qual, index) -> bool:
        """#2011 call 2, Arch's four bounds: a MODULE-LEVEL function is armed
        iff (1) at least one caller exists and EVERY caller arms by its own
        body, (2) callers drawn from services/**, web/** and main.py, (3)
        tests never counted, (4) never if referenced other than by a direct
        call; one hop only (a consumer-armed caller does not arm)."""
        callers_of, indirect, arming = index[:3]
        if "." in qual or qual in indirect:
            return False
        callers = callers_of.get(qual, set()) - {(rel, qual)}
        return bool(callers) and callers <= arming

    def _census(self):
        """Run the predicate. Returns (rows, stats) where rows is the set of
        (file, holder, literal-count, fingerprint) for UNARMED ask sites and
        stats carries the vacuity-guard denominators."""
        import ast

        root = self._repo_root()
        parsed = []
        utterance_ctors = set()
        for pattern in self._SCAN_GLOBS:
            for path in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                if rel in self._EXCLUDED_MODULES or rel.startswith(self._EXCLUDED_PACKAGES):
                    continue
                with open(path, encoding="utf-8") as fh:
                    source = fh.read()
                tree = ast.parse(source)
                parsed.append((rel, source, tree))
                utterance_ctors |= self._utterance_ctors(tree)

        sites = {}
        arming = set()
        hint_armed = {}
        marker_exemptions = []
        open_invitations = []
        # #2011 call 2 (bounds blessed by Arch 2026-10-14 round 2): the
        # one-hop caller index spans services/**, web/** and main.py (bound
        # 2), never tests/ (bound 3).
        caller_index = self._caller_index(self._caller_trees())
        for rel, source, tree in parsed:
            marked = self._marker_lines(source)
            excluded = self._excluded_string_ids(tree, utterance_ctors)
            docs = self._docstring_ids(tree)
            for qual, nodes in self._collect_holders(tree):
                key = (rel, qual)
                simple = qual.rsplit(".", 1)[-1].upper()
                skip_holder = (
                    "EXAMPLE" in simple
                    or "PROMPT" in simple
                    or self._QUESTION_NAME_RE.search(simple)
                )
                if self._holder_arms(nodes, rel):
                    arming.add(key)
                    if not self._holder_arms(nodes):
                        # armed by #2010 signal (ii) alone: its rows are
                        # credited only if offer_text covers them (below).
                        hint_armed[key] = self._offer_texts(nodes)
                for sub in nodes:
                    text = None
                    if isinstance(sub, ast.JoinedStr) and id(sub) not in excluded:
                        text = self._joined_text(sub)
                        for part in sub.values:
                            excluded.add(id(part))
                    elif (
                        isinstance(sub, ast.Constant)
                        and isinstance(sub.value, str)
                        and id(sub) not in excluded
                        and id(sub) not in docs
                    ):
                        text = sub.value
                    if text is None or not self._interrogative(text):
                        continue
                    if skip_holder:
                        continue
                    if self._open_invitation(text):
                        open_invitations.append((rel, qual, text))
                        continue
                    lineno = getattr(sub, "lineno", 0)
                    if lineno in marked or (lineno - 1) in marked:
                        marker_exemptions.append((rel, qual, lineno))
                        continue
                    sites.setdefault(key, []).append(text)

        # #2011 call 2 — CONSUMER-ARMED (one hop, four bounds; see
        # _consumer_armed). E.g. slot_prompts.format_final_confirmation,
        # called only by the slot-filling handlers that enter/hold CONFIRMING.
        # #2010 condition 2 (Arch 2026-10-15): a holder armed by signal (ii)
        # alone has its row removed only if every interrogative literal it
        # holds is covered by an offer_text it arms; otherwise the row STAYS
        # and the mismatch is reported (stats["offer_text_mismatch"]).
        offer_text_mismatch = {}
        for key, offer_texts in hint_armed.items():
            uncovered = [
                t for t in sites.get(key, []) if not self._offer_text_covers(t, offer_texts)
            ]
            if uncovered:
                offer_text_mismatch[key] = uncovered
        row_arming = arming - set(offer_text_mismatch)

        consumer_armed = {
            (rel, qual)
            for rel, qual in sites
            if (rel, qual) not in row_arming and self._consumer_armed(rel, qual, caller_index)
        }
        # consumer-armed through at least one caller armed by (ii) alone —
        # pinned and audited in test_2010_offer_hint_consumer_adequacy.
        consumer_armed_via_offer_hint = {
            (rel, qual)
            for rel, qual in consumer_armed
            if (caller_index[0].get(qual, set()) - {(rel, qual)}) & caller_index[3]
        }

        rows = set()
        for (rel, qual), texts in sites.items():
            if (rel, qual) in row_arming or (rel, qual) in consumer_armed:
                continue
            normalized = sorted(" ".join(t.split()) for t in texts)
            rows.add((rel, qual, len(texts), normalized[0][:60]))

        stats = {
            "files": len(parsed),
            "interrogative_literals": sum(len(v) for v in sites.values()),
            "arming_holders": len(arming),
            "arming": arming,
            "marker_exemptions": marker_exemptions,
            "open_invitations": open_invitations,
            "consumer_armed": consumer_armed,
            "offer_hint_credited": {k for k in hint_armed if k in sites} - set(offer_text_mismatch),
            "offer_text_mismatch": offer_text_mismatch,
            "consumer_armed_via_offer_hint": consumer_armed_via_offer_hint,
        }
        return rows, stats

    # ---- the tests ----

    def test_scan_space_is_populated(self):
        """Vacuity guard (m-44): the census must actually see the known
        world — an empty derivation is indistinguishable from a broken
        scanner and must fail loudly, never pass as 'no violations'."""
        rows, stats = self._census()
        # Floor 40 -> 400 (2026-10-14, #2011): measured 454 files under the
        # services/** widening; 400 also fails if the glob silently reverts
        # to the old two packages (56 files).
        assert stats["files"] >= 400, (
            f"ask-site census scanned only {stats['files']} files — the scan "
            f"glob broke; fix the derivation before trusting any result."
        )
        # Floor lowered 42 -> 35 (2026-10-04, #1595 Phase 3 manage_portfolio
        # WRITE split): measured 42 before this unit, 38 after — a REAL,
        # deliberate reduction (4 interrogative literals removed), not a
        # scanner regression. Hoisting _handle_portfolio_query's ARCHIVE/
        # RESTORE branches into their own methods would have duplicated
        # their "project not found… Would you like me to list…?" message +
        # offer_hint literals into two NEW holders (TestUnarmedAskSiteRatchet
        # below would then have failed on the new-row check) — rewritten as
        # imperative, non-interrogative copy instead (the #1856 precedent),
        # which legitimately shrinks the total. 35 keeps headroom under the
        # measured 38 while still catching true scanner breakage (near-zero),
        # which is this guard's actual job per its own docstring.
        # Floor 35 -> 30 (2026-10-06): measured 34 after the close/reopen multi-match
        # asks became declarative (two literals removed deliberately, CXO 10-05 flag).
        # Headroom under the measured count; a broken detector reads near zero.
        assert stats["interrogative_literals"] >= 30, (
            f"ask-site census found only {stats['interrogative_literals']} "
            f"interrogative literals (dozens exist) — the literal detector "
            f"broke; fix it before trusting any result."
        )
        assert stats["arming_holders"] >= 30, (
            f"ask-site census found only {stats['arming_holders']} arming "
            f"holders (the corpus has dozens of set_pending_offer sites) — "
            f"the arm detector broke; fix it before trusting any result."
        )
        assert any(
            rel == "services/intent_service/reminder_clear.py" for rel, _ in stats["arming"]
        ), (
            "The arm scan no longer sees reminder_clear.py's arm sites (the "
            "densest set_pending_offer file) — the scanner is measuring "
            "nothing; fix it before trusting this class's other results."
        )

    def test_no_new_unarmed_ask_sites(self):
        """#1766 requirement 1: a NEW question-emitting site that does not
        arm fails the build BY BEING FOUND. Fix: arm through the one-slot
        store — render the ask once, store it (question= / \"question\" key,
        #1665) and set_pending_offer — or don't ask. Do NOT add a row."""
        rows, _stats = self._census()
        new_rows = rows - self.KNOWN_UNARMED_ASK_SITES
        assert not new_rows, (
            f"NEW unarmed ask site(s): {sorted(new_rows)}. The #1730 Gap-2 "
            f"ruling: every question-emitting site arms through the one-slot "
            f"store (#846) or doesn't ask. Arm the site (store the rendered "
            f"ask + set_pending_offer — see reminder_clear.py's verb-question "
            f"seam for the reference shape) instead of adding a row; "
            f"KNOWN_UNARMED_ASK_SITES only shrinks. (A changed row for an "
            f"already-listed holder means its ask copy or count changed — "
            f"re-measure and update the row in the same commit, shrinking if "
            f"you armed it.)"
        )

    def test_unarmed_baseline_stays_tight(self):
        """Shrink-only, enforced: a row whose site no longer emits an
        unarmed ask is STALE — remove it in the arming commit so the table
        always states the true remaining debt (m-44)."""
        rows, _stats = self._census()
        stale = self.KNOWN_UNARMED_ASK_SITES - rows
        assert not stale, (
            f"KNOWN_UNARMED_ASK_SITES lists sites the census no longer "
            f"finds unarmed: {sorted(stale)}. Remove the rows (the table "
            f"only shrinks); if the holder still asks but its copy changed, "
            f"update the row's count/fingerprint in the same commit."
        )

    def test_marker_exemptions_stay_bounded(self):
        """The `# ask-census:` marker is the sanctioned residual annotation
        (it lives AT the site with its reason) — ceilinged and tight so it
        stays an exception, never an exit ramp from the ratchet."""
        _rows, stats = self._census()
        n = len(stats["marker_exemptions"])
        assert n == self.MAX_MARKER_EXEMPTIONS, (
            f"ask-census marker exemptions: {n} "
            f"(expected exactly {self.MAX_MARKER_EXEMPTIONS}): "
            f"{stats['marker_exemptions']}. A new marker needs review — it "
            f"must state at its site why the literal is not an unarmed ask "
            f"(armed-in-turn via a callee, or not user-facing ask copy) — "
            f"and this ceiling updated deliberately in the same commit; a "
            f"removed marker lowers it."
        )


class TestSentinelSiteMypyEnforcement1800:
    """#1800 — the #1425 sentinel contract ("a source that FAILED returns
    ``None``/``source_failed: True``, never an empty list/0") IS mechanically
    enforceable, and the mechanism already exists: mypy, run via the #1436
    gate (scripts/check_mypy_gate.py), already reports every drift site
    where a sentinel-carrying value is produced with a type mypy can't
    reconcile against its own declared return type. #1777's crash
    (canonical_handlers.py, pre-fix) WAS reported by mypy — as
    ``[arg-type]``/``[return-value]``/``[assignment]`` errors — it just sat
    buried inside PER-CODE AGGREGATE ceilings of 377/240/49, where five
    real drift lines are invisible against ~1,300 legacy errors elsewhere
    in the tree. #1777's own quote: "Those five lines ARE the census."

    **The decision, stated** (closing #1777 AC3's ask for "a stated decision
    on mechanical enforcement vs. per-site discipline", and #1800's own
    scope-unit question): **mechanical, symbol-scoped — not per-site
    discipline, and not a per-file zero.** Per-site discipline is refuted
    by the record: #1425, #1460, #1472, #1573, #1639, #1645, #1717 and
    #1776 each hand-guarded the sites they touched, and #1777 still
    happened, four lines below a comment describing the exact crash — eight
    rounds of discipline is a control that has already failed eight times,
    not an unlucky ninth. A per-FILE zero is not viable either:
    canonical_handlers.py alone carries ~60 unrelated legacy mypy errors,
    so a whole-file zero-ceiling could never be satisfied without fixing
    debt this issue doesn't own. The viable unit is PER-SYMBOL: for each
    named sentinel-PRODUCING function below, assert mypy reports ZERO
    errors whose (file, line) falls inside that function's own body. These
    six functions are each small and self-contained, and each already
    sits at zero today (#1777 fixed exactly these sites) — this test pins
    that outcome so it cannot silently regress back under the aggregate
    the way it did the first time.

    **Sentinel-producer census** (the #1777 census — "the sentinel family
    splits in two ... bare-None (4 producers) vs dict-flag (6 producers,
    the #1717 SOURCE_FAILED_FLAGS registry)" — function names resolved
    against the three files that carry the #1425 fix):
      1. ``_get_priority_metadata`` (canonical_handlers.py) — dict-flag
         sentinel (``source_failed``)
      2. ``_get_todays_todos`` (canonical_handlers.py) — bare-None sentinel
         (agenda todos)
      3. ``_get_completed_todos_for_date`` (canonical_handlers.py) —
         bare-None sentinel (retrospective / completed todos)
      4. ``_handle_status_report`` (canonical_handlers.py) — bare-None
         sentinel (``open_todos_count``, produced and consumed inline)
      5. ``get_due_reminders`` (todo_handlers.py) — bare-None sentinel
         (due reminders)
      6. ``_compute_reminder_context`` (context_assembler.py) — dict-flag
         sentinel (``source_failed``), the #1717-registry sibling of #1

    **Denominator, stated**: 6 of 6 census-named sentinel-PRODUCING
    functions (#1777's "5 handlers" — priority metadata, agenda todos,
    retrospective, status report, reminders — with the reminder handler
    split into its two-file pair, ``get_due_reminders`` /
    ``_compute_reminder_context``, both of which independently produce a
    sentinel). **What this test does NOT cover** (named, not silently
    absorbed, per m-43/m-44): the #1777 census also found 21 CONSUMER
    sites (12 is-None guards, 4 len(), 3 iterations, 2 ``or []`` defaults)
    scattered across large orchestrator methods
    (``_handle_agenda_query``, ``_handle_retrospective_query``,
    ``gather_context``) that this test does not scope to, because those
    methods carry substantial PRE-EXISTING, unrelated mypy debt (e.g.
    ``gather_context`` alone has ~14 legacy ``[assignment]`` errors from
    implicit-Optional parameter defaults) — a zero-ceiling on the whole
    method would fail today for reasons that have nothing to do with the
    sentinel contract, and scoping to the exact call line rather than the
    whole method is the finer-grained mechanism #1800 leaves open for
    Arch. This test covers the PRODUCER half of the census: the point
    where the sentinel is created and typed. It is layer: static
    type-check (mypy), same invocation as the #1436 gate — not a runtime
    behavioral test.
    """

    # (relative path from repo root, function name, sentinel shape)
    SENTINEL_SITES = [
        (
            "services/intent_service/canonical_handlers.py",
            "_get_priority_metadata",
            "dict-flag (source_failed)",
        ),
        ("services/intent_service/canonical_handlers.py", "_get_todays_todos", "bare-None"),
        (
            "services/intent_service/canonical_handlers.py",
            "_get_completed_todos_for_date",
            "bare-None",
        ),
        ("services/intent_service/canonical_handlers.py", "_handle_status_report", "bare-None"),
        ("services/intent_service/todo_handlers.py", "get_due_reminders", "bare-None"),
        (
            "services/intent_service/context_assembler.py",
            "_compute_reminder_context",
            "dict-flag (source_failed)",
        ),
    ]

    _MYPY_ERROR_LINE = re.compile(
        r"^(?P<file>[^:]+):(?P<line>\d+): error: .*\[(?P<code>[a-z-]+)\]\s*$"
    )

    def _repo_root(self) -> Path:
        return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def _function_range(self, repo_root: Path, rel_path: str, func_name: str) -> tuple:
        """(start_line, end_line) of the named top-level-or-method function,
        via ast — not a line-count guess. Fails loudly (not a skip) if the
        name isn't found: a renamed/removed sentinel producer must not
        silently make this test vacuous."""
        source = (repo_root / rel_path).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rel_path)
        matches = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name
        ]
        assert matches, (
            f"{rel_path}: no function named `{func_name}` found. It was "
            f"renamed or removed — update SENTINEL_SITES (#1800) rather "
            f"than let this test go silently vacuous."
        )
        assert len(matches) == 1, (
            f"{rel_path}: `{func_name}` matched {len(matches)} function defs "
            f"— name is ambiguous in this file; SENTINEL_SITES needs a more "
            f"specific locator (#1800)."
        )
        node = matches[0]
        assert node.end_lineno is not None
        return node.lineno, node.end_lineno

    def _run_gate_mypy_raw(self, repo_root: Path) -> str:
        """The #1436 gate's OWN mypy invocation, reused verbatim via
        scripts/check_mypy_gate.py --raw (added for #1800) — never
        re-implemented. Line-level output, not the per-code Counter the
        gate normally reports."""
        gate_python = repo_root / "venv-mypy-gate" / "bin" / "python"
        proc = subprocess.run(
            [str(gate_python), "scripts/check_mypy_gate.py", "--raw"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=900,
        )
        assert proc.returncode == 0, (
            f"scripts/check_mypy_gate.py --raw exited {proc.returncode} "
            f"(expected 0 — --raw always exits 0 on a completed mypy run): "
            f"stderr tail: {proc.stderr[-2000:]}"
        )
        assert proc.stdout.strip(), (
            "scripts/check_mypy_gate.py --raw produced no output — mypy did "
            "not run; refusing to treat empty output as zero errors (the "
            "same m-44 guard run_mypy_raw() itself applies)."
        )
        return proc.stdout

    def test_zero_mypy_errors_on_sentinel_producing_functions(self):
        """Layer: static type-check (mypy, the #1436 gate's own invocation).
        Denominator: 6 of 6 census-named sentinel-producing functions across
        3 files (see class docstring for what's covered vs. not)."""
        repo_root = self._repo_root()
        gate_python = repo_root / "venv-mypy-gate" / "bin" / "python"
        if not gate_python.exists():
            pytest.skip(
                "venv-mypy-gate/ absent — the #1436 mypy gate is not built "
                "in this environment. Build it with "
                "scripts/bootstrap-mypy-gate-venv.sh, or run this test where "
                "it already exists (e.g. `scripts/run-sweep.sh ratchets`). "
                "Not run != zero errors — skipping states that explicitly "
                "rather than reporting a false pass (m-44)."
            )

        # Resolve each named function's line range via ast (fails loudly,
        # not silently, on a rename/removal — see _function_range).
        ranges = {}
        for rel_path, func_name, _shape in self.SENTINEL_SITES:
            ranges[(rel_path, func_name)] = self._function_range(repo_root, rel_path, func_name)

        raw = self._run_gate_mypy_raw(repo_root)
        error_lines = [ln for ln in raw.splitlines() if self._MYPY_ERROR_LINE.match(ln)]

        violations = []
        for rel_path, func_name, shape in self.SENTINEL_SITES:
            start, end = ranges[(rel_path, func_name)]
            for line in error_lines:
                m = self._MYPY_ERROR_LINE.match(line)
                if m and m.group("file") == rel_path and start <= int(m.group("line")) <= end:
                    violations.append(f"{func_name} [{shape}] — {line}")

        assert not violations, (
            f"mypy reports {len(violations)} error(s) inside sentinel-"
            f"producing function bodies (denominator: 6 of 6 census-named "
            f"functions, {len(error_lines)} total gate errors scanned): \n"
            + "\n".join(violations)
            + "\n\nThis is exactly the #1777 shape: a sentinel-returning "
            "function whose own return/assignment type mypy can't "
            "reconcile. Fix the annotation or the return value at the "
            "site — do not widen SENTINEL_SITES to route around it."
        )

    def test_sentinel_producer_names_resolve_uniquely(self):
        """Guard on the census list itself: every SENTINEL_SITES entry must
        resolve to exactly one function in its file. This is what makes the
        main test's silence trustworthy — a name that stopped resolving
        would otherwise make the zero-error assertion vacuously true."""
        repo_root = self._repo_root()
        for rel_path, func_name, _shape in self.SENTINEL_SITES:
            start, end = self._function_range(repo_root, rel_path, func_name)
            assert (
                start <= end
            ), f"{rel_path}:{func_name} resolved to an inverted range ({start}, {end})"


class TestConsentSlotTouchRatchet1817:
    """#1817 — the invalidation trigger for #1816's dated assumption, made
    mechanical.

    ``resolve_authorized_providers`` (services/llm/provider_selection.py) reads
    a verified-ABSENT consent list as "everything configured is authorized" —
    consent inferred from key presence. That is safe for exactly one reason:
    the ``authorized_llm_providers`` slot has ONE writer (``/setup``), derived
    mechanically from which keys the user supplied, so "has a key" and
    "authorized it" cannot disagree. The first surface that lets a user
    de-authorize a provider whose key they still hold (a Settings toggle, an
    org policy, an import path that writes keys without a consent list) turns
    "absent" from "nothing was restricted" into "we never asked" — and the
    branch reads the two identically.

    A comment states that expiry; an issue makes it findable; THIS makes it
    unmissable: the exact set of production files that touch the slot is
    pinned. A new file touching it fails the build with the instruction
    #1817's requirement 1 states — revisit the verified-absent branch in the
    same change, and either re-decide it or retire the inference for an
    explicitly-written consent list. Never widen the set without doing that.
    """

    SLOT = "authorized_llm_providers"
    # The three files that touch the slot today, and why each is allowed to:
    #   provider_selection.py — the reader (CONSENT_SLOT + the dated branch)
    #   llm_config_service.py — documents the slot's origin (#946 comment)
    #   setup.py              — THE ONE WRITER (derived from the supplied keys)
    KNOWN_TOUCHERS = {
        "services/llm/provider_selection.py",
        "services/config/llm_config_service.py",
        "web/api/routes/setup.py",
    }

    def _touchers(self):
        repo_root = Path(__file__).resolve().parents[1]
        found = set()
        for root in ("services", "web", "cli"):
            for path in (repo_root / root).rglob("*.py"):
                if "tests" in path.parts:
                    continue
                if self.SLOT in path.read_text(encoding="utf-8", errors="ignore"):
                    found.add(path.relative_to(repo_root).as_posix())
        if (repo_root / "main.py").exists() and self.SLOT in (repo_root / "main.py").read_text():
            found.add("main.py")
        return found

    def test_consent_slot_touchers_are_exactly_the_known_set(self):
        found = self._touchers()
        new = sorted(found - self.KNOWN_TOUCHERS)
        gone = sorted(self.KNOWN_TOUCHERS - found)
        assert not new, (
            f"NEW file(s) touch the '{self.SLOT}' consent slot: {new}. This is "
            "#1817's invalidation trigger firing. If the new code can WRITE the "
            "slot (a de-authorize surface, a policy, an import path), the "
            "verified-absent branch in services/llm/provider_selection.py::"
            "resolve_authorized_providers must be re-decided in this same change "
            "(absent no longer means 'nothing was restricted'), and #1817 closed "
            "or amended with that decision. Then, and only then, add the file here."
        )
        assert not gone, (
            f"Known consent-slot file(s) no longer touch it: {gone} — update "
            "KNOWN_TOUCHERS (and check whether the one writer moved: if setup.py "
            "stopped writing the slot, who writes it now?)."
        )

    def test_the_slot_still_has_exactly_one_production_writer(self):
        """The inference's whole justification. A write is a call that stores
        the slot's value; today that is setup.py's keychain store call. Counted
        by the slot literal appearing as a store ARGUMENT (not a read)."""
        repo_root = Path(__file__).resolve().parents[1]
        writers = []
        # A write is the slot literal appearing as an ARGUMENT of a store-shaped
        # call — `store_api_key(\n "authorized_llm_providers", …` — so look at
        # the literal's line and the two lines above it for the call opener. A
        # read (`CONSENT_SLOT = "…"`, `.get("…")`, a comment) never matches.
        store_call = re.compile(r"\b(store|set|save|write|put)\w*\s*\($")
        for rel in sorted(self.KNOWN_TOUCHERS | self._touchers()):
            lines = (repo_root / rel).read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if f'"{self.SLOT}"' in line or f"'{self.SLOT}'" in line:
                    window = [ln.strip() for ln in lines[max(0, i - 2) : i + 1]]
                    if any(store_call.search(ln) for ln in window) or re.search(
                        r"\b(store|set|save|write|put)\w*\s*\(\s*['\"]" + self.SLOT, line
                    ):
                        writers.append(rel)
                        break
        assert writers == ["web/api/routes/setup.py"], (
            f"Expected exactly one production writer of '{self.SLOT}' (setup.py); "
            f"found {writers}. A second writer invalidates the consent-from-key-"
            "presence inference (#1817) — see the class docstring."
        )


class TestGuidedProcessStartersRegistered1867:
    """#1867 — every guided-process SESSION-START call site must name a
    ``ProcessType`` that ``services.process.guided_process_registry.
    GUIDED_PROCESSES`` declares LIVE (i.e. an adapter is actually registered
    with ``ProcessRegistry``, so a follow-up turn can reach it).

    Background (ADR-059, #1856): onboarding was put "on ice" as a code
    comment — ``# registry.register(OnboardingProcessAdapter())`` in
    ``services/process/adapters.py``. Nothing enforced that a session-start
    call site actually agreed with that comment. #1856 found the live
    consequence: a guided-process session got created for the dark
    onboarding process and asked a question no later turn could reach
    (``PortfolioOnboardingHandler.handle_turn`` — unreachable, because
    ``OnboardingProcessAdapter`` is never registered and
    ``IntentService._check_active_onboarding`` has zero production callers).

    THE CENSUS PREDICATE (mechanical, the denominator this test states in
    its own failure message — m-44): every regex below is a call SITE for a
    known session-starting operation (a leading ``.`` or an explicit
    ``await self.``/``await intent_service.`` — never the method's OWN
    ``def``/``async def`` line, filtered by stripped-line prefix), scanned
    over every ``*.py`` under ``services/`` and ``web/`` excluding
    ``tests/``. Each match maps DETERMINISTICALLY to the ``ProcessType`` the
    call starts a session for:

    - ``onboarding_manager.create_session(`` / ``self.manager.create_session(``
      (inside the onboarding package) / ``.offer_onboarding(`` /
      ``.start_onboarding(`` → ONBOARDING
    - ``_start_standup_conversation(`` (call form only) → STANDUP
    - ``slot_filling_adapter.manager.start_filling(`` → SLOT_FILLING

    KNOWN_SITES below is the full MEASURED set (2026-09-24) — every one of
    these file:line pairs the predicate finds today. The test asserts the
    scan reproduces this exact set (so a NEW site — one the table doesn't
    already know about — fails loud by being FOUND, not by someone
    remembering to add a row) AND that every site whose process is DARK
    fails with the #1856 explanation.

    ✅ RESOLVED 2026-10-07 (#1886, Arch's 2026-10-06 ruling, binding): all
    four onboarding-naming sites #1867 found are gone. ``_handle_add_project``
    now arms a durable per-turn carrier (the #846/#1190 pending-offer idiom,
    ``services/intent_service/add_project_clarify.py``) instead of creating
    an onboarding session inline — Arch's option (b), not the re-registered-
    adapter option (c). The dead ``_check_portfolio_onboarding`` /
    ``offer_onboarding`` / ``start_onboarding`` chain (findings 2-4) was
    Rule-0 deleted outright (zero production callers; grep evidence in the
    #1886 session log). ``KNOWN_SITES`` below is the re-measured set — four
    STANDUP/SLOT_FILLING sites, all LIVE, zero DARK — and
    ``test_every_known_site_names_a_live_process`` XPASSes without the
    strict-xfail marker.

    PRESENT-NOT-ENFORCED BOUNDARY (m-44): this predicate is a fixed regex
    set over known call shapes, not a general call-graph analysis or a
    reachability prover — it finds sites 2-4 above even though 2-4 are
    unreachable or dead, because the predicate deliberately does not try to
    prove reachability (a cheap, sound "is this call expression present"
    check beats an expensive, unsound "is this call ever actually made"
    one). It cannot see a NEW way of starting a guided-process session (a
    different variable name, a dynamically-dispatched call, a fresh manager
    class) — that surface's compliance is Present, not Enforced, until a row
    is added here.
    """

    _SCAN_ROOTS = ("services", "web")

    # (compiled call-site regex, ProcessType) — see predicate above.
    _SITE_PATTERNS: tuple = (
        (re.compile(r"\bonboarding_manager\.create_session\("), ProcessType.ONBOARDING),
        (re.compile(r"\bself\.manager\.create_session\("), ProcessType.ONBOARDING),
        (re.compile(r"\.offer_onboarding\("), ProcessType.ONBOARDING),
        (re.compile(r"\.start_onboarding\("), ProcessType.ONBOARDING),
        (re.compile(r"\bslot_filling_adapter\.manager\.start_filling\("), ProcessType.SLOT_FILLING),
        (re.compile(r"_start_standup_conversation\("), ProcessType.STANDUP),
    )

    # THE CENSUS — MEASURED 2026-09-24, (file, line_no, process_type.value).
    # A call site's own ``def``/``async def`` line is never a member (the
    # scan filters those out; only call SITES count). SHRINK/GROW only by
    # re-running the scan and updating this table in the same commit as the
    # code change that added/removed a site.
    #
    # Re-measured 2026-10-07 (#1886): the four onboarding-naming sites are
    # GONE — _handle_add_project no longer creates a session at all (its
    # no-name ask now arms the add-project name-clarify carrier instead,
    # services/intent_service/add_project_clarify.py), and the dead
    # _check_portfolio_onboarding / offer_onboarding / start_onboarding
    # chain was Rule-0 deleted outright. The scan now finds exactly the
    # four STANDUP/SLOT_FILLING sites below, all LIVE, zero DARK.
    # Keyed (file, enclosing function, process) — see _scan_sites for why not
    # line numbers. Several call sites inside ONE function collapse to one key
    # (intent_service._handle_standup_query has three); the census question is
    # "which process is started from where", and a function is the "where".
    KNOWN_SITES = frozenset(
        {
            (
                "services/intent_service/workflow_entries.py",
                "start_meeting_workflow",
                "slot_filling",
            ),
            (
                "services/intent_service/workflow_entries.py",
                "run_standup_interview_workflow",
                "standup",
            ),
            ("services/intent/intent_service.py", "_process_intent_internal", "standup"),
            ("services/intent/intent_service.py", "_handle_standup_query", "standup"),
        }
    )

    # #1886: the dark subset is now EMPTY — all four onboarding-naming sites
    # named in the (now-historical) docstring findings above are gone.
    # Kept as an explicit empty frozenset, not deleted, so
    # test_known_dark_sites_are_exactly_the_dark_subset keeps proving the
    # negative (no site in KNOWN_SITES is dark) rather than that check
    # vanishing along with the table.
    KNOWN_DARK_SITES = frozenset()

    def _scan_sites(self) -> set:
        repo_root = Path(__file__).resolve().parents[1]
        found = set()
        for root_name in self._SCAN_ROOTS:
            for path in (repo_root / root_name).rglob("*.py"):
                if "tests" in path.parts or "__pycache__" in path.parts:
                    continue
                rel = path.relative_to(repo_root).as_posix()
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
                # Sites are keyed by (file, ENCLOSING FUNCTION, process) — never by
                # line number. Line numbers shift on every unrelated edit above a
                # site (the #1565 lane had to re-measure this table twice in one
                # session, once after ruff), which turns a census into churn; the
                # enclosing def is stable across edits and still unique per site.
                enclosing = "<module>"
                for line in lines:
                    stripped = line.strip()
                    m = re.match(r"(?:async\s+)?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", stripped)
                    if m:
                        enclosing = m.group(1)
                        continue
                    for pattern, process_type in self._SITE_PATTERNS:
                        if pattern.search(line):
                            found.add((rel, enclosing, process_type.value))
        return found

    def test_census_matches_measured_sites(self):
        """The scan must find EXACTLY KNOWN_SITES — no more, no less. A new
        match is a NEW session-start site (must be triaged: registered
        process, or a new dark-starter finding); a disappeared match means
        KNOWN_SITES is stale and must be edited down in the same commit as
        whatever removed the site."""
        found = self._scan_sites()
        new = sorted(found - self.KNOWN_SITES)
        gone = sorted(self.KNOWN_SITES - found)
        assert not new, (
            f"NEW guided-process session-start site(s) found, not in KNOWN_SITES: "
            f"{new}. Triage each: does it name a LIVE process (add it to "
            "KNOWN_SITES) or a DARK one (this is a #1856-class defect — file it, "
            "add to both KNOWN_SITES and KNOWN_DARK_SITES if not a one-line fix, "
            "or fix it directly if it is)."
        )
        assert not gone, (
            f"KNOWN_SITES entries no longer found by the scan: {gone}. Update "
            "KNOWN_SITES (and KNOWN_DARK_SITES if applicable) to match — a site "
            "that moved or was deleted must not linger in the census."
        )

    def test_every_known_site_names_a_live_process(self):
        """Every KNOWN_SITES entry must name a LIVE process — full stop, NO
        exclusion for KNOWN_DARK_SITES. #1867's instruction was explicit:
        "if the census finds a real dark starter today, the test must be
        RED for it — do not allowlist it." This test was strict-xfail on
        #1886 from 2026-09-24 to 2026-10-07: all four onboarding-naming
        findings are now resolved (see the class docstring), KNOWN_SITES
        holds only the four LIVE STANDUP/SLOT_FILLING sites, and this test
        XPASSed — removing the marker per its own stated instruction
        ("the moment the last dark starter is fixed this XPASSes and FAILS
        the build — remove the marker then, never allowlist a site")."""
        from services.process.guided_process_registry import (
            GUIDED_PROCESSES,
            GuidedProcessStatus,
        )

        status_by_value = {info.process_type.value: info.status for info in GUIDED_PROCESSES}

        bad = sorted(
            site
            for site in self.KNOWN_SITES
            if status_by_value.get(site[2]) != GuidedProcessStatus.LIVE
        )
        assert not bad, (
            f"{len(bad)} of {len(self.KNOWN_SITES)} known guided-process "
            f"session-start sites name a process that is NOT registered LIVE: "
            f"{bad}. See this class's docstring for the numbered explanation of "
            "each (the #1867 census findings) — these are expected failures "
            "carried in KNOWN_DARK_SITES, not new regressions, UNLESS this list "
            "is longer than KNOWN_DARK_SITES (run "
            "test_known_dark_sites_are_exactly_the_dark_subset to check)."
        )

    def test_known_dark_sites_are_exactly_the_dark_subset(self):
        """Tightness check, independent of whether the sites above are
        fixed: KNOWN_DARK_SITES must equal the actual dark subset of
        KNOWN_SITES — no more (a site wrongly marked dark that is actually
        live would hide a real registration gap), no less (a dark site
        missing from KNOWN_DARK_SITES means it's invisible here). Post-#1886
        this is the "denominator" for ``test_every_known_site_names_a_live_
        process``'s GREEN result: it proves the dark subset is exactly
        EMPTY, not drifting silently in either direction."""
        from services.process.guided_process_registry import (
            GUIDED_PROCESSES,
            GuidedProcessStatus,
        )

        status_by_value = {info.process_type.value: info.status for info in GUIDED_PROCESSES}
        actual_dark = {
            site
            for site in self.KNOWN_SITES
            if status_by_value.get(site[2]) != GuidedProcessStatus.LIVE
        }
        extra = sorted(self.KNOWN_DARK_SITES - actual_dark)
        missing = sorted(actual_dark - self.KNOWN_DARK_SITES)
        assert not extra, (
            f"KNOWN_DARK_SITES lists site(s) that are actually LIVE now: {extra}. "
            "The upstream process was registered — remove these rows (and their "
            "docstring findings) as RESOLVED."
        )
        assert not missing, (
            f"KNOWN_DARK_SITES is missing dark site(s) the scan finds: {missing}. "
            "Add them to KNOWN_DARK_SITES with a docstring finding — a dark "
            "starter must never be invisible to this table."
        )

    def test_guided_process_census_covers_every_process_type(self):
        """`GUIDED_PROCESSES` must have exactly one row per `ProcessType`
        member — an enum member with no census row is invisible to every
        other check in this class."""
        from services.process.guided_process_registry import GUIDED_PROCESSES
        from services.process.registry import ProcessType

        census_types = {info.process_type for info in GUIDED_PROCESSES}
        all_types = set(ProcessType)
        assert census_types == all_types, (
            f"GUIDED_PROCESSES is missing or has extra ProcessType rows. "
            f"Missing: {sorted(t.value for t in all_types - census_types)}; "
            f"extra: {sorted(t.value for t in census_types - all_types)}."
        )

    def test_declared_live_set_matches_live_registration(self):
        """The declared LIVE set in GUIDED_PROCESSES must equal what actually
        gets registered when the real registration entry points run — this
        is what keeps the table from drifting out from under the code (#1867
        requirement: "derived from the real registry where possible... a
        mismatch fails loud")."""
        from services.process.guided_process_registry import (
            compute_live_registered_types,
            live_process_types,
        )

        declared = live_process_types()
        actual = compute_live_registered_types()
        assert declared == actual, (
            f"GUIDED_PROCESSES declares LIVE={sorted(t.value for t in declared)} "
            f"but calling the real registration entry points actually registers "
            f"{sorted(t.value for t in actual)}. Update the GUIDED_PROCESSES "
            "status rows in services/process/guided_process_registry.py to match "
            "reality — this table must never assert a status the code disagrees "
            "with."
        )


class TestNoLocalEscapeHelpers1582:
    """#1582 — escapeHtml/escapeAttr have exactly ONE definition site in the
    whole tree: web/static/js/escape.js. Every template that needs them loads
    that shared asset (layouts/app_shell.html includes it shell-wide); no
    template or other static JS file may define its own copy.

    Before this consolidation, `function escapeHtml`/`function escapeAttr`
    was duplicated inline across 11 templates. Two (todos.html/#1578,
    files.html/#1581) had the safe, quote-complete string-based copy. EIGHT
    others (greeting_context.html, project_config_panel.html, lists.html,
    project_detail.html, settings_calendar.html, settings_github.html,
    settings_notion.html, settings_projects.html) carried a DOM-based copy
    (`div.textContent -> div.innerHTML`) that does NOT escape quotes — the
    exact attribute-injection hole #1581 found and fixed in files.html,
    left live in eight other templates. One (transparency.html) had its own
    quote-complete regex-based copy. This ratchet keeps a NEW local copy —
    of either shape — from ever being (re)introduced.

    PATTERN (deliberately narrow, m-44 denominator stated): a `function
    escapeHtml`/`function escapeAttr` declaration, or a `const escapeHtml =`/
    `const escapeAttr =` assignment. This does NOT match (by construction,
    not by exclusion list) the unrelated underscore-prefixed
    `_escapeHtml`/`_escapeAttr` helpers (web/static/js/loading.js's class
    method; the chat suggestion-card renderer pinned by
    tests/unit/templates/test_suggestions_xss_escaping_1741.py) — those are a
    different identifier, not a copy of this pair, and out of #1582's scope.

    LAYER (m-43): static source-text scan over templates/**/*.html and
    web/static/js/*.js. Proves no NEW definition site exists in source; does
    not re-prove escape.js's own escaping correctness (that's
    tests/frontend/unit/escape.test.js) or that a given template actually
    loads escape.js before calling it (that's the render-time template
    tests in tests/unit/templates/).
    """

    _DEFINITION_RE = re.compile(
        r"\b(?:function\s+(escapeHtml|escapeAttr)\s*\(|const\s+(escapeHtml|escapeAttr)\s*=)"
    )

    _ALLOWED = {"web/static/js/escape.js"}

    def _scan(self):
        repo_root = Path(__file__).resolve().parents[1]
        hits = []
        candidates = list((repo_root / "templates").rglob("*.html")) + list(
            (repo_root / "web" / "static" / "js").glob("*.js")
        )
        for path in candidates:
            rel = path.relative_to(repo_root).as_posix()
            if rel in self._ALLOWED:
                continue
            text = path.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), start=1):
                m = self._DEFINITION_RE.search(line)
                if m:
                    name = m.group(1) or m.group(2)
                    hits.append(f"{rel}:{lineno}: local `{name}` definition — {line.strip()!r}")
        return hits

    def test_no_local_escape_helper_definitions_outside_shared_asset(self):
        hits = self._scan()
        assert not hits, (
            "Local escapeHtml/escapeAttr definition(s) found outside "
            "web/static/js/escape.js (#1582 — the single shared source of "
            "truth). A template needing these helpers should load "
            "/static/js/escape.js (layouts/app_shell.html already does this "
            "shell-wide for every extending page) and call the resulting "
            "global escapeHtml/escapeAttr, not redefine them locally — a "
            "fresh local copy risks reintroducing the quote-incomplete "
            "DOM-based variant (`div.textContent -> innerHTML`) #1581 found "
            "to be attribute-injection-breakable:\n  " + "\n  ".join(hits)
        )

    def test_shared_asset_still_defines_both_helpers(self):
        """Guard the other direction: escape.js itself must still define
        both names (protects against a future refactor accidentally renaming
        or removing one while this ratchet's allowlist keeps the file
        exempt)."""
        repo_root = Path(__file__).resolve().parents[1]
        src = (repo_root / "web" / "static" / "js" / "escape.js").read_text(encoding="utf-8")
        assert re.search(r"\bfunction\s+escapeHtml\s*\(", src), (
            "web/static/js/escape.js no longer defines escapeHtml() — the "
            "shared source of truth this ratchet allowlists would be empty."
        )
        assert re.search(r"\bfunction\s+escapeAttr\s*\(", src), (
            "web/static/js/escape.js no longer defines escapeAttr() — the "
            "shared source of truth this ratchet allowlists would be empty."
        )


class TestOriginalMessageWriteRatchet1459:
    """#1459 — the user's message has ONE writer: ``Intent.bind_original_message``.

    The message lives on two surfaces (``Intent.original_message`` and
    ``context["original_message"]``, Issue #744). #1942 made every constructor
    mirror them; #1459 (Arch's ruling, 2026-10-12) makes divergence AFTER
    construction impossible by counting every write shape that could defeat the
    mirror and holding the count at ZERO outside ``services/domain/models.py``:

    (a) a single-surface assignment — ``x.original_message = …`` or
        ``x.context["original_message"] = …``;
    (b) replacing the whole context dict (``x.context = …``) with anything other
        than the two exempt idioms: a bare ``{}`` directly under that receiver's
        own ``if x.context is None:`` guard, and the copy ``dict(x.context or {})``;
    (c) ``x.context.update(…)`` / ``setdefault`` carrying the key, or
        ``setattr(x, "original_message", …)``;
    (d) ``x.context.pop("original_message")`` / ``del x.context["original_message"]``.

    Receivers are identified by name: any name or attribute chain whose last
    name contains ``intent`` (``intent``, ``pre_intent``, ``sibling_intent``,
    ``self.intent``). A SQLAlchemy row's ``.context`` or a local ``context =
    dict(intent.context)`` copy is outside the scan on purpose. This is the
    scanner's stated limit; widen it here, never narrow it quietly.

    Denominator: a shrink-lock at zero passes just as happily when the scanner is
    broken, so the scan must still SEE the construction sites that set the
    message (kwarg or dict-literal key) and the scanner must flag each of the four
    shapes on a synthetic module. Both are asserted before the bound.
    """

    MAX_SINGLE_SURFACE_WRITES = 0
    EXEMPT = {"services/domain/models.py"}
    KEY = "original_message"

    # ---- scanner -------------------------------------------------------------

    @staticmethod
    def _receiver_is_intent(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return "intent" in node.id.lower()
        if isinstance(node, ast.Attribute):
            return "intent" in node.attr.lower()
        return False

    @classmethod
    def _is_intent_context(cls, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Attribute)
            and node.attr == "context"
            and cls._receiver_is_intent(node.value)
        )

    @classmethod
    def _is_key(cls, node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and node.value == cls.KEY

    @classmethod
    def _dict_carries_key(cls, node: ast.AST) -> bool:
        return isinstance(node, ast.Dict) and any(cls._is_key(k) for k in node.keys if k)

    @classmethod
    def _guarded_assignments(cls, tree: ast.AST) -> set[int]:
        """ids of the Assign nodes that sit directly in the body of
        ``if <intent>.context is None:`` — the only place a bare ``{}`` is a
        no-op rather than a wipe (Arch's addendum, 2026-10-12)."""
        guarded: set[int] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Is)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value is None
                and cls._is_intent_context(test.left)
            ):
                # Compare the receiver beneath ``.context``: a Store target and a
                # Load test differ in ``ctx``, so a whole-node dump never matches.
                receiver = ast.dump(test.left.value)
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign) and any(
                        isinstance(t, ast.Attribute)
                        and t.attr == "context"
                        and ast.dump(t.value) == receiver
                        for t in stmt.targets
                    ):
                        guarded.add(id(stmt))
        return guarded

    @classmethod
    def _exempt_context_replacement(
        cls, target: ast.Attribute, value: ast.AST, *, guarded: bool
    ) -> bool:
        # ``x.context = {}`` ONLY under its own ``if x.context is None`` guard; an
        # unguarded bare ``{}`` wipes the key and leaves the field set — the
        # divergence shape (b) exists to catch …
        if isinstance(value, ast.Dict) and not value.keys:
            return guarded
        # … and ``x.context = dict(x.context or {})`` (the copy-before-mutate idiom).
        if (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "dict"
            and len(value.args) == 1
            and not value.keywords
        ):
            arg = value.args[0]
            if (
                isinstance(arg, ast.BoolOp)
                and isinstance(arg.op, ast.Or)
                and len(arg.values) == 2
                and cls._is_intent_context(arg.values[0])
                and isinstance(arg.values[1], ast.Dict)
                and not arg.values[1].keys
            ):
                return True
        return False

    @classmethod
    def _scan_tree(cls, tree: ast.AST, path: str) -> tuple[list[str], int]:
        """Return (violations, construction_sites) for one module."""
        violations: list[str] = []
        constructions = 0
        guarded = cls._guarded_assignments(tree)
        for node in ast.walk(tree):
            # denominator: Intent(...) with the message set either way
            if isinstance(node, ast.Call):
                fn = node.func
                fname = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", "")
                if fname == "Intent":
                    kws = {k.arg: k.value for k in node.keywords if k.arg}
                    if cls.KEY in kws or cls._dict_carries_key(
                        kws.get("context", ast.Dict([], []))
                    ):
                        constructions += 1
            # (a) single-surface assignment (plain, augmented or annotated)
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for t in targets:
                    if (
                        isinstance(t, ast.Attribute)
                        and t.attr == cls.KEY
                        and cls._receiver_is_intent(t.value)
                    ):
                        violations.append(f"{path}:{node.lineno} (a) attribute-only write")
                    elif (
                        isinstance(t, ast.Subscript)
                        and cls._is_intent_context(t.value)
                        and cls._is_key(t.slice)
                    ):
                        violations.append(f"{path}:{node.lineno} (a) dict-only write")
                    # (b) whole-context replacement outside the two exempt idioms
                    elif (
                        isinstance(node, ast.Assign)
                        and cls._is_intent_context(t)
                        and not cls._exempt_context_replacement(
                            t, node.value, guarded=id(node) in guarded
                        )
                    ):
                        violations.append(f"{path}:{node.lineno} (b) context replaced")
            # (c) update/setdefault on the key; setattr on the field; (d) pop
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Attribute) and cls._is_intent_context(fn.value):
                    if fn.attr in ("update", "setdefault", "pop"):
                        carries = any(cls._is_key(a) or cls._dict_carries_key(a) for a in node.args)
                        carries = carries or any(k.arg == cls.KEY for k in node.keywords)
                        if carries:
                            shape = "(d) pop" if fn.attr == "pop" else f"(c) {fn.attr}"
                            violations.append(f"{path}:{node.lineno} {shape} on the key")
                if (
                    isinstance(fn, ast.Name)
                    and fn.id == "setattr"
                    and len(node.args) >= 2
                    and cls._receiver_is_intent(node.args[0])
                    and cls._is_key(node.args[1])
                ):
                    violations.append(f"{path}:{node.lineno} (c) setattr on the field")
            # (d) del x.context["original_message"]
            if isinstance(node, ast.Delete):
                for t in node.targets:
                    if (
                        isinstance(t, ast.Subscript)
                        and cls._is_intent_context(t.value)
                        and cls._is_key(t.slice)
                    ):
                        violations.append(f"{path}:{node.lineno} (d) del on the key")
        return violations, constructions

    @classmethod
    def _scan_repo(cls) -> tuple[list[str], int, int]:
        violations: list[str] = []
        constructions = 0
        files = 0
        for pattern in ("services/**/*.py", "web/**/*.py"):
            for path in sorted(glob.glob(pattern, recursive=True)):
                norm = path.replace(os.sep, "/")
                if norm in cls.EXEMPT or "/tests/" in norm or "/test_" in norm:
                    continue
                with open(path, encoding="utf-8") as fh:
                    source = fh.read()
                if cls.KEY not in source and ".context" not in source:
                    continue
                files += 1
                v, c = cls._scan_tree(ast.parse(source, filename=path), norm)
                violations.extend(v)
                constructions += c
        return violations, constructions, files

    # ---- the scanner's own denominator ----------------------------------------

    SYNTHETIC = """
def f(intent, pre_intent, other):
    intent.original_message = "a"                      # (a)
    intent.context["original_message"] = "a"           # (a)
    pre_intent.context = {"original_message": "a"}     # (b)
    intent.context = dict(other.context or {})         # (b) — not the exempt copy of ITS OWN context
    intent.context.update({"original_message": "a"})   # (c)
    intent.context.setdefault("original_message", "a") # (c)
    setattr(intent, "original_message", "a")           # (c)
    intent.context.pop("original_message", None)       # (d)
    del intent.context["original_message"]             # (d)
    intent.context = {}                                # (b) — bare {} with NO is-None guard wipes the key
    if other.context is None:
        intent.context = {}                            # (b) — guarded, but by ANOTHER receiver's test
    # exempt / out of scope:
    if intent.context is None:
        intent.context = {}
    intent.context = dict(intent.context or {})
    intent.context["user_id"] = "u"
    row.context = {"original_message": "a"}
    ctx = dict(intent.context or {})
    ctx.setdefault("original_message", "")
    made = Intent(category=c, action="x", original_message="m")
    made2 = Intent(category=c, action="x", context={"original_message": "m"})
"""

    def test_scanner_flags_every_write_shape(self):
        """A shrink-lock that cannot see the shapes it locks is not a lock."""
        violations, constructions = self._scan_tree(ast.parse(self.SYNTHETIC), "synthetic")
        shapes = sorted(v.split(" ", 1)[1] for v in violations)
        assert shapes == sorted(
            [
                "(a) attribute-only write",
                "(a) dict-only write",
                "(b) context replaced",
                "(b) context replaced",
                "(b) context replaced",
                "(b) context replaced",
                "(c) update on the key",
                "(c) setdefault on the key",
                "(c) setattr on the field",
                "(d) pop on the key",
                "(d) del on the key",
            ]
        ), violations
        assert constructions == 2

    def test_scan_sees_the_construction_sites(self):
        """The denominator: the repo scan must find the sites that SET the message
        at construction (dozens on main), or the scanner is broken and a zero
        below means nothing."""
        _, constructions, files = self._scan_repo()
        assert files >= 10, f"scanned only {files} files — glob or filter broke"
        assert constructions >= 20, (
            f"found only {constructions} Intent(...) construction sites that set "
            f"original_message — the scanner is broken, not the code clean"
        )

    def test_no_single_surface_writes_outside_the_model(self):
        """The ratchet. Every fill of the user's message after construction goes
        through ``Intent.bind_original_message``; nothing outside models.py writes
        either surface alone, replaces the context without carrying it forward,
        or edits the key through update/setdefault/pop/del/setattr."""
        violations, constructions, _ = self._scan_repo()
        assert constructions >= 20  # never trust the zero without the denominator
        assert len(violations) <= self.MAX_SINGLE_SURFACE_WRITES, (
            f"{len(violations)} single-surface original_message write(s) outside "
            f"services/domain/models.py (ratchet target {self.MAX_SINGLE_SURFACE_WRITES}). "
            f"Use intent.bind_original_message(msg) instead:\n  " + "\n  ".join(violations)
        )

    def test_ratchet_target_stays_tight(self):
        violations, _, _ = self._scan_repo()
        assert len(violations) == self.MAX_SINGLE_SURFACE_WRITES, (
            f"Ratchet drift: actual count {len(violations)}, target "
            f"{self.MAX_SINGLE_SURFACE_WRITES}; the direction is DOWN only."
        )


class TestOwnerIdNullabilityPin2009:
    """2009 (Arch step 3): every ``owner_id`` column is NOT NULL unless its table is
    listed here with a reason.

    A nullable ``owner_id`` on a table that has no other owner column is a second,
    optional copy of who owns the row, and production showed what that costs:
    ``project_integrations`` read 3 of 3 rows NULL because no writer ever set it.
    The pin is on ``Base.metadata`` (the model), so a new user-data table cannot
    ship a nullable owner without being named here. The allowlist only shrinks:
    when a table's owner goes NOT NULL, remove its row (the second test fails
    until you do).
    """

    NULLABLE_OWNER_ALLOWED = {
        # ADR-071 D2 mid-transition tables: user_id (NOT NULL) scopes them.
        "conversations": "ADR-071 D2 mid-transition; scoped by user_id (NOT NULL)",
        "conversational_memory_entries": "ADR-071 D2 mid-transition; scoped by user_id",
        "insights": "ADR-071 D2 mid-transition; scoped by user_id (NOT NULL)",
        "personality_profiles": "ADR-071 D2 mid-transition; scoped by user_id (NOT NULL)",
        "standup_conversations": "ADR-071 D2 mid-transition; scoped by user_id (NOT NULL)",
        # 2009 tier C: user_id is the scoping column and went NOT NULL instead.
        "feedback": "2009 tier C; scoped by user_id (NOT NULL); owner_id follows ADR-071 D2",
    }

    @staticmethod
    def _nullable_owner_tables() -> set:
        import services.database.models  # noqa: F401  (registers every model table)
        from services.database.models import Base

        tables = set()
        for table in Base.metadata.tables.values():
            col = table.columns.get("owner_id")
            if col is not None and col.nullable:
                tables.add(table.name)
        return tables

    def test_denominator_metadata_has_owner_columns(self):
        """m-44: the scan must see the owner-bearing tables, or a pass means nothing."""
        import services.database.models  # noqa: F401
        from services.database.models import Base

        with_owner = [t for t in Base.metadata.tables.values() if "owner_id" in t.columns]
        assert len(with_owner) >= 20, (
            f"only {len(with_owner)} tables with owner_id in Base.metadata; "
            "the model import broke, not the schema got clean"
        )

    def test_no_nullable_owner_id_outside_the_allowlist(self):
        unexpected = self._nullable_owner_tables() - set(self.NULLABLE_OWNER_ALLOWED)
        assert not unexpected, (
            f"owner_id is nullable on {sorted(unexpected)}. A user-data table's owner is "
            "NOT NULL (2009): set nullable=False and ship the backfill + NOT NULL "
            "migration with the writer fix, or, if it is a genuine transition case, add "
            "it to NULLABLE_OWNER_ALLOWED with a one-line reason in review."
        )

    def test_allowlist_stays_tight(self):
        stale = set(self.NULLABLE_OWNER_ALLOWED) - self._nullable_owner_tables()
        assert not stale, (
            f"NULLABLE_OWNER_ALLOWED lists tables whose owner_id is no longer nullable "
            f"(or that no longer exist): {sorted(stale)}. Remove them; the list only shrinks."
        )


class TestItemServiceNotReachableFromWeb2014:
    """2014: ``ItemService.get_item`` / ``update_item_text`` / ``delete_item`` select by id
    alone, with no list-ownership check (the four list-item routes scope through
    ``get_list_by_id(list_id, owner_id=...)`` instead). No route calls them today, so the
    exposure is zero. This pin keeps it that way: a route that wants one of these must give
    it an ownership check first, then be named here with a reason.
    """

    METHODS = ("get_item", "update_item_text", "delete_item")
    # Route-handler functions that merely share a method's name (they do not call the service).
    ALLOWED_DEFS = {"web/api/routes/lists.py": {"delete_item"}}

    @staticmethod
    def _web_files():
        return sorted(Path("web").rglob("*.py"))

    def test_denominator_web_files_scanned(self):
        assert len(self._web_files()) >= 20, "web/ scan found too few files to mean anything"

    def test_no_web_module_calls_unscoped_item_service_methods(self):
        violations = []
        for path in self._web_files():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr in self.METHODS:
                        violations.append(f"{path}:{node.lineno} calls .{node.func.attr}()")
                elif isinstance(node, ast.ImportFrom) and node.module == "services.item_service":
                    violations.append(f"{path}:{node.lineno} imports services.item_service")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "services.item_service":
                            violations.append(f"{path}:{node.lineno} imports services.item_service")
        assert not violations, (
            "2014: web/ must not call ItemService.get_item/update_item_text/delete_item "
            "(they select by id alone, no list-ownership check). Add the "
            "get_list_by_id(list_id, owner_id=...) check first. " + "; ".join(violations)
        )


class TestLogNeverSlicesUserText2059:
    """#2059 — the privacy page says server logs keep at most a fingerprint of
    user text. Arch's ruling (2026-10-16, issue comment 6223725838, ADR-080 D3:
    code holds the guarantee, the log LEVEL does not): every site that logs user
    text, or text derived from it, goes through ``utterance_fields`` /
    ``utterance_preview`` (``services/utils/utterance_log.py``) at EVERY level.

    THE CENSUS PREDICATE (mechanical, over ``services/`` and ``web/`` ``*.py``):
    a LOG CALL is ``<recv>.<level>(...)`` with level in debug/info/warning/warn/
    error/exception/critical and a receiver whose terminal name contains "log"
    (``logger``, ``self.logger``, ``logging``, ``log``) or is
    ``structlog.get_logger()``. A log call is an OFFENDER when, outside any
    ``utterance_preview(...)``/``utterance_fields(...)`` call, it contains

    - a SLICE of a user-text name (terminal identifier ``message``,
      ``original_message``, ``user_message``, ``text``, ``utterance``,
      ``ctx_str``, ``raw``, ``response_message``, ``markdown_text``, e.g.
      ``message[:50]``, ``self.original_message[:80]``), or
    - a bare name that the SAME function assigned from such a slice
      (``preview = text[:120]`` then ``logger.warning(..., preview)``).

    - (Arch's third ruling, issue comment 6225894664) a user-text name passed
      WHOLE, UNSLICED: a bare/attribute name in ``UNSLICED_NAMES`` (the
      ``USER_NAMES`` plus ``query`` and ``resolved_message``) as a logger kwarg
      value, a positional argument or an f-string interpolation, at any level,
      outside ``utterance_preview``/``utterance_fields`` and outside
      length-style wrappers (``len`` ...). EXEMPT: a log call inside an
      ``if log_full_utterance():`` body, CIO's deliberate opt-in.

    CEILING 0, never raised. Not offenders by construction: slices that are
    not inside a log call (stored context, display titles).

    ALLOW-LIST (each entry needs a reason; empty of sites, the helper module
    is the only exempt FILE because it implements the slice for the knob).
    """

    LEVELS = {"debug", "info", "warning", "warn", "error", "exception", "critical"}
    USER_NAMES = {
        "message",
        "original_message",
        "user_message",
        "text",
        "utterance",
        "ctx_str",
        "raw",
        "response_message",
        "markdown_text",
    }
    UNSLICED_NAMES = USER_NAMES | {"query", "resolved_message"}
    # Attribute reads (``x.name``) count only for these: ``e.message``,
    # ``resp.error.message``, ``exc.user_message`` are exception/response text,
    # while ``intent.original_message`` is the user's words. A BARE name counts
    # for every UNSLICED_NAMES entry.
    UNSLICED_ATTRS = {
        "original_message",
        "resolved_message",
        "utterance",
        "ctx_str",
        "markdown_text",
    }
    SAFE_CALLS = {
        "utterance_preview",
        "utterance_fields",
        # import aliases / the cache's stdlib-logger twin of utterance_preview
        "_utterance_preview",
        "_utterance_fields",
        "_text_ref",
    }
    # Wrappers whose result carries no user text (a count, a flag, a type name).
    NON_TEXT_CALLS = {"len", "bool", "type", "id", "hash", "isinstance"}
    ALLOW_FILES = {
        "services/utils/utterance_log.py": "the helper: implements the knob-gated slice itself",
    }
    # "path:line" -> reason. Every entry is a name that LOOKS like user text but is
    # system text (verified by reading the call and its callers, 2026-10-16).
    ALLOW_SITES: dict = {
        "services/infrastructure/keychain_service.py:128": "`raw` is an environment-variable value (the keychain timeout), not user text",
        "web/startup.py:114": "`message` is the upload-dir probe's own status string",
        "web/startup.py:117": "`message` is the upload-dir probe's own status string",
        "web/utils/error_responses.py:124": "`message` is the server's HTTP error summary (system copy)",
        "web/utils/error_responses.py:156": "`message` is the server's HTTP error summary (system copy)",
        "web/utils/error_responses.py:188": "`message` is the server's HTTP error summary (system copy)",
        "web/utils/error_responses.py:227": "`message` is the server's HTTP error summary (system copy)",
        "web/api/routes/intent.py:503": "#1332 blank-payload diagnostic: only reached when `not message or not message.strip()`, so repr() is '', None or whitespace, never content",
        "services/process/registry.py:827": "`_escape_word(message)` is only reached after `_is_escape_command(message)`, a closed vocabulary of escape words",
    }

    @staticmethod
    def _term(node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return None

    @classmethod
    def _is_log_call(cls, node) -> bool:
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            return False
        if node.func.attr not in cls.LEVELS:
            return False
        recv = node.func.value
        if isinstance(recv, ast.Call):  # structlog.get_logger().info(...)
            return cls._term(recv.func) == "get_logger"
        return "log" in (cls._term(recv) or "").lower()

    @classmethod
    def _unsafe_walk(cls, node):
        """Yield nodes under ``node``, not descending into the safe helpers."""
        stack = [node]
        while stack:
            cur = stack.pop()
            yield cur
            if isinstance(cur, ast.Call) and cls._term(cur.func) in cls.SAFE_CALLS:
                continue
            stack.extend(ast.iter_child_nodes(cur))

    @classmethod
    def _gated_ranges(cls, tree):
        """Line spans of ``if log_full_utterance():`` bodies (the knob opt-in)."""
        spans = []
        for n in ast.walk(tree):
            if (
                isinstance(n, ast.If)
                and isinstance(n.test, ast.Call)
                and cls._term(n.test.func) == "log_full_utterance"
            ):
                spans.append((n.body[0].lineno, max(b.end_lineno for b in n.body)))
        return spans

    @classmethod
    def _unsliced_name(cls, call):
        """The first whole user-text name under a log call, else None."""
        stack = [call]
        while stack:
            cur = stack.pop()
            if isinstance(cur, ast.Call) and cur is not call:
                name = cls._term(cur.func)
                if name in cls.SAFE_CALLS or name in cls.NON_TEXT_CALLS:
                    continue
            if isinstance(cur, ast.IfExp):  # `x if x else None`: the test is not logged
                stack.extend([cur.body, cur.orelse])
                continue
            if isinstance(cur, ast.Subscript):  # slices are the other predicate
                stack.append(cur.slice)
                if not isinstance(cur.slice, ast.Slice):
                    stack.append(cur.value)
                continue
            if isinstance(cur, (ast.Name, ast.Attribute)) and isinstance(
                getattr(cur, "ctx", None), ast.Load
            ):
                if isinstance(cur, ast.Name) and cur.id in cls.UNSLICED_NAMES:
                    return cur.id
                if isinstance(cur, ast.Attribute) and cur.attr in cls.UNSLICED_ATTRS:
                    return cur.attr
                if isinstance(cur, ast.Attribute):
                    stack.append(cur.value)
                continue
            stack.extend(ast.iter_child_nodes(cur))
        return None

    # Calls that pass a string through (the result is still the user's text).
    PASS_THROUGH = {"str", "repr", "strip", "lstrip", "rstrip", "lower", "upper", "join"}

    @classmethod
    def _has_user_slice(cls, node, direct_only: bool = False) -> bool:
        """True when a user-text slice sits under ``node``. With ``direct_only``
        (assignments) the walk stops at calls other than pass-through string
        calls: ``pattern_id = await handler(context={"m": message[:100]})`` is a
        stored context, not a text-valued variable."""
        stack = [node]
        while stack:
            cur = stack.pop()
            if (
                isinstance(cur, ast.Subscript)
                and isinstance(cur.slice, ast.Slice)
                and cls._term(cur.value) in cls.USER_NAMES
            ):
                return True
            if isinstance(cur, ast.Call):
                name = cls._term(cur.func)
                if name in cls.SAFE_CALLS:
                    continue
                if direct_only and name not in cls.PASS_THROUGH:
                    continue
            stack.extend(ast.iter_child_nodes(cur))
        return False

    @classmethod
    def scan_source(cls, src: str):
        """Return (log_calls_seen, [(lineno, why)]) for one module's source."""
        tree = ast.parse(src)
        scopes = [tree] + [
            n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        seen_calls, hits = set(), {}
        gated = cls._gated_ranges(tree)
        for scope in scopes:
            sliced_vars = set()
            for n in ast.walk(scope):
                targets = []
                if isinstance(n, ast.Assign):
                    targets, value = n.targets, n.value
                elif isinstance(n, ast.AnnAssign) and n.value is not None:
                    targets, value = [n.target], n.value
                else:
                    continue
                if cls._has_user_slice(value, direct_only=True):
                    sliced_vars.update(t.id for t in targets if isinstance(t, ast.Name))
            for n in ast.walk(scope):
                if not cls._is_log_call(n):
                    continue
                seen_calls.add(n.lineno)
                if cls._has_user_slice(n):
                    hits[n.lineno] = "slices user text inside a log call"
                    continue
                for m in cls._unsafe_walk(n):
                    if isinstance(m, ast.Name) and m.id in sliced_vars:
                        hits.setdefault(n.lineno, f"logs {m.id!r}, assigned from a user-text slice")
                if n.lineno in hits or any(a <= n.lineno <= b for a, b in gated):
                    continue
                whole = cls._unsliced_name(n)
                if whole:
                    hits[n.lineno] = f"passes user-text name {whole!r} UNSLICED to a log call"
        return len(seen_calls), sorted(hits.items())

    @staticmethod
    def _files():
        root = Path(__file__).resolve().parents[1]
        return root, sorted(p for base in ("services", "web") for p in (root / base).rglob("*.py"))

    # --- the scanner itself is pinned on synthetic sources (so zero means zero) ---
    @pytest.mark.parametrize(
        "src",
        [
            "logger.info('x', message_preview=message[:50])",
            "self.logger.debug(f'p {message[:50]}')",
            "logger.warning('x', head=self.original_message[:80])",
            "logger.warning('x', extra={'raw_preview': text[:200]})",
            "structlog.get_logger().info('x', p=message[:9])",
            "def f(text):\n    preview = text[:120]\n    logger.warning('x', p=preview)",
            # the 9 unsliced sites of Arch's third ruling, as shapes
            "logger.info('x', original_message=message, resolved_message=resolved_message)",
            "self.logger.info('x', original_message=intent.original_message)",
            "logger.info('x', text=text, priority=p)",
            "logger.info(f'Search found {n} results for query: {query}')",
            "logger.info(f'Searching files, query: {query}')",
            "logger.warning('x %s', message)",
            "if other():\n    logger.info('x', text=text)",
            "if log_full_utterance():\n    pass\nelse:\n    logger.info('x', text=text)",
        ],
    )
    def test_scanner_catches_known_shapes(self, src):
        _, hits = self.scan_source(src)
        assert hits, src

    @pytest.mark.parametrize(
        "src",
        [
            "logger.info('x', message_preview=utterance_preview(message))",
            "logger.info('x', **utterance_fields(message))",
            "logger.info('x', n=len(message))",
            "title = text[:80]\nitems.append(title)",
            "logger.info('x', ids=issues[:3])",
            "logger.info('x', **_utterance_fields(intent.original_message, key='original_message'))",
            "logger.info(f'q: {utterance_preview(query)}')",
            "logger.info('x', n=len(text), m=bool(query))",
            "logger.info('x', p=utterance_preview(m) if m else None)",
            "logger.warning('x', error=response.error.message, e=exc.user_message)",
            "if log_full_utterance():\n    logger.info('x', text=text)",
        ],
    )
    def test_scanner_passes_safe_shapes(self, src):
        _, hits = self.scan_source(src)
        assert not hits, src

    def test_denominator_log_calls_scanned(self):
        root, files = self._files()
        assert len(files) > 500, "services/ + web/ scan found too few files to mean anything"
        total = sum(self.scan_source(p.read_text(encoding="utf-8"))[0] for p in files)
        assert total > 2000, f"only {total} log calls scanned; the log-call predicate has drifted"

    def test_no_log_call_slices_user_text_ceiling_zero(self):
        root, files = self._files()
        offenders = []
        for p in files:
            rel = p.relative_to(root).as_posix()
            if rel in self.ALLOW_FILES:
                continue
            for lineno, why in self.scan_source(p.read_text(encoding="utf-8"))[1]:
                if f"{rel}:{lineno}" not in self.ALLOW_SITES:
                    offenders.append(f"{rel}:{lineno} {why}")
        assert not offenders, (
            "2059: a log call carries a slice of user text. The privacy page promises "
            "fingerprints only, at EVERY log level. Route it through "
            "services.utils.utterance_log.utterance_fields(text) (structlog kwargs) or "
            "utterance_preview(text, limit) (one string). Ceiling 0, never raised. "
            + "; ".join(offenders)
        )

    def test_allow_list_is_only_the_helper_and_commented_system_text(self):
        assert set(self.ALLOW_FILES) == {"services/utils/utterance_log.py"}
        assert len(self.ALLOW_SITES) == 9, "ALLOW_SITES grew: it is for system text only"
        assert all(len(reason) > 20 for reason in self.ALLOW_SITES.values())

    def test_census_unsliced_names_ceiling_zero_and_allow_list_not_stale(self):
        """The census: UNSLICED hits over services/ + web/ (before the #2059 third
        pass: 20 = the 9 of Arch's ruling + recognition_feedback + audit_logger
        + 9 system-text sites; after: only the 9 allow-listed system-text sites)."""
        root, files = self._files()
        found = set()
        for p in files:
            rel = p.relative_to(root).as_posix()
            for lineno, why in self.scan_source(p.read_text(encoding="utf-8"))[1]:
                if "UNSLICED" in why:
                    found.add(f"{rel}:{lineno}")
        assert found - set(self.ALLOW_SITES) == set(), sorted(found - set(self.ALLOW_SITES))
        assert set(self.ALLOW_SITES) - found == set(), (
            "stale ALLOW_SITES entries (line moved or call fixed): "
            + str(sorted(set(self.ALLOW_SITES) - found))
        )


class TestEraseUserCensus2064:
    """2064 (Arch-ruled shape, 2026-10-16): the /privacy page promises "we'll
    delete your account and everything in it within 14 days", and
    ``scripts/erase_user.py`` is the one path that keeps it. This census keeps
    a new table from escaping that path.

    Walks ``Base.metadata``. A table is user-owned when it has an owner-named
    column (``user_id``, ``owner_id``, ``created_by``, ``added_by``,
    ``linked_by``, ``principal``/``principal_id``, any ``*_user_id``), an FK to
    ``users``, or an FK to another user-owned table (children of user data are
    user data; run to a fixed point). Every user-owned table must be in
    ``erase_user.PLAN`` or in ``erase_user.ALLOW_LIST`` with a written reason.
    Ceiling 0 unplanned, never raised: a new user table ships with its plan
    step (in FK dependency order; tests/unit/scripts/test_erase_user_2064.py
    pins the order) or an allow-list line saying why its rows outlive the user.
    """

    @staticmethod
    def _census():
        import importlib

        import services.database.models  # noqa: F401  (registers every model table)
        from services.database.models import Base

        erase_user = importlib.import_module("scripts.erase_user")
        return erase_user, Base.metadata, erase_user.user_owned_tables(Base.metadata)

    def test_denominator_census_sees_the_user_tables(self):
        """m-44: a pass means nothing if the walk found nothing."""
        _, md, owned = self._census()
        assert len(md.tables) >= 45, f"only {len(md.tables)} tables in Base.metadata"
        assert len(owned) >= 40, (
            f"only {len(owned)} user-owned tables found; the model import or the "
            "owner predicate broke, not the schema got smaller"
        )

    def test_every_user_owned_table_is_planned_or_allow_listed_ceiling_zero(self):
        erase_user, _, owned = self._census()
        missing = erase_user.unplanned(owned)
        assert not missing, (
            "2064: user-owned tables that scripts/erase_user.py would leave behind: "
            + "; ".join(f"{t} ({owned[t]})" for t in missing)
            + ". Add a Step to erase_user.PLAN in FK dependency order (children before "
            "parents), or an ALLOW_LIST entry with the reason its rows outlive the user. "
            "Ceiling 0, never raised."
        )

    def test_allow_list_entries_are_live_and_reasoned(self):
        erase_user, md, owned = self._census()
        for table, reason in erase_user.ALLOW_LIST.items():
            assert table in md.tables, f"ALLOW_LIST names {table}, which no longer exists"
            assert table in owned, f"ALLOW_LIST names {table}, which holds no user data"
            assert (
                table not in erase_user.plan_tables()
            ), f"{table} is both planned and allow-listed"
            assert len(reason.split()) >= 4, f"ALLOW_LIST[{table!r}] needs a written reason"

    def test_plan_names_only_real_tables(self):
        erase_user, md, _ = self._census()
        stale = [t for t in erase_user.plan_tables() if t not in md.tables]
        assert not stale, f"erase_user.PLAN names tables that no longer exist: {stale}"


class TestPerPrincipalTestResultRatchet2071:
    """2071 (Arch-ruled shape, 2026-10-16): the Integrations Test result is keyed by
    ``(principal, integration)`` in ``services/integrations/principal_test_results.py``.
    Before 2071 it lived on the host ``IntegrationHealthMonitor`` keyed by integration
    name alone, so one account's Test set the status, error text and check time every
    other account saw on the card and in chat.

    Ceiling 0, never raised: no ``get_component_health(...)`` call in ``services/`` or
    ``web/`` whose argument is a user-facing integration id (derived from the route's
    ``INTEGRATION_REGISTRY``) or is not a string literal at all (a variable could carry
    one, and is not provably host-level). Host-level components (``redis_connection``,
    ``conversation_cache``, ...) are named by literal and stay on the host monitor. The
    same rule covers the host monitor's writers (``record_success`` /
    ``record_failure`` with a component argument), so no Test result is written
    host-wide again. A per-person result goes through
    ``record_test_result(principal, ...)`` / ``get_test_result(principal, ...)``.
    """

    READERS = ("get_component_health",)
    WRITERS = ("record_success", "record_failure")
    ACCESSOR = Path("services/integrations/principal_test_results.py")
    MONITOR = Path("services/health/integration_health_monitor.py")

    @staticmethod
    def _user_facing_ids():
        from services.integrations.integration_status_service import KNOWN_INTEGRATIONS
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        return set(INTEGRATION_REGISTRY) | set(KNOWN_INTEGRATIONS)

    @staticmethod
    def _files():
        return sorted(p for root in ("services", "web") for p in Path(root).rglob("*.py"))

    @classmethod
    def _scan(cls, src: str, user_facing):
        """Return (offending, host_level) call descriptions in ``src``."""
        offending, host_level = [], []
        for node in ast.walk(ast.parse(src)):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            name = node.func.attr
            if name not in cls.READERS + cls.WRITERS:
                continue
            if not node.args:
                continue  # e.g. a circuit breaker's record_success(): not a component
            arg = node.args[0]
            where = f"{node.lineno} .{name}({ast.unparse(arg)})"
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                (offending if arg.value in user_facing else host_level).append(where)
            elif name in cls.READERS or len(node.args) >= 2:
                offending.append(where)  # non-literal component: not provably host-level
        return offending, host_level

    def test_user_facing_ids_derive_from_the_registry(self):
        ids = self._user_facing_ids()
        assert {"github", "notion", "slack", "calendar"} <= ids, ids

    def test_scanner_flags_the_pre_2071_shapes(self):
        ids = self._user_facing_ids()
        for src in (
            'm.get_component_health("calendar")',
            "m.get_component_health(integration_id)",
            "m.record_failure(integration_name, error_msg)",
            'm.record_success("slack", 12.0)',
        ):
            assert self._scan(src, ids)[0], src
        for src in (
            'm.get_component_health("redis_connection")',
            'health_monitor.record_failure("conversation_cache", str(e))',
            "self.circuit_breaker.record_success()",
            "s.get_test_result(principal, integration_id)",
        ):
            assert not self._scan(src, ids)[0], src

    def test_denominator_host_level_callers_are_seen(self):
        """m-44: the scan must see the host-level writers it lets through."""
        ids = self._user_facing_ids()
        seen = []
        for path in self._files():
            seen += self._scan(path.read_text(encoding="utf-8"), ids)[1]
        assert len(seen) >= 5, f"only {len(seen)} host-level monitor calls seen: {seen}"

    def test_no_host_keyed_user_facing_test_result_ceiling_zero(self):
        ids = self._user_facing_ids()
        violations = []
        for path in self._files():
            if path == self.MONITOR:
                continue  # the monitor's own definitions
            offending, _ = self._scan(path.read_text(encoding="utf-8"), ids)
            violations += [f"{path}:{o}" for o in offending]
        assert not violations, (
            "2071: a user-facing integration's Test result must be keyed by principal "
            "(principal_test_results.record_test_result / get_test_result), never read "
            "or written on the host IntegrationHealthMonitor by integration name. "
            "Ceiling 0, never raised. " + "; ".join(violations)
        )

    def test_the_accessor_is_principal_keyed(self):
        import inspect

        from services.integrations.principal_test_results import PrincipalTestResultStore

        for method in ("record_test_result", "get_test_result"):
            params = list(inspect.signature(getattr(PrincipalTestResultStore, method)).parameters)
            assert params[1:3] == ["principal", "integration"], (method, params)
        assert self.ACCESSOR.exists()


class TestStaleBindingRendererRatchet2072:
    """2072 follow-up (Arch's ruling, issuecomment-6234453553): ``configured`` means a
    connection EXISTS, not that it works. Since b1fbfa3da1 a GitHub binding GitHub has
    rejected reads ``configured=True, via="oauth_binding_stale", healthy=False``. Gates
    (radar, repo resolver, first contact, the canonical metadata gates) stay on
    ``configured``: the read runs and discloses STALE_TOKEN. A surface that RENDERS a
    working-connection claim ("connected", "active", ``valid: True``) must also consult
    the broken-binding signal (``needs_reconnecting(...)``, ``healthy`` or ``via``).

    Denominator: the four renderer sites Arch named, five functions (site 2 is a feed and
    its renderer):

    1. Settings GitHub status: ``web/api/routes/settings_integrations.py``
       ``get_github_settings`` (``"valid": True``).
    2. Chat floor: ``services/intent_service/context_assembler.py``
       ``_gather_status_priority_context`` (``github_connected``), rendered by
       ``services/intent_service/conversational_floor.py`` ``_format_domain_context``
       ("- GitHub: connected", which must read ``github_needs_reconnecting``).
    3. Setup guidance: ``services/intent_service/canonical_handlers.py``
       ``_format_integration_setup_guidance`` ("**Connected:**").
    4. Identity context: ``context_assembler.py`` ``_gather_identity_context``
       (``"active"``).

    Ceiling 0, never raised. The scan reads each function's code (AST, docstring
    dropped, comments gone), so a comment naming the signal does not satisfy it.
    """

    # (path, function, claim marker, markers of which one must appear)
    _STATUS_SIGNAL = ("needs_reconnecting(", "'healthy'", "'via'")
    SITES = (
        (
            "web/api/routes/settings_integrations.py",
            "get_github_settings",
            "'valid': True",
            _STATUS_SIGNAL,
        ),
        (
            "services/intent_service/context_assembler.py",
            "_gather_status_priority_context",
            "context['github_connected']",
            _STATUS_SIGNAL,
        ),
        (
            "services/intent_service/conversational_floor.py",
            "_format_domain_context",
            "- GitHub: connected",
            ("github_needs_reconnecting",),
        ),
        (
            "services/intent_service/canonical_handlers.py",
            "_format_integration_setup_guidance",
            "**Connected:**",
            _STATUS_SIGNAL,
        ),
        (
            "services/intent_service/context_assembler.py",
            "_gather_identity_context",
            "'active'",
            _STATUS_SIGNAL,
        ),
    )

    @staticmethod
    def _function_code(src: str, name: str):
        """``ast.unparse`` of the named (async) function, docstring dropped; else None."""
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
                body = node.body
                if (
                    body
                    and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)
                ):
                    body = body[1:]
                return "\n".join(ast.unparse(stmt) for stmt in body)
        return None

    @classmethod
    def _violation(cls, code: str, claim: str, signals) -> bool:
        return claim in code and not any(s in code for s in signals)

    def test_scanner_flags_the_pre_fix_shapes(self):
        pre_fix = (
            (
                "async def f(s):\n    if s.get('configured'):\n"
                "        return {'configured': True, 'valid': True}",
                "'valid': True",
            ),
            (
                "def f(statuses):\n    return [{'status': 'active' if s.get('configured') "
                "else 'inactive'} for s in statuses]",
                "'active'",
            ),
        )
        for src, claim in pre_fix:
            code = self._function_code(src, "f")
            assert self._violation(code, claim, self._STATUS_SIGNAL), src
        fixed = (
            "def f(statuses):\n    return [{'status': 'needs_reconnecting' if "
            "needs_reconnecting(s) else 'active'} for s in statuses]"
        )
        assert not self._violation(self._function_code(fixed, "f"), "'active'", self._STATUS_SIGNAL)
        commented = (
            "def f(s):\n    '''needs_reconnecting( is named only here'''\n"
            "    # needs_reconnecting(\n    return {'valid': True}"
        )
        assert self._violation(
            self._function_code(commented, "f"), "'valid': True", self._STATUS_SIGNAL
        )

    def test_denominator_every_site_found_and_still_renders_its_claim(self):
        """m-44: the scan is not vacuous: all five functions exist and carry the claim."""
        seen = []
        for path, func, claim, _ in self.SITES:
            code = self._function_code(Path(path).read_text(encoding="utf-8"), func)
            assert code is not None, f"{path}::{func} not found (renamed? update SITES)"
            assert claim in code, f"{path}::{func} no longer renders {claim!r}; update SITES"
            seen.append(func)
        assert len(seen) == 5, seen

    def test_no_connection_claim_from_configured_alone_ceiling_zero(self):
        violations = []
        for path, func, claim, signals in self.SITES:
            code = self._function_code(Path(path).read_text(encoding="utf-8"), func)
            if code is not None and self._violation(code, claim, signals):
                violations.append(f"{path}::{func} renders {claim!r} without {signals}")
        assert len(violations) <= 0, (
            "Renderer claims a working connection from `configured` alone; a STALE "
            "GitHub binding would read as connected (2072 follow-up). Consult "
            "needs_reconnecting(status) / healthy / via:\n  " + "\n  ".join(violations)
        )


class TestSecurityCheckBypassCallers1982:
    """Arch's #1982 condition 1 (2026-10-11): ``UserAPIKeyService.store_user_key``
    gained a keyword-only ``security_check`` that skips the #268 format/strength/
    leak validator. That is a bypass parameter on a security API, so the callers
    allowed to pass ``False`` are a CLOSED LIST, not a docstring: a token verified
    live with its provider by the caller in the same request (the GitHub PAT dual
    write) and the one-off backfill of PATs that were accepted the same way.

    Adding a caller means adding it here, deliberately, with a reason.

    LAYER (m-43): a source sweep of the non-test trees that ship (services/, web/,
    scripts/, the entrypoints), so a new caller anywhere in the product fails the
    build; tests may pass False to exercise the service. Vacuity guard: the two
    allowed files must still contain the call, so a refactor that moves the
    bypass elsewhere is caught rather than silently un-swept.
    """

    ALLOWED = {
        "services/connectors/github_pat_store.py",
        "scripts/backfill_github_pat_rows_1982.py",
    }
    NEEDLE = "security_check=False"

    def _hits(self, repo_root: Path) -> set[str]:
        hits: set[str] = set()
        roots = ["services", "web", "scripts"]
        files = [p for r in roots for p in (repo_root / r).rglob("*.py")] + list(
            repo_root.glob("main*.py")
        )
        for path in files:
            if "archive" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if self.NEEDLE in text:
                hits.add(path.relative_to(repo_root).as_posix())
        return hits

    def test_security_check_bypass_callers_are_a_closed_list(self):
        repo_root = Path(__file__).resolve().parent.parent
        hits = self._hits(repo_root)
        extra = hits - self.ALLOWED
        assert not extra, (
            f"security_check=False passed outside the #1982 closed list: {sorted(extra)}. "
            "A caller may skip the #268 validator only for a token it verified live with "
            "its provider in the same request; add it to ALLOWED with the reason, or don't."
        )
        missing = self.ALLOWED - hits
        assert not missing, (
            f"vacuity guard: expected the bypass in {sorted(missing)} and found none; "
            "the sweep is not seeing what it must see"
        )

    def test_security_check_is_keyword_only(self):
        import inspect

        from services.security.user_api_key_service import UserAPIKeyService

        param = inspect.signature(UserAPIKeyService.store_user_key).parameters["security_check"]
        assert param.kind is inspect.Parameter.KEYWORD_ONLY
        assert param.default is True


class TestBinderFileRatchet:
    """#1943 / xian's ask (2026-10-19, "Please do ask Arch for a ratchet on binders"),
    Arch's ruling on #1943 (comment 6277415066): every regex binder in the two intent
    packages is counted PER FILE, whether or not it sits inside a named span.

    The ratchet:
    1. Scope is the package, not a list: every ``.py`` under ``services/intent_service/``
       and ``services/intent/`` found by glob. A file absent from ``CEILINGS`` has ceiling
       0, so a new module with a regex fails, and so does moving a binder into a new file.
       ``pre_classifier.py`` is excluded: it stays under the Phase 3 gate alone.
    2. Per-file ceilings: a shrink in one file never pays for growth in another.
    3. Counting rule: ``TestExtractionPatternRatchet._count_regex_literals`` applied to the
       WHOLE module (shared, not a second copy) — every ``re``/``_re`` call with an inline
       pattern, every element of a ``*pattern*``-named list or tuple — plus one per module-
       or class-level string constant passed BY NAME to an ``re`` call. A compiled pattern
       counts at its ``compile``, not at each use. Patterns, not call sites.
    4. Tightness: ceilings equal the measured counts exactly; drift either way is loud.
       Lower a ceiling in the commit that earns it.
    5. The rule: a new failing phrasing gets a corpus row and a router arg
       (``intent.context["inversion_args"]``), never a new binder. A raise is allowed only
       for a regex that does not read the user's message (output formatting, a code-made
       id), with the reason in the ceiling comment and a decisions.log line; Arch validates.
    6. Honest limit: this counts regex only. Word sets and ``str.split`` on the message are
       binders too, held by review (the #2098 marker list was one).

    MEASURED 2026-10-19 by this class at 3a837f20fa: 298 literals in 24 files (59 files in
    scope), matching Arch's independent AST count the same day (298 / 24, same top six).
    """

    PACKAGES = ("services/intent_service", "services/intent")
    EXCLUDED = frozenset({"services/intent_service/pre_classifier.py"})
    MIN_FILES_IN_SCOPE = 50  # vacuity: 59 measured 2026-10-19

    # Frozen per-file ceilings — MEASURED 2026-10-19 (see class docstring). A file not
    # listed has ceiling 0.
    CEILINGS = {
        "services/intent_service/canonical_handlers.py": 81,
        "services/intent_service/classifier.py": 51,
        "services/intent/intent_service.py": 37,
        "services/intent_service/todo_handlers.py": 33,
        "services/intent_service/reminder_clear.py": 18,
        "services/intent_service/repo_clarification.py": 14,
        "services/intent_service/drafted_issue.py": 9,
        "services/intent_service/conversational_floor.py": 7,
        "services/intent_service/temporal_utils.py": 7,
        "services/intent_service/collaboration_gate.py": 6,
        "services/intent_service/unarmed_offer.py": 6,
        "services/intent_service/destructive_confirm.py": 4,
        "services/intent_service/scope_guard.py": 4,
        "services/intent_service/unwired_writes.py": 4,
        "services/intent_service/acceptance.py": 3,
        "services/intent_service/soft_invocation.py": 3,
        "services/intent_service/standup_preferences.py": 3,
        "services/intent_service/verified_inference.py": 2,
        "services/intent_service/add_project_clarify.py": 1,
        "services/intent_service/adopted_category_reads_only.py": 1,
        "services/intent_service/clear_todos.py": 1,
        "services/intent_service/consent_gate.py": 1,
        "services/intent_service/inversion_router.py": 1,
        "services/intent_service/workflow_entries.py": 1,
    }

    @classmethod
    def _files(cls):
        import glob

        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        out = []
        for pkg in cls.PACKAGES:
            for path in glob.glob(os.path.join(root, pkg, "**", "*.py"), recursive=True):
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                if rel not in cls.EXCLUDED:
                    out.append((rel, path))
        return sorted(out)

    @staticmethod
    def _named_constants_passed(tree) -> int:
        """Module- or class-level string constants passed by name to an ``re`` call,
        counted once each (the file-scope half of Arch's rule 3)."""
        import ast

        consts = set()
        for node in tree.body:
            scope = node.body if isinstance(node, ast.ClassDef) else [node]
            for n in scope:
                if (
                    isinstance(n, ast.Assign)
                    and isinstance(n.value, ast.Constant)
                    and isinstance(n.value.value, str)
                ):
                    consts.update(t.id for t in n.targets if isinstance(t, ast.Name))
        used = set()
        methods = TestExtractionPatternRatchet._RE_METHODS
        for sub in ast.walk(tree):
            if isinstance(sub, ast.Call):
                f = sub.func
                if (
                    isinstance(f, ast.Attribute)
                    and f.attr in methods
                    and isinstance(f.value, ast.Name)
                    and f.value.id in ("re", "_re")
                    and sub.args
                    and isinstance(sub.args[0], ast.Name)
                    and sub.args[0].id in consts
                ):
                    used.add(sub.args[0].id)
        return len(used)

    @classmethod
    def _count_file(cls, path) -> int:
        import ast

        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        shared = TestExtractionPatternRatchet()._count_regex_literals(tree)
        return shared + cls._named_constants_passed(tree)

    @classmethod
    def _all_counts(cls) -> dict:
        return {rel: cls._count_file(path) for rel, path in cls._files()}

    def test_scope_is_the_package(self):
        files = self._files()
        assert len(files) >= self.MIN_FILES_IN_SCOPE, (
            f"VACUITY: only {len(files)} files found under {self.PACKAGES}; "
            "the glob or the packages moved — re-point the ratchet."
        )
        assert not any(rel.endswith("pre_classifier.py") for rel, _ in files)
        for rel in self.CEILINGS:
            assert any(r == rel for r, _ in files), (
                f"VACUITY: {rel} has a ceiling but no longer exists in scope — "
                "remove its row (and re-measure) in the same commit."
            )

    def test_no_file_exceeds_its_ceiling(self):
        over = {
            rel: (count, self.CEILINGS.get(rel, 0))
            for rel, count in self._all_counts().items()
            if count > self.CEILINGS.get(rel, 0)
        }
        assert not over, (
            "BINDER RATCHET (Arch, #1943, 2026-10-19): regex binders grew in "
            f"{sorted(over)} (count, ceiling): {over}. A new failing phrasing gets a corpus "
            "row and a router arg (intent.context['inversion_args']), never a new binder. "
            "A raise is allowed only for a regex that does not read the user's message, "
            "with the reason in the ceiling comment and a decisions.log line (Arch validates)."
        )

    def test_binder_ratchet_stays_tight(self):
        counts = {rel: c for rel, c in self._all_counts().items() if c}
        assert counts == self.CEILINGS, (
            "Binder ceilings are frozen at MEASURED counts (tightness). Drift: "
            f"measured={counts} ceilings={self.CEILINGS}. Lower a ceiling in the commit "
            "that earns it; never raise one without Arch's review."
        )


class TestSyncCredentialCallsInAsyncRatchet:
    """#2101 (Arch's shape, 2026-10-19): a credential read on the hosted path is a
    synchronous psycopg2 connect (``EncryptedDBCredentialStore``, NullPool) and on a Mac
    a C call; a coroutine that calls the sync method directly blocks the event loop for
    the whole connect, and a chat turn reads several credentials (the 16:13 stall's
    window: 33 s of nothing logged inside one turn). ``KeychainService`` now carries
    ``aget_api_key`` / ``aread_secret`` / ``astore_api_key`` / ``adelete_api_key`` and
    ``GitHubConfigService.aget_authentication_token`` (each the sync op in
    ``asyncio.to_thread``); the chat-path callers were moved first.

    The ratchet, shrink-only:
    1. Scope: every ``.py`` under ``services/`` and ``web/`` (glob, no list).
    2. Count: a direct call ``<expr>.<name>(...)`` with ``name`` in ``SYNC_NAMES`` that
       sits anywhere inside an ``async def`` (nested sync helpers called from a
       coroutine are not seen; that limit is stated, not hidden).
    3. Per-file ceilings equal the measured counts exactly; a file not listed has
       ceiling 0, so a new coroutine with a sync credential call fails. Lower a ceiling
       in the commit that migrates a call; never raise one (Arch rules).

    MEASURED 2026-10-20 by this class in the #2101 lane: 39 calls in 10 files (527 files
    scanned), after the chat-path migrations (integration status ×3, calendar adapter,
    GitHub config via the router and the issue fetch, the adapter's PAT read).
    """

    PACKAGES = ("services", "web")
    SYNC_NAMES = frozenset(
        {
            "get_api_key",
            "store_api_key",
            "delete_api_key",
            "read_secret",
            "get_authentication_token",
        }
    )
    MIN_FILES_IN_SCOPE = 400  # vacuity: 527 measured 2026-10-20

    CEILINGS = {
        "web/api/routes/settings_integrations.py": 10,  # 2026-10-24: get_all_oauth_status retired (#2151); 2026-10-20: the calendars list read moved to aget_api_key (#2105)
        "services/connectors/disconnect.py": 6,
        "web/api/routes/setup.py": 6,
        "services/security/user_api_key_service.py": 4,
        "services/integrations/slack/socket_mode_runner.py": 3,
        "web/api/routes/integrations.py": 2,  # 2026-10-24: _test_calendar reads with provenance (#2151)
        "services/integrations/slack/oauth_handler.py": 2,
        "services/config/llm_config_service.py": 1,
        "services/integrations/notion/notion_integration_router.py": 1,
        "services/mcp/consumer/notion_adapter.py": 1,
    }

    @classmethod
    def _files(cls):
        root = Path(__file__).resolve().parent.parent
        out = []
        for pkg in cls.PACKAGES:
            out.extend(sorted((root / pkg).rglob("*.py")))
        return root, out

    @classmethod
    def _count_file(cls, path) -> int:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            return 0
        count = 0
        for node in ast.walk(tree):
            if not isinstance(node, ast.AsyncFunctionDef):
                continue
            for sub in ast.walk(node):
                if (
                    isinstance(sub, ast.Call)
                    and isinstance(sub.func, ast.Attribute)
                    and sub.func.attr in cls.SYNC_NAMES
                ):
                    count += 1
        return count

    @classmethod
    def _all_counts(cls):
        root, files = cls._files()
        counts = {}
        for f in files:
            n = cls._count_file(f)
            if n:
                counts[str(f.relative_to(root))] = n
        return len(files), counts

    def test_scope_is_not_vacuous(self):
        scanned, _ = self._all_counts()
        assert (
            scanned >= self.MIN_FILES_IN_SCOPE
        ), f"only {scanned} files scanned under {self.PACKAGES}"

    def test_no_file_exceeds_its_ceiling(self):
        _, counts = self._all_counts()
        over = {
            f: (n, self.CEILINGS.get(f, 0))
            for f, n in counts.items()
            if n > self.CEILINGS.get(f, 0)
        }
        assert not over, (
            "sync credential calls inside async def grew (#2101): "
            f"{over} (file: (measured, ceiling)). Await the a-prefixed method "
            "(KeychainService.aget_api_key etc.) instead of the sync one."
        )

    def test_ceilings_are_tight(self):
        _, counts = self._all_counts()
        slack = {f: (counts.get(f, 0), c) for f, c in self.CEILINGS.items() if counts.get(f, 0) < c}
        assert not slack, (
            f"a sync credential call was migrated: lower its ceiling in this commit: {slack} "
            "(file: (measured, ceiling))"
        )
