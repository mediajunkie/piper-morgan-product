#!/usr/bin/env python3
"""Inversion Phase-2.1 gate (#1595) — the SNAPSHOT-AWARE corpus rerun.

m-43 (name the layer): this run measures the INVERSION ROUTER ONLY — the
constrained routing call against corpus fixtures. It is not live traffic,
not the production chain, and not handler behavior. Three conditions:

  1. **phase0 corpus, context-free** — every row of
     tests/fixtures/inversion_corpus_phase0.yaml routed with NO session
     state; method identical to Phase 1b
     (scripts/inversion_phase1_shadow_score.py) so the per-category table
     is comparable to the 33/39-vs-36/39 baseline.
  2. **armed-state rows, WITH snapshot** — each fixture-bearing row of
     tests/fixtures/inversion_corpus_phase2_armed.yaml builds the REAL
     ``SessionSnapshot`` dataclass from its fixture, serializes it via
     ``serialize_for_prompt`` (never a hand-rolled block), and routes with
     ``RouterSnapshot(state_block=...)`` — the exact path
     ``inversion_shadow._shadow_check`` uses.
  3. **armed-state rows, WITHOUT snapshot** — the same phrases routed with
     no session state, scored against the SAME armed expectation. The
     armed-state delta (the gate question: does context flip the loss
     class?) is condition 2 minus condition 3, per row.

Stateless CONTROL twins (condition: control, no fixture) run once — their
with/without prompts would be byte-identical (an empty snapshot serializes
to "" and ``RouterSnapshot.is_empty()`` drops the block), so a second call
would measure only stochasticity. Stated, not hidden (m-44).

Scoring reuses the Phase-0/1 idioms unchanged (registry-alias-aware
matching, per-category denominators, ERROR recorded never faked, REVIEW as
its own bucket), plus two sentinel expectations for armed rows:
``route:NONE`` / ``route:CLARIFY`` — the correct decision for a turn that
answers an armed flow's open question is the NONE sentinel (the flow's
handler is the offer seam, not a catalog operation).

HONESTY RULE (task item 4): if with-snapshot does NOT beat without on the
armed rows, that is a REPORTED RESULT. This script contains no
tune-until-green loop and its report prints raw REFUSED/mismatch rows
verbatim.

Usage (env-stripped per CLAUDE.md; keys resolve via Keychain):

    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
      venv/bin/python scripts/inversion_phase2_gate.py [--dry] [--out PATH]

Cost: one Haiku-class call per phase0 row (93) + two per armed row (7) +
one per control row (7) = 114 planned calls, plus at most one repair retry
each. --dry validates fixtures + serialization + pairing, no LLM calls.
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402  (corpus + matching idioms)
import inversion_phase1_shadow_score as p1  # noqa: E402  (scorer + baseline)

ARMED_CORPUS = ROOT / "tests" / "fixtures" / "inversion_corpus_phase2_armed.yaml"

DEFAULT_OUT = (
    ROOT
    / "docs"
    / "internal"
    / "operations"
    / f"inversion-phase2-gate-{datetime.now(timezone.utc):%Y-%m-%d}.md"
)

_VALID_CONDITIONS = {"armed", "control"}
_ROUTE_SENTINELS = {"route:NONE": "none", "route:CLARIFY": "clarify"}


def snapshot_field_names() -> Tuple[str, ...]:
    from services.intent_service.session_snapshot import SessionSnapshot

    return tuple(f.name for f in dataclasses.fields(SessionSnapshot))


def load_armed_corpus(path: Path = ARMED_CORPUS) -> List[Dict[str, Any]]:
    """Load + validate the armed-state extension. Fails loudly on any
    malformed row — a fixture that cannot build the REAL dataclass must
    never reach a scored run."""
    import yaml

    from services.intent_service.session_snapshot import (
        SessionSnapshot,
        serialize_for_prompt,
    )

    data = yaml.safe_load(path.read_text())
    rows = data.get("corpus") or []
    if not rows:
        raise ValueError(f"{path.name}: empty corpus")

    valid_fields = set(snapshot_field_names())
    pairs: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for i, r in enumerate(rows):
        where = f"{path.name} row {i} ({r.get('phrase', '?')[:40]!r})"
        for key in ("phrase", "pair", "condition", "category", "expected", "source"):
            if not r.get(key):
                raise ValueError(f"{where}: missing required key {key!r}")
        if r["condition"] not in _VALID_CONDITIONS:
            raise ValueError(f"{where}: bad condition {r['condition']!r}")
        exp = r["expected"]
        if not (
            exp == "REVIEW"
            or exp in _ROUTE_SENTINELS
            or exp.startswith("action:")
            or exp.startswith("category:")
        ):
            raise ValueError(f"{where}: bad expected {exp!r}")
        fixture = r.get("fixture")
        if r["condition"] == "armed":
            if not isinstance(fixture, dict) or not fixture:
                raise ValueError(f"{where}: armed row requires a fixture")
            unknown = set(fixture) - valid_fields
            if unknown:
                raise ValueError(
                    f"{where}: fixture keys not on SessionSnapshot: {sorted(unknown)}"
                )
            snap = SessionSnapshot(**fixture)  # the REAL dataclass — loud on drift
            block = serialize_for_prompt(snap)  # loud on cap breach
            if not block:
                raise ValueError(f"{where}: fixture serializes to an EMPTY block")
            r["_snapshot"] = snap
            r["_state_block"] = block
        else:
            if fixture:
                raise ValueError(f"{where}: control row must carry NO fixture")
        if r["condition"] in pairs[r["pair"]]:
            raise ValueError(f"{where}: duplicate {r['condition']} for pair {r['pair']!r}")
        pairs[r["pair"]][r["condition"]] = r

    for pair, members in pairs.items():
        if set(members) != _VALID_CONDITIONS:
            raise ValueError(f"pair {pair!r}: needs exactly one armed + one control row")
        if members["armed"]["phrase"] != members["control"]["phrase"]:
            raise ValueError(f"pair {pair!r}: armed/control phrases differ")
    return rows


def armed_matches(
    expected: str, decision: Any, op_categories: Dict[str, str]
) -> Tuple[bool, str]:
    """Score one armed-family assertion; extends p1.router_matches with the
    route: sentinels. Returns (matched, annotation)."""
    if decision is None or getattr(decision, "outcome", "error") == "error":
        return False, "ERROR"
    if decision.outcome == "refused":
        return False, "REFUSED"
    if expected in _ROUTE_SENTINELS:
        want = _ROUTE_SENTINELS[expected]
        if decision.outcome == want:
            return True, ""
        return False, decision.route_label
    return p1.router_matches(expected, decision, op_categories)


async def _route_rows(
    rows: List[Dict[str, Any]],
    llm: Any,
    grammar: Any,
    *,
    state_key: Optional[str] = None,
    label: str = "",
) -> List[Any]:
    """Route each row; ``state_key`` names the row key holding a serialized
    state block (None → context-free). ERROR recorded, never faked."""
    from services.intent_service.inversion_router import (
        RoutingDecision,
        SessionSnapshot as RouterSnapshot,
        route,
    )

    decisions = []
    for i, r in enumerate(rows, 1):
        session_state = None
        if state_key and r.get(state_key):
            session_state = RouterSnapshot(state_block=r[state_key])
        try:
            d = await route(
                r["phrase"], session_state, llm_service=llm, grammar=grammar
            )
        except Exception as e:  # probe discipline: ERROR recorded, run continues
            d = RoutingDecision(outcome="error", error=f"{type(e).__name__}: {e}")
        decisions.append(d)
        print(f"[{label}{i}/{len(rows)}] {d.route_label:<28} {r['phrase'][:56]!r}")
    return decisions


def _fmt_route(d: Any) -> str:
    conf = getattr(d, "confidence", None)
    return f"`{d.route_label}`" + (f" @{conf}" if conf is not None else "")


def build_report(
    p0_scored: dict,
    armed_rows: List[Dict[str, Any]],
    armed_with: Dict[str, Any],
    armed_without: Dict[str, Any],
    grammar: Any,
    llm_note: str,
    duration_s: float,
) -> str:
    """The gate doc. Everything below mirrors the Phase-0/1 conventions:
    per-category denominators, REVIEW as its own bucket, raw rows verbatim."""
    op_categories = p1._op_category_map()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    n_ops = len(grammar.operations)
    n_aliases = sum(len(op.aliases) for op in grammar.operations)
    per_cat = p0_scored["per_cat"]
    row_results = p0_scored["rows"]

    lines = [
        "# Inversion Phase-2.1 gate — SNAPSHOT-AWARE router vs context-free, per category",
        f"Run: {stamp} · corpora: inversion_corpus_phase0.yaml ({len(row_results)} rows, "
        f"untouched) + inversion_corpus_phase2_armed.yaml ({len(armed_rows)} rows: "
        f"{sum(1 for r in armed_rows if r['condition'] == 'armed')} armed + "
        f"{sum(1 for r in armed_rows if r['condition'] == 'control')} control twins) · "
        "scripts/inversion_phase2_gate.py",
        "",
        "LAYER (m-43): **router only, against corpus fixtures** — one constrained "
        f"Haiku-class call per (row, condition) ({llm_note}), grammar derived from "
        f"the live registry at run time ({n_ops} canonical operations, {n_aliases} "
        "input-side aliases collapsed, + NONE/CLARIFY). NOT live traffic, NOT the "
        "production chain, NOT handler behavior: a MATCH here means the router "
        "would have picked the right destination, not that the destination's "
        "handler succeeds (the #1651 extraction failure lived one layer below "
        "routing). Armed-state session context is FIXTURE-built via the real "
        "`SessionSnapshot` dataclass and `serialize_for_prompt` — the exact "
        "shadow-path serialization, but the field VALUES are corpus assertions, "
        "not live store reads.",
        "",
        "## Part 1 — phase0 corpus rerun, context-free (denominators stated — m-44)",
        "",
        "Method identical to Phase 1b (inversion-phase1-shadow-score-2026-08-14b.md: "
        "33/39). Baseline column is Phase-0's FULL-CHAIN production decision "
        "(inversion-phase0-baseline-full-2026-08-12.md: 36/39).",
        "",
        "| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |",
        "|---|---|---|---|---|---|---|---|",
    ]
    tot = {"n": 0, "asserted": 0, "match": 0, "review": 0}
    regressions = []
    for cat in sorted(per_cat, key=lambda c: -per_cat[c]["n"]):
        c = per_cat[cat]
        for k in tot:
            tot[k] += c[k]
        base_asserted, base_match = p1.PHASE0_BASELINE.get(cat, (None, None))
        if base_match is None:
            base_cell, delta_cell, gate = "—", "—", "no baseline row"
        elif c["asserted"] == 0:
            base_cell = f"{base_match}/{base_asserted}"
            delta_cell = "—"
            gate = "**UNGATEABLE** (REVIEW-only denominator)"
        else:
            base_cell = f"{base_match}/{base_asserted}"
            delta = c["match"] - base_match
            delta_cell = f"{delta:+d}"
            if delta < 0:
                gate = "**REGRESSION**"
                regressions.append((cat, base_match, c["match"]))
            else:
                gate = "no regression"
        lines.append(
            f"| {cat} | {c['n']} | {c['asserted']} | {c['match']} | "
            f"{base_cell} | {delta_cell} | {c['review']} | {gate} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['n']} | {tot['asserted']} | {tot['match']} | 36/39 | "
        f"{tot['match'] - 36:+d} | {tot['review']} | (aggregate is NOT the gate) |"
    )
    lines += [
        "",
        "Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category "
        "may regress; the aggregate is never the gate**. REVIEW-only-denominator "
        "categories remain ungateable, same as Phase 0/1 stated.",
    ]
    if regressions:
        lines += [
            "",
            "🔴 **Per-category regressions vs baseline** (recorded as data — this "
            "run does not tune-until-green): "
            + "; ".join(f"{c}: {b}→{m}" for c, b, m in regressions),
        ]

    # ── Part 2: the armed-state family ────────────────────────────────────
    armed_only = [r for r in armed_rows if r["condition"] == "armed"]
    controls = {r["pair"]: r for r in armed_rows if r["condition"] == "control"}
    n_with = n_without = n_asserted_armed = 0
    pair_lines = []
    for r in armed_only:
        dw = armed_with[r["pair"]]
        dwo = armed_without[r["pair"]]
        ctrl = controls[r["pair"]]
        dc = ctrl["_decision"]
        if r["expected"] == "REVIEW":
            vw = vwo = "REVIEW"
        else:
            n_asserted_armed += 1
            okw, notew = armed_matches(r["expected"], dw, op_categories)
            okwo, notewo = armed_matches(r["expected"], dwo, op_categories)
            n_with += okw
            n_without += okwo
            vw = "MATCH" if okw else f"MISS({notew})" if notew else "MISS"
            vwo = "MATCH" if okwo else f"MISS({notewo})" if notewo else "MISS"
        if ctrl["expected"] == "REVIEW":
            vc = "REVIEW"
        else:
            okc, notec = armed_matches(ctrl["expected"], dc, op_categories)
            vc = "MATCH" if okc else f"MISS({notec})" if notec else "MISS"
        pair_lines.append(
            f"| {r['pair']} | {r['phrase'][:44]} | {r['expected']} | "
            f"{_fmt_route(dw)} → {vw} | {_fmt_route(dwo)} → {vwo} | "
            f"{ctrl['expected']}: {_fmt_route(dc)} → {vc} |"
        )
    lines += [
        "",
        "## Part 2 — ARMED-STATE rows: with-snapshot vs without (the gate question)",
        "",
        f"**Armed-state delta: {n_with}/{n_asserted_armed} with-snapshot vs "
        f"{n_without}/{n_asserted_armed} without-snapshot** (asserted armed rows; "
        "the same expectation scored under both conditions). Does context flip "
        "the loss class: "
        + (
            "**YES** — the snapshot flips rows the context-free router loses."
            if n_with > n_without
            else (
                "**NO** — the snapshot did not improve the armed rows. This is "
                "the reported result; nothing was tuned to move it."
                if n_with < n_without or n_with == n_without
                else ""
            )
        ),
        "",
        "Each armed row: fixture → real `SessionSnapshot` → `serialize_for_prompt` "
        "→ `RouterSnapshot(state_block=…)`. Control twins (same text, no fixture) "
        "run once: an empty snapshot's with/without prompts are byte-identical by "
        "construction, so a second call would measure only stochasticity.",
        "",
        "| pair | phrase | armed expected | WITH snapshot | WITHOUT snapshot | control (stateless) |",
        "|---|---|---|---|---|---|",
        *pair_lines,
    ]

    # ── raw rationales for the armed family (verbatim — task item 4) ──────
    lines += [
        "",
        "### Armed-family raw router output (verbatim rationales)",
        "",
        "| pair | condition | route @conf | rationale | error |",
        "|---|---|---|---|---|",
    ]
    for r in armed_only:
        for cond, d in (
            ("with-snapshot", armed_with[r["pair"]]),
            ("without-snapshot", armed_without[r["pair"]]),
            ("control", controls[r["pair"]]["_decision"]),
        ):
            rationale = (getattr(d, "rationale", "") or "").replace("|", "/")
            err = (getattr(d, "error", "") or "").replace("|", "/")[:80]
            lines.append(
                f"| {r['pair']} | {cond} | {_fmt_route(d)} | {rationale} | {err} |"
            )

    # ── Part 3: phase0 REVIEW + row detail (the question book, continued) ─
    lines += [
        "",
        "## Part 3 — phase0 REVIEW rows (informational, unscored)",
        "",
        "| phrase | category | router route @conf | rationale |",
        "|---|---|---|---|",
    ]
    for rr in row_results:
        if rr["verdict"] != "REVIEW":
            continue
        r, d = rr["row"], rr["decision"]
        rationale = (getattr(d, "rationale", "") or "").replace("|", "/")[:60]
        lines.append(
            f"| {r['phrase'][:55]} | {r['category']} | {_fmt_route(d)} | {rationale} |"
        )
    lines += [
        "",
        "## Row detail — phase0 asserted rows",
        "",
        "| phrase | category | expected | router route @conf | verdict | note |",
        "|---|---|---|---|---|---|",
    ]
    for rr in row_results:
        if rr["verdict"] == "REVIEW":
            continue
        r, d = rr["row"], rr["decision"]
        lines.append(
            f"| {r['phrase'][:55]} | {r['category']} | {r['expected']} | "
            f"{_fmt_route(d)} | {rr['verdict']} | {rr['note']} |"
        )

    # ── honest caveats ────────────────────────────────────────────────────
    lines += [
        "",
        "## Honest caveats — what this measures and does not (m-43 / m-44)",
        "",
        "- **Routing layer only, corpus fixtures only.** Not live traffic, not "
        "handlers, not the floor. A route:NONE MATCH says the router declined to "
        "steal an answer-turn; whether the offer seam then consumes it (and "
        "whether the floor stays honest if it doesn't — #1648's fabrication "
        "class) are separate lanes this run cannot see.",
        "- **Fixture `pending_offer_question` values exceed today's live "
        "assembly.** Arm sites currently store `summary`, not their rendered "
        "ask, so live snapshots carry question=None for most kinds "
        "(snapshot_assembly.py module docstring). The fixtures carry the ask "
        "copy the user actually saw (quoted from each arm site's own "
        "question-copy functions) — measuring the contract as designed for "
        "Phase 2.2 threading. A live shadow rerun BEFORE arm sites carry their "
        "asks would see weaker context than this run did.",
        "- **route:NONE conflates two readings on one pair.** For the "
        "confirm-aside pair, NONE is correct both as 'aside, not an answer' and "
        "as 'answer belongs to the flow' — the rationale column, not the "
        "verdict, shows which reading the router took.",
        "- **Armed expectations are Lead-contract-derived, not PM-ratified.** "
        "The route:NONE assertions follow the serialized RULE in "
        "session_snapshot.py; if Phase 2.2 decides answer-turns should emit a "
        "different sentinel, these rows re-score, not the runner.",
        "- **Single run per condition.** No repetition; margin rows can flip "
        "run-to-run (the Phase-1b calendar-flip precedent). Deltas of ±1 on "
        "any category are within observed stochasticity.",
        "- **is_confirm=true on the repo-question fixture is faithful to live "
        "assembly** (the repo question rides CONFIRM_PENDING_ACTION_WORKFLOW), "
        "but renders '(yes/no confirm)' on a which-repo question — a rendering "
        "wrinkle for Phase 2.2 to consider (flagged as discovered work).",
        "",
        f"Cost/duration: {llm_note}; wall time {duration_s:.0f}s.",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# --audit: the flip-unit COVERAGE report (#1667). No LLM, no corpus, no async.
#
# Why it lives here rather than in a new script: this is the Phase-2 flip
# lane's tooling. The gate answers "does the router pick the right operation";
# --audit answers "which operations can a flag even name" — the question #1667
# was filed about, and the one that must be answered BEFORE a wave flips. It
# is a sibling of --dry: a no-LLM mode that validates the flip's inputs.
# ---------------------------------------------------------------------------


def flip_coverage_audit() -> str:
    """The flip-unit coverage table, with denominators and the FULL unassigned
    list (m-44: an unassigned op that appears nowhere in the output is
    indistinguishable from one that doesn't exist).

    m-43, the layer this measures: the RAIL REGISTRY as constructed in this
    process (``register_default_workflows`` → ``get_action_workflows``), plus
    ACTION_REGISTRY categories via the derived routing grammar. It says what a
    flag CAN address. It says nothing about what live routing did, whether the
    flag is set anywhere, or whether a handler behaves.
    """
    from services.intent_service.action_registry import ACTION_REGISTRY
    from services.intent_service.inversion_live import _category_by_operation
    from services.intent_service.inversion_router import derive_routing_grammar
    from services.intent_service.workflow_dispatcher import (
        FLIP_GROUPS,
        get_action_workflows,
    )
    from services.intent_service.workflow_entries import register_default_workflows
    from services.shared_types import EffectClass

    register_default_workflows()  # idempotent
    rail = get_action_workflows()
    cat_of = _category_by_operation(derive_routing_grammar())

    entries = {id(e) for e in rail.values()}
    read_keys = sorted(k for k, e in rail.items() if e.effect == EffectClass.READ)
    other_keys = sorted(k for k, e in rail.items() if e.effect != EffectClass.READ)
    read_entries = {id(e) for e in rail.values() if e.effect == EffectClass.READ}

    by_group: Dict[Optional[str], List[str]] = defaultdict(list)
    for k in read_keys:
        by_group[rail[k].flip_group].append(k)
    ungrouped = sorted(by_group.get(None, []))
    no_category = [k for k in read_keys if cat_of.get(k) is None]
    # The SECOND category measurement (see the note in the report): direct
    # ACTION_REGISTRY action names only, without the grammar's canonical
    # back-mapping. This is the mapping #1667's "23 of 93" was measured with.
    direct: Dict[str, str] = {}
    for (cat, action), _spec in ACTION_REGISTRY.items():
        direct.setdefault(action, cat)
    direct_category = [k for k in read_keys if k in direct]

    # The invariant, RE-MEASURED here rather than asserted: a non-READ entry
    # cannot carry a group (WorkflowEntry.__post_init__). If this ever prints
    # non-empty, the construction guard has been bypassed and no wave should
    # flip until that is understood.
    violations = sorted(k for k in other_keys if rail[k].flip_group is not None)

    n_read = len(read_keys)
    L: List[str] = []
    L.append(f"#1667 inversion flip-unit coverage audit — {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")
    L.append("layer measured (m-43): the rail registry in THIS process "
             "(register_default_workflows → get_action_workflows) + "
             "ACTION_REGISTRY categories via the derived grammar.")
    L.append("It reports what a flag CAN address — not what routing did, and "
             "not whether any flag is set.")
    L.append("")
    L.append("DENOMINATORS")
    L.append(f"  rail operation keys (action_triggered) : {len(rail):3d}  "
             f"({len(entries)} unique entries)")
    L.append(f"    READ effect (flippable at all)       : {n_read:3d}  "
             f"({len(read_entries)} entries)")
    L.append(f"    non-READ (never flippable, any flag) : {len(other_keys):3d}  "
             f"({len(entries) - len(read_entries)} entries)")
    L.append("")
    L.append(f"READ KEYS BY FLIP GROUP  (denominator: {n_read} READ keys)")
    for group in sorted(FLIP_GROUPS):
        keys = sorted(by_group.get(group, []))
        L.append(f"  {group:<16} {len(keys):3d}/{n_read}   {', '.join(keys) or '(none)'}")
    L.append(f"  {'UNGROUPED':<16} {len(ungrouped):3d}/{n_read}")
    grouped = n_read - len(ungrouped)
    L.append(f"  {'—— grouped':<16} {grouped:3d}/{n_read}  "
             f"({100.0 * grouped / n_read:.0f}% of READ keys addressable by a wave)")
    L.append("")
    L.append(f"UNASSIGNED — the {len(ungrouped)} READ keys NO WAVE CAN FLIP, by name")
    L.append("  (this list is the point of the audit; 'unassigned' is never a "
             "silent remainder)")
    orphans = [k for k in ungrouped if cat_of.get(k) is None]
    swept = sorted((cat_of[k], k) for k in ungrouped if cat_of.get(k))
    L.append(f"  a. no group AND no registry category — reachable ONLY by naming "
             f"the operation itself: {len(orphans)}")
    for k in sorted(orphans):
        L.append(f"       {k}")
    L.append(f"  b. no group BUT carries a registry category — ⚠️ STILL SWEPT IN "
             f"when that category is named: {len(swept)}")
    for cat, k in swept:
        L.append(f"       {k:<28} (category {cat})")
    L.append("")
    L.append("FLIP-1 COVERAGE, FOR COMPARISON (the #1667 measurement, re-run)")
    L.append(f"  READ keys a CATEGORY flag can address      : "
             f"{n_read - len(no_category):3d}/{n_read}   "
             "(alias-resolved — the mapping inversion_live actually uses)")
    L.append(f"  READ keys with NO registry category        : {len(no_category):3d}/{n_read}"
             "   ← unaddressable by ANY category-only flag")
    L.append(f"  same count by DIRECT registry action only  : "
             f"{len(direct_category):3d}/{n_read} addressable "
             f"({n_read - len(direct_category)} not)")
    L.append("  ⚠️ Two measurements, both correct, of different mappings. The "
             "#1667 decision cites 23/93 addressable (70 unaddressable); that "
             "is the DIRECT count — ACTION_REGISTRY's own action names only. "
             "inversion_live._category_by_operation ALSO back-maps each action "
             "through grammar.alias_to_canonical, so the number that governs "
             "live behavior is the first line above. The decision's conclusion "
             "is unaffected (most READ ops are still unreachable by category); "
             "its figure is measured against a mapping the live path doesn't "
             "use. Measured 2026-08-20 during the #1667 build.")
    L.append("")
    L.append("READ-ONLY INVARIANT (re-measured, not assumed)")
    if violations:
        L.append(f"  🔴 {len(violations)} non-READ keys carry a flip_group: "
                 f"{', '.join(violations)}")
        L.append("     WorkflowEntry.__post_init__ should make this impossible. "
                 "Do not flip anything until this is explained.")
    else:
        L.append(f"  ✅ 0 of {len(other_keys)} non-READ keys carry a flip_group "
                 "(enforced at construction, WorkflowEntry.__post_init__)")
    L.append("")
    L.append("HOW TO FLIP  (PIPER_INVERSION_LIVE_CATEGORIES accepts all three)")
    L.append("  a wave      : PIPER_INVERSION_LIVE_CATEGORIES=read_status")
    L.append("  one op      : PIPER_INVERSION_LIVE_CATEGORIES=show_standup")
    L.append("  a category  : PIPER_INVERSION_LIVE_CATEGORIES=QUERY   (flip-1's "
             "unit; sweeps the b-list above)")
    L.append("  revert      : unset it. Default-empty = fully dark.")
    return "\n".join(L) + "\n"


async def run(dry: bool, out: Optional[Path]) -> int:
    from services.intent_service.inversion_router import derive_routing_grammar

    p0_rows = p0.load_corpus()
    armed_rows = load_armed_corpus()
    grammar = derive_routing_grammar()
    n_aliases = sum(len(op.aliases) for op in grammar.operations)
    n_armed = sum(1 for r in armed_rows if r["condition"] == "armed")
    n_control = len(armed_rows) - n_armed
    planned = len(p0_rows) + 2 * n_armed + n_control
    print(
        f"phase0 corpus: {len(p0_rows)} rows (untouched) · armed extension: "
        f"{len(armed_rows)} rows ({n_armed} armed ×2 conditions + {n_control} "
        f"control ×1) · planned calls: {planned}"
    )
    print(
        f"grammar: {len(grammar.operations)} canonical operations (+NONE/CLARIFY), "
        f"{n_aliases} aliases collapsed input-side"
    )
    if dry:
        for r in armed_rows:
            if r["condition"] == "armed":
                print(f"--- {r['pair']} state block ({len(r['_state_block'])} chars):")
                print(r["_state_block"])
        print("dry run complete: fixtures build the real dataclass, serialize "
              "under the cap, pairs are twinned. No LLM calls made.")
        return 0

    from services.llm.clients import LLMClient

    llm = LLMClient()  # #322 constructor-injection; keys via app config path
    t0 = time.monotonic()

    armed_only = [r for r in armed_rows if r["condition"] == "armed"]
    controls = [r for r in armed_rows if r["condition"] == "control"]

    p0_decisions = await _route_rows(p0_rows, llm, grammar, label="p0 ")
    with_decisions = await _route_rows(
        armed_only, llm, grammar, state_key="_state_block", label="armed+snap "
    )
    without_decisions = await _route_rows(armed_only, llm, grammar, label="armed-bare ")
    control_decisions = await _route_rows(controls, llm, grammar, label="control ")
    duration = time.monotonic() - t0

    for r, d in zip(controls, control_decisions):
        r["_decision"] = d
    armed_with = {r["pair"]: d for r, d in zip(armed_only, with_decisions)}
    armed_without = {r["pair"]: d for r, d in zip(armed_only, without_decisions)}

    p0_scored = p1.score(p0_rows, p0_decisions)
    all_decisions = p0_decisions + with_decisions + without_decisions + control_decisions
    calls = sum(getattr(d, "llm_calls", 0) for d in all_decisions)
    errors = sum(1 for d in all_decisions if getattr(d, "outcome", "") == "error")
    refused = sum(1 for d in all_decisions if getattr(d, "outcome", "") == "refused")
    llm_note = (
        f"{calls} LLM calls incl. repair retries across {len(all_decisions)} "
        f"routed (row, condition) pairs; {errors} ERROR, {refused} REFUSED"
    )
    report = build_report(
        p0_scored, armed_rows, armed_with, armed_without, grammar, llm_note, duration
    )
    out = out or DEFAULT_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(f"wrote {out}")
    tot_match = sum(c["match"] for c in p0_scored["per_cat"].values())
    tot_asserted = sum(c["asserted"] for c in p0_scored["per_cat"].values())
    print(
        f"phase0 context-free: {tot_match}/{tot_asserted} · {calls} LLM calls · "
        f"{errors} ERROR · {refused} REFUSED · {duration:.0f}s"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="validate fixtures, no LLM")
    ap.add_argument(
        "--audit",
        action="store_true",
        help="print the #1667 flip-unit coverage table (no LLM, no corpus)",
    )
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    if args.audit:
        # Handled before run(): the audit touches no corpus, no fixtures and
        # no event loop — it is a registry read.
        print(flip_coverage_audit(), end="")
        sys.exit(0)
    sys.exit(asyncio.run(run(args.dry, args.out)))
