"""#2151 (Arch 10-24 09:09): two routes with no caller made a read claim
(``connected: false`` / "nothing set up") on a failure, and ``/setup/status`` handed
instance-wide facts to anyone, ungated. Both are retired, not EXEMPT; these pins keep
them retired and uncalled."""

import subprocess
from pathlib import Path

import pytest

RETIRED = ("/api/v1/settings/integrations/status", "/api/v1/setup/status")
ROOT = Path(__file__).resolve().parents[5]


@pytest.mark.parametrize("path", RETIRED)
def test_the_route_is_not_mounted(path):
    from web.app import app

    mounted = {getattr(r, "path", None) for r in app.routes}
    assert path not in mounted


@pytest.mark.parametrize("path", RETIRED)
def test_no_front_end_calls_the_path(path):
    out = subprocess.run(
        ["git", "grep", "-l", "-F", path, "--", "templates", "web/static", "web/templates"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == "", out.stdout
