"""Tests for scripts/regenerate-mailbox-manifests.py (#1106 derive mechanism).

Covers the #1106 acceptance criteria:
- frontmatter `subject:` populates the Summary column
- fallback to the file's first H1 when frontmatter subject is absent
- `(no subject)` only when both are absent — and warned to stderr, not silent
- curated-prose preservation via the `<!-- curated -->` marker (the register-
  separation design: derived table above, recipient-curated tail below)
- whole-state regen reflects inbox/ → read/ moves consistently
- idempotency (second regen of unchanged state is a no-op)
"""

import importlib.util
import sys
from pathlib import Path

import pytest

# The script has a dash-separated filename, so import it via spec.
_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "regenerate-mailbox-manifests.py"
_spec = importlib.util.spec_from_file_location("regen_manifests", _SCRIPT)
regen = importlib.util.module_from_spec(_spec)
sys.modules["regen_manifests"] = regen  # dataclass decorator needs the module registered
_spec.loader.exec_module(regen)


def _write_memo(directory: Path, name: str, frontmatter: dict | None, body: str = ""):
    directory.mkdir(parents=True, exist_ok=True)
    parts = []
    if frontmatter is not None:
        parts.append("---")
        for k, v in frontmatter.items():
            parts.append(f"{k}: {v}")
        parts.append("---")
        parts.append("")
    parts.append(body)
    (directory / name).write_text("\n".join(parts), encoding="utf-8")


@pytest.fixture
def mailbox(tmp_path, monkeypatch):
    """Point the module at a temp mailboxes root with one role."""
    root = tmp_path / "mailboxes"
    monkeypatch.setattr(regen, "MAILBOXES_ROOT", root)
    return root


class TestSummaryExtraction:
    def test_subject_frontmatter_wins(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-pa-to-cio-test-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "The subject line"},
            "# A different H1\n\nbody",
        )
        entries = regen.collect_memos(inbox)
        assert len(entries) == 1
        assert entries[0].summary == "The subject line"

    def test_h1_fallback_when_no_subject(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-pa-to-cio-noheader-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12"},
            "# Fallback heading as summary\n\nbody",
        )
        entries = regen.collect_memos(inbox)
        assert entries[0].summary == "Fallback heading as summary"

    def test_h1_fallback_without_frontmatter(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-legacy-2026-06-12.md",
            None,
            "# Legacy memo heading\n\nbody",
        )
        entries = regen.collect_memos(inbox)
        assert entries[0].summary == "Legacy memo heading"

    def test_no_subject_is_warned_not_silent(self, mailbox, capsys):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-bare-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12"},
            "no heading anywhere, just prose",
        )
        entries = regen.collect_memos(inbox)
        assert entries[0].summary == "(no subject)"
        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "memo-bare-2026-06-12.md" in captured.err

    def test_long_subject_truncated(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        long_subject = "x" * 200
        _write_memo(
            inbox,
            "memo-long-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": long_subject},
        )
        entries = regen.collect_memos(inbox)
        assert len(entries[0].summary) <= regen.SUMMARY_TRUNCATE
        assert entries[0].summary.endswith("…")


class TestCuratedTailPreservation:
    def test_curated_tail_survives_regen(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-pa-to-cio-one-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "One"},
        )
        # Seed a MANIFEST with a curated tail.
        regen.regenerate_for_role("cio", quiet=True)
        manifest = inbox / "MANIFEST.md"
        content = manifest.read_text(encoding="utf-8")
        curated = (
            f"{regen.CURATED_MARKER}\n\n"
            "## Open carrying\n"
            "- Ship #047 thread: PM-decision queue\n"
        )
        manifest.write_text(content + curated, encoding="utf-8")

        # New mail arrives; regen again.
        _write_memo(
            inbox,
            "memo-pa-to-cio-two-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "Two"},
        )
        regen.regenerate_for_role("cio", quiet=True)
        new_content = manifest.read_text(encoding="utf-8")
        # Derived register updated...
        assert "Two" in new_content
        # ...curated register preserved verbatim.
        assert regen.CURATED_MARKER in new_content
        assert "## Open carrying" in new_content
        assert "Ship #047 thread: PM-decision queue" in new_content

    def test_no_marker_no_tail(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-pa-to-cio-one-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "One"},
        )
        regen.regenerate_for_role("cio", quiet=True)
        content = (inbox / "MANIFEST.md").read_text(encoding="utf-8")
        assert regen.CURATED_MARKER not in content

    def test_extract_curated_tail_unit(self):
        content = (
            "# Inbox Manifest — cio\n\n| a | b |\n\n"
            f"{regen.CURATED_MARKER}\nkeep me\n"
        )
        tail = regen.extract_curated_tail(content)
        assert tail.startswith(regen.CURATED_MARKER)
        assert "keep me" in tail
        assert regen.extract_curated_tail("no marker here") == ""
        assert regen.extract_curated_tail("") == ""


class TestMoveConsistency:
    def test_inbox_to_read_move_reflected_in_both(self, mailbox):
        role = mailbox / "cio"
        inbox, read = role / "inbox", role / "read"
        _write_memo(
            inbox,
            "memo-pa-to-cio-moving-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "Will move"},
        )
        read.mkdir(parents=True, exist_ok=True)
        regen.regenerate_for_role("cio", quiet=True)
        assert "Will move" in (inbox / "MANIFEST.md").read_text(encoding="utf-8")

        # Move the memo inbox -> read (the triage gesture), regen again.
        (inbox / "memo-pa-to-cio-moving-2026-06-12.md").rename(
            read / "memo-pa-to-cio-moving-2026-06-12.md"
        )
        regen.regenerate_for_role("cio", quiet=True)
        inbox_content = (inbox / "MANIFEST.md").read_text(encoding="utf-8")
        read_content = (read / "MANIFEST.md").read_text(encoding="utf-8")
        assert "Will move" not in inbox_content
        assert "_(empty)_" in inbox_content
        assert "Will move" in read_content


class TestIdempotency:
    def test_second_regen_is_noop(self, mailbox):
        inbox = mailbox / "cio" / "inbox"
        _write_memo(
            inbox,
            "memo-pa-to-cio-one-2026-06-12.md",
            {"from": "PA", "date": "2026-06-12", "subject": "One"},
        )
        first = regen.regenerate_for_role("cio", quiet=True)
        assert first == 1  # wrote the manifest
        second = regen.regenerate_for_role("cio", quiet=True)
        assert second == 0  # unchanged -> no write
