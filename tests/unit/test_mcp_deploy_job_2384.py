"""Issue 2384 (ADR-084 D6): the MCP deploy job in ``fly-deploy.yml`` keeps HOST's bounds.

A workflow-file pin, read as YAML and as text. It cannot show the job runs: the first
real dispatch is that test, and it needs xian's one-time token.
DENOMINATOR: every job and every dispatch input in the workflow.
"""

import re
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "fly-deploy.yml"
TEXT = WORKFLOW.read_text(encoding="utf-8")
DOC = yaml.safe_load(TEXT)
JOBS = DOC["jobs"]
MCP = JOBS["deploy-mcp"]
INPUTS = DOC[True]["workflow_dispatch"]["inputs"]  # PyYAML reads the key `on` as True
MCP_TEXT = TEXT[TEXT.index("  deploy-mcp:") :]
MCP_TOKEN = "FLY_API_TOKEN_MCP"


def _run_text(job):
    return "\n".join(step.get("run", "") for step in job["steps"])


def test_every_dispatch_input_is_a_boolean_so_there_is_no_free_text():
    assert {name: spec["type"] for name, spec in INPUTS.items()} == {
        "promote_to_alpha": "boolean",
        "health_gate_drill": "boolean",
        "quiet_override": "boolean",
        "deploy_mcp": "boolean",
    }
    assert INPUTS["deploy_mcp"]["default"] is False


def test_it_runs_only_for_its_own_box_dispatched_from_main():
    cond = " ".join(MCP["if"].split())
    assert "github.event_name == 'workflow_dispatch'" in cond
    assert "inputs.deploy_mcp" in cond
    assert "github.ref == 'refs/heads/main'" in cond
    for other in ("promote_to_alpha", "health_gate_drill", "quiet_override"):
        assert f"!inputs.{other}" in cond
    assert "||" not in cond  # every clause must hold
    assert '[ "${GITHUB_REF}" = "refs/heads/main" ]' in _run_text(MCP)


def test_it_deploys_the_dispatched_main_sha_to_the_mcp_app_and_nothing_else():
    run = _run_text(MCP)
    assert "--app piper-morgan-mcp" in run and "--config fly.mcp.toml" in run
    assert '--build-arg PIPER_GIT_SHA="${GITHUB_SHA}"' in run
    assert "grep -qx 'app = \"piper-morgan-mcp\"' fly.mcp.toml" in run
    apps = set(re.findall(r"--app (\S+)", run))
    assert apps == {"piper-morgan-mcp"}
    checkout = next(
        s for s in MCP["steps"] if str(s.get("uses", "")).startswith("actions/checkout")
    )
    assert "with" not in checkout  # no ref override: it builds the dispatched commit


def test_the_token_lives_in_the_mcp_environment_and_only_this_job_names_it():
    assert MCP["environment"] == "mcp"
    assert MCP_TOKEN in MCP_TEXT
    before = TEXT[: TEXT.index("  deploy-mcp:")]
    code_lines = [line for line in before.splitlines() if not line.lstrip().startswith("#")]
    assert not any(MCP_TOKEN in line for line in code_lines)
    named = set(re.findall(r"secrets\.([A-Z0-9_]+)", MCP_TEXT))
    assert named == {MCP_TOKEN}
    for name in ("deploy-staging", "promote-alpha"):
        assert MCP_TOKEN not in str(JOBS[name])


def test_it_asks_for_no_more_than_read_access_to_the_repository():
    assert MCP["permissions"] == {"contents": "read"}


def test_flyctl_is_the_pinned_action_the_other_jobs_use():
    pins = set(re.findall(r"superfly/flyctl-actions/setup-flyctl@([0-9a-f]{40})", TEXT))
    assert len(pins) == 1


def test_it_prints_the_sha_and_release_and_never_flyctls_own_output():
    run = _run_text(MCP)
    assert "set -x" not in MCP_TEXT
    deploy = next(s for s in MCP["steps"] if s.get("name") == "Deploy main to piper-morgan-mcp")
    body = deploy["run"]
    assert ">/dev/null 2>&1" in body[body.index("flyctl deploy") : body.index("then")]
    assert "2>/dev/null" in body[body.index("flyctl releases") :]
    assert 'echo "deployed: sha ${GITHUB_SHA}"' in body
    assert '*[!0-9]*) echo "release: not read"' in body  # digits only reach the log
    echoes = re.findall(r'echo "([^"]*)"', run)
    for line in echoes:
        for word in ("TOKEN", "FLY_API", "email"):
            assert word not in line.replace("FLY_API_TOKEN_MCP is not set", ""), line


def test_an_unset_token_skips_with_a_notice_and_does_not_fail():
    gate = next(s for s in MCP["steps"] if s.get("id") == "mcp_gate")
    assert "present=false" in gate["run"] and "::notice title=MCP deploy skipped::" in gate["run"]
    assert "exit 1" not in gate["run"]
    later = MCP["steps"][MCP["steps"].index(gate) + 1 :]
    assert later and all(s.get("if") == "steps.mcp_gate.outputs.present == 'true'" for s in later)


def test_it_checks_the_running_app_reports_the_sha():
    verify = MCP["steps"][-1]
    assert "https://mcp.pipermorgan.ai/health" in verify["run"]
    assert '[ "$got" = "$GITHUB_SHA" ]' in verify["run"]
    assert "[0-9a-f]{40}" in verify["run"]  # only a sha-shaped value is echoed from the reply


def test_it_has_its_own_concurrency_group_and_leaves_the_others_as_they_were():
    group = DOC["concurrency"]["group"]
    assert group == (
        "fly-deploy-${{ github.event_name == 'push' && 'staging' || "
        "(inputs.promote_to_alpha && 'alpha' || (inputs.deploy_mcp && 'mcp' || 'drill')) }}"
    )
    assert DOC["concurrency"]["cancel-in-progress"] is False


def test_the_other_jobs_conditions_are_untouched():
    assert JOBS["deploy-staging"]["if"] == (
        "github.event_name == 'push' || "
        "(github.event_name == 'workflow_dispatch' && inputs.health_gate_drill)"
    )
    assert JOBS["promote-alpha"]["if"] == (
        "github.event_name == 'workflow_dispatch' && inputs.promote_to_alpha"
    )
    assert JOBS["promote-alpha"]["environment"] == "alpha"
