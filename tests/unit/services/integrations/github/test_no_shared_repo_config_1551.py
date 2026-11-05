"""#1551 (Arch 2026-11-04 18:34, REMOVE not SYSTEM_ONLY): ``GitHubConfigService`` no longer
offers a deployment-wide default repository or repository allowlist. A repository is
per-account (the 13:16 family rule, #2266); the two getters fed only the debugging
summary and had no live consumer, so they went under delete-module-safely rather than
being ruled system-only."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def test_the_shared_repository_getters_are_gone():
    from services.integrations.github.config_service import GitHubConfigService

    for name in ("get_default_repository", "get_allowed_repositories", "is_repository_allowed"):
        assert not hasattr(GitHubConfigService, name), name


def test_the_env_names_are_not_read_anywhere_in_services_or_web():
    import subprocess

    out = subprocess.run(
        [
            "git",
            "grep",
            "-n",
            "-E",
            "GITHUB_ALLOWED_REPOS|GITHUB_REPO_(PRODUCTION|STAGING|DEVELOPMENT|TEST)",
            "--",
            "services/",
            "web/",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == "", out.stdout


def test_the_summary_names_no_shared_repository():
    src = (ROOT / "services/integrations/github/config_service.py").read_text()
    assert '"default_repository"' not in src and '"allowed_repositories_count"' not in src
