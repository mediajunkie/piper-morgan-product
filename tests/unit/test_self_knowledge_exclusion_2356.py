"""Issue 2356, part 4 of the self-knowledge epic (2349): the exclusion test.

Session logs (``dev/``), agent mail (``mailboxes/``), the omnibus logs and agent memory
are never in a self-knowledge index or manifest, for any tier. They hold working notes,
outside people's details and unratified claims; Piper must never answer from them.

Three things are pinned:

1. Every corpus manifest in the repo (found by name, so a Tier 2 manifest is covered the
   day it lands) has no ``item`` under a never-indexed tree. Every row, whatever its
   status. This reads the CSV itself and does not call the checker, so a fault in the
   checker cannot hide a bad row.
2. The checker (``scripts/validate_tier1_manifest.py``) keeps all of those trees on its
   list and refuses the ways of writing such a path that a plain prefix check misses.
3. No runtime code (``services/``, ``web/``, ``cli/``) names one of those trees in a
   string, so nothing can read them into a prompt without this test changing.

DENOMINATOR: every ``*corpus-manifest*.csv`` under ``docs/`` and ``config/``; every
tracked ``.py`` file under ``services/``, ``web/`` and ``cli/``.
"""

import ast
import csv
import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# The trees no tier may index. ``.claude-pm/`` and ``memory/`` are agent memory.
NEVER_INDEXED = ("dev/", "mailboxes/", "docs/omnibus-logs/", ".claude-pm/", "memory/")


def _manifests():
    found = []
    for folder in ("docs", "config"):
        found += sorted((ROOT / folder).rglob("*corpus-manifest*.csv"))
    return found


def _item_paths(cell):
    """The file paths in an ``item`` cell: ``path``, ``path#heading`` or ``path::symbol``,
    several joined by ``;``."""
    for part in cell.split(";"):
        part = part.strip()
        if part:
            yield part.split("::")[0].split("#", 1)[0].strip()


def _lands_in_a_never_indexed_tree(path):
    raw = path.strip().replace(os.sep, "/")
    if ".." in raw.split("/") or os.path.isabs(raw) or raw.startswith("~"):
        return True
    p = os.path.normpath(raw).replace(os.sep, "/")
    return any(("/" + tree) in ("/" + p + "/") for tree in NEVER_INDEXED)


def _checker():
    script = ROOT / "scripts" / "validate_tier1_manifest.py"
    spec = importlib.util.spec_from_file_location("validate_tier1_manifest_2356", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestNoManifestRowPointsAtWorkingNotes:
    def test_there_is_a_manifest_to_check(self):
        names = [m.relative_to(ROOT).as_posix() for m in _manifests()]
        assert "docs/internal/design/tier1-corpus-manifest.csv" in names

    def test_no_item_in_any_tier_lies_under_a_never_indexed_tree(self):
        offenders, rows_read = [], 0
        for manifest in _manifests():
            with open(manifest, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    rows_read += 1
                    for path in _item_paths(row.get("item") or ""):
                        if _lands_in_a_never_indexed_tree(path):
                            label = manifest.relative_to(ROOT).as_posix()
                            offenders.append(f"{label}: {row.get('id')}: {path}")
        assert rows_read > 0
        assert offenders == []

    def test_every_manifest_has_an_item_column(self):
        # A manifest that names its files in another column would pass the test above
        # by having nothing to read.
        for manifest in _manifests():
            with open(manifest, newline="", encoding="utf-8") as f:
                assert "item" in (csv.DictReader(f).fieldnames or []), manifest.name


class TestTheCheckerKeepsTheRule:
    def test_the_checker_lists_every_never_indexed_tree(self):
        assert set(NEVER_INDEXED) <= set(_checker().EXCLUDED)

    @pytest.mark.parametrize(
        "path, refused",
        [
            ("dev/2026/11/13/x.md", True),
            ("./dev/2026/11/13/x.md", True),
            ("docs/../dev/2026/11/13/x.md", True),
            ("mailboxes/lead/inbox/x.md", True),
            ("docs/omnibus-logs/2026-11-13-omnibus-log.md", True),
            ("docs//omnibus-logs/2026-11-13-omnibus-log.md", True),
            (".claude-pm/projects/x/memory/user.md", True),
            ("memory/user.md", True),
            ("/Users/someone/.claude-pm/memory/user.md", True),
            ("~/.claude-pm/memory/user.md", True),
            ("../piper-morgan-mail/x.md", True),
            # Any ".." is refused, even one that resolves outside the excluded trees
            # (Arch, mail 01M89KB8TK): the old prefix rule refused this one too.
            ("dev/../docs/tier1/how-i-act.md", True),
            ("docs/tier1/../tier1/how-i-act.md", True),
            (" dev/x.md", True),
            ("docs/a/memory/x.md", True),
            ("docs/tier1/how-i-act.md", False),
            ("docs/BETA_KNOWN_ISSUES.md", False),
            ("docs/developer-guide.md", False),  # "dev" inside a name is not the tree
            ("services/intent_service/capability_legibility.py", False),
        ],
    )
    def test_the_checker_refuses_each_way_of_writing_an_excluded_path(self, path, refused):
        assert _checker().under_excluded(path) is refused
        assert _lands_in_a_never_indexed_tree(path) is refused

    def test_a_candidate_row_on_an_excluded_path_is_an_error_too(self, monkeypatch, tmp_path):
        # Status does not matter: the path is refused before any row is indexed.
        checker = _checker()
        monkeypatch.chdir(ROOT)
        with open(checker.PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        col = {name: rows[0].index(name) for name in rows[0]}
        rows[1][col["item"]] = "docs/../mailboxes/lead/inbox/x.md"
        rows[1][col["status"]] = "candidate"
        out = tmp_path / "manifest.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)
        checker.PATH = str(out)
        assert checker.main([]) == 1
        assert checker.main(["--deploy"]) == 1


class TestRuntimeCodeNamesNoNeverIndexedTree:
    # A string that starts with one of these is a path into working notes or memory.
    STARTS = ("dev/", "./dev/", "mailboxes/", "./mailboxes/", "docs/omnibus-logs", ".claude-pm")
    HOLDS = ("/.claude-pm", "/mailboxes/", "/omnibus-logs")

    @classmethod
    def _offenders_in(cls, tree, label):
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value.strip()
                if "\n" in text or " " in text:
                    continue  # prose (a docstring or a sentence), not a path
                if text.startswith(cls.STARTS) or any(h in text for h in cls.HOLDS):
                    found.append(f"{label}:{node.lineno}: {text[:60]}")
        return found

    def test_no_runtime_file_does(self):
        offenders, files = [], 0
        for folder in ("services", "web", "cli"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                files += 1
                offenders += self._offenders_in(
                    ast.parse(path.read_text(encoding="utf-8")),
                    path.relative_to(ROOT).as_posix(),
                )
        assert files > 500
        assert offenders == []

    @pytest.mark.parametrize(
        "source, caught",
        [
            ('p = "dev/2026/11/13/log.md"', True),
            ('p = "mailboxes/lead/inbox"', True),
            ('p = "docs/omnibus-logs/2026-11-13-omnibus-log.md"', True),
            ('p = os.path.expanduser("~/.claude-pm/projects")', True),
            ('p = "docs/tier1/how-i-act.md"', False),
            ('p = "developer"', False),
            ('"""Session logs live under dev/ and are never read here."""', False),
        ],
    )
    def test_the_scan_catches_a_path_and_leaves_prose(self, source, caught):
        assert bool(self._offenders_in(ast.parse(source), "x.py")) is caught
