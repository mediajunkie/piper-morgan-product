"""#1835 — every compose service that BUILDS points at a Dockerfile that exists.

`docker-compose.yml` carried an `orchestration` service building from
`services/orchestration/Dockerfile` months after that directory was deleted;
a bare `docker compose up -d` failed on every current tree, unnoticed because
every habitual invocation names its services. This pins the shape so the
next deleted module can't leave a dead build context behind.

LAYER (m-43): static — the compose files are parsed as YAML and the build
paths checked on disk; no docker daemon involved, so this runs in CI and
proves "the file is consistent with the tree", not "the stack comes up".
DENOMINATOR: every `docker-compose*.yml` at the repo root, every service
with a `build:` key.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILES = sorted(REPO_ROOT.glob("docker-compose*.yml"))

# Known-dead build contexts, pinned so they cannot grow and cannot outlive their
# referents. `docker-compose.staging.yml` is the 2025-07 compose-era staging
# stack the deployment-pipeline plan (v0.1, 2026-09-20) already records as
# "present but nothing can run it"; staging is a Fly app as of 2026-09-23.
# Disposal of the file is a Rule-0 item (Arch), not this test's call.
KNOWN_DEAD = {
    ("docker-compose.staging.yml", "api-staging"),
    ("docker-compose.staging.yml", "web-staging"),
}


def _build_targets(compose: Path) -> list[tuple[str, Path]]:
    services = (yaml.safe_load(compose.read_text()) or {}).get("services", {}) or {}
    out = []
    for name, spec in services.items():
        build = (spec or {}).get("build")
        if build is None:
            continue
        if isinstance(build, str):
            context, dockerfile = build, "Dockerfile"
        else:
            context = build.get("context", ".")
            dockerfile = build.get("dockerfile", "Dockerfile")
        out.append((name, (compose.parent / context / dockerfile).resolve()))
    return out


@pytest.mark.smoke
@pytest.mark.parametrize("compose", COMPOSE_FILES, ids=[c.name for c in COMPOSE_FILES])
def test_every_build_context_has_its_dockerfile(compose: Path):
    targets = _build_targets(compose)
    assert targets, f"{compose.name}: no build services found — denominator would be empty"
    missing = {name: str(df.relative_to(REPO_ROOT)) for name, df in targets if not df.is_file()}
    known = {svc for f, svc in KNOWN_DEAD if f == compose.name}
    new = {n: p for n, p in missing.items() if n not in known}
    assert not new, (
        f"{compose.name}: service(s) build from a Dockerfile that does not exist: {new} — "
        "delete the dead service block or restore the file; a bare `docker compose up` fails on it."
    )
    stale = known - set(missing)
    assert not stale, (
        f"{compose.name}: KNOWN_DEAD row(s) {sorted(stale)} are no longer dead — remove them; "
        "the list must never outlive its referents."
    )
