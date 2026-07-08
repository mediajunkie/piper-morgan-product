"""#1283 behavioral routing probe — run the corpus through the REAL classifier chain.

Step 2 of the three-step #1283 plan (static audit → behavioral probe → CI
enforcement). Loads ``tests/fixtures/routing_corpus_1283.yaml``, classifies each
phrase with the live ``IntentClassifier`` + ``LLMClient`` (real LLM calls — ~30
calls, cents), and reports where each one would actually route:

- ``action:<name>`` rows PASS when the classifier emits that action AND the
  action is registered on the dispatch rail (``get_action_workflows()``) — i.e.
  it dispatches pre-floor, deterministically.
- ``category:<NAME>`` rows PASS when the classified category matches. If the
  classifier ALSO emits a rail-registered action, that's flagged (routes via the
  action rail before category handling — not a failure, but Arch should see it).
- ``REVIEW`` rows are never pass/fail — the observed routing IS the deliverable.

Run (env-stripped per CLAUDE.md — inherited empty ANTHROPIC_API_KEY shadows .env):

    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
      venv/bin/python scripts/routing_probe_1283.py [--out report.md]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml  # noqa: E402

CORPUS_PATH = PROJECT_ROOT / "tests" / "fixtures" / "routing_corpus_1283.yaml"


async def run_probe(out_path: Path | None) -> int:
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows
    from services.llm.clients import LLMClient

    register_default_workflows()
    rail = set(get_action_workflows().keys())

    corpus = yaml.safe_load(CORPUS_PATH.read_text())["corpus"]
    classifier = IntentClassifier(llm_service=LLMClient())

    rows = []
    for i, row in enumerate(corpus, 1):
        phrase, expected = row["phrase"], row["expected"]
        try:
            intent = await classifier.classify(phrase, use_cache=False)
            action = intent.action or ""
            category = intent.category.name if intent.category else ""
            on_rail = action in rail
            if expected.startswith("action:"):
                want = expected.split(":", 1)[1]
                verdict = "PASS" if (action == want and on_rail) else "FAIL"
                if action == want and not on_rail:
                    verdict = "FAIL(mode-2: emitted but NOT on rail)"
            elif expected.startswith("category:"):
                want = expected.split(":", 1)[1]
                verdict = "PASS" if category == want else "FAIL"
                if verdict == "PASS" and on_rail:
                    verdict = "PASS(note: action-rail dispatch precedes)"
            else:  # REVIEW
                verdict = "REVIEW"
            rows.append((phrase, expected, action, category, round(intent.confidence, 2), on_rail, verdict))
            print(f"[{i}/{len(corpus)}] {verdict:<40} {phrase!r} -> action={action!r} category={category}")
        except Exception as e:  # a crash on one row shouldn't kill the run
            rows.append((phrase, expected, "<ERROR>", type(e).__name__, 0.0, False, f"ERROR: {e}"))
            print(f"[{i}/{len(corpus)}] ERROR {phrase!r}: {e}")

    passed = sum(1 for r in rows if r[6].startswith("PASS"))
    failed = sum(1 for r in rows if r[6].startswith("FAIL") or r[6].startswith("ERROR"))
    review = sum(1 for r in rows if r[6] == "REVIEW")
    print(f"\n== {passed} PASS / {failed} FAIL / {review} REVIEW of {len(rows)} ==")

    if out_path:
        lines = [
            f"# #1283 behavioral routing probe — {datetime.now():%Y-%m-%d %H:%M} PT",
            "",
            f"Corpus: `{CORPUS_PATH.relative_to(PROJECT_ROOT)}` ({len(rows)} rows). "
            f"Rail size at probe time: {len(rail)} registered actions.",
            f"**Result: {passed} PASS / {failed} FAIL / {review} REVIEW**",
            "",
            "| phrase | expected | got action | got category | conf | on rail | verdict |",
            "|---|---|---|---|---|---|---|",
        ]
        for p, e, a, c, conf, r, v in rows:
            lines.append(f"| {p} | `{e}` | `{a or '—'}` | {c} | {conf} | {'✓' if r else '✗'} | {v} |")
        out_path.write_text("\n".join(lines) + "\n")
        print(f"report -> {out_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    sys.exit(asyncio.run(run_probe(ap.parse_args().out)))
