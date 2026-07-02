# PPM Duty-Cycle Escalations — Attention Doc

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "attention doc" per v0.6 architectural decision 2 (reframed escalations file; no new doc). Holds open questions for PM that surface during autonomous fires — what PM should weigh in on when bandwidth lands.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

**Severity typology** (per CXO Framing 2, cross-cohort convention): blocking | drift | uncertainty | complete-stale

---

## Open escalations for PM

(none open — PDR-005 v1.0 ratified 6/5; see Resolved.)

### RESOLVED 2026-06-05 — PDR-005 v1.0 RATIFICATION — ~~decision~~ PM RATIFIED
**PM ratified PDR-005 v1.0 (BYOC) 6/5** (PA relay) — Foundational PDR; Docs swapping draft → canonical; Q6/Q7 ADRs unblocked. Comms voice-pass on outward copy remains PM's (non-gating). Was: ↓

### 2026-06-03 — PDR-005 v1.0 RATIFICATION-READY — decision
**Severity**: uncertainty (awaiting PM gate; not blocking other work)
**Summary**: **PDR-005 (BYOC) is now ratification-ready** — all v1.0 inputs folded into `dev/active/PDR-005-bring-your-own-chat-draft-v0.6-2026-06-03.md`: EC-2 platform-affordance-bounded qualifier **fully cohort-concurred** (Arch + CXO + Lead); **Comms external-language frame** folded (§External-Language Frame; your voice-pass is final on outward copy); BYOC packaging **plugin-correct**; CT citations **v2.3.2**.
**Decision for PM**: ratify PDR-005 v1.0 → it becomes canonical (the BYOC distribution model formalized as a Foundational PDR alongside 001-004), per the v18 ratify-the-draft precedent. Companion ADRs Q6/Q7 (context-package format + packaging-layer abstraction) then proceed in Architect's lane.
**Note**: outward public copy still gets your voice-pass — the Comms frame is scaffolding, not final words. No action needed until bandwidth lands; v0.6 holds clean.

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
