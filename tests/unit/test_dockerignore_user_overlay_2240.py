"""#2240: the operator's local overlay (config/PIPER.user.md, gitignored) must never ship in an
image. deploy-mcp.sh's stray-file guard uses --exclude-standard, which skips gitignored files, so
.dockerignore is the backstop for both alpha's image and the MCP app's (same Dockerfile, COPY . .)."""

from __future__ import annotations

import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _patterns() -> list[str]:
    return [
        line.strip()
        for line in (ROOT / ".dockerignore").read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _excluded(path: str) -> bool:
    return any(
        fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path, p.rstrip("/") + "/*") for p in _patterns()
    )


def test_operator_overlay_is_excluded_from_the_build_context():
    assert _excluded("config/PIPER.user.md")


def test_the_tracked_example_and_piper_md_stay_in_the_image():
    assert not _excluded("config/PIPER.user.md.example")
    assert not _excluded("config/PIPER.md")


def test_deploy_mcp_guard_refuses_a_gitignored_overlay():
    script = (ROOT / "scripts" / "deploy-mcp.sh").read_text()
    assert "--ignored --exclude-standard -- config/" in script
    assert "operator overlay in config/" in script


# ---------------------------------------------------------------------------
# #2240 follow-up (PA, 2026-10-30 22:0x): the first guard killed every CLEAN deploy, because
# `grep` exits 1 on no match and the script runs under `set -euo pipefail`; the pin above only
# read the script's text, so it passed. This pin RUNS the guard's own pipeline line, lifted
# from the script, under the script's shell options, in a scratch git repo: once clean
# (must exit 0 with an empty result) and once with a dummy overlay (must name it).
# ---------------------------------------------------------------------------
import os
import re
import subprocess
import tempfile


def _guard_line() -> str:
    script = (ROOT / "scripts" / "deploy-mcp.sh").read_text()
    m = re.search(r'^overlay="\$\(.*\)"$', script, re.M)
    assert m, "deploy-mcp.sh no longer has the overlay guard line"
    return m.group(0)


def _run_guard(with_overlay: bool) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
        }
        subprocess.run(["git", "init", "-q", tmp], check=True, env=env)
        os.makedirs(os.path.join(tmp, "config"))
        with open(os.path.join(tmp, ".gitignore"), "w") as f:
            f.write("*.user.md\n")
        with open(os.path.join(tmp, "config", "PIPER.md"), "w") as f:
            f.write("# tracked\n")
        subprocess.run(["git", "-C", tmp, "add", "-A"], check=True, env=env)
        subprocess.run(["git", "-C", tmp, "commit", "-q", "-m", "init"], check=True, env=env)
        if with_overlay:
            with open(os.path.join(tmp, "config", "PIPER.user.md"), "w") as f:
                f.write("# operator overlay\n")
        snippet = "set -euo pipefail\n" + _guard_line() + '\nprintf "%s" "$overlay"\n'
        return subprocess.run(
            ["bash", "-c", snippet], cwd=tmp, capture_output=True, text=True, env=env
        )


def test_guard_pipeline_passes_a_clean_tree_under_pipefail():
    done = _run_guard(with_overlay=False)
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == ""


def test_guard_pipeline_names_an_overlay_under_pipefail():
    done = _run_guard(with_overlay=True)
    assert done.returncode == 0, done.stderr
    assert "config/PIPER.user.md" in done.stdout
