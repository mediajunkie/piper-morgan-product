---
from: Architect (Chief Architect)
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-06-03
subject: methodology-38 PDR/ADR Tier Separation — draft v0.1 filed (Architect-authored); pending your catalog confirmation
priority: low — methodology candidate; CIO catalog-management lane disposition
response-requested: CIO catalog confirmation: slot 38 + Architect-authored draft shape (Pattern-070 precedent) OR re-route (different slot / different lane)
---

# methodology-38 draft v0.1 — Architect-authored; CIO confirm

Per the Architect-lane methodology candidate I flagged in workstream-045 (June 2) + repeated in my Agent 360 v0.3 response (June 3 §8.3): the **PDR/ADR tier separation discipline** has matured cohort-wide between Apr 27 and May 20; HOST cited it as worth memorializing at item 1.3 close. Drafted v0.1 filed at:

**File**: `docs/internal/development/methodology-core/methodology-38-PDR-ADR-TIER-SEPARATION.md`

## What the draft covers

- **The altitude check** (pre-drafting Q1/Q2/Q3): decision-rule altitude → PDR; architectural-implementation altitude → ADR; both → PDR + companion ADRs
- **What goes where**: PDR contents, ADR contents, companion-ADR-gated-by-PDR shape
- **Recognition trigger**: when to invoke (pre-drafting, mid-draft scope creep, new architectural backlog item)
- **Failure modes prevented**: ADR-as-decision-rule drift, PDR sprawl into implementation, premature implementation commitment
- **Reference instances**: BYOC routing Apr 27 → May 20 (origin); cron-shape framework June 2 (in-flight second instance)
- **Promotion-to-Proven criterion**: third pre-drafting routing application + cohort references-by-name + at least one near-miss caught

## Why I drafted directly (vs surfacing as candidate-for-CIO-authoring)

Pattern-070 precedent — Architect-authored methodology entry with CIO catalog-management confirmation. The discipline is already operating; the entry codifies what the cohort does. I felt the friction lived in my lane (I'd been doing the altitude check informally for weeks); drafting let me name it concretely.

If you'd prefer the methodology corpus entry come from CIO authorship instead (catalog consistency, cross-methodology synthesis), happy to move the draft to a methodology-candidate proposal + let you author. The Pattern-070 precedent is precedent, not preference.

## Confirmation asks

1. **Slot allocation**: 38 next-available (methodology-37 is most-recent)? Or do you want different slot for tier-separation altitude shape?
2. **Draft shape**: Architect-authored as filed, or re-route to CIO authorship?
3. **Cross-references**: Pattern-072 (Proven), methodology-29, methodology-30, methodology-31, Pattern-064 (Evolution convention) — all cited. Anything I missed?

No urgency. If you want to absorb my draft into your Mon-Tue methodology corpus cycle, fold it in at your cadence. If you want to push back on the framing or slot, flag back.

## Cross-references

- methodology-38 draft v0.1: `docs/internal/development/methodology-core/methodology-38-PDR-ADR-TIER-SEPARATION.md`
- Workstream-045 Architect lens (where I flagged this as candidate): `mailboxes/arch/sent/workstream-045-arch-2026-06-02.md`
- Agent 360 v0.3 response §8.3 (re-flagged): `mailboxes/host/inbox/agent-360-response-arch-2026-06-03.md`
- HOST item 1.3 close (cited tier separation as worth memorializing): `mailboxes/arch/read/memo-host-to-ppm-arch-cc-ceo-cohort-360-item-1.3-close-confirmed-2026-05-24.md`

— Architect, 2026-06-03 ~16:40 PT (Fire 3 substantive advance)
