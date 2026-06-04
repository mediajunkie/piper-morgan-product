# PPM Duty-Cycle Escalations — Attention Doc

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "attention doc" per v0.6 architectural decision 2 (reframed escalations file; no new doc). Holds open questions for PM that surface during autonomous fires — what PM should weigh in on when bandwidth lands.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

**Severity typology** (per CXO Framing 2, cross-cohort convention): blocking | drift | uncertainty | complete-stale

---

## Open escalations for PM

### 2026-06-03 — ROADMAP v18 READY FOR RATIFICATION — decision
**Severity**: uncertainty (awaiting PM gate; not blocking)
**Summary**: Roadmap **v18 is substantively complete and ready for your ratification** (#1128). Both section reviews now absorbed — PA §M5/BYOC (6/2) + CIO §Methodology (6/3). Draft: `dev/active/roadmap-v18-draft-2026-06-02.md` (HTML render also available: `roadmap-v18-2026-06-02.html`, pre-§Methodology-absorption — can re-render on ratification).
**Decision for PM**: ratify v18 → Docs swaps into canonical `roadmap.md` (per v15→v16 precedent). One nuance to confirm: I treated the **Comms external-language frame** as a parallel polish input (external-facing language) that can fold at ratification or as v18.1, NOT as gating the internal canonical — flag if you'd rather hold for it.
**Updates since escalation (still ratification-ready, now cleaner)**: CT citations reconciled to canonical v2.3.2 (6/3); **BYOC packaging model corrected — plugin is canonical, not MCPB** (PM 6/1 clarification via PA, folded 6/3). v18 now carries the correct packaging model + correct CT version. **No action needed from PM until bandwidth lands; v18 holds clean and is packaging-correct.**

---

## Resolved escalations

### Escalation — 2026-05-28 — adoption-decisions — RESOLVED

**Severity**: uncertainty → **resolved Fire-0**
**Summary**: Two duty-cycle adoption decisions (cron interval; go-autonomous timing).
**Resolution**: PM chose **hourly interval** + **launch Fire-0 now** (2026-05-28 ~7:55 AM PT). Offset `:47` confirmed. Cron `2aba0768` registered + Fire-0 ran. Triage lane (#1128 + #967) accepted.

---

*Duty-cycle attention doc; PM reads when bandwidth lands. Inbox-empty + no-open-escalations is a valid IDLE state.*
