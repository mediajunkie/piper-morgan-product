"""#1466 binding-invariant guard (Arch-spec'd, 2026-08-03).

The property that preserves the Slack-side proof is not "who writes" but
"who CALLS the writer, and where their arguments come from" (Arch). Four
assertions, creator and deleter deliberately split (different risk profiles):

1. SlackIdentity has exactly ONE creator: redeem_link_code.
2. Exactly ONE deleter: unlink_slack_identity (owner-scoped, benign).
3. redeem_link_code's caller set is EXACTLY the Slack webhook path — a web
   route calling it with URL-param values would reintroduce unsolicited
   binding through the sanctioned function; this assertion makes that loud.
4. In settings routes, slack ids appear only in status/unlink surfaces —
   never on a create path.

Scope: services/ + web/ (product code). Tests/fixtures are exempt.
"""
import ast
import glob
import re

import pytest

PRODUCT_GLOBS = ("services/**/*.py", "web/**/*.py")
CREATOR_HOME = "services/auth/slack_link_service.py"
SLACK_CALLER_HOME = "services/integrations/slack/webhook_router.py"


def _product_files():
    out = []
    for g in PRODUCT_GLOBS:
        out.extend(glob.glob(g, recursive=True))
    return [f for f in out if "__pycache__" not in f]


def _enclosing_functions(path, needle):
    """Names of top-level/async functions whose source contains needle."""
    src = open(path).read()
    if needle not in src:
        return set()
    tree = ast.parse(src)
    hits = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            seg = ast.get_source_segment(src, node) or ""
            if needle in seg:
                hits.add(node.name)
    return hits


@pytest.mark.smoke
def test_slack_identity_has_exactly_one_creator():
    creators = {}
    for f in _product_files():
        src = open(f).read()
        if re.search(r"(?<!class )SlackIdentity\s*\(", src):
            fns = _enclosing_functions(f, "SlackIdentity(")
            creators[f] = fns
    assert set(creators) == {CREATOR_HOME}, (
        f"SlackIdentity constructed outside {CREATOR_HOME}: {creators}. "
        "The redemption path is the ONLY sanctioned binding site (#1466/Arch)."
    )
    assert creators[CREATOR_HOME] <= {"redeem_link_code"}, (
        f"SlackIdentity constructed by unexpected function(s): {creators[CREATOR_HOME]}"
    )


@pytest.mark.smoke
def test_slack_identity_has_exactly_one_deleter():
    deleters = {}
    pat = re.compile(r"delete\(.*SlackIdentity|SlackIdentity.*\.delete|delete\s*\(\s*ident", re.I)
    for f in _product_files():
        src = open(f).read()
        if "SlackIdentity" in src and pat.search(src):
            deleters[f] = _enclosing_functions(f, "SlackIdentity")
    assert set(deleters) <= {CREATOR_HOME}, f"unexpected deleter site(s): {deleters}"


@pytest.mark.smoke
def test_redeem_link_code_called_only_from_slack_path():
    callers = {}
    for f in _product_files():
        if f == CREATOR_HOME:
            continue  # the def itself
        src = open(f).read()
        if re.search(r"redeem_link_code\s*\(", src):
            callers[f] = sorted(_enclosing_functions(f, "redeem_link_code"))
    assert set(callers) == {SLACK_CALLER_HOME}, (
        f"redeem_link_code called outside the Slack webhook path: {callers}. "
        "A non-Slack caller (esp. a web route with URL-param arguments) would "
        "reintroduce unsolicited binding THROUGH the sanctioned writer — the "
        "attack Arch's 2026-08-03 ruling forbids. The caller set IS the invariant."
    )


@pytest.mark.smoke
def test_settings_routes_slack_ids_confined_to_status_and_unlink():
    path = "web/api/routes/settings_integrations.py"
    src = open(path).read()
    tree = ast.parse(src)
    offenders = {}
    allowed = {"get_slack_link_status", "unlink_slack_account"}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            seg = ast.get_source_segment(src, node) or ""
            if "slack_user_id" in seg and node.name not in allowed:
                # route handlers only (decorated with router.*)
                if any("router" in ast.dump(d) for d in node.decorator_list):
                    offenders[node.name] = True
    assert not offenders, (
        f"Route handler(s) outside status/unlink reference slack_user_id: "
        f"{sorted(offenders)}. Create-path routes must never accept Slack ids "
        f"(prefill may never bind — Arch ruling 2026-08-03)."
    )
