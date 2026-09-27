#!/usr/bin/env python3
"""Shared AST counter for the pre-classifier's ``*PATTERNS`` class-attribute
lists (#1595 Phase 3).

Factored OUT of ``tests/test_architecture_enforcement.py::TestExtractionPatternRatchet
._pre_classifier_count`` (2026-09-27) so the deletion-ratchet instrument
(``scripts/inversion_phase3_deletion_gate.py``) and the extraction ratchet
consult the SAME per-list counting logic instead of two copies drifting apart
— the identical rationale ``_pattern_list_name`` already applies (a
hand-maintained parallel table is the whack-a-mole class this epic exists to
retire). The ratchet test now calls :func:`per_list_literal_counts` and sums
it; the ceiling (567) and the vacuity floor (30 lists) are unchanged, and
``test_extraction_ratchet_stays_tight`` re-measures this on every run so a
divergence between the two consumers is loud (a change here that alters the
sum fails that test immediately).

Only counts DIRECT class-body assignments to a name ending ``PATTERNS`` whose
value is a list/tuple literal — the same scope
``TestExtractionPatternRatchet`` has always scanned (module-level helper
guards like ``REMINDER_QUERY_BLOCKERS`` are included since they too end in
neither... note: only names ending in PATTERNS are counted, matching the
original derivation exactly).
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
PRE_CLASSIFIER_PY = REPO_ROOT / "services" / "intent_service" / "pre_classifier.py"

# Vacuity floor: the class held 35 `*PATTERNS` lists at freeze time (2026-08-29).
# A scan finding far fewer means the derivation broke (renamed class / moved
# lists), not that patterns went away. Mirrors
# TestExtractionPatternRatchet._MIN_PATTERN_LISTS exactly.
MIN_PATTERN_LISTS = 30


def per_list_literal_counts(pre_classifier_path: Path = PRE_CLASSIFIER_PY) -> Dict[str, int]:
    """Return ``{LIST_NAME: literal_count}`` for every class-level ``*PATTERNS``
    list assigned directly in the ``PreClassifier`` class body.

    Byte-identical derivation to the pre-2026-09-27
    ``TestExtractionPatternRatchet._pre_classifier_count`` inline scan: an
    AST walk over the class body, matching ``ast.Assign`` nodes whose target
    is a bare ``Name`` ending in ``PATTERNS`` and whose value is an
    ``ast.List``/``ast.Tuple`` literal, counting ``len(value.elts)``.

    Raises ``AssertionError`` (vacuity guard) if the ``PreClassifier`` class
    cannot be found, or if fewer than :data:`MIN_PATTERN_LISTS` lists are
    found — a refactor that silently unhooks this scan must fail loud, never
    return a quietly-wrong smaller count.
    """
    tree = ast.parse(Path(pre_classifier_path).read_text(encoding="utf-8"))
    cls = next(
        (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "PreClassifier"),
        None,
    )
    assert cls is not None, (
        f"VACUITY: PreClassifier class not found in {pre_classifier_path} — "
        f"re-point per_list_literal_counts() in the same commit."
    )
    lists: Dict[str, int] = {}
    for stmt in cls.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.value, (ast.List, ast.Tuple)):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id.endswith("PATTERNS"):
                    lists[target.id] = len(stmt.value.elts)
    assert len(lists) >= MIN_PATTERN_LISTS, (
        f"VACUITY: pre-classifier scan found only {len(lists)} `*PATTERNS` "
        f"lists (expected >= {MIN_PATTERN_LISTS}) — the derivation idiom "
        f"changed; fix per_list_literal_counts(), don't trust this count."
    )
    return lists


def total_literal_count(pre_classifier_path: Path = PRE_CLASSIFIER_PY) -> int:
    """Sum of :func:`per_list_literal_counts` — what the extraction ratchet's
    ``pre-classifier`` ceiling (567) measures."""
    return sum(per_list_literal_counts(pre_classifier_path).values())


if __name__ == "__main__":
    counts = per_list_literal_counts()
    for name in sorted(counts):
        print(f"{name}: {counts[name]}")
    print(f"TOTAL: {sum(counts.values())} ({len(counts)} lists)")
