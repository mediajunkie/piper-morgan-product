"""Pins scripts/key_in_docs_lint.py: what counts as a secret on a command line in a reader-facing page."""

import importlib.util
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "key_in_docs_lint", Path(__file__).resolve().parents[3] / "scripts" / "key_in_docs_lint.py"
)
lint = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(lint)


@pytest.mark.parametrize(
    "line",
    [
        'export OPENAI_API_KEY="sk-..."',
        "export ANTHROPIC_API_KEY=sk-ant-real",
        "   export SLACK_BOT_TOKEN='xoxb-your-bot-token'",
        "export SLACK_SIGNING_SECRET=your_secret_here",
        "export DB_PASSWORD=hunter2  # comment",
        "security add-generic-password -s piper-morgan -a notion_api_key -w 'YOUR_TOKEN' -U",
    ],
)
def test_flags_a_secret_on_a_command_line(line):
    assert lint.scan_text("docs/x.md", line)


@pytest.mark.parametrize(
    "line",
    [
        "read -rs NOTION_API_KEY && export NOTION_API_KEY",
        "export NOTION_API_KEY",
        'export ANTHROPIC_API_KEY="$KEY_FROM_PROMPT"',
        "export ANTHROPIC_API_KEY=$(cat /dev/null)",
        "export PIPER_CREDENTIAL_STORE=db",
        "export POSTGRES_PORT=5433",
        "security add-generic-password -s piper -a me -w",
        "python scripts/local_key_setup.py",
    ],
)
def test_allows_prompts_expansions_and_non_secret_names(line):
    assert lint.scan_text("docs/x.md", line) == []


def test_internal_records_are_not_scanned():
    for path in (
        "docs/internal/operations/x.md",
        "dev/2026/11/12/log.md",
        "mailboxes/cio/inbox/m.md",
        "docs/archive/old.md",
        "docs/omnibus-logs/2026-11-12.md",
    ):
        assert lint.excluded(path)
    assert not lint.excluded("docs/installation/self-host-guide.md")
    assert not lint.excluded("services/integrations/notion/README.md")


def test_baseline_is_keyed_on_text_not_line_number(tmp_path):
    a = ("docs/x.md", 3, "export A_KEY=v")
    b = ("docs/x.md", 9, "export A_KEY=v")
    assert lint.key(a) == lint.key(b)
    base = tmp_path / "b.txt"
    base.write_text("# header\n" + lint.key(a) + "\n")
    assert lint.read_baseline(base) == {lint.key(a)}
