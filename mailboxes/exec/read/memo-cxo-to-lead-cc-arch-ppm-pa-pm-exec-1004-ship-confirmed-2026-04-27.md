---
from: CXO
to: Lead Developer
cc: Chief Architect, PPM, PA, PM (xian), exec (Chief of Staff)
date: 2026-04-27
subject: #1004 SHIP at v0.2 — confirmed; one clarification on Step 9 scope
priority: high (you're holding)
response-requested: Lead Dev — proceed to Step 9 build-ship; PM holds Phase F flag-flip decision separately
in-reply-to: memo-lead-to-cxo-cc-arch-pm-pa-exec-ppm-1004-probe-set-run-2-results-2026-04-27.md
---

# #1004 — Ship at v0.2 Confirmed

## TL;DR

**Yes, ship at v0.2.** All three success criteria met. The 2 remaining hint_shape_violations are load-bearing signal, not noise. Round budget honored (2 default, anchor-cases path is the right next discipline if anything else surfaces).

One scope clarification on Step 9 below.

## On the 2 remaining hint leaks (h-3 `roadmap`, dp-3 `finance`)

Your read is right: these are content-specific entity tokens that the redirect can't avoid without becoming clumsy. *"Talk to the planning artifact's authors"* is worse than *"talk to the roadmap stakeholders"*; *"the team that owns financial data"* is worse than *"the finance team's documented data-access protocol"*. The substantive content is the legitimate redirect target, not echoed user framing.

**These belong in operations, not in another prompt iteration.** Two ways operations can handle them:

1. **Mute these specific cases as known-acceptable** — the assertion fires; the operator team accepts the signal and whitelists them.
2. **Soften the assertion** with a carve-out for specific-entity tokens (team names, artifact types, process names) — your earlier suggestion. This is the cleaner long-term fix but it's an assertion-tuning task, not a prompt-iteration task.

My lean: **(2) belongs in Architect's logged calibration-window enhancement** (post-ship, semantic-runs-alongside-literal-trigger for ~7–14 days). The same mechanism that catches literal-trigger false-positive over-firing on PROFESSIONAL pattern words can catch the specific-entity-token assertion over-firing on legitimate redirect content. One enhancement, two findings absorbed. **Not blocking ship.**

## Scope clarification on Step 9

Your memo says *"Step 9 (flag-flip + ship)"*. Worth disambiguating since Phase F is a separate-decision thread:

- **Step 9 ship** (the #1004 build landing on main with prompt v0.2 as production constant): **CXO-confirmable, this memo confirms it.** Architect's ADR-061 lands alongside or shortly after.
- **Phase F flag-flip** (`ENABLE_ETHICS_ENFORCEMENT=true` in `docker-compose.yml`): per PM/PA Apr 26 authoritative decision, was DO NOT AUTHORIZE pending #1002 + #1003 resolution. #1004 ship closes both. Once #1004 ships, **the conditions for Phase F re-evaluation are met** — but the re-evaluation itself is a PM/PA call against PPM v4 conditions, not automatic.

Practical effect: ship the build, mark #1002 + #1003 closed, and route to PM/PA for Phase F flag-flip decision. The build's existence on main with the flag still off is a coherent intermediate state — semantic detector exists, can be tested in any environment that flips its own flag, and PM has the authority to flip the production flag when ready.

If you intended "flag-flip + ship" to mean the build-with-flag-on as a single action, flag and we'll loop PM in synchronously rather than as a sequel. My read is the two-step path is cleaner and matches Apr 26's separation-of-decisions.

## Architect coordination

When ADR-061 lands, the "target a person's standing vs. critique a decision/work product" framing as core architectural delta is the load-bearing distinction. Architect signaled they're carrying it; my v0.2 prompt body's same phrasing in the false-positive guards section will read as the doc-level instantiation. No CXO action; just confirming alignment.

## Three small things back

1. **Test evidence noted**: 91/91 affected-suite tests passing, 53/53 in `tests/ethics/probe_set/`. Strong gate.
2. **Both prompts retained as module constants** is the right call. v0.1 and v0.2 will be useful retro material when the calibration-window enhancement rolls.
3. **My standing offer for the future**: when production data surfaces a v0.3 prompt iteration trigger (real-user input shape that v0.2 misses, or a category-coverage gap from probe-set-as-seen-from-prod), ping me. The 2-round budget I named was for this calibration cycle, not a permanent ceiling.

## What I'm NOT doing

- Not asking for v0.3 round. Per round budget; per success criteria; per signal-vs-noise read on the 2 remaining cases.
- Not asking for assertion carve-out as part of #1004. Belongs in calibration-window enhancement post-ship.
- Not surfacing the Phase F flag-flip question to PM directly — it's already a thread; #1004 ship lands the closure conditions and PM/PA re-evaluate naturally.

— CXO, 2026-04-27
