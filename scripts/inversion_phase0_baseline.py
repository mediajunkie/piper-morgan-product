#!/usr/bin/env python3
"""Inversion Phase-0 baseline (#1595) — score the CURRENT router per category.

m-43 (name the layer): this runner has two modes measuring two different
things, and says so in its output:

  --surface1  (default) Deterministic. For each corpus row, what does
              PreClassifier.pre_classify claim? Reports claim-rate and,
              where the row asserts an expected destination, agreement.
              NO LLM runs. This is "what surface 1 does", not "what the
              user gets" — rows surface 1 declines fall to the LLM in
              production, which this mode does NOT execute.

  --full      The production decision: IntentClassifier.classify with the
              pre-classifier active (surface 1 wins where it claims, LLM
              otherwise). Requires LLM keys; costs one call per undeclined
              row. This IS "what the user gets" at the classification layer
              (rails/floor still downstream).

Per-category tables always state denominators (m-44). REVIEW rows are
reported as a separate bucket — they are questions, not passes or failures,
and folding them into a score would manufacture either optimism or alarm.

Usage:
  POSTGRES_PORT=5433 venv/bin/python scripts/inversion_phase0_baseline.py [--full] [--out PATH]
"""

import argparse
import asyncio
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CORPUS = ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml"


def load_corpus() -> list:
    rows, cur = [], None
    for raw in CORPUS.read_text().splitlines():
        m = re.match(r'  - phrase: "(.*)"$', raw)
        if m:
            if cur:
                rows.append(cur)
            cur = {"phrase": m.group(1).replace('\\"', '"')}
            continue
        if cur is None:
            continue
        # `framing` (2026-10-09): TestExecuteVocabCoverage reads `framing: question`
        # — documented there, but this loader never parsed it until a row needed it.
        for key in ("category", "expected", "framing"):
            m = re.match(rf"    {key}: (\S+)$", raw)
            if m:
                cur[key] = m.group(1)
        m = re.match(r'    (source|surface1_claim|probe_verdict|notes): "(.*)"$', raw)
        if m:
            cur[m.group(1)] = m.group(2)
        # Arch's (a), 2026-10-06: an asserted TARGET SET rides the row as a
        # JSON flow mapping (valid YAML flow syntax, emitted by the builder).
        m = re.match(r"    expected_args: (\{.*\})$", raw)
        if m:
            cur["expected_args"] = json.loads(m.group(1))
    if cur:
        rows.append(cur)
    return rows


_RAIL = None


def _rail():
    """alias -> shared entry point, REGISTRY-DERIVED (Arch condition: aliases
    are input-side; two names sharing a rail entry are the same operation —
    exact-name matching under-credits, e.g. set_reminder IS create_reminder)."""
    global _RAIL
    if _RAIL is None:
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        _RAIL = get_action_workflows()
    return _RAIL


def same_operation(a: str, b: str) -> bool:
    if a == b:
        return True
    ea, eb = _rail().get(a), _rail().get(b)
    return ea is not None and eb is not None and ea.entry_point == eb.entry_point


def matches(expected: str, category, action) -> bool:
    cat = (category.value if hasattr(category, "value") else str(category or "")).lower()
    act = str(action or "").lower()
    if expected.startswith("action:"):
        return same_operation(act, expected.split(":", 1)[1].lower())
    if expected.startswith("category:"):
        return cat == expected.split(":", 1)[1].lower()
    return False


def expected_framing_for_row(row: dict) -> "str | None":
    """The EXPECTED ``collaboration_gate.FRAMING_*`` value for a corpus row
    (#1970 steps (1)/(6)), derived — never hand-edited onto any of the
    corpus's ~570 rows:

    - a row already carrying the corpus's own ``framing: question`` or
      ``framing: declarative`` annotation (read by
      ``tests/test_architecture_enforcement.py::TestExecuteVocabCoverage``)
      expects ``FRAMING_AMBIGUOUS`` — a question or a declared wish is not
      an imperative, whatever action it names.
    - otherwise, a row whose ``expected:`` action resolves to a rail entry
      declared ``EffectClass.WRITE`` expects ``FRAMING_EXECUTE``. This is
      exactly the scope
      ``TestExecuteVocabCoverage._write_or_allowlisted_destructive_corpus_rows``
      + ``test_every_corpus_write_phrase_classifies_execute`` already assert
      classifies EXECUTE via the real gate classifier (minus that test's
      DESTRUCTIVE half — Arch's design item 3: framing is irrelevant for
      DESTRUCTIVE, CONFIRM in every cell, so a DESTRUCTIVE-resolved row gets
      NO framing expectation here, never ``FRAMING_EXECUTE``) — reused as
      ground truth, not re-derived. A row that test's own scope excludes
      (no rail entry, no registered verb, or already covered by the
      question/declarative branch above) gets no expectation either.
    - "compose" framing has no corpus marker today — no ``framing: compose``
      row exists, and no test names a compose-phrasing row set. Rows are
      NOT guessed into this bucket; the caller reports the resulting zero
      count rather than silently omitting it (m-44).
    - everything else: ``None`` (not scored for framing).

    The ``manage_repos`` special case mirrors
    ``TestExecuteVocabCoverage._repo_management_list_literals``'s own
    resolution (manage_repos has no rail entry of its own — it is resolved
    to ``list_repos`` (READ) or ``link_repo`` (WRITE) by the 1 list-shaped
    literal inside ``PreClassifier.REPO_MANAGEMENT_PATTERNS``, never a
    second hand-written regex) — duplicated here by the same precedent that
    test's own docstring cites (no shared import boundary from scripts/
    into tests/), not re-invented.
    """
    from services.intent_service.collaboration_gate import FRAMING_AMBIGUOUS, FRAMING_EXECUTE
    from services.intent_service.pre_classifier import PreClassifier
    from services.shared_types import EffectClass

    if row.get("framing") in ("question", "declarative"):
        return FRAMING_AMBIGUOUS

    expected = row.get("expected", "")
    if not expected.startswith("action:"):
        return None
    action = expected.split(":", 1)[1]

    workflows = _rail()

    if action == "manage_repos":
        # last literal in REPO_MANAGEMENT_PATTERNS is the 1 LIST-shaped one
        # (identity pointer, not a copy of the regex text).
        list_literals = list(PreClassifier.REPO_MANAGEMENT_PATTERNS)[-1:]
        is_list_shaped = PreClassifier._matches_patterns(row["phrase"].lower(), list_literals)
        canonical = "list_repos" if is_list_shaped else "link_repo"
    else:
        from services.intent_service.inversion_router import derive_routing_grammar

        grammar = derive_routing_grammar()
        canonical = grammar.alias_to_canonical.get(action, action)

    entry = workflows.get(canonical)
    if entry is None or entry.effect != EffectClass.WRITE:
        return None
    return FRAMING_EXECUTE


def framing_expectation_denominators(rows: list) -> dict:
    """Per-value counts of ``expected_framing_for_row`` over a row set —
    stated denominators (m-44), never left implicit. Always reports all
    three gate values plus ``none`` even when zero, so a caller cannot
    mistake "not computed" for "computed as zero rows"."""
    from services.intent_service.collaboration_gate import (
        FRAMING_AMBIGUOUS,
        FRAMING_COMPOSE,
        FRAMING_EXECUTE,
    )

    counts = {FRAMING_EXECUTE: 0, FRAMING_AMBIGUOUS: 0, FRAMING_COMPOSE: 0, "none": 0}
    for r in rows:
        value = expected_framing_for_row(r)
        counts[value if value is not None else "none"] += 1
    return counts


async def run(full: bool, out: Path | None) -> None:
    from services.intent_service.pre_classifier import PreClassifier

    pre = PreClassifier()
    classifier = None
    if full:
        from services.intent_service.classifier import IntentClassifier
        from services.llm.clients import LLMClient

        # #322: pass llm_service via constructor (the container is per-app,
        # NOT a singleton — a fresh ServiceContainer() here would stay
        # uninitialized from the classifier's lazy access). Same shape the
        # surface-1 counterfactual probe used for its 52 calls.
        classifier = IntentClassifier(llm_service=LLMClient())

    rows = load_corpus()
    results = []
    for r in rows:
        phrase = r["phrase"]
        claimed = pre.pre_classify(phrase)
        entry = dict(r)
        entry["s1_claimed"] = claimed is not None
        if claimed is not None:
            entry["s1_result"] = f"{claimed.category.value}/{claimed.action}"
            entry["decision"] = (claimed.category, claimed.action)
        if full:
            if claimed is None:
                try:
                    intent = await classifier.classify(phrase, use_cache=False)
                    entry["decision"] = (intent.category, intent.action)
                    entry["llm_result"] = f"{intent.category.value}/{intent.action}"
                except Exception as e:  # probe discipline: ERROR is recorded, never a faked verdict
                    entry["llm_result"] = f"ERROR({type(e).__name__})"
                    entry["error"] = str(e)[:200]
            # claimed rows: surface 1 IS the production decision
        results.append(entry)

    mode = "FULL CHAIN (production decision)" if full else "SURFACE-1 ONLY (claims, not outcomes)"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    lines = [
        f"# Inversion Phase-0 baseline — {mode}",
        f"Run: {stamp} · corpus: {CORPUS.name} ({len(rows)} rows) · scripts/inversion_phase0_baseline.py",
        "",
        "LAYER (m-43): "
        + (
            "full classification chain — surface 1 where it claims, LLM otherwise. "
            "Rails/floor are downstream and NOT measured here."
            if full
            else "surface-1 claims only. Unclaimed rows fall to the LLM in production, "
            "which this run did NOT execute — claim-rate is not a correctness rate."
        ),
        "",
    ]

    per_cat = defaultdict(lambda: {"n": 0, "review": 0, "asserted": 0, "match": 0, "claimed": 0})
    for e in results:
        c = per_cat[e["category"]]
        c["n"] += 1
        if e["s1_claimed"]:
            c["claimed"] += 1
        if e["expected"] == "REVIEW":
            c["review"] += 1
        else:
            c["asserted"] += 1
            if "decision" in e and matches(e["expected"], *e["decision"]):
                c["match"] += 1

    lines.append("## Per-category (denominators stated — m-44)")
    lines.append("")
    lines.append(
        "| category | rows | s1-claimed | asserted-expected | match | REVIEW (open questions) |"
    )
    lines.append("|---|---|---|---|---|---|")
    tot = {"n": 0, "review": 0, "asserted": 0, "match": 0, "claimed": 0}
    for cat in sorted(per_cat, key=lambda c: -per_cat[c]["n"]):
        c = per_cat[cat]
        for k in tot:
            tot[k] += c[k]
        note = "—" if not full and c["asserted"] > c["claimed"] else ""
        lines.append(
            f"| {cat} | {c['n']} | {c['claimed']} | {c['asserted']} | "
            f"{c['match']}{'*' if note else ''} | {c['review']} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['n']} | {tot['claimed']} | {tot['asserted']} | {tot['match']} | {tot['review']} |"
    )
    if not full:
        lines.append("")
        lines.append(
            "*surface-1-only: an asserted row surface 1 declines shows as non-match here "
            "while production may still route it correctly via the LLM — run --full for the "
            "production number. This table CANNOT be read as a correctness score.*"
        )

    lines.append("")
    lines.append("## Row detail")
    lines.append("")
    lines.append("| phrase | category | expected | s1 | decision | verdict | source |")
    lines.append("|---|---|---|---|---|---|---|")
    for e in results:
        s1 = e.get("s1_result", "declined")
        dec = e.get("llm_result", e.get("s1_result", "—" if not full else "?"))
        if e["expected"] == "REVIEW":
            verdict = "REVIEW"
        elif "decision" in e:
            verdict = "MATCH" if matches(e["expected"], *e["decision"]) else "MISMATCH"
        elif e.get("error"):
            verdict = "ERROR"
        else:
            verdict = "unmeasured (s1 declined; no LLM this mode)"
        lines.append(
            f"| {e['phrase'][:60]} | {e['category']} | {e['expected']} | {s1} | {dec} | {verdict} | {e['source'][:50]} |"
        )

    text = "\n".join(lines) + "\n"
    if out:
        out.write_text(text)
        print(f"wrote {out}")
    # console summary
    print(
        f"{mode}: {tot['n']} rows · s1 claimed {tot['claimed']} · "
        f"asserted {tot['asserted']} · matched {tot['match']} · REVIEW {tot['review']}"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    # #1812 aftermath: bind the developer's own keys (no server-key fallback).
    sys.path.insert(0, str(ROOT / "scripts"))
    from dev_key_binding import developer_keys_bound

    with developer_keys_bound():
        asyncio.run(run(args.full, args.out))
