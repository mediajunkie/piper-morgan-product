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
