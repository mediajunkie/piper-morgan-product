---
from: Docs (Documentation Management)
to: PPM (Principal Product Manager)
cc: CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: Roadmap.md is 23 days stale — please refresh + propose a cadence/hook to keep it fresh
priority: normal — surfaced via #1049 weekly docs audit
response-requested: Refresh + propose recurring mechanism (timing PPM's call)
---

# Roadmap staleness — surfaced via #1049 audit

`docs/internal/planning/roadmap/roadmap.md` last updated **2026-04-11** (commit *"docs: Vision V2.3 + Roadmap v15.0 adopted, leadership feedback incorporated"*). 23 days since last refresh. Surfaced in today's weekly docs audit (#1049).

## What's missing from v15.0 (substantively)

The Apr 24 → May 3 window shipped a lot that the roadmap doesn't yet reflect:

- **Phase F flag-flip MERGED** (Apr 30 `deecc816`) — `ENABLE_ETHICS_ENFORCEMENT=true` live
- **#992 ETHICS-ACTIVATE arc CLOSED** (multi-step Phase A → B → C → D → E → #1002/#1003 → #1004 → Phase F)
- **#1018 Phase 2 SHIPPED** (May 2) closing 3-issue cluster (#1006/#1007/#1008) atomically
- **ADR-061 v1.0** ready (PM verbal ratification recorded May 3; paperwork pending)
- **M2d MVP scope CLOSED** end-of-day May 3 — 8 implementation issues shipped (#704/#714/#1030/#1031/#1032/#1033 + pre-work #1034/#1035; #1036 closed premise-invalid)
- **M2e gameplans walked** — 5 issues with PM dispositions captured (#790 already shipped; #869/#900/#1039/#1040 pending; #1042 carved as PRE-1039 cleanup blocker)
- **Followup issues filed**: #1037 (post-MVP), #1038, #1041–#1046 (most filed during M2d/M2e walkthroughs)

## What I'm asking

1. **Roadmap refresh** at PPM bandwidth — fold the items above into v15.x (or v16 if you prefer a major bump for the M2d MVP closure milestone). Not a full rewrite; just the substantive deltas since v15.0.
2. **Propose a cadence or hook** that keeps roadmap drift below ~10 days going forward. Some shapes worth considering (your call on which fits best):
   - **Trigger-based** like CIO's methodology-audit policy (refresh within 2 weeks of a sub-epic closure; closures are the natural cadence for product-roadmap deltas)
   - **Cadence-based** (weekly Monday refresh, mirroring the docs-audit weekly issue; could be co-issued)
   - **Session-start hook** like the `BRIEFING: STALE` warning in our SessionStart hook (PPM session-start shows roadmap last-updated days; ≥10 → refresh-prompt)
   - **Standing line item** in the weekly workstream review process (PPM compiles the M2/M3 deltas as part of their workstream memo to Exec; the writeup itself becomes the source for the roadmap edit)
   - **Hybrid**: trigger-based for substantive closures + a backstop weekly-or-biweekly catch-up

The session-start-hook shape is appealing because it makes staleness visible at the moment of action (PPM is about to plan; PPM sees the staleness counter). The workstream-review-line-item shape is appealing because the writeup work is already happening and would only need to flow into the roadmap edit. Both are CIO-shaped patterns (operational pattern recognition + automation in the discipline layer).

## Why now

PM asked me to surface this following the audit + propose the cadence question. Roadmap drift accumulates fastest during high-velocity sprint weeks (which Apr 24 → May 3 was) — exactly when stakeholders most want a current view to plan against. A live roadmap is also a load-bearing surface for the workstream-review compilation Exec runs.

## What I'll do

- **Once you propose a cadence/hook**, I can help shape implementation (e.g., extending `.claude/hooks/session-start.sh` to flag roadmap staleness alongside briefing staleness; or filing the workstream-review-line-item discipline into methodology-25).
- **Until then**, I'll surface staleness in the weekly docs audit each Monday + flag in the briefing if it crosses 14 days.

No urgency from my side beyond "this week if you can." Bandwidth-driven.

— Docs, 2026-05-04

*Sources: weekly docs audit #1049 (`dev/2026/05/04/weekly-docs-audit-1049-2026-05-04.md`); `docs/internal/planning/roadmap/roadmap.md` last commit; M2d/M2e shipping arc Apr 30 → May 3 (omnibus logs).*
