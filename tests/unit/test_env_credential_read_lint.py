"""#1551 workstream 5: the env credential-read lint (Arch's design 2026-11-04 15:54).

A read of a credential- or identity-shaped name through ``os.environ`` / ``os.getenv`` /
the config helpers is a site that must be ruled system-only or per-account; the lint
baselines today's sites and fails CI on a new one. These pins hold the detector's shape:
the constant-resolved read that a literal regex misses (``PIPER_DEFAULT_REPO`` on 11-04),
whole-segment name matching (``KEYCHAIN`` is not ``KEY``), the helper call, and the ratchet.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from scripts.env_credential_read_lint import (
    CREDENTIAL_WORDS,
    find_credential_env_reads,
    new_against_baseline,
)

ROOT = Path(__file__).resolve().parents[2]


def _names(src: str) -> list[str]:
    return [v.env_name for v in find_credential_env_reads(src)]


class TestDetector:
    def test_literal_reads_in_every_form(self):
        src = (
            "import os\nfrom os import environ, getenv\n"
            "a = os.environ['GITHUB_TOKEN']\n"
            "b = os.environ.get('PIPER_GITHUB_HANDLE')\n"
            "c = os.getenv('NOTION_API_KEY', '')\n"
            "d = environ.get('SLACK_BOT_TOKEN')\n"
            "e = getenv('GOOGLE_CLIENT_SECRET')\n"
        )
        assert _names(src) == [
            "GITHUB_TOKEN",
            "PIPER_GITHUB_HANDLE",
            "NOTION_API_KEY",
            "SLACK_BOT_TOKEN",
            "GOOGLE_CLIENT_SECRET",
        ]

    def test_a_read_through_a_module_constant_is_a_site(self):
        """The 11-04 shape: ``ENV_DEFAULT_REPO = "PIPER_DEFAULT_REPO"`` then a read by name."""
        src = (
            "import os\nENV_DEFAULT_REPO = 'PIPER_DEFAULT_REPO'\n"
            "def f(user_id):\n    return os.environ.get(ENV_DEFAULT_REPO) if user_id is None else None\n"
        )
        assert _names(src) == ["PIPER_DEFAULT_REPO"]

    def test_names_match_on_whole_segments(self):
        src = (
            "import os\n"
            "t = os.getenv('PIPER_KEYCHAIN_TIMEOUT_SECONDS')\n"  # KEYCHAIN is not KEY
            "u = os.getenv('GITHUB_ALLOWED_REPOS')\n"  # the plural counts
            "v = os.getenv('PIPER_BASE_URL')\n"  # not a credential or identity
        )
        assert _names(src) == ["GITHUB_ALLOWED_REPOS"]

    def test_a_helper_call_is_a_site(self):
        src = "def f(svc):\n    return svc.get_environment(user_id)\n"
        assert _names(src) == ["helper:get_environment"]

    def test_get_authentication_token_left_the_helper_set_on_arch_s_word(self):
        """2026-11-04 19:11: its own env loop is a visible site ruled under the #1461 pin."""
        src = "def f(svc):\n    return svc.get_authentication_token(user_id)\n"
        assert _names(src) == []

    def test_non_env_gets_and_dict_reads_are_not_sites(self):
        src = (
            "def f(ctx, d):\n"
            "    a = ctx.get('GITHUB_TOKEN')\n"  # not the environment
            "    b = d['API_KEY']\n"
            "    return a, b\n"
        )
        assert _names(src) == []

    def test_syntax_error_file_yields_no_violations(self):
        assert find_credential_env_reads("def (:\n") == []

    def test_the_word_list_is_the_ruled_one(self):
        for w in ("TOKEN", "KEY", "SECRET", "HANDLE", "LOGIN", "REPO", "OWNER", "EMAIL"):
            assert w in CREDENTIAL_WORDS


class TestRatchet:
    def test_new_sites_are_the_multiset_difference(self):
        base = Counter({"a|X|r": 1, "b|Y|r": 2})
        cur = Counter({"a|X|r": 1, "b|Y|r": 3, "c|Z|r": 1})
        assert new_against_baseline(cur, base) == Counter({"b|Y|r": 1, "c|Z|r": 1})

    def test_removed_sites_do_not_fail(self):
        base = Counter({"a|X|r": 2})
        assert new_against_baseline(Counter({"a|X|r": 1}), base) == Counter()


class TestImportedConstants:
    def test_a_constant_imported_from_another_module_resolves(self, tmp_path, monkeypatch):
        """Arch 2026-11-04 16:38: ``from pkg.names import ENV_TOKEN`` then a read by name."""
        pkg = tmp_path / "pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "names.py").write_text('ENV_TOKEN = "PIPER_GITHUB_TOKEN"\nOTHER = 3\n')
        reader = (
            "import os\nfrom pkg.names import ENV_TOKEN, OTHER\n"
            "def f():\n    return os.environ.get(ENV_TOKEN)\n"
        )
        monkeypatch.chdir(tmp_path)
        assert _names(reader) == ["PIPER_GITHUB_TOKEN"]

    def test_an_aliased_import_resolves_under_its_alias(self, tmp_path, monkeypatch):
        pkg = tmp_path / "pkg"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "names.py").write_text('HANDLE_VAR = "PIPER_GITHUB_HANDLE"\n')
        reader = "import os\nfrom pkg.names import HANDLE_VAR as H\nx = os.getenv(H)\n"
        monkeypatch.chdir(tmp_path)
        assert _names(reader) == ["PIPER_GITHUB_HANDLE"]

    def test_an_unresolvable_import_is_a_site_named_unresolved(self, tmp_path, monkeypatch):
        """Arch 18:34: fail closed; a name the lint cannot resolve is still a site."""
        reader = "import os\nfrom nowhere.names import X\nx = os.getenv(X)\n"
        monkeypatch.chdir(tmp_path)
        assert _names(reader) == ["unresolved"]


class TestUnresolvedReadsAndTheRulingKey:
    def test_a_read_through_a_variable_is_a_site_named_unresolved(self):
        """Arch 2026-11-04 18:34: the GITHUB_TOKEN loop shape."""
        src = (
            "import os\n"
            "def f(env):\n"
            "    for env_var in ('GITHUB_TOKEN', f'GITHUB_TOKEN_{env}'):\n"
            "        t = os.getenv(env_var)\n"
            "    return os.environ.get(provider_key())\n"
        )
        assert _names(src) == ["unresolved", "unresolved"]

    def test_system_only_is_keyed_on_path_and_name(self, tmp_path, monkeypatch):
        from scripts import env_credential_read_lint as lint

        f = tmp_path / "svc.py"
        f.write_text("import os\na = os.getenv('JWT_SECRET_KEY')\nb = os.getenv('GITHUB_TOKEN')\n")
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(
            lint, "SYSTEM_ONLY", {("svc.py", "JWT_SECRET_KEY"): "the deployment's key"}
        )
        found = [v.env_name for _, v in lint.lint_paths([Path("svc.py")])]
        assert found == ["GITHUB_TOKEN"]  # the ruled name is exempt; the other still fails

    def test_every_system_only_entry_carries_a_reason_and_names_a_real_file(self):
        from scripts import env_credential_read_lint as lint

        for (path, name), reason in lint.SYSTEM_ONLY.items():
            assert reason.strip(), (path, name)
            assert (ROOT / path).is_file(), path


class TestOnlyTheIssueGatedFamiliesRemainBaselined:
    """Arch 2026-11-04 19:11: after the 17 unresolved sites are ruled and the two MCP key
    mappings removed, the baseline holds only Slack (#1481) and Notion (#2238), behind the
    offer gate. A new file in the baseline is a site nobody has judged yet."""

    ALLOWED_FILES = {
        "services/integrations/slack/config_service.py",
        "services/integrations/slack/socket_mode_runner.py",
        "services/integrations/notion/config_service.py",
        "services/integrations/integration_status_service.py",  # its Slack and Notion legs
        "web/api/routes/settings_integrations.py",  # its Slack app-token save
    }

    def test_baseline_files_are_the_two_families(self):
        lines = (ROOT / ".credential-env-read-baseline.txt").read_text().splitlines()
        files = {ln.split("|", 1)[0] for ln in lines if ln.strip()}
        assert files <= self.ALLOWED_FILES, sorted(files - self.ALLOWED_FILES)

    def test_baseline_names_are_slack_or_notion_shaped(self):
        lines = (ROOT / ".credential-env-read-baseline.txt").read_text().splitlines()
        names = {ln.split("|")[1] for ln in lines if ln.strip()}
        for n in names:
            assert n.startswith(("SLACK_", "NOTION_")) or n == "helper:get_environment", n


class TestTheUnresolvedExemptionIsCountBound:
    """Arch 2026-11-04 19:45: a ``(path, "unresolved")`` ruling covers the reads it counted,
    not every future one in that file."""

    def test_one_more_unresolved_read_than_ruled_is_a_site(self, tmp_path, monkeypatch):
        from scripts import env_credential_read_lint as lint

        f = tmp_path / "svc.py"
        f.write_text("import os\ndef f(a, b):\n    return os.getenv(a), os.getenv(b)\n")
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(lint, "SYSTEM_ONLY", {("svc.py", "unresolved"): "typed readers"})
        monkeypatch.setattr(lint, "UNRESOLVED_COUNTS", {"svc.py": 1})
        found = [v.env_name for _, v in lint.lint_paths([Path("svc.py")])]
        assert found == ["unresolved"]

    def test_every_unresolved_ruling_has_a_count_and_the_counts_match_today(self):
        from scripts import env_credential_read_lint as lint

        ruled = {p for (p, n) in lint.SYSTEM_ONLY if n == "unresolved"}
        assert ruled == set(lint.UNRESOLVED_COUNTS)
        for path, n in lint.UNRESOLVED_COUNTS.items():
            text = (ROOT / path).read_text()
            seen = sum(
                1 for v in lint.find_credential_env_reads(text) if v.env_name == "unresolved"
            )
            assert (
                seen == n
            ), f"{path}: {seen} unresolved reads, ruled for {n}; lower the count or get a ruling"


def test_no_mcp_configuration_env_mapping_is_credential_shaped():
    """Arch 19:45: the loop over ``_env_mappings`` is ruled as typed flag and number readers;
    a credential-shaped key added there would ride that ruling unseen."""
    from scripts.env_credential_read_lint import _is_credential_name
    from services.infrastructure.config.mcp_configuration import MCPConfigurationService

    keys = list(MCPConfigurationService()._env_mappings)
    assert keys and not [k for k in keys if _is_credential_name(k)]
