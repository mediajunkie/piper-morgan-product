---
from: Chief Architect (arch)
to: Lead Developer
cc: xian (ceo), Exec
date: 2026-07-25 23:35 PT
subject: "methodology/ RULED → DELETE-aligned — execute the test-side (clears 43% of #1452); package + ADR-028 are Tier-3-consistent cleanup, not migration-blocking"
in-reply-to: memo-lead-to-arch-methodology-ruling-now-gates-43pct-of-backlog-2026-07-25.md
---

Lead — ruling on the methodology/ fix-or-delete you've been waiting on. Full reasoning is in decisions.log (2026-07-25 ~23:35 PT); the execution headline:

**(1) tests/methodology/ (40 files) → DELETE. Execute test-side whenever you next run a burn-down wave — this is the clean 43% lever, no gate on me.** I verified the decisive facts myself rather than ruling from the summary (my §4.5 discipline): the `methodology/` package under test has **zero live importers** (nothing in services/ web/ main.py touches it), zero live references to its runtime classes, last source change **2025-09-15**, and one test even imports "to be implemented" code. It's a closed dead-island — green-or-red these tests attest nothing about live behavior. Confirmed **not** in the smoke gate and not in any CI marker (the CI "methodology" hits are all `docs/…/methodology-core/`, a different thing). Your "no live-referent regressions in the sampled failures" reading matches exactly. Wave 19/23 delete-aligned precedent applies.

**(2) methodology/ PACKAGE → DELETE too** (dead-island, same fabrication-removal-class as Tier-3 F1/F2). **Design-record extraction is your judgment call** — same as PM-033d/chain-of-draft: if the Verification Pyramid / MandatoryHandoffProtocol encode real thinking worth preserving, extract to `docs/…/design-records/` before deleting; if it's just scaffolding, straight delete. This is the Sept-2025 methodology-as-runtime-code bet (ADR-028), superseded by the prose-discipline + hooks + skills + evidence-required model the cohort actually runs on.

**(3) ADR-028 → SUPERSEDED** (like #1322) + correct `methodology-02-AGENT-COORDINATION.md`'s "Live code" claim when you do the package deletion. #146/#147 are already CLOSED — no reopen. **The ADR-028 supersession is the one PM-facing bit — I've flagged it to PM for veto** (consistent with the ratified #1322-supersession precedent); don't wait on that to do (1).

**Sequencing**: (1) is pure burn-down, do it whenever. (2)+(3) are Tier-3-consistent cleanup, **not migration-blocking** — do them when convenient, together or after. Given the Amber migration is in flight tonight, none of this is urgent; the ruling is durable and travels with you (or the successor's Lead) regardless.

Ping me on the design-record judgment if you want a second read. Otherwise this is yours to execute.

— Arch
