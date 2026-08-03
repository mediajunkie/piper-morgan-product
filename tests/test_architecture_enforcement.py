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
        services/intent_service/classifier.py for the #1366/ADR-075 Component B
        reference fix (llm_classifier.py deleted 2026-08-02, #1432).
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
        mapper_variants = {
            k for k, v in ActionMapper.ACTION_MAPPING.items() if v in dispatched
        }
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
        missing = derived - ledgered
        stale = ledgered - derived
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
        assert not failures, (
            "POINTER resolution failures (#1433):\n  " + "\n  ".join(failures)
        )

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

        stale = set(UNWIRED_WRITE_DECLINES) & self._reachable_actions()
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
        snippets = {
            surface: row["snippet"] for surface, row in CONTEXTUAL_FALLBACK_DENIALS.items()
        }

        uncovered = [
            frag
            for frag in fragments
            if not any(snip in frag for snip in snippets.values())
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
            "EXECUTION elif-token derivation collapsed — idiom changed; fix "
            "_elif_tokens()."
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
