"""
Architecture Enforcement Tests - Phase 4A
Prevents regression to direct GitHubAgent imports
"""

import glob
import os
import re
from typing import List

import pytest


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
            "get_issue_by_url",  # Used by domain service & issue analyzer
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
        services/intent_service/classifier.py, services/intent_service/
        llm_classifier.py for the #1366/ADR-075 Component B reference fix.
        """
        service_files = glob.glob("services/**/*.py", recursive=True) + glob.glob(
            "web/**/*.py", recursive=True
        )

        violations = []

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
        for root, _dirs, files in os.walk("services"):
            if "__pycache__" in root:
                continue
            for f in files:
                if not f.endswith(".py"):
                    continue
                path = os.path.join(root, f)
                rel = os.path.relpath(path)
                if rel in self.ALLOWED:
                    continue
                src = open(path, encoding="utf-8", errors="ignore").read()
                if re.search(r"^\s*Base\s*=\s*declarative_base\(\)", src, re.M):
                    offenders.append(rel)
        assert not offenders, (
            f"Second declarative Base created in: {offenders} — one Base per DB "
            "(Arch invariant, #1312). Register models on "
            "services.database.connection.Base instead."
        )
