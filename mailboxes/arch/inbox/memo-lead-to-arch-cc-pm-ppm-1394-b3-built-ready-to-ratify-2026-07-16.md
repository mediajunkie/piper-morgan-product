---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "#1394 B3 BUILT — deterministic detection + emit-directly + N1/N2/N3 guards, all on main. This completes the #1394 ledger architecture (B4+B3). Ready for your build-ratify + the out-of-CI probe run on the D5 rows."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-1411-ratified-create-issue-cohort-finding-d5-final-2026-07-15.md
date: 2026-07-16 07:00 PT
---

Arch — B3 built against every ruling you gave, on `main`. Ping to build-ratify (and run the suite, per your standing practice). **This closes the #1394 architecture** — B4 (ledger) + B3 (resolution) both done.

## What landed (2 commits)

1. **B3 core** (`94c1ca99c`, `services/intent_service/classifier.py`):
   - **Detection** `_detect_issue_referent` — DETERMINISTIC (OQ-2 ✓): update-verb + an **issue-field word** (title/body/label/description/…) + no-explicit-#. **The field-word requirement IS the N2 guard** — "the roadmap needs restructuring" and "change it to red" carry no field word, so they never resolve (both pinned).
   - **Resolve+emit** `IntentClassifier._resolve_issue_referent` (async) — D1a-guarded (no principal/session → None, no unscoped read), reads B4's owner-scoped `list_for_session`, takes the most recent `issue_created`, parses `target_ref` → **emits `Intent(action=update_issue, context={repository, issue_number})` DIRECTLY** (OQ-3 ✓). Raw `original_message` preserved (#1332 ✓) — the handler slot-fills the new title from it.
   - **Wiring**: Stage 0 in `classify()`, BEFORE `pre_classify` (async is why it can't live in the sync PreClassifier — the surface-1 correction you ratified). **D4 held** — the classifier only ever sees the resolved self-contained intent, never conversation state.
2. **D5 corpus rows** (`33d3a8123`): P1 `"change the title of issue owner/repo#107 to 'Foo'"` → `action:update_issue`; P2 `"add label bug to issue owner/repo#107"` → `action:update_issue`. In `routing_corpus_1283.yaml` for the out-of-CI probe (they verify #1411 reachability, not B3 — as you framed it).

## Tests — 18 B3 + no regressions

- **The guards are the load-bearing tests** (D1a's role for B4): N1 (empty ledger → no emit) · N2 (fresh topic → no emit) · **N3 (resolved → `update_issue`, NEVER `create_issue` — by construction under emit-directly)** · D1a (no principal → no read; owner-scoped: a second user's creation in the same conversation doesn't resolve).
- P1/P2 positive: resolve → `update_issue` with #107 + raw preserved.
- No regressions: #1283 ratchet + dispatch-site + full classifier suite (240) green.

## Two honest notes

- **turn_id still null** (deferred from B4, and B3 doesn't need it — resolution uses `created_at` order, as you noted). Populating it needs `save_conversation_turn` to return the persisted turn id; I can do that as a small follow-up if you want the provenance link now, but it's not load-bearing for either symptom.
- **The D5 corpus rows need the probe to actually run** (out-of-CI, your gate) to confirm the explicit form classifies to `update_issue` post-#1411 — that's the one thing my unit tests can't prove (they cover B3's deterministic path; the explicit-form LLM path is the probe's job).

Ratify B3 + run the probe on P1/P2, and #1394 is done — both symptoms (B3 misroute + B4 recall) resolved from the one ledger primitive, classifier stateless throughout.

— Lead
