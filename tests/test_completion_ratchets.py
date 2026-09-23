"""Completion ratchets — the Finish-the-Unfinished sprint's growth guards (#1424).

Each test compares a mechanically-detected debt count against a frozen ceiling in
scripts/ratchet_ceilings.json. Counts may only go DOWN: a fix that removes debt
MUST lower the ceiling in the same commit (the MAX_DISPATCH_SITES discipline);
new debt that raises a count fails the build immediately.

These are growth-only guards: they cannot false-positive existing code, so they
CI-gate from day one (PM-ratified 2026-07-16) while the richer lints run
warn-mode pending Arch ratification.

Detectors:
  - silent_death_core     -> scripts/check_silent_death.py   (#1423)
  - unscoped_reads        -> scripts/check_unscoped_reads.py (#1419)
  - notimplementederror   -> raise-site count in production code (Census C)
  - todo_markers          -> TODO/FIXME/XXX/HACK comment count (Census C)

Plan of record: docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CEILINGS = json.loads((REPO_ROOT / "scripts" / "ratchet_ceilings.json").read_text())

RATCHET_MSG = (
    "\n{name}: count {count} exceeds frozen ceiling {ceiling} (#1424 ratchet).\n"
    "New debt of this class may not ship. Either remove it, or (for a reviewed "
    "exception) use the detector's annotation mechanism ({fix_hint}).\n"
    "If you MIGRATED debt away, lower the ceiling in scripts/ratchet_ceilings.json "
    "in this same commit."
)

SHRINK_MSG = (
    "\n{name}: count {count} is BELOW ceiling {ceiling} — nice, debt was removed. "
    "Lower the ceiling to {count} in scripts/ratchet_ceilings.json in this same "
    "commit so the improvement is locked in."
)


def _script_count(script: str, flag: str = "--count") -> int:
    out = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / script), flag],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=120,
    )
    assert out.returncode == 0, f"{script} failed: {out.stderr[:500]}"
    return int(out.stdout.strip())


def _grep_count(pattern: str, *, flags: int = 0) -> int:
    """Canonical pure-python recipe (embedded so the ratchet can't drift from a
    shell grep's quoting): count matching LINES in production .py under
    services/ + web/, excluding tests/archive/__pycache__."""
    rx = re.compile(pattern, flags)
    count = 0
    for root in ("services", "web"):
        for f in (REPO_ROOT / root).rglob("*.py"):
            if any(p in ("tests", "archive", "__pycache__") for p in f.parts):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count += sum(1 for line in text.splitlines() if rx.search(line))
    return count


def _assert_ratchet(name: str, count: int, fix_hint: str) -> None:
    ceiling = CEILINGS[name]
    assert count <= ceiling, RATCHET_MSG.format(
        name=name, count=count, ceiling=ceiling, fix_hint=fix_hint
    )
    # Shrinkage is success, but an un-lowered ceiling lets the next regression
    # hide inside the slack — force the lock-in.
    assert count == ceiling, SHRINK_MSG.format(name=name, count=count, ceiling=ceiling)


@pytest.mark.smoke
def test_silent_death_ratchet():
    """#1423: broad no-reraise except handlers on the core path may only decrease."""
    _assert_ratchet(
        "silent_death_core",
        _script_count("check_silent_death.py"),
        "narrow the exception type, re-raise, or '# silent-ok: <reason>'",
    )


@pytest.mark.smoke
def test_unscoped_reads_ratchet():
    """#1419: global reads of user-specific credential/config state may only decrease."""
    _assert_ratchet(
        "unscoped_reads",
        _script_count("check_unscoped_reads.py"),
        "pass the principal (username=/user_id=) or '# global-ok: <reason>'",
    )


@pytest.mark.smoke
def test_unscoped_repo_reads_ratchet():
    """ADR-079 D2b: owner-bearing repository reads without an owner predicate may
    only decrease. The model set is DERIVED (D3) — a new owner-bearing table is
    auto-covered, so genuinely-new unscoped reads raise this count and fail here.
    Legit-indirect scoping (fetch-then-check, join/subquery) gets
    '# global-ok: <how>' per the D4/D6 allowlist discipline (Arch calibrates)."""
    _assert_ratchet(
        "unscoped_repo_reads",
        _script_count("check_unscoped_reads.py", flag="--count-repo"),
        "add the owner predicate to the WHERE, or '# global-ok: <how it is scoped>'",
    )


@pytest.mark.smoke
def test_notimplementederror_ratchet():
    """Census C: NotImplementedError raise sites in production code may only decrease."""
    # Lines carrying '# nie-ok: <reason>' are reviewed LOUD stubs (e.g. the
    # Arch-ruled security raise in token_blacklist, #1436 F4) — the ratchet
    # hunts silent stubs, and converting a silent no-op into a loud raise is an
    # improvement the raw count would misread as regression.
    count = _grep_count(r"raise NotImplementedError") - _grep_count(
        r"raise NotImplementedError\(.*# nie-ok:"
    )
    _assert_ratchet(
        "notimplementederror",
        count,
        "implement it, annotate '# nie-ok: <reason>' for a reviewed loud stub, "
        "or route through a documented-legit abstract/guard shape",
    )


@pytest.mark.smoke
def test_todo_marker_ratchet():
    """Census C: TODO/FIXME/XXX/HACK comment markers may only decrease."""
    _assert_ratchet(
        "todo_markers",
        _grep_count(r"#\s*(TODO|FIXME|XXX|HACK)\b", flags=re.IGNORECASE),
        "do the work, file an issue and reference it, or delete the stale marker",
    )


# ---------------------------------------------------------------------------
# #1522 / #1499: surface-reachability ratchets — the dead-surface class may
# only SHRINK. A router defined but mounted nowhere, or a backup/shadow file
# sitting in the tree, manufactures false confidence (tests pass against code
# no request can reach; audits chase route defs that never serve). Both
# audits ended with "make this a ratchet so the class cannot regrow" — this
# is that ratchet. Each guard is an EXPLICIT allowlist plus a count ceiling:
# a NEW dark router or shadow file fails by being found; a router that gets
# mounted or deleted (or a file removed) fails "stays tight" until it leaves
# the list, so the allowlist can never quietly outlive its referents.
#
# LAYER (m-43): static — AST over module-level ``X = APIRouter(...)`` in
# web/ + services/, mount sites = ``RouterInitializer.mount_router(app, "<mod>",
# "<var>", ...)`` calls in web/app.py + web/startup.py. DENOMINATOR (m-44):
# module-level routers only. KNOWN BLIND SPOT, stated not hidden: routers
# created as CLASS attributes (the Slack webhook router, plugin routers mounted
# at runtime via registry.get_routers()) are outside this scan — the plugin
# ones are live by construction, the webhook one is #1496's — a class-scoped
# router census is the follow-up if this ever needs to see them.
# ---------------------------------------------------------------------------

_ROUTER_ROOTS = ("web", "services")
_MOUNT_FILES = ("web/app.py", "web/startup.py")

# Dark today (fresh census 2026-09-23), each with the issue that owns its fate.
UNMOUNTED_ROUTER_ALLOWLIST = {
    ("services.api.feedback_api", "feedback_router"),  # #1499 1.4 — collision-armed twin
    (
        "services.api.health.staging_health",
        "staging_health_router",
    ),  # #1499 1.3 — doc-credited, dead
    ("web.api.routes.conversation_context_demo", "router"),  # #1499 Class 2 — demo, unreferenced
    ("web.api.routes.loading_demo", "router"),  # #1499 Class 2 — demo, unreferenced
}

# Tracked backup/shadow files the audits flagged as misleaders (#1499 Class 5,
# #1522). Disposal is a Rule-0 item with Arch; until then they are pinned so
# no NEW one can join them.
SHADOW_FILE_ALLOWLIST = {
    "config/PIPER.md.backup-20251101",
    "services/integrations/slack/webhook_router.py.security-fix-backup",
    "backup_before_phase2_20251104_104652.sql",
    "backup_before_phase2_20251104_110227.sql",
    "backup_before_phase2_20251104_110245.sql",
    "backup_before_phase2_20251104_110300.sql",
}
_SHADOW_PATTERNS = re.compile(
    r"(\.bak$|\.backup(-|\.|$)|\.orig$|-backup$|\.security-fix-backup$|^backup_.*\.sql$)"
)


def _defined_module_level_routers() -> set[tuple[str, str]]:
    import ast

    found: set[tuple[str, str]] = set()
    for base in _ROUTER_ROOTS:
        for p in (REPO_ROOT / base).rglob("*.py"):
            if "__pycache__" in p.parts or "tests" in p.parts:
                continue
            try:
                tree = ast.parse(p.read_text())
            except (SyntaxError, UnicodeDecodeError):
                continue
            mod = ".".join(p.relative_to(REPO_ROOT).with_suffix("").parts)
            for node in tree.body:
                targets = []
                value = None
                if isinstance(node, ast.Assign):
                    targets, value = node.targets, node.value
                elif isinstance(node, ast.AnnAssign) and node.value is not None:
                    targets, value = [node.target], node.value
                if not isinstance(value, ast.Call):
                    continue
                f = value.func
                fname = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
                if fname != "APIRouter":
                    continue
                for t in targets:
                    if isinstance(t, ast.Name):
                        found.add((mod, t.id))
    return found


def _mounted_routers() -> set[tuple[str, str]]:
    import ast

    mounted: set[tuple[str, str]] = set()
    for rel in _MOUNT_FILES:
        tree = ast.parse((REPO_ROOT / rel).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "mount_router":
                consts = [a.value for a in node.args if isinstance(a, ast.Constant)]
                if len(consts) >= 2:
                    mounted.add((consts[0], consts[1]))
    return mounted


@pytest.mark.smoke
def test_unmounted_routers_ratchet():
    """#1522/#1499: every module-level APIRouter is mounted, or explicitly allowlisted."""
    dark = _defined_module_level_routers() - _mounted_routers()
    new = dark - UNMOUNTED_ROUTER_ALLOWLIST
    assert not new, (
        f"NEW unmounted router(s) {sorted(new)} — mount it (web/app.py or web/startup.py "
        "via RouterInitializer.mount_router) or delete it; do not add to the allowlist "
        "without an issue number."
    )
    stale = UNMOUNTED_ROUTER_ALLOWLIST - dark
    assert not stale, (
        f"allowlist row(s) {sorted(stale)} no longer dark (mounted or deleted) — remove them "
        "and lower the ceiling: the list must never outlive its referents."
    )
    _assert_ratchet(
        "unmounted_routers",
        len(dark),
        "mount or delete the router (Rule-0 ruling for deletions, #1499 Class 2)",
    )


@pytest.mark.smoke
def test_shadow_files_ratchet():
    """#1522/#1499 Class 5: no tracked backup/shadow files beyond the pinned set."""
    tracked = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, cwd=REPO_ROOT, check=True
    ).stdout.splitlines()
    shadows = {
        f for f in tracked if _SHADOW_PATTERNS.search(Path(f).name) or f.startswith("backup_")
    }
    new = shadows - SHADOW_FILE_ALLOWLIST
    assert (
        not new
    ), f"NEW backup/shadow file(s) tracked: {sorted(new)} — delete them; never commit backups."
    stale = SHADOW_FILE_ALLOWLIST - shadows
    assert (
        not stale
    ), f"allowlist row(s) {sorted(stale)} no longer exist — remove them and lower the ceiling."
    _assert_ratchet("shadow_files", len(shadows), "delete the shadow file (audit-misleader)")


# ---------------------------------------------------------------------------
# #1522 legs 3 + 4 (2026-09-23): templates reachable-or-allowlisted, assets
# referenced-or-allowlisted. The audit's "48% of components included by
# nothing" was a one-shot census; these make it a ceiling.
#
# LAYER (m-43): static. Templates — roots are every ``"<name>.html"`` string
# literal in web/ + services/ + main.py (TemplateResponse / get_template /
# render sites), edges are Jinja ``include`` / ``extends`` / ``import`` /
# ``from`` tags; a template is DARK when no root reaches it. Assets — every
# tracked file under web/static + web/assets is LIVE when its basename occurs
# in any template, JS, CSS or python file other than itself. DENOMINATOR
# (m-44): templates/ only (web/templates/admin is dev_trust's private root, one
# file, mounted by its own router — not scanned); basename matching is
# deliberately loose in the LIVE direction (a basename that appears anywhere
# counts), so this can under-report dark assets but never invents one; a
# template rendered via a dynamic path (f-string) is outside the root scan and
# would show as dark — none exist today (census 2026-09-23), and a false-dark
# fails loudly by name rather than silently passing.
# ---------------------------------------------------------------------------

_TEMPLATES_ROOT = "templates"
_TEMPLATE_ROOT_SCAN = ("web", "services", "main.py")
_ASSET_ROOTS = ("web/static", "web/assets")
_ASSET_REFERRER_ROOTS = ("templates", "web", "services", "main.py")
_JINJA_EDGE = re.compile(r"""{%-?\s*(?:include|extends|import|from)\s+['"]([^'"]+)['"]""")
_HTML_LITERAL = re.compile(r"""['"]([\w\-/\.]+\.html)['"]""")

# Dark today (fresh census 2026-09-23), each with the issue that owns its fate.
# Disposal (delete vs re-wire) is #1522's Rule-0 item with Arch; until ruled,
# pinned so no NEW dark template can join them.
DARK_TEMPLATE_ALLOWLIST = {
    "404.html",  # no exception handler renders it — app answers JSON
    "500.html",  # same
    "network-error.html",  # same family
    "documents.html",  # marked dead at #1270 (345fbb7db0); page self-titles elsewhere
    "layouts/base.html",  # every page extends layouts/app_shell.html (#1171 F2)
    "components/channel_continuity.html",
    "components/document_window.html",  # included only by dead documents.html
    "components/greeting_context.html",
    "components/insight_card.html",
    "components/insight_controls.html",
    "components/lifecycle_detail.html",
    "components/lifecycle_notification.html",
    "components/navigation.html",  # superseded by the nav rail (#1280)
    "components/place_window.html",  # documented dead twin (web/api/routes/places.py:7)
    "components/preference_suggestion.html",  # self-include in a usage comment only
    "components/privacy_mode.html",
    "components/reflection_summary.html",
    "components/skeleton.html",
    "components/spinner.html",
}

DARK_ASSET_ALLOWLIST = {
    "web/assets/favicon-16x16.png",  # only favicon.ico is linked
    "web/assets/favicon-32x32.png",
    "web/assets/favicon-icon.ico",
    "web/assets/favicon-simple.ico",
    "web/assets/markdown-renderer-v2.js",  # markdown-renderer.js is the live one
    "web/assets/markdown-renderer-v3.js",
    "web/static/admin/compose.css",  # #1499 — admin surface, nothing links it
    "web/static/admin/compose.js",
    "web/static/css/home-modules.css",
    "web/static/css/skeleton.css",  # pairs with dark components/skeleton.html
}


def _tracked(*roots: str) -> list[str]:
    return subprocess.run(
        ["git", "ls-files", *roots], capture_output=True, text=True, cwd=REPO_ROOT, check=True
    ).stdout.split()


def _dark_templates() -> set[str]:
    troot = REPO_ROOT / _TEMPLATES_ROOT
    templates = {str(p.relative_to(troot)) for p in troot.rglob("*.html")}
    edges = {t: set(_JINJA_EDGE.findall((troot / t).read_text())) for t in templates}
    roots: set[str] = set()
    for base in _TEMPLATE_ROOT_SCAN:
        paths = [REPO_ROOT / base] if base.endswith(".py") else (REPO_ROOT / base).rglob("*.py")
        for p in paths:
            if "__pycache__" in p.parts or "tests" in p.parts:
                continue
            roots.update(_HTML_LITERAL.findall(p.read_text(errors="ignore")))
    reach: set[str] = set()
    stack = [r for r in roots if r in templates]
    while stack:
        t = stack.pop()
        if t in reach:
            continue
        reach.add(t)
        stack.extend(r for r in edges[t] if r in templates)
    return templates - reach


def _dark_assets() -> set[str]:
    assets = [a for a in _tracked(*_ASSET_ROOTS) if not a.endswith((".md", ".txt"))]
    corpus: dict[str, str] = {}
    for base in _ASSET_REFERRER_ROOTS:
        paths = [REPO_ROOT / base] if base.endswith(".py") else (REPO_ROOT / base).rglob("*")
        for p in paths:
            if p.is_file() and p.suffix in (".html", ".js", ".css", ".py", ".json"):
                if "__pycache__" in p.parts or "node_modules" in p.parts:
                    continue
                corpus[str(p.relative_to(REPO_ROOT))] = p.read_text(errors="ignore")
    return {
        a
        for a in assets
        if not any(Path(a).name in s for p, s in corpus.items() if p != a)
    }


@pytest.mark.smoke
def test_dark_templates_ratchet():
    """#1522 leg 3: every template is reachable from a render site, or allowlisted."""
    dark = _dark_templates()
    new = dark - DARK_TEMPLATE_ALLOWLIST
    assert not new, (
        f"NEW unreachable template(s) {sorted(new)} — render it (a TemplateResponse root or "
        "a Jinja include/extends from a reachable one) or delete it; do not add to the "
        "allowlist without an issue number."
    )
    stale = DARK_TEMPLATE_ALLOWLIST - dark
    assert not stale, (
        f"allowlist row(s) {sorted(stale)} no longer dark (wired or deleted) — remove them "
        "and lower the ceiling: the list must never outlive its referents."
    )
    _assert_ratchet(
        "dark_templates", len(dark), "wire or delete the template (Rule-0 ruling, #1522)"
    )


@pytest.mark.smoke
def test_dark_assets_ratchet():
    """#1522 leg 4: every tracked static asset is referenced somewhere, or allowlisted."""
    dark = _dark_assets()
    new = dark - DARK_ASSET_ALLOWLIST
    assert not new, (
        f"NEW unreferenced asset(s) {sorted(new)} — reference it or delete it; do not add to "
        "the allowlist without an issue number."
    )
    stale = DARK_ASSET_ALLOWLIST - dark
    assert not stale, (
        f"allowlist row(s) {sorted(stale)} no longer dark (referenced or deleted) — remove "
        "them and lower the ceiling."
    )
    _assert_ratchet("dark_assets", len(dark), "reference or delete the asset (#1522)")


@pytest.mark.smoke
def test_principal_blind_suites_ratchet():
    """#1533: test files that drive a principal-keyed surface without ever passing a
    real user_id may only decrease. Census + denominator:
    scripts/census_principal_blind_tests.py (batch 2, 2026-09-23: 30 of 92 keyed)."""
    _assert_ratchet(
        "principal_blind_suites",
        _script_count("census_principal_blind_tests.py"),
        "add an authenticated sibling class (two real user_ids, one session_id) — shape: "
        "tests/intent/contracts/test_multiuser_contracts.py::TestMultiUserContractsAuthenticated",
    )
