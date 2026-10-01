#!/usr/bin/env python3
"""Inversion Phase 3 — the DELETION-RATCHET INSTRUMENT (#1595, epic-0 unit 5).

Builds the census + per-list GO/NO-GO verdict the deletion procedure needs.
**This script deletes nothing** — it is the gate a future deletion commit
must pass, and the pattern→corpus conversion audit that commit must satisfy
first (epic-0's own condition: "pattern→corpus-case conversion is a STEP IN
the deletion procedure, not an intention").

m-43 (name the layer): three layers are joined here, each read exactly as
production reads it — none re-derived:

  1. **Surface 1's claim** — ``PreClassifier.pre_classify_with_pattern_list``
     (the single-intent entry ``classifier.py``'s ``classify`` consults) and
     ``PreClassifier.detect_multiple_intents`` (the ``classify_multiple``
     entry), exactly as production calls them. The claiming ``*_PATTERNS``
     list's NAME comes from the pre-claim shadow probe's own threading
     (``pre_classify_with_pattern_list`` / ``MultiIntentResult.pattern_lists``)
     — never a second regex pass, per the #1595 Phase-3 prompt's explicit
     condition.
  2. **The router's verdict** — parsed from the two LATEST Phase-1 shadow-score
     reports' own markdown tables (asserted-rows MATCH/MISMATCH and the
     REVIEW-rows question book), never re-scored (NO LLM CALLS in this
     script).
  3. **The live flag's routable set** — ``PIPER_INVERSION_LIVE_CATEGORIES``,
     read via the SAME ``resolve_live_match`` production's live consult
     uses (``services/intent_service/inversion_live.py``), never
     re-implemented.

PRECEDENCE (documented, not implicit): for TEMPORAL-category corpus rows,
the 2026-09-25 TEMPORAL RE-SCORE report OVERRIDES the same-day full run —
the re-score exists precisely because the full run's TEMPORAL numbers used a
pre-sharpening registry description (Lead's read in that report). Every
other category reads the full run only; the temporal-rescore file carries no
other categories.

GO/NO-GO rule for a ``*_PATTERNS`` list (Phase-3 prompt, verbatim): a list is
DELETABLE iff every corpus row it claims is one of —
  (a) MATCH under the router,
  (b) REVIEW where the router's own route equals the SAME row's surface-1
      claimed action (the inversion agrees with surface 1 on this specific
      case), or
  (c) the row's corpus-expected action is already a member of the LIVE
      flag's routable set (``--live`` / ``PIPER_INVERSION_LIVE_CATEGORIES``)
      — deleting the pattern only matters if the row would otherwise fall to
      an unproven destination; a row whose expected action already flipped
      live falls to a destination the Phase-2 per-category gate already
      covers.
Any row failing all three (MISMATCH, UNSCORED, or a REVIEW disagreement to a
non-live destination) makes the WHOLE list NO-GO, named.

Usage:
    scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS
    scripts/inversion_phase3_deletion_gate.py --all
    scripts/inversion_phase3_deletion_gate.py --all --live read_temporal,read_strategic,create_todo,create_reminder,delete_todo,set_default_repo
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402  (load_corpus, same_operation)
import inversion_phase1_shadow_score as p1  # noqa: E402  (_norm_phrase, _prefix_candidates)
import pattern_literal_counts  # noqa: E402  (shared literal counter)

CORPUS_PATH = ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml"
FULL_REPORT = (
    ROOT
    / "docs"
    / "internal"
    / "architecture"
    / "current"
    / "inversion-phase1-shadow-score-2026-09-25.md"
)
TEMPORAL_RESCORE_REPORT = (
    ROOT
    / "docs"
    / "internal"
    / "architecture"
    / "current"
    / "inversion-phase1-shadow-score-2026-09-25-temporal-rescore.md"
)
# Phase-3 reports, NEWEST FIRST — an explicit, ordered list, not a glob (a
# glob's order would be an accident of naming; this is a precedence rule).
# Each Phase-3 scoring run (a conversion-deposits score, or a one-row
# re-score after a destination ruling) writes its own report; the lookup
# checks them in this order before the 09-25 full report and the TEMPORAL
# re-score, so a later re-score of a phrase overrides its earlier verdict
# (2026-09-27: "what should I do next" scored MISMATCH against the pattern's
# list_todos_query, then RULED get_top_priority by CXO/PPM and re-scored
# 1/1 MATCH — the re-score report is first, so that verdict wins). Asserted
# rows only: these partial runs' REVIEW tables are empty boilerplate.
# Append a new run at the FRONT.
_P3 = ROOT / "docs" / "internal" / "architecture" / "current"
PHASE3_REPORTS: List[Path] = [
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-13.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-01.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-02.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-03.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-04.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-05.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-06.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-07.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-08.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-09.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-10.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-11.md",  # ruled row (Haiku)
    _P3 / "inversion-phase3-ruled-rows-rescore-2026-10-01-12.md",  # ruled row (Haiku)
    _P3
    / "inversion-phase3-plan-rows-rescore-2026-10-01-thisweekspri.md",  # 1 row, plan expectation (Haiku)
    _P3
    / "inversion-phase3-plan-rows-rescore-2026-10-01-nextweekspri.md",  # 1 row, plan expectation (Haiku)
    _P3
    / "inversion-phase3-plan-rows-rescore-2026-10-01-thismonthsnu.md",  # 1 row, plan expectation (Haiku)
    _P3
    / "inversion-phase3-temporal-rescore-2026-10-01.md",  # TEMPORAL category after the per-row sort (Haiku, 55/65)
    _P3
    / "inversion-phase3-next-to-do-rescore-2026-10-01.md",  # 1 row re-expected after the Haiku baseline (Haiku)
    # 2026-10-01: the SERVED model on alpha is Anthropic Haiku (the user's stored
    # key), not the dev scorer's gpt-4o-mini. This full-corpus Haiku run is the
    # verdict of record for every row; the per-list reports below it stay as
    # history and as the fallback for rows a later run omits.
    _P3 / "inversion-phase1-shadow-score-2026-10-01-haiku-baseline.md",  # 283 rows, served model
    _P3
    / "inversion-phase3-calendar-query-rescore-2026-10-01.md",  # 46 rows after CXO/PPM rulings (39/46)
    _P3
    / "inversion-phase3-priority-rescore-2026-10-01.md",  # 38 rows after CXO/PPM rulings (35/38)
    _P3
    / "inversion-phase3-calendar-rescore-2026-09-30.md",  # 46 rows re-scored after the description fix (32/46)
    _P3 / "inversion-phase3-calendar-score-2026-09-30.md",  # 46 rows: CALENDAR_QUERY (24/46)
    _P3 / "inversion-phase3-priority-score-2026-09-30.md",  # 38 rows: PRIORITY (26/38)
    _P3
    / "inversion-phase3-guidance-rescore-2026-09-28.md",  # 20 rows re-scored after the registry-description fix (18/20)
    _P3 / "inversion-phase3-guidance-score-2026-09-28.md",  # 20 rows: GUIDANCE (8/20 — NO-GO)
    _P3 / "inversion-phase3-todo-query-rescore-2026-09-27.md",  # 1 row, ruled destination
    _P3
    / "inversion-phase3-deposits-score-2026-09-27.md",  # 15 rows: REMINDER/REMINDER_QUERY/TODO_QUERY
]
# Backward-compatible name for the first deposits report (tests/docs cite it).
DEPOSITS_REPORT = PHASE3_REPORTS[-1]
DELETED_PATTERNS_JSON = ROOT / "scripts" / "inversion_phase3_deleted_patterns.json"

# The --live categories every Phase-3 deletion run (gate GO reads, deletion
# commits, non-regression ledger pins) has used throughout this epic —
# promoted to a single shared constant 2026-10-01 (#1595 Phase 3 fourth
# deletion) when a second caller needed it (TestChatPointersReachabilityRatchet
# ._phase3_ledger_resolve, tests/test_architecture_enforcement.py): a POINTER
# phrase ledgered under an entry with a MISMATCH-but-live-route row (e.g.
# TEMPORAL_PATTERNS' "what is on my calendar") needs this exact set to pass
# check_deleted_entry_non_regression — the "unknown" (cats=None) strictest
# reading, correct for an entry with no deployment context, is NOT what the
# reachability ratchet wants: it exists to confirm a chat pointer resolves
# the way PRODUCTION actually resolves it, and production's live flag does
# carry these categories (dispatch-verified, repeatedly, across this epic).
# "Reuse it, don't re-implement it" — same principle as Arch's gate-defect
# ruling (mailboxes/lead/read/rule-arch-to-lead-cc-ppm-cxo-temporal-...-
# 2026-10-01.md) applied to this constant specifically.
CURRENT_LIVE_CATEGORIES: frozenset = frozenset(
    {
        "CREATE_REMINDER",
        "CREATE_TODO",
        "READ_REFERENT",
        "READ_STATUS",
        "READ_STRATEGIC",
        "READ_SYNTHESIS",
        "READ_TEMPORAL",
    }
)

_ROUTE_CELL_RE = re.compile(r"^`([^`]+)`(?:\s*@([0-9.]+))?$")


# ---------------------------------------------------------------------------
# Layer 1 — surface-1 claim census (no LLM, no re-matching: reuses the
# pre-claim shadow probe's own claiming-list threading).
# ---------------------------------------------------------------------------


@dataclass
class ClaimResult:
    pattern_list: Optional[str]
    action: Optional[str]
    category: Optional[str]
    entry_surface: Optional[str]  # "pre_classify" | "detect_multiple_intents" | None


def claim_for_phrase(pc, phrase: str) -> ClaimResult:
    """Surface 1's claim for one corpus phrase, exactly as production's two
    entry points would claim it — no new matching logic.

    Precedence: ``pre_classify_with_pattern_list`` (the single-intent entry,
    ``classifier.classify``'s branch) wins if it claims; otherwise
    ``detect_multiple_intents``'s PRIMARY intent (the ``classify_multiple``
    entry) is consulted. This mirrors the two claim sites the pre-claim
    shadow probe itself instruments (intent-routing-stack.md, surface 1) —
    a row claimed by neither is UNCLAIMED, never guessed.
    """
    single_intent, single_list = pc.pre_classify_with_pattern_list(phrase)
    if single_intent is not None:
        return ClaimResult(
            pattern_list=single_list,
            action=single_intent.action,
            category=(
                single_intent.category.value
                if hasattr(single_intent.category, "value")
                else str(single_intent.category)
            ),
            entry_surface="pre_classify",
        )

    multi = pc.detect_multiple_intents(phrase)
    primary = multi.primary_intent
    if primary is not None:
        idx = next((i for i, it in enumerate(multi.intents) if it is primary), None)
        multi_list = (
            multi.pattern_lists[idx] if idx is not None and idx < len(multi.pattern_lists) else None
        )
        return ClaimResult(
            pattern_list=multi_list,
            action=primary.action,
            category=(
                primary.category.value
                if hasattr(primary.category, "value")
                else str(primary.category)
            ),
            entry_surface="detect_multiple_intents",
        )

    return ClaimResult(pattern_list=None, action=None, category=None, entry_surface=None)


# ---------------------------------------------------------------------------
# Layer 2 — router verdicts, parsed from the existing shadow-score reports
# (no LLM calls here; the reports already carry the LLM-produced verdicts).
# ---------------------------------------------------------------------------


@dataclass
class RouterLookup:
    route: Optional[str]
    conf: Optional[float]
    verdict: str  # "MATCH" | "MISMATCH" | "REVIEW" | "UNSCORED"
    source_table: Optional[str]


def _parse_route_cell(cell: str) -> Tuple[Optional[str], Optional[float]]:
    m = _ROUTE_CELL_RE.match(cell.strip())
    if not m:
        return None, None
    route = m.group(1)
    conf = float(m.group(2)) if m.group(2) else None
    return route, conf


def parse_asserted_rows(path: Path) -> List[dict]:
    """Parse a Phase-1 report's '## Row detail (asserted rows)' table,
    RETAINING the route column that
    ``inversion_phase1_shadow_score.parse_phase1_report_row_detail`` drops
    (that function is the scorer's shared-subset input, whose shape this
    script deliberately doesn't touch — see the module docstring on why a
    separate parser, not a shared-code edit, was the lower-risk reuse here).
    Same column-split idiom as that function; same table shape
    (``| phrase | category | expected | router route @conf | verdict | note |``).
    """
    lines = path.read_text().splitlines()
    try:
        start = next(
            i for i, line in enumerate(lines) if line.strip() == "## Row detail (asserted rows)"
        )
    except StopIteration:
        raise ValueError(f"{path}: no '## Row detail (asserted rows)' section")
    rows: List[dict] = []
    in_table = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("| phrase |"):
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if not stripped.startswith("|"):
            break
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 6:
            continue
        phrase, category, expected, route_cell, verdict, _note = cols[:6]
        route, conf = _parse_route_cell(route_cell)
        rows.append(
            {
                "phrase": phrase,
                "category": category,
                "expected": expected,
                "route": route,
                "conf": conf,
                "verdict": verdict,
            }
        )
    if not rows:
        raise ValueError(f"{path}: parsed zero rows from '## Row detail (asserted rows)'")
    return rows


def parse_review_rows(path: Path) -> List[dict]:
    """Parse a Phase-1 report's '## REVIEW rows' table
    (``| phrase | category | router route @conf | rationale | source |``).
    No existing parser covers this table shape (the asserted-rows parsers
    both skip REVIEW rows by construction); this is markdown-table parsing,
    not a second pass over surface-1's regex patterns, so it is outside the
    Phase-3 prompt's "never re-match" constraint."""
    lines = path.read_text().splitlines()
    try:
        start = next(
            i
            for i, line in enumerate(lines)
            if line.strip()
            == "## REVIEW rows — the router's answers as data (informational, unscored)"
        )
    except StopIteration:
        raise ValueError(f"{path}: no '## REVIEW rows' section")
    rows: List[dict] = []
    in_table = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("| phrase |"):
            in_table = True
            continue
        if not in_table:
            continue
        if stripped.startswith("|---"):
            continue
        if not stripped.startswith("|"):
            break
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 5:
            continue
        phrase, category, route_cell, _rationale, _source = cols[:5]
        route, conf = _parse_route_cell(route_cell)
        rows.append({"phrase": phrase, "category": category, "route": route, "conf": conf})
    if not rows:
        raise ValueError(f"{path}: parsed zero rows from '## REVIEW rows'")
    return rows


class RouterReports:
    """Joins a corpus phrase to its router verdict, applying the documented
    TEMPORAL-rescore precedence. Built once; reused per row."""

    def __init__(
        self,
        full_report: Path,
        temporal_report: Path,
        phase3_reports: Optional[List[Path]] = None,
    ):
        self.full_asserted = parse_asserted_rows(full_report)
        self.full_review = parse_review_rows(full_report)
        self.temporal_asserted = parse_asserted_rows(temporal_report)
        self.temporal_review = parse_review_rows(temporal_report)
        # Phase-3 reports, newest first; asserted-rows table only (their
        # REVIEW tables are empty boilerplate — parse_review_rows would raise
        # on zero rows). A missing file is skipped: a report is evidence when
        # present, never a crash when absent.
        self.deposits_asserted: List[dict] = []
        for rp in phase3_reports or []:
            if rp.exists():
                self.deposits_asserted.extend(parse_asserted_rows(rp))

        self._full_asserted_by_norm = {p1._norm_phrase(r["phrase"]): r for r in self.full_asserted}
        self._full_review_by_norm = {p1._norm_phrase(r["phrase"]): r for r in self.full_review}
        self._temporal_asserted_by_norm = {
            p1._norm_phrase(r["phrase"]): r for r in self.temporal_asserted
        }
        self._temporal_review_by_norm = {
            p1._norm_phrase(r["phrase"]): r for r in self.temporal_review
        }
        # First occurrence wins (newest report first) — never overwrite.
        self._deposits_asserted_by_norm: Dict[str, dict] = {}
        for r in self.deposits_asserted:
            self._deposits_asserted_by_norm.setdefault(p1._norm_phrase(r["phrase"]), r)

    @staticmethod
    def _find(norm: str, table: Dict[str, dict]) -> Optional[dict]:
        if norm in table:
            return table[norm]
        candidates = p1._prefix_candidates(norm, table.keys())
        if len(candidates) == 1:
            return table[candidates[0]]
        return None

    def lookup(self, phrase: str, category: str) -> RouterLookup:
        norm = p1._norm_phrase(phrase)
        search_order: List[Tuple[str, Dict[str, dict], bool]] = []
        # Phase-3 reports checked first, all categories, newest report first:
        # they carry only conversion-deposit rows and ruled re-scores, none of
        # which overlap FULL_REPORT or TEMPORAL_RESCORE_REPORT's phrases, so
        # this is additive, not an override of the TEMPORAL precedence below.
        if self._deposits_asserted_by_norm:
            search_order.append(("deposits-asserted", self._deposits_asserted_by_norm, True))
        if category == "TEMPORAL":
            search_order.append(
                ("temporal-rescore-asserted", self._temporal_asserted_by_norm, True)
            )
            search_order.append(("temporal-rescore-review", self._temporal_review_by_norm, False))
        search_order.append(("full-asserted", self._full_asserted_by_norm, True))
        search_order.append(("full-review", self._full_review_by_norm, False))

        for source, table, is_asserted in search_order:
            hit = self._find(norm, table)
            if hit is None:
                continue
            if is_asserted:
                return RouterLookup(
                    route=hit["route"],
                    conf=hit["conf"],
                    verdict=hit["verdict"],
                    source_table=source,
                )
            return RouterLookup(
                route=hit["route"], conf=hit["conf"], verdict="REVIEW", source_table=source
            )
        return RouterLookup(route=None, conf=None, verdict="UNSCORED", source_table=None)


# ---------------------------------------------------------------------------
# Layer 3 — the live flag's routable set (reused, not re-implemented).
# ---------------------------------------------------------------------------


def live_set(explicit: Optional[str]) -> Tuple[Optional[frozenset], str]:
    """Returns (cats, source). cats is None iff the flag is genuinely unknown
    (unset AND no --live override) — callers must handle that honestly
    rather than treating it as empty."""
    if explicit is not None:
        cats = frozenset(t.strip().upper() for t in explicit.split(",") if t.strip())
        return cats, "--live"
    import os

    raw = os.environ.get("PIPER_INVERSION_LIVE_CATEGORIES", "")
    if raw.strip():
        from services.intent_service.inversion_live import live_categories

        return live_categories(), "PIPER_INVERSION_LIVE_CATEGORIES (env)"
    return None, "unknown"


def expected_action_is_live(expected: str, cats: Optional[frozenset]) -> Tuple[bool, str]:
    """Condition (c): is this corpus row's corpus-EXPECTED action already a
    member of the live flag's routable set? Only applicable to
    ``action:<name>`` expectations (category:/REVIEW expectations don't name
    a single action to check). Reuses inversion_live.resolve_live_match —
    the SAME function the live consult itself calls — never re-derived."""
    if cats is None:
        return False, "live-set-unknown"
    if not expected.startswith("action:"):
        return False, "expected-not-action-shaped"
    action = expected.split(":", 1)[1]

    from services.intent_service.inversion_live import (
        _category_by_operation,
        _effect_guard_passes,
        resolve_live_match,
    )
    from services.intent_service.inversion_router import derive_routing_grammar
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()  # idempotent
    grammar = derive_routing_grammar()
    canonical = grammar.alias_to_canonical.get(action, action)
    category = _category_by_operation(grammar).get(action)
    entry = get_action_workflows().get(action)
    # Arch, 2026-10-01: "live" at the gate must mean what it means in
    # production. consult_inversion_live dispatches ONLY rail keys
    # (get_action_workflows) that pass the #1677 effect guard — a name that
    # merely matches the flag (op / group / category) but has no WorkflowEntry
    # (e.g. get_current_time, CANONICAL/floor-routed) can never be served by
    # the live consult, so a GO on its rows would delete a pattern for rows
    # the router will never dispatch. Same functions production uses, never
    # re-derived; checked BEFORE naming so the reason names the real gap.
    if entry is None:
        return False, "not-live (no WorkflowEntry — the live consult dispatches rail keys only)"
    if not _effect_guard_passes(entry, action, canonical):
        return False, "not-live (WorkflowEntry fails the #1677 effect guard)"
    flip_group = entry.flip_group
    match = resolve_live_match(
        operation=action, canonical=canonical, flip_group=flip_group, category=category, cats=cats
    )
    if match is None:
        return False, f"not-live (checked op/canonical/group/category, none in {sorted(cats)})"
    return True, f"live via {match}"


# ---------------------------------------------------------------------------
# The census + per-list verdict
# ---------------------------------------------------------------------------


@dataclass
class RowRecord:
    phrase: str
    category: str
    expected: str
    source: str
    claim: ClaimResult
    router: RouterLookup
    row_ok: bool
    reason: str


@dataclass
class ListVerdict:
    list_name: str
    literal_count: int
    rows: List[RowRecord] = field(default_factory=list)
    deletable: bool = False
    failing_rows: List[RowRecord] = field(default_factory=list)


def row_disposition(
    claim: ClaimResult,
    router: RouterLookup,
    expected: str,
    cats: Optional[frozenset],
) -> Tuple[bool, str]:
    """The per-row deletion rule, factored out of build_census so it can be
    pinned with synthetic inputs (2026-10-01). Returns (row_ok, reason).
    A row is OK to lose its pattern when the router already owns the phrase
    live (MATCH, agreeing REVIEW, or a MISMATCH whose ROUTER route is a live
    op); it is NOT OK when the router declined (the pattern is the live
    path), when the destination merely exists, or when nothing scored it."""
    row_ok = False
    reason = ""
    if claim.pattern_list is None:
        # Unclaimed by surface 1 — not part of any list's census, but
        # still recorded (denominator: claimed + unclaimed == corpus size).
        reason = "unclaimed-by-surface-1"
    elif router.verdict == "MATCH":
        row_ok = True
        reason = "MATCH"
    elif router.verdict == "REVIEW":
        if router.route is not None and p0.same_operation(router.route, claim.action or ""):
            row_ok = True
            reason = f"REVIEW-agrees (route={router.route} == claim={claim.action})"
        else:
            live_ok, live_reason = expected_action_is_live(expected, cats)
            if live_ok:
                row_ok = True
                reason = f"REVIEW-disagrees but expected action {live_reason}"
            else:
                reason = (
                    f"REVIEW-disagrees (route={router.route} != claim={claim.action}); "
                    f"{live_reason}"
                )
    elif router.verdict == "MISMATCH":
        # 2026-10-01 (Lead, found on CALENDAR's GO read): a MISMATCH is
        # harmless to delete only when the ROUTER's answer is itself a
        # live operation — then the live consult already owns the phrase
        # and the pattern is dead weight. When the router said NONE /
        # CLARIFY / REFUSED, or named an op the live set can't dispatch,
        # the consult STANDS DOWN and surface 1 — this pattern — is the
        # live path; deleting it moves the phrase to the LLM classifier.
        # The old rule checked the EXPECTED action's liveness, which is
        # the wrong object (m-43): it says the destination exists, not
        # that the router reaches it.
        route_is_op = (
            bool(router.route)
            and router.route.upper()
            not in (
                "NONE",
                "CLARIFY",
                "REFUSED",
                "ERROR",
            )
            and not str(router.route).startswith("PLAN[")
        )
        live_ok, live_reason = (
            expected_action_is_live(f"action:{router.route}", cats)
            if route_is_op
            else (False, f"router did not name an operation (route={router.route})")
        )
        if live_ok:
            row_ok = True
            reason = (
                f"MISMATCH but the router's own route {live_reason} — the consult owns this phrase"
            )
        elif (
            expected.startswith("action:")
            and claim.action
            and not p0.same_operation(claim.action, expected.split(":", 1)[1])
        ) or (expected in ("floor", "plan") and claim.action):
            # 2026-10-01 (Lead, found on TEMPORAL after the CALENDAR deletion):
            # the pattern IS the live path here, but it serves the row WRONG —
            # its claim disagrees with the ruled destination (e.g. TEMPORAL
            # claims "pull up my calendar" as get_current_time; ruled
            # week_calendar / floor). Deleting it moves the fallback from a
            # deterministic wrong answer to the LLM classifier, which cannot
            # be worse than definitionally wrong. OK to delete; the row stays
            # open for the ROUTER (it still declined), which is a grammar
            # question, not a reason to keep a mis-serving regex.
            row_ok = True
            reason = (
                f"MISMATCH and the router declined (route={router.route}), but the pattern "
                f"mis-serves this row (claim={claim.action} != ruled {expected}) — deleting "
                f"cannot make the fallback worse"
            )
        else:
            reason = (
                f"MISMATCH (route={router.route} != expected {expected}); the pattern is the live "
                f"path for this phrase — {live_reason}"
            )
    else:  # UNSCORED
        # 2026-10-01: an unscored row is a row we know nothing about. The
        # pre-deposit rule let "expected action live" stand in for a
        # verdict; with deposits + the served-model baseline there is no
        # excuse for not scoring it. Never OK.
        live_ok, live_reason = False, "UNSCORED — score it (one router call); no verdict, no GO"
        if live_ok:
            row_ok = True
            reason = f"UNSCORED but expected action {live_reason}"
        else:
            reason = f"UNSCORED; {live_reason}"

    return row_ok, reason


def build_census(cats: Optional[frozenset]) -> Tuple[List[RowRecord], Dict[str, ListVerdict]]:
    from services.intent_service.pre_classifier import PreClassifier

    rows = p0.load_corpus()
    literal_counts = pattern_literal_counts.per_list_literal_counts()

    records: List[RowRecord] = []
    by_list: Dict[str, ListVerdict] = {
        name: ListVerdict(list_name=name, literal_count=count)
        for name, count in literal_counts.items()
    }

    reports = RouterReports(FULL_REPORT, TEMPORAL_RESCORE_REPORT, PHASE3_REPORTS)

    for r in rows:
        phrase = r["phrase"]
        category = r.get("category", "")
        expected = r.get("expected", "")
        source = r.get("source", "")

        claim = claim_for_phrase(PreClassifier, phrase)
        router = reports.lookup(phrase, category)

        row_ok, reason = row_disposition(claim, router, expected, cats)
        rec = RowRecord(
            phrase=phrase,
            category=category,
            expected=expected,
            source=source,
            claim=claim,
            router=router,
            row_ok=row_ok,
            reason=reason,
        )
        records.append(rec)

        if claim.pattern_list is not None:
            lv = by_list.setdefault(
                claim.pattern_list,
                ListVerdict(
                    list_name=claim.pattern_list,
                    literal_count=literal_counts.get(claim.pattern_list, 0),
                ),
            )
            lv.rows.append(rec)
            if not row_ok:
                lv.failing_rows.append(rec)

    for lv in by_list.values():
        lv.deletable = len(lv.rows) > 0 and len(lv.failing_rows) == 0

    return records, by_list


# ---------------------------------------------------------------------------
# Layer 4 — pattern→corpus conversion check for a DELETABLE list.
# ---------------------------------------------------------------------------


def _clean_for_matching(message: str) -> str:
    """The exact two-line preprocessing
    ``PreClassifier.pre_classify_with_pattern_list`` applies before matching
    (its own docstring/body, replicated verbatim here — NOT new matching
    logic, just the cleaning step, so ``_first_pattern_match`` sees the same
    string production matched against)."""
    import string

    clean_msg = message.strip().lower()
    return clean_msg.rstrip(string.punctuation + "!?.,;:😊🙂👋")


def unexercised_literals(list_name: str, claimed_rows: List[RowRecord]) -> List[str]:
    """For a DELETABLE list, which of its regex literals matched NO corpus
    row at all. Calls the production matcher (``PreClassifier._first_pattern_match``)
    on each claiming row's cleaned text against the ALREADY-KNOWN claiming
    list — reusing the real matcher on a known list is not the "second
    regex pass" the Phase-3 prompt prohibits (that phrase means inventing
    new matching/claim logic; this calls the existing one, read-only, to
    report which literal fired)."""
    from services.intent_service.pre_classifier import PreClassifier

    patterns = getattr(PreClassifier, list_name, None)
    if patterns is None:
        return []
    exercised: set = set()
    for rec in claimed_rows:
        cleaned = _clean_for_matching(rec.phrase)
        match = PreClassifier._first_pattern_match(cleaned, patterns)
        if match is not None:
            exercised.add(match.re.pattern)
    return [p for p in patterns if p not in exercised]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def render_list_report(
    list_name: str,
    by_list: Dict[str, ListVerdict],
    all_literal_counts: Dict[str, int],
    corpus_total: int,
) -> str:
    lines: List[str] = []
    lv = by_list.get(list_name)
    if lv is None:
        lines.append(f"{list_name}: not found in the census (0 rows claimed, 0 literals?)")
        return "\n".join(lines)

    total_literals = sum(all_literal_counts.values())
    lines.append(f"## {list_name}")
    lines.append(f"literals: {lv.literal_count}  |  rows claimed: {len(lv.rows)}/{corpus_total}")
    lines.append(
        f"verdict: {'GO (deletable)' if lv.deletable else 'NO-GO'}"
        + (
            f" — deleting removes {lv.literal_count} literals: ceiling {total_literals} -> {total_literals - lv.literal_count}"
            if lv.deletable
            else ""
        )
    )
    if lv.rows:
        lines.append("")
        lines.append("rows claimed:")
        for rec in lv.rows:
            mark = "OK" if rec.row_ok else "FAIL"
            lines.append(
                f'  [{mark}] "{rec.phrase}" -> claim={rec.claim.action} '
                f"expected={rec.expected} router={rec.router.route}@{rec.router.conf} "
                f"verdict={rec.router.verdict} :: {rec.reason}"
            )
    else:
        lines.append("")
        lines.append(
            "(zero corpus rows claim this list — deletable on the corpus evidence alone, "
            "but that is also the honest signal that the corpus doesn't exercise this list; "
            "deleting on zero coverage is NOT the same as deleting on proven agreement.)"
        )

    if lv.deletable and lv.rows:
        missing = unexercised_literals(list_name, lv.rows)
        lines.append("")
        if missing:
            lines.append(
                f"pattern->corpus conversion needed ({len(missing)} literal(s) unexercised):"
            )
            for pat in missing:
                lines.append(f'  needs a corpus row before deletion: r"{pat}"  (list={list_name})')
        else:
            lines.append(
                "pattern->corpus conversion: every literal in this list is exercised by >=1 corpus row."
            )

    return "\n".join(lines)


def render_census_table(by_list: Dict[str, ListVerdict]) -> str:
    lines: List[str] = []
    lines.append(f"{'list':<40} {'literals':>8} {'rows':>6} {'verdict':>12}")
    lines.append("-" * 70)
    total_rows_claimed = 0
    for name in sorted(by_list):
        lv = by_list[name]
        n_rows = len(lv.rows)
        total_rows_claimed += n_rows
        verdict = "GO" if lv.deletable else ("NO-GO" if n_rows else "NO ROWS")
        lines.append(f"{name:<40} {lv.literal_count:>8} {n_rows:>6} {verdict:>12}")
    lines.append("-" * 70)
    lines.append(
        f"total rows claimed (may double-count if a row's list changes across parses): {total_rows_claimed}"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# The deletion ledger — DELETED_PATTERN_LISTS non-regression check (the
# pinning test's mechanism half; #1595 Phase-3 prompt condition (b)).
# ---------------------------------------------------------------------------


def load_deleted_pattern_lists() -> List[dict]:
    """Read scripts/inversion_phase3_deleted_patterns.json's
    ``DELETED_PATTERN_LISTS`` array. As of 2026-09-27 this carries the
    first two real entries (REMINDER_PATTERNS, REMINDER_QUERY_PATTERNS);
    each future deletion commit appends its own entry, carrying
    ``rows_claimed_at_deletion``, ``verdict_report``, and ``expected_ops``
    for later re-check."""
    import json

    data = json.loads(DELETED_PATTERNS_JSON.read_text())
    return data.get("DELETED_PATTERN_LISTS", [])


def expected_op_for_phrase(entry: dict, phrase: str, corpus_row: Optional[dict]) -> Optional[str]:
    """The specific canonical action THIS phrase is licensed against, within
    one ``DELETED_PATTERN_LISTS`` entry — never "any of the entry's ops"
    once a per-phrase answer is available (TODO_QUERY_PATTERNS is the first
    entry whose ``expected_ops`` has more than one member: 'what should I do
    next' ruled ``get_top_priority``, its ten siblings ``list_todos_query``
    — treating either as valid for every row would silently accept a row
    that drifted to the WRONG one of the two).

    Precedence:
      1. the corpus row's own asserted ``expected`` (an ``action:<name>``
         row already names its own destination — the entry's
         ``expected_ops``/``expected_op_by_phrase`` are irrelevant to it);
      2. the entry's own ``expected_op_by_phrase`` map, when the ledger
         author supplied one (required once ``expected_ops`` has more than
         one member and an UN-asserted ``REVIEW`` row is in play);
      3. ``expected_ops`` itself, ONLY when it has exactly one member (the
         original, unambiguous single-destination shape the REMINDER_*
         entries have — unchanged behavior for those).

    Returns ``None`` when none of these can name a single action for this
    phrase — never a guess.
    """
    expected = (corpus_row or {}).get("expected", "")
    if expected.startswith("action:"):
        return expected.split(":", 1)[1]
    by_phrase = entry.get("expected_op_by_phrase") or {}
    if phrase in by_phrase:
        return by_phrase[phrase]
    expected_ops = entry.get("expected_ops") or []
    if len(expected_ops) == 1:
        return expected_ops[0]
    return None


def check_deleted_entry_non_regression(
    entry: dict,
    reports: Optional[RouterReports] = None,
    cats: Optional[frozenset] = None,
) -> Tuple[bool, List[str]]:
    """Non-regression check for ONE ``DELETED_PATTERN_LISTS`` entry.

    Two things must hold for every phrase in ``entry["rows_claimed_at_deletion"]``:
      1. if a SURVIVING surface-1 ``*_PATTERNS`` list claims it now, that
         reclaim must be DOCUMENTED (``known_reabsorptions`` — never
         inferred, always an explicit deposit; an undocumented reclaim fails
         loud unconditionally, because the SURPRISE itself — a pattern
         silently reabsorbing territory the ledger author didn't expect — is
         what this check exists to catch, independent of whether the end
         state happens to be harmless);
      2. the phrase's own frozen router evidence — the SAME MATCH /
         agreeing-REVIEW / live-MISMATCH proof ``row_disposition`` used to
         call the deleting list GO in the first place — still holds, re-run
         against ``reports`` and this phrase's resolved target op
         (:func:`expected_op_for_phrase`; never a guess).

    ``cats`` is the live-flag routable set (same shape ``row_disposition``'s
    condition (c) takes) — pass it when an entry's rows depend on a
    MISMATCH-but-live-route proof (CALENDAR_QUERY_PATTERNS, #1595 Phase 3
    third deletion, is the first entry that does); omitted/``None`` means
    "live set unknown," the strictest reading, matching every prior caller's
    behavior byte-for-byte (REMINDER_PATTERNS/REMINDER_QUERY_PATTERNS/
    TODO_QUERY_PATTERNS never needed a live condition, so this parameter
    changes nothing for them).

    A DOCUMENTED reclaim comes in two shapes, both keyed by ``known_reabsorptions``:
      (a) **AGREEING** (the original, #1595 second deletion shape; ``agrees``
          omitted or not explicitly ``False``) — the reclaiming list's own
          claimed action still equals this phrase's target op.
      (b) **DISAGREEING**, explicitly marked ``"agrees": false`` (#1595 third
          deletion — CALENDAR_QUERY_PATTERNS rows TEMPORAL_PATTERNS reclaims
          as ``get_current_time``) — the reclaim is WRONG and is NAMED as
          wrong, never silenced, but the phrase's own frozen router evidence
          independently still proves it safe regardless of what the
          reclaiming pattern itself claims. This is sound because production
          consults the live Inversion router BEFORE this surface-1 fallback
          (``consult_inversion_live``'s precedence —
          docs/internal/architecture/current/intent-routing-stack.md): the
          fallback reclaim only matters when the live consult stands down, a
          pre-existing, orthogonal fallback-quality question this deletion
          did not introduce and this check does not adjudicate — it only
          proves the phrase's PRIMARY (live) path is unaffected.

    A phrase can also be licensed by a third, UNCLAIMED shape, keyed by
    ``misserved_at_deletion`` (#1595 Phase 3 fourth deletion —
    TEMPORAL_PATTERNS): the deleted pattern's OWN claim for this phrase
    disagreed with the ruled destination AND the router independently
    declined (``row_disposition``'s "mis-serves this row" branch, at GATE
    time) — deletion was licensed because removing a deterministically-wrong
    fallback cannot regress a row that was already unserved correctly. That
    proof can never be re-derived here (this function's synthetic claim is
    deliberately the CORRECT target op, so the mis-serve condition can never
    fire on it), so the re-verified invariant is narrower: the phrase must
    still be UNCLAIMED (``claim.pattern_list is None``) — strictly as safe or
    safer than being wrongly claimed. A phrase that instead gets reclaimed by
    some surviving pattern falls through to the reclaim branch above, which
    still demands ``known_reabsorptions`` documentation — this shape never
    bypasses that check.

    Returns ``(ok, problems)`` — problems is empty iff ok.
    """
    from services.intent_service.pre_classifier import PreClassifier

    problems: List[str] = []
    reports = reports or RouterReports(FULL_REPORT, TEMPORAL_RESCORE_REPORT, PHASE3_REPORTS)
    corpus_by_phrase = {r["phrase"]: r for r in p0.load_corpus()}

    for phrase in entry.get("rows_claimed_at_deletion", []):
        claim = claim_for_phrase(PreClassifier, phrase)
        corpus_row = corpus_by_phrase.get(phrase)
        if corpus_row is None:
            problems.append(f"{phrase!r}: no longer a corpus row — cannot re-verify")
            continue

        target_op = expected_op_for_phrase(entry, phrase, corpus_row)
        expected = corpus_row.get("expected", "")
        lookup = reports.lookup(phrase, corpus_row.get("category", ""))
        # Re-derive the SAME row-safety proof build_census's row_disposition
        # used at deletion time, driven by THIS phrase's resolved target op
        # — never the (possibly reabsorbing, possibly wrong) surface-1
        # claim. A synthetic non-None pattern_list only satisfies
        # row_disposition's "was this row claimed by something" branch point;
        # it names no real list and is never compared against anything.
        synthetic_claim = ClaimResult(
            pattern_list="phase3-non-regression-reproof",
            action=target_op,
            category=None,
            entry_surface=None,
        )
        row_ok, reason = row_disposition(synthetic_claim, lookup, expected, cats)

        if claim.pattern_list is not None:
            known = (entry.get("known_reabsorptions") or {}).get(phrase)
            if known is not None and known.get("reclaimed_by") == claim.pattern_list:
                agrees = (
                    target_op is not None
                    and claim.action is not None
                    and p0.same_operation(claim.action, target_op)
                )
                if agrees:
                    continue
                if known.get("agrees") is False and row_ok:
                    continue
            problems.append(
                f"{phrase!r}: claimed again by {claim.pattern_list} — the deleted "
                f"list's territory was reabsorbed by a surviving pattern"
                + (
                    ""
                    if known is None
                    else " (documented reabsorption, but the claim no longer agrees and "
                    f"the independent live-routing re-proof failed: {reason})"
                )
            )
            continue

        if row_ok:
            continue

        # Documented MISSERVED-at-deletion shape (#1595 Phase 3 fourth
        # deletion, TEMPORAL_PATTERNS): a phrase whose ORIGINAL pattern claim
        # disagreed with the ruled destination AND the router independently
        # declined (row_disposition's "mis-serves this row" branch in
        # build_census, at GATE time). That proof is a one-time fact about
        # the deleted pattern's own (wrong) claim — it can never be
        # reproduced here, because `synthetic_claim.action` is deliberately
        # the CORRECT target_op, not the deleted pattern's wrong one (so
        # `row_disposition`'s mis-serve condition, which requires
        # claim.action to DISAGREE with expected, can structurally never
        # fire on this re-derivation). The invariant actually worth
        # re-verifying forever is narrower and cheaper: is this phrase STILL
        # at least as safe as it was when a demonstrably-wrong pattern owned
        # it? Since `claim.pattern_list is None` here (just checked above —
        # we're past the reclaim branch), the phrase is UNCLAIMED, which is
        # strictly safer than being wrongly claimed. A phrase that instead
        # gets reclaimed by some OTHER pattern is caught by the reclaim
        # branch above (still requires documentation via
        # known_reabsorptions), so this escape only ever fires on the
        # genuinely-unclaimed case.
        misserved = (entry.get("misserved_at_deletion") or {}).get(phrase)
        if misserved is not None:
            continue

        problems.append(
            f"{phrase!r}: router verdict now {lookup.verdict} (route={lookup.route}) — "
            f"no longer MATCH or an agreeing REVIEW ({reason})"
        )

    return (len(problems) == 0, problems)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", dest="list_name", help="Report GO/NO-GO for one *_PATTERNS list")
    ap.add_argument("--all", action="store_true", help="Print the full census table")
    ap.add_argument(
        "--live",
        dest="live",
        default=None,
        help="Comma-separated live-flag token override (else reads PIPER_INVERSION_LIVE_CATEGORIES)",
    )
    args = ap.parse_args()

    cats, live_source = live_set(args.live)
    print(
        f"live set source: {live_source}"
        + (f" = {sorted(cats)}" if cats is not None else " (UNKNOWN — pass --live)")
    )

    records, by_list = build_census(cats)
    claimed = sum(1 for r in records if r.claim.pattern_list is not None)
    unclaimed = len(records) - claimed
    print(
        f"corpus denominator: {len(records)} rows total = {claimed} claimed + {unclaimed} unclaimed"
    )
    print()

    literal_counts = pattern_literal_counts.per_list_literal_counts()

    if args.list_name:
        print(render_list_report(args.list_name, by_list, literal_counts, len(records)))

    if args.all or not args.list_name:
        print(render_census_table(by_list))
        zero_claim = sorted(
            n for n in literal_counts if n not in by_list or len(by_list[n].rows) == 0
        )
        if zero_claim:
            print()
            print(
                f"lists with ZERO corpus claims ({len(zero_claim)}): deletable on corpus evidence alone, "
                f"but this is also an honest 'corpus doesn't exercise this list' signal:"
            )
            for n in zero_claim:
                print(f"  {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
