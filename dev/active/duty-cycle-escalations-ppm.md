# PPM Duty-Cycle Escalations — Attention Doc

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "attention doc" per v0.6 architectural decision 2 (reframed escalations file; no new doc). Holds open questions for PM that surface during autonomous fires — what PM should weigh in on when bandwidth lands.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

**Severity typology** (per CXO Framing 2, cross-cohort convention): blocking | drift | uncertainty | complete-stale

---

## Open escalations for PM

(none — the v18-ratification decision resolved 6/3 evening; see Resolved below)

---

## Resolved escalations

### 2026-06-03 — ROADMAP v18 RATIFICATION — RESOLVED (PM ratified)
**Severity**: uncertainty → **resolved**. PM **ratified v18** 6/3 evening (PA relay). Both flagged confirmations ratified: Comms external-language frame is non-gating (folds at ratification or v18.1); ratification is on the packaging-correct version (MCPB→plugin fix folded 6/3) + CT-reconciled (v2.3.2). Docs is doing the canonical swap (v18 draft → `roadmap.md` + archive v16.0). #1128 PPM-complete; closes on Docs swap. PDR-005 line-376 "MCPB hybrid" flagged separately for PDR-005 v1.0 (not a v18 blocker).

### Escalation — 2026-05-28 — adoption-decisions — RESOLVED

**Severity**: uncertainty → **resolved Fire-0**
**Summary**: Two duty-cycle adoption decisions (cron interval; go-autonomous timing).
**Resolution**: PM chose **hourly interval** + **launch Fire-0 now** (2026-05-28 ~7:55 AM PT). Offset `:47` confirmed. Cron `2aba0768` registered + Fire-0 ran. Triage lane (#1128 + #967) accepted.

---

*Duty-cycle attention doc; PM reads when bandwidth lands. Inbox-empty + no-open-escalations is a valid IDLE state.*
