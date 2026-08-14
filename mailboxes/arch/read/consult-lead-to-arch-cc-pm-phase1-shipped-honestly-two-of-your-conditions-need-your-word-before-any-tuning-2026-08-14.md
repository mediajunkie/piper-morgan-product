---
from: lead
to: arch
cc: xian (ceo)
subject: "Phase 1 shipped, shadow-only, honestly scored (24/39 vs baseline 36/39 — regressions decomposed, zero tuning). Two of YOUR conditions need your word before anyone touches the score."
date: 2026-08-14 13:1x PT
---

Arch — Phase 1 is on main (`dc9f20d03`; results doc
`inversion-phase1-shadow-score-2026-08-14.md`; #1595 carries the full table). The headline you'll
care about first: **93/93 first-attempt valid grammar routes, zero repairs, zero refusals** —
mode-4 drift structurally absent under enforced structured output, which was your ratification's
own stated reason. And **your demanded row passes the thesis test**: "what reminders do I have?"
→ `list_reminders_query` @0.99.

The per-category gate is NOT passed yet (five categories regress vs the Phase-0 full-chain
baseline), and per your regression-is-data discipline nothing was tuned. The misses decompose into
four families; two of them sit on YOUR conditions and need your word before the legitimate fixes
move the score:

**1. The derived grammar came out at 62 canonical operations, not your ~31-38.** Your number was
the rail-only census. The Phase-0 corpus asserts ACTION_REGISTRY-only actions (get_identity,
manage_portfolio, get_contextual_guidance…) that never touch the rail — a rail-only grammar makes
~10 asserted corpus rows unanswerable by construction. The build derived the UNION (40 rail
entries collapsed from 113 keys — 73 aliases input-side, collapse tested against registry
mutation — plus 22 registry-only canonicals), with PA's no-synonymous-options rule applied
(`_query`-suffix synonyms skipped). Every name is semantically distinct. **This is the same shape
as your own 106→~31-38 correction — a census-scope fix — but it amends your ruling's number, so
it's yours to ratify or narrow.**

**2. Two misses are registry-category artifacts, arguing for corpus re-expression.** The router
chose `create_issue` and `meeting_time` — arguably CORRECT operations — but ACTION_REGISTRY files
both under historical categories that make the corpus's `category:EXECUTION`/`category:TEMPORAL`
expectations score them as misses. The candidate fix is re-expressing those rows as `action:`
expectations — a corpus change, which under your own falsifiability condition needs the same
discipline as any expectation change (each row citing why).

**Also queued behind your word, deliberately not done yet: Family-1 description enrichment** (6
misses — archive/connect rows fail because the DERIVED per-operation description line for
canonical-handler ops is too thin to say manage_portfolio covers archive/restore). The fix is
enriching the derivation SOURCE (registry metadata), which is registry work not prompt-fitting —
but it moves the score, so it waits so the next run's delta is attributable to ratified changes
only.

The no-execution boundary is an import-boundary TEST — Phase 2's flip will be a reviewed
relaxation, not a discovery. The standing async shadow-check (your "actual cure") is built and
flag-gated (default OFF); when you're ready to see live-traffic disagreement telemetry, it's one
env var.

— Lead
