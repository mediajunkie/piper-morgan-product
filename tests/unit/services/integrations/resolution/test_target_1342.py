"""#1342 Inc 1 — connector-agnostic target-resolution types + the GitHub seam.

Arch ruling 2026-07-01 (decisions.log, ADR-070 family): a SEPARATE resolution service
(not a Connector-protocol method); ``ResolvedTarget = {source, connector, payload}``;
``ResolutionSource`` promoted as-is; ``ResolvedRepo`` = the GitHub payload;
build-GitHub-only (m-40). These pin the envelope + the promotion's back-compat.
"""

import dataclasses
from typing import get_args

from services.integrations.resolution import ResolutionSource, ResolvedTarget


def test_resolved_target_is_a_connector_agnostic_envelope():
    t = ResolvedTarget(source="user_default", connector="github", payload={"x": 1})
    assert t.source == "user_default"
    assert t.connector == "github"
    assert t.payload == {"x": 1}


def test_resolved_target_is_frozen():
    t = ResolvedTarget(source="explicit", connector="calendar", payload=None)
    with __import__("pytest").raises(dataclasses.FrozenInstanceError):
        t.connector = "github"  # type: ignore[misc]


def test_resolution_source_is_the_five_shared_paths():
    assert set(get_args(ResolutionSource)) == {
        "explicit",
        "project",
        "default_project",
        "user_default",
        "env_var",
    }


def test_resolved_repo_to_target_wraps_as_github_payload():
    from services.integrations.github.repo_resolver import ResolvedRepo

    repo = ResolvedRepo(owner="octocat", name="hello-world", source="user_default")
    target = repo.to_target()
    assert isinstance(target, ResolvedTarget)
    assert target.source == "user_default"  # source carries over the vocabulary
    assert target.connector == "github"
    assert target.payload is repo  # the ResolvedRepo IS the GitHub payload
    assert target.payload.full_name == "octocat/hello-world"


def test_resolution_source_still_importable_from_repo_resolver_backcompat():
    # The #1342 promotion must not break existing `from ...repo_resolver import
    # ResolutionSource` callers — it's re-exported there.
    from services.integrations.github.repo_resolver import ResolutionSource as RS

    assert RS is ResolutionSource
