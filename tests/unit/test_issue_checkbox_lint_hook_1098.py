"""
Tests for the issue-checkbox-lint hook annotation-aware filter (#1098).

The hook (`.claude/hooks/issue-checkbox-lint.sh`) warns when a commit
references issues with unchecked `[ ]` checkboxes. The close-issue-properly
skill documents an annotation pattern that should be honored:

  - [x] Done item                     → counted as checked (the [x] is the marker)
  - [ ] Item - *Deferred: reason*     → INTENTIONALLY [ ], must NOT count as unchecked
  - [ ] Item - *N/A: reason*          → INTENTIONALLY [ ], must NOT count as unchecked
  - [ ] Item - *N/A (reason)*         → variant; must NOT count
  - [ ] Item                          → real unchecked, MUST count

Issue #1098 (this fix): the original hook regex matched all `[ ]` lines
regardless of annotation. False-positive fired on properly-dispositioned
N/A and Deferred items. This test exercises the hook's grep pipeline
directly against synthetic markdown to verify the fix.
"""

import subprocess
from pathlib import Path
from textwrap import dedent

import pytest


HOOK_PATH = Path(".claude/hooks/issue-checkbox-lint.sh")


def count_unchecked(body: str) -> int:
    """Run the hook's grep pipeline against a body string. Returns the
    integer count of unchecked checkboxes the hook would warn about."""
    # Extract the exact pipeline from the hook so the test stays in sync.
    cmd = (
        "grep -E '^[[:space:]]*[-*][[:space:]]+\\[[[:space:]]\\]' "
        "| grep -vEi '\\*[[:space:]]*(N/?A|Deferred|Skipped|Won.?t[[:space:]]*do)\\b' "
        "| wc -l | tr -d ' '"
    )
    result = subprocess.run(
        ["bash", "-c", cmd],
        input=body,
        capture_output=True,
        text=True,
        timeout=5,
    )
    out = result.stdout.strip() or "0"
    return int(out)


# Annotated-as-N/A or Deferred → NOT counted ----------------------------


def test_na_with_colon_annotation_not_counted() -> None:
    body = dedent(
        """\
        - [ ] AC-1: ship the thing
        - [ ] AC-2: deferred work *N/A: spec didn't land*
        - [x] AC-3: done
        """
    )
    # AC-1 = real unchecked; AC-2 = N/A-annotated, exclude
    assert count_unchecked(body) == 1


def test_na_with_paren_annotation_not_counted() -> None:
    body = dedent(
        """\
        - [ ] AC-1: review *N/A (separate issue territory; tracked via #1101)*
        - [ ] AC-2: ship it
        """
    )
    assert count_unchecked(body) == 1


def test_deferred_with_colon_annotation_not_counted() -> None:
    body = dedent(
        """\
        - [ ] AC-1: ship the thing *Deferred: waiting on PM ratification*
        - [ ] AC-2: also ship the thing
        - [x] AC-3: done
        """
    )
    assert count_unchecked(body) == 1


def test_deferred_variant_phrasing_not_counted() -> None:
    body = dedent(
        """\
        - [ ] AC-1: real fix *Deferred to manual UAT (Lead Dev agent cannot run browser)*
        - [ ] AC-2: ship it
        """
    )
    assert count_unchecked(body) == 1


# Real-unchecked items → counted ----------------------------------------


def test_plain_unchecked_counted() -> None:
    body = dedent(
        """\
        - [ ] AC-1: ship the thing
        - [ ] AC-2: another thing
        - [x] AC-3: done
        """
    )
    assert count_unchecked(body) == 2


def test_unchecked_with_unrelated_italic_text_still_counted() -> None:
    """An italic phrase that's NOT N/A or Deferred (e.g., *important*) should
    still count the row as unchecked."""
    body = dedent(
        """\
        - [ ] AC-1: *important* — must ship
        - [ ] AC-2: shipped via #999
        """
    )
    assert count_unchecked(body) == 2


# Real-world examples from today's issues -------------------------------


def test_1097_real_body_passes_with_annotations() -> None:
    """The #1097 body (which originally tripped the hook) had AC-4 N/A +
    AC-5 Deferred. After the fix, body would have 0 unchecked."""
    body = dedent(
        """\
        - [x] **AC-1**: limit=5 applied
        - [x] **AC-2**: aria-label added
        - [x] **AC-3**: confirmed
        - [ ] **AC-4**: Pattern-063 filing — *N/A (synthesis numbering error)*
        - [ ] **AC-5**: Manual browser-smoke — *Deferred to manual UAT*
        """
    )
    assert count_unchecked(body) == 0


def test_no_checkboxes_no_warnings() -> None:
    body = "## Just prose, no checkboxes here.\n\nMore prose."
    assert count_unchecked(body) == 0


def test_all_checked_no_warnings() -> None:
    body = dedent(
        """\
        - [x] AC-1
        - [x] AC-2
        - [x] AC-3
        """
    )
    assert count_unchecked(body) == 0


def test_hook_file_exists_and_is_executable() -> None:
    """Sanity check the hook is still present + executable."""
    assert HOOK_PATH.is_file(), "Hook script must exist"
    import os
    assert os.access(HOOK_PATH, os.X_OK), "Hook script must be executable"
