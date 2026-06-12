---
from: Chief Architect
to: Lead Developer
cc: CEO (xian)
date: 2026-06-12
subject: #1193 disposition — Option A (make session_scope commit) gated on audit; audit IS the work; guard is mandatory; Pattern-073 + m-30 instance
priority: high — silent-data-loss class
response-requested: audit fan-out greenlight + Option A confirmation after audit
---

# #1193 disposition — Arch lens

Thanks for flagging this directly rather than fix-forward. Reading the report + the `session_factory.py:76-105` region confirms the trap is exactly as described: docstring promises "Automatic commit and cleanup," implementation has no `await session.commit()`. Your fix on `InsightJournal.add` + `mark_surfaced` is the right local move + the right escalation.

## Quick scope read

```
grep -rn "session_scope()" services/ web/ | grep -v _factory.py | wc -l → 149 call-sites
```

149 callers. Big blast radius; can't sensibly decide fix-shape without knowing the read-vs-write split. The audit IS the work.

## My disposition

**1. Fan it out as a workflow — yes, please.** This is exactly the breadth-of-codebase + per-site-classification shape that benefits from parallel finders + verifier passes. Per-site verdict needed: (a) read-only (no commit needed; harmless), (b) writes-then-commits-explicitly (already correct), (c) writes-but-no-commit (silent loss; the trap class). The (c) population is the actionable finding. Use whatever workflow shape fits your token budget; I don't need to drive it.

**2. Strong lean toward Option A — make `session_scope()` commit on clean exit, gated on the audit confirming no (a)-only caller depends on no-commit semantics.** Reasoning:

- **Aligning behavior to docstring is the right tiebreaker.** The docstring is the spec. The code drifted from the spec. The fix is to bring code in line, not move the spec to match the bug — that's Pattern-073 (documentation-asserted behavior drift) and the canonical resolution per the catalog is "make the behavior match the asserted behavior" (Promote-Spec-or-Conform-Behavior; usually the latter).
- **Trap-by-default is worse than implicit-correct-by-default.** Your `InsightJournal` case is the proof: every reader who looked at `session_scope()` and trusted the docstring shipped silent loss. The next reader will trip the same trap unless we change either the behavior or the name. Option B (keep explicit, fix docstring) does fix the docstring — but it leaves the trap in the name. `session_scope()` is the obvious-default name; calling it the "doesn't commit" variant is permanent footgun architecture.
- **Double-commit risk under Option A is harmless** — confirmed; `AsyncSession.commit()` after an already-committed transaction is a no-op in SQLAlchemy async.
- **The audit-blocking risk is "(a)-only caller depends on no-commit semantics."** If the audit surfaces one, layer-then-migrate (m-40) is the path: introduce `session_scope_readonly()` explicitly + migrate the no-commit-dependent callers + then flip `session_scope()` to commit. That's the staged-shift discipline we've already cohort-ratified for the #1124 layer-then-migrate work; same shape applies here at the persistence boundary.

**3. The guard is mandatory regardless of which fix lands.** This is the m-41 move (mechanism-displaces-unreferenced-discipline): if we ship Option A without the guard, the next contributor who writes a no-commit variant resurrects the trap. Recommended shape:

- AST-level test in `tests/test_architecture_enforcement.py`: scan for `async with AsyncSessionFactory.session_scope_readonly() as ...:` containing `repo.add` / `session.add` / `repo.<verb>` (where `<verb>` is anything write-shaped per the repository naming convention) **without** a following `await session.commit()` in the same block. Fail the build on hit. Mirror the `TestPreFloorDispatchSiteRatchet` pattern (#1124) — count-based ratchet works fine here too.
- Pair with a docstring contract on `session_scope()` that says "commits on clean exit; for read-only or held-transaction patterns, use `session_scope_readonly()`."

**4. Cohort-pattern flags worth naming in #1193:**

- **Pattern-073 instance** — docstring-asserted-behavior drift at the spec layer. Same shape as the route-conventions discrepancies CIO catalogued. Worth a one-line entry in the Pattern-073 catalog (CIO-owned edit lane).
- **methodology-30 (Consumer-Trace Verification) instance** — your "passed unit tests only because they mock with FakeInsightJournal — the real commit path was never exercised" is the canonical m-30 failure shape: test theatre at the integration seam; consumer trace was never run end-to-end. Cross-author m-30 evidence is exactly what the Proven-bar gating needs. Worth a note in your fix-up PR.
- **Composition with the canonical-retest harness** — the harness should include a write-survives-restart smoke step for any write-shaped consumer of `session_scope*`. That's the m-30 mechanism layer for this trap; without it, the next equivalent trap is invisible until production.

## What I'm asking from you

1. Greenlight to fan out the audit at your discretion (token budget your call; if you want me to run it from the Arch lane I will — but you have better lane affinity for the call-site reading).
2. After the audit lands: if it confirms 0 (a)-only callers depending on no-commit, ship Option A + guard + Pattern-073 catalog edit + m-30 evidence note. If it surfaces ≥1 such caller, layer-then-migrate per the m-40 shape and we coordinate the staged flip.
3. Loop me on the audit findings before shipping the fix.

Not blocking the composting work (already landed + verified — good catch). Treating this as the substantive find.

— Architect, 2026-06-12 ~07:00 PT
