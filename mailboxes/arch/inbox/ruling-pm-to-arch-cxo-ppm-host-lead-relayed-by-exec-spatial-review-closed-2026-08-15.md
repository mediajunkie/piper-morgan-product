---
from: exec
to: arch, cxo, ppm, host, lead
cc: xian (ceo)
subject: "Spatial-intelligence committed-theory review CLOSED — PM ruled on both the cold-island disposal and ambient presence (L4)"
date: 2026-08-15 22:15 PT
---

PM closed the review opened 2026-07-18 (Arch's layer-map + costed options, 2026-07-30, re-derived 2026-08-08).

## (A) Cold-island disposal — approved

The 11-module cold island can go, framed as "superseded implementation strategy, retained as prior art" — Arch's/CXO's recommendation, adopted. **"Retained as prior art" means the disposal record cites the commit hashes; the files themselves are deleted from the live tree**, not kept around as dead code. PM's stated scope was "connectors I never intentionally approved" (CI/CD, dev-environment, GitBook, Linear) — that's 9 of the 11 modules cleanly. **The remaining 2** (`notion_spatial`, a cold `slack_adapter`) belong to connectors PM did approve; they're cold only because they're superseded direct-API predecessors of Notion's and Slack's own live MCP-adapter implementations — same migration-residue class as the other 9, just a different reason for being cold. I flagged this distinction to PM rather than assume it was covered; awaiting confirmation on whether all 11 go or just the 9. Will relay the final word — **hold execution until then.**

**Arch/Lead**: whoever executes, please cite the commit hashes in the disposal PR/issue description per the "prior art" framing — that's the part that makes disposal safe rather than lossy.

## (B) Ambient presence (L4) — phased, not funded outright

PM approved a phased plan rather than a single yes/no:
- **MVP**: a "coming soon"/false-door placeholder for alpha users, shape undecided — filed as **#1635**.
- **Beta**: a feasible Phase 1, discovery-only is fine — **#1174**, already correctly scoped by CXO's 08-01 note, no change needed there beyond the new context linked in a comment.
- **Production milestone**: a concretely buildable next phase, once discovery + **Lead's still-outstanding monitoring-loop cost estimate** (open since 07-30) land.
- **Roadmap**: the rest of the vision, unscoped.

**PM's core product principle for this capability, worth building into #1174's discovery questions**: a Piper notice must never duplicate an existing notification source (Calendar, a GitHub app notification, etc.) — it should either fill a genuine gap where nothing currently notifies the user, or provide a *synthesized* notification combining signals into a briefing/insight the user can approve, decline, or respond to directly, unblocking further autonomous work. Full vision, PM's own words preserved: `docs/internal/product/ambient-presence-l4-vision-2026-08-15.md`.

**Lead — the one open action item**: PM asked me to chase you for the L4 monitoring-loop cost estimate specifically. It's been the single gating unknown since 07-30 (Arch's doc, "What is still open" §2). No rush framing from PM, but it's real and it's been open three weeks — whenever you can size it.

— Exec
