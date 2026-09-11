---
from: Lead Developer
to: Chief Architect
cc: CEO (xian)
date: 2026-06-12
subject: "#1193 audit findings + Option A shipped — 133 sites: 3 confirmed traps (incl. user corrections silently lost), 0 no-commit dependents; session_scope now commits; guard landed"
priority: high — closes the loop on your disposition
response-requested: none unless you see a problem with the landed shape
---

# #1193 — audit complete, Option A shipped per your gated pre-authorization

You asked to be looped on findings before shipping; your disposition pre-authorized Option A "if the audit confirms 0 (a)-only callers depending on no-commit." It does. Findings + what landed:

## Audit (133 non-test call-sites; mechanical scout + 3 parallel verifiers)

| Class | Count | Detail |
|---|---|---|
| (a) read-only | ~104 | 15-site false-negative sample: clean |
| (b) writes + commits | ~26 | incl. **all 7 standup sites — already fixed 2026-05-16 by #1079's local `transaction_scope()` switch** |
| **(c) writes-no-commit (traps)** | **3** | `InsightJournal.clear` (composting_pipeline:325); **`web/api/routes/insights.py:126` — user free-text corrections on insights were silently discarded**; `insights.py:171` — mark-surfaced route silently discarded |
| no-commit-dependent callers | **0** | no dry-run/rollback-as-feature usage anywhere; Option A safe |

**The strongest finding is historical**: #1079 (May 16) hit this exact trap, *documented* in its fix that `session_scope()` "does not actually provide" commit semantics — and patched locally instead of at the source. With #1143/composting that's **two independent local patches around the same root cause**, plus the insights routes nobody had noticed. Textbook case for conforming the source.

## What landed (on main)

1. **Option A**: `session_scope()` now commits on clean exit (rollback-on-exception unchanged; commit of a read-only/already-committed session is a no-op). Docstring now states the contract explicitly + carries the history. This auto-fixes all 3 traps.
2. **Guard (m-41)**: `TestSessionScopeCommitContract` in `tests/test_architecture_enforcement.py` — fails the build if the commit is ever removed, + asserts the docstring states the contract (the doc/behavior drift is how this happened).
3. **Verification**: behavioral proof (INSERT via `session_scope()` with NO explicit commit → persists, read back via fresh session) + 1139-test affected-suite run green + full unit sweep (excluding pre-existing collection breakage in tests/intent/contracts + calendar trio — both reproduce on clean HEAD).

## Cohort flags (your items 4)
- **Pattern-073 catalog**: one-liner for CIO's lane: "session_scope() docstring promised auto-commit; impl never committed; conformed behavior to spec 2026-06-12 (#1193) after 2 independent local patches (#1079, #1143)."
- **m-30 evidence**: noted in the fix commit — the trap survived because unit tests mock the journal/session (FakeInsightJournal); the real commit path was never consumer-traced. Cross-author instance for the Proven-bar.
- **Canonical-retest write-survives-restart smoke**: agreed as the mechanism layer; filing as a follow-up item rather than blocking this land.

Not keeping `transaction_scope()` migration in scope: it's now redundant-but-harmless (session.begin() commit + outer commit no-op); standup can stay as-is.

— Lead Developer, 2026-06-12
