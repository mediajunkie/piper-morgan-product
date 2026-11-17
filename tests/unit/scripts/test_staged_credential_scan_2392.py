"""staged_credential_scan.py (issue 2392, ADR-084 D2): each shape is refused at commit and in
the gate, the report and the baseline never carry a value, and a masked form passes.

Every made-up value here is built at run time from parts, so this file holds no matching run.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
BODY = "Zq7Rk2Wm9Xc4Vb6Nh8Jt3Lp5Gd1Fs0Ya"  # 32 characters, mixed case and digits


def _load():
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "staged_credential_scan", ROOT / "scripts" / "staged_credential_scan.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FAKES = {
    "Anthropic key": "sk-" + "ant-" + "api03-" + BODY,
    "OpenAI-style key": "sk-" + "proj-" + BODY,
    "Google key": "AI" + "za" + BODY + "Qw9",
    "GitHub token": "gh" + "p_" + BODY,
    "GitHub token (app)": "gh" + "s_" + BODY,
    "GitHub token (fine-grained)": "github" + "_pat_" + BODY,
    "Fly token": "fo" + "1_" + BODY,
    "Fly token (scheme)": "Fly" + "V1 " + "fm2_" + BODY,
    "Fly token (bare)": "fm" + "2_" + BODY,
}


@pytest.mark.parametrize("label", sorted(FAKES))
def test_each_shape_is_found_and_named(label):
    mod = _load()
    found = mod.find(f'KEY = "{FAKES[label]}"', "services/x.py")
    assert len(found) >= 1
    assert mod.shape_name(found[0]) == label.split(" (")[0]


@pytest.mark.parametrize(
    "line",
    [
        "the key is sk-a…Ya12 and the invite is ABCD…WXYZ",
        "the key is sk-a...Ya12",
        'placeholder="gh' + "p_" + "x" * 36 + '"',
        'logger.warning("github' + '_pat_at_rest_clear_failed", error=str(e))',
        "task-2392-staged-credential-scan-notes",
    ],
)
def test_masked_placeholder_and_identifier_forms_pass(line):
    assert _load().find(line, "services/x.py") == []


def test_dashed_invite_shape_counts_only_in_the_bearer_roots():
    mod = _load()
    grouped = "-".join(["7KQ2", "M9XW", "4VBN", "8JT3", "P5GD", "1FS0"])
    assert mod.find(grouped, "services/x.py") == []
    assert mod.find(grouped, "mailboxes/cio/inbox/memo.md") == [grouped]
    assert mod.find(grouped.replace("-", ""), "services/x.py") == [grouped.replace("-", "")]


def test_baseline_key_carries_nothing_from_the_value():
    mod = _load()
    one, two = FAKES["Anthropic key"], FAKES["Anthropic key"][::-1].replace("-", "x") + "9"
    key_one = mod.baseline_key("tests/a.py", f'  KEY = "{one}"', [one])
    key_two = mod.baseline_key("tests/a.py", f'KEY = "{two}"', [two])
    assert key_one == key_two  # same line, different value, same key
    assert key_one.startswith("tests/a.py:") and one[:6] not in key_one


def test_added_lines_reads_only_additions_with_their_numbers():
    mod = _load()
    diff = "\n".join(
        [
            "diff --git a/a.py b/a.py",
            "--- a/a.py",
            "+++ b/a.py",
            "@@ -3,0 +4,2 @@ def f():",
            "+first",
            "+second",
            "@@ -9 +11 @@",
            "-gone",
            "+third",
            "diff --git a/old.md b/new.md",
            "similarity index 100%",
            "rename from old.md",
            "rename to new.md",
        ]
    )
    assert mod.added_lines(diff) == [
        ("a.py", 4, "first"),
        ("a.py", 5, "second"),
        ("a.py", 11, "third"),
    ]


def test_an_added_line_starting_with_two_pluses_is_scanned_under_the_right_path():
    """Arch, 2026-11-16: in the diff it reads '+++ ...' and was taken for a file header."""
    mod = _load()
    value = FAKES["Anthropic key"]
    diff = "\n".join(
        [
            "diff --git a/dev/log.md b/dev/log.md",
            "--- a/dev/log.md",
            "+++ b/dev/log.md",
            "@@ -1,0 +2,4 @@",
            "+before",
            "+++ " + value,
            "+-- not a header either",
            "+after",
        ]
    )
    rows = mod.added_lines(diff)
    assert rows == [
        ("dev/log.md", 2, "before"),
        ("dev/log.md", 3, "++ " + value),
        ("dev/log.md", 4, "-- not a header either"),
        ("dev/log.md", 5, "after"),
    ]
    hits = mod.hits_in("dev/log.md", [(n, text) for _, n, text in rows])
    assert [(h[0], h[1], h[2]) for h in hits] == [("dev/log.md", 3, "Anthropic key")]


@pytest.fixture
def repo(tmp_path, monkeypatch):
    for name in [n for n in os.environ if n.startswith("GIT_")]:
        monkeypatch.delenv(name)
    mod = _load()
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    def git(*args):
        subprocess.run(
            [
                "git",
                "-C",
                str(tmp_path),
                "-c",
                "user.name=t",
                "-c",
                "user.email=t@example.invalid",
                *args,
            ],
            check=True,
            capture_output=True,
        )

    git("init", "-q")
    (tmp_path / "services").mkdir()
    (tmp_path / "services" / "old.py").write_text(f'OLD = "{FAKES["GitHub token"]}"\n')
    (tmp_path / "README.md").write_text("hello\n")
    git("add", ".")
    git("commit", "-q", "-m", "first")
    return mod, tmp_path, git


def test_staged_refuses_a_new_line_and_prints_no_value(repo, capsys):
    mod, root, git = repo
    value = FAKES["Anthropic key"]
    (root / "services" / "new.py").write_text(f'import os\n\nKEY = "{value}"\n')
    git("add", "services/new.py")
    assert mod.main(["--staged"]) == 1
    out = capsys.readouterr()
    text = out.out + out.err
    assert "services/new.py:3  Anthropic key" in text
    assert value not in text and value[:10] not in text and value[-6:] not in text


def test_staged_passes_a_clean_change_and_a_move(repo, capsys):
    mod, root, git = repo
    (root / "README.md").write_text("hello\nthe key is sk-a…Ya12\n")
    git("mv", "services/old.py", "services/moved.py")
    git("add", "README.md")
    assert mod.main(["--staged"]) == 0
    assert "OK" in capsys.readouterr().out


def test_staged_honours_a_baselined_line_that_is_added_again(repo, tmp_path):
    mod, root, git = repo
    baseline = root / "baseline.txt"
    assert mod.main(["--tracked", "--write-baseline", str(baseline)]) == 0
    (root / "services" / "old.py").write_text(f'# note\n    OLD = "{FAKES["GitHub token"]}"\n')
    git("add", "services/old.py")
    assert mod.main(["--staged"]) == 1
    assert mod.main(["--staged", "--baseline", str(baseline)]) == 0


def test_tracked_ratchets_against_a_baseline_that_holds_no_value(repo, capsys):
    mod, root, git = repo
    baseline = root / "baseline.txt"
    assert mod.main(["--tracked"]) == 1
    assert mod.main(["--tracked", "--write-baseline", str(baseline)]) == 0
    listed = baseline.read_text()
    assert listed.startswith("services/old.py:") and len(listed.splitlines()) == 1
    assert FAKES["GitHub token"][:8] not in listed and BODY[:8] not in listed
    assert mod.main(["--tracked", "--baseline", str(baseline)]) == 0
    (root / "tests").mkdir()
    (root / "tests" / "t.py").write_text(f'K = "{FAKES["Fly token"]}"\n')
    (root / "mailboxes").mkdir()
    (root / "mailboxes" / "memo.md").write_text(f'{FAKES["Google key"]}\n')
    git("add", ".")
    git("commit", "-q", "-m", "second")
    capsys.readouterr()
    assert mod.main(["--tracked", "--baseline", str(baseline)]) == 1
    out = capsys.readouterr().err
    assert "tests/t.py:1  Fly token" in out
    assert "mailboxes/memo.md" not in out  # the bearer lint's root, not this scan's
    assert BODY not in out


def test_staged_refuses_a_double_plus_line_end_to_end(repo, capsys):
    mod, root, git = repo
    (root / "README.md").write_text("hello\n++ " + FAKES["GitHub token (app)"] + "\nbye\n")
    git("add", "README.md")
    assert mod.main(["--staged"]) == 1
    assert "README.md:2  GitHub token" in capsys.readouterr().err


@pytest.mark.parametrize("label", ["GitHub token (app)", "Fly token (bare)"])
def test_tracked_reads_the_bearer_roots_for_the_shapes_the_bearer_lint_lacks(repo, capsys, label):
    """Arch, 2026-11-16: an app token in a session log was read by neither check."""
    mod, root, git = repo
    sys.path.insert(0, str(ROOT / "scripts"))
    import mailbox_bearer_lint as bearer

    assert (
        bearer.scan_line(FAKES[label]) == []
    )  # the gap: delete this test's reason if that changes
    (root / "dev").mkdir()
    (root / "dev" / "log.md").write_text("ran it\ntoken " + FAKES[label] + "\n")
    (root / "docs").mkdir()
    (root / "docs" / "page.md").write_text(
        FAKES["Google key"] + "\n"
    )  # the bearer lint's own shape
    git("add", ".")
    git("commit", "-q", "-m", "log")
    baseline = root / "b.txt"
    baseline.write_text(mod.baseline_key("services/old.py", 'OLD = "x"', []) + "\n")
    mod.main(["--tracked"])
    err = capsys.readouterr().err
    assert "dev/log.md:2  " + label.split(" (")[0] in err
    assert "docs/page.md" not in err


def test_unreadable_git_is_exit_3_not_a_pass(tmp_path, monkeypatch, capsys):
    mod = _load()
    monkeypatch.setattr(mod, "ROOT", tmp_path / "not-a-repo")
    assert mod.main(["--staged"]) == 3
    assert "nothing was checked" in capsys.readouterr().err


def test_the_repo_is_clean_against_its_own_baseline():
    """The gate as lint.yml runs it. Also proves this file and the script hold no shape."""
    mod = _load()
    assert (
        mod.main(["--tracked", "--baseline", str(ROOT / ".staged-credential-scan-baseline.txt")])
        == 0
    )
    for path in (
        "tests/unit/scripts/test_staged_credential_scan_2392.py",
        "scripts/staged_credential_scan.py",
    ):
        lines = enumerate((ROOT / path).read_text().splitlines(), 1)
        assert mod.hits_in(path, lines) == []


def test_the_baseline_file_holds_only_path_and_hash():
    import re

    for line in (ROOT / ".staged-credential-scan-baseline.txt").read_text().splitlines():
        assert re.fullmatch(r"[A-Za-z0-9_./-]+:[0-9a-f]{12}", line), "a baseline line is path:hash"


def test_the_commit_hook_and_the_workflow_call_the_scan():
    hook = (ROOT / "scripts" / "git-hooks" / "pre-commit").read_text()
    assert "staged_credential_scan.py" in hook and "--staged" in hook
    workflow = (ROOT / ".github" / "workflows" / "lint.yml").read_text()
    assert "python scripts/staged_credential_scan.py --tracked --baseline" in workflow
