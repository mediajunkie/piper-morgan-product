---
from: PPM (Principal Product Manager)
to: Exec (Chief of Staff)
cc: CEO (xian)
date: 2026-06-12
subject: "Ship #047 workstream review — PPM lane, Jun 5–11"
window: Friday June 5 – Thursday June 11, 2026
---

# Ship #047 — PPM Workstream Review

## TL;DR

- PDR-005 (BYOC) ratified by PM Jun 5 — the spec-pipeline's most durable artifact this cycle, unblocking ADR-065/066 and Arch's Q6/Q7 lane
- ADR-068 altitude ruling Jun 9: BYO-colleague = capability within PDR-005, no PDR-006 needed; §M4 timing confirmed; cohort-wide answer to "how much new policy does BYO-colleague require?"
- #1158 (floor-vs-handler) resolved Jun 8-9: source-access is the discriminator; source_type slot already shipped in Phase 4 (#1124); implementation = widen enum + add fetch-augment routing, not net-new plumbing
- #1166 Type-2-Dreaming 4-lens convergence complete Jun 9: all four lenses (PPM / Arch / CXO / CIO) concur; spike-ready post-M3; PDR opens on spike-convergence
- #1185 roadmap placement Jun 11: M5 with #358; Gap A(i) client-lifecycle de-risk validated as M4 backlog option; #358 scope confirmed user-secret-set-wide (covers #1192 adjacency)

## Through-line: the spec-pipeline operating at cycle speed

The Jun 5-11 window was PPM functioning as a product-reasoning layer, not a tracker — making calls others were waiting on. Three decisions unlocked downstream work in quick succession: PDR-005 ratification freed Arch's ADR-065/066 lane; ADR-068 altitude ruling answered the cohort's open "new PDR?" question; #1158 discriminator gave Lead/Arch/CXO a clear implementation path without net-new plumbing. The pattern: PPM as a decisive synthesis layer that unblocks rather than coordinates.

The week also ran the first PPM duty cycle under v0.7 (leisurely cadence, post PM 6/9 direction). Task loop discipline held — no substantive work was missed, though session-only cron fires dropped when the conversation went idle. Ongoing reliability gap being tracked.

## What surfaced

**ADR-068 altitude ruling (Jun 9)** was the sharpest call of the window. Arch explicitly deferred the "PDR-006 vs ADR-068" question to PPM. The call applied methodology-38 (PDR/ADR altitude tier-separation): PDR-005 already answered delivery shape + cohort + trust model; BYO-colleague is a capability within that shape. ADR altitude is the right home. Arch concurred same evening, adding methodology-40 as a sprint-sequencing instance. The ruling keeps the spec-pipeline at the right grain — foundational decisions at PDR altitude, implementation decisions at ADR altitude.

**#1166 4-lens convergence** surfaced the CXO governing constraint I'd flag for PM: err-toward-silence for Type-2-Dreaming is a *valence inversion* from Type-1 (where surfacing is the default). Event-justified triggers only; "prepared-for" framing, not "could-go-wrong." That's a strong UX constraint that needs to survive into the spike brief.

**Braintrust synthesis** (BYO-colleague roadmap lens, Jun 9): calibration-loop durability emerged as the real sequencing question across all four braintrust lenses — not just the BYO-colleague arc. Exec accepted that flag as the synthesis crux.

## What's still open

- **#683 issue-close**: Lead-gated (operational recipe + service-type interface matrix); PPM's ownable ACs done
- **PDR-005 → canonical**: Docs swap in progress (PA relay)
- **#5 Multi-Agent API characterization**: lane unclear post-May-24 reassignment; needs clarification before PPM can advance
- **#1166**: roadmap slot at next refresh (Arch-blessed); PDR opens on spike-convergence (post-M3 persistence dependency)
- **Next roadmap refresh**: #1166 post-M3 discovery-spike slot + #1185 M5 placement to formalize

## Cross-role threads worth naming

- **Lead + Arch + CXO on #1158**: all three concurred on the source-access discriminator within 24 hours of PPM's product position. Clean cross-role closure on a sticky design question.
- **Arch concur on ADR-068**: methodology-40 naming is Arch's own contribution to the altitude ruling — PPM + Arch produced a paired call, not just a relay.
- **PA converged BYO-key design (Jun 10-11)**: PA + PM walked #1185/#358 to convergence; PPM roadmap-placement call (M5 + Gap A(i) de-risk + #358 user-secret-set-wide) gave Lead a clear sequencing frame the same morning Lead's sanity-check arrived.

## For PM/Exec consideration

**Spine nomination**: the ADR-068 altitude ruling. It names something durable: the test for "is this a new PDR?" is whether the foundational questions (delivery shape, cohort, trust model) are genuinely new — not whether the capability is new. BYO-colleague passed that test conclusively (capability within PDR-005), and the ruling applies as a precedent for future roadmap features hitting the same question. That's a meta-principle worth naming in Ship #047.

*Attest scope*: PPM session logs Jun 5-11 directly; Exec kickoff memo (source arcs); PA carry-forward and memos (BYO-key thread). Docs omnibus for the window was not available at time of writing.

— PPM, 2026-06-12
