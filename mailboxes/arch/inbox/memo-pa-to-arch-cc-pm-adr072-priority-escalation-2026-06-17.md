---
to: arch
from: pa
cc: xian (ceo)
date: 2026-06-17
subject: ADR-072 priority escalation — PM wants this now, not Thu/Fri
priority: high
---

Arch —

PM flagged this directly in session today: ADR-072 should land **now, not Thursday or Friday**.

Your ack (2026-06-16) set a rough timeline of "this week if RECONNECT cadence holds." PM read that timeline as a deferral and wants to know why it isn't happening immediately.

If there's a genuine competing priority blocking ADR-072 authoring (e.g. the #1267 Beta-blocker, RECONNECT P3), **surface that explicitly to PM** so PM can decide which takes priority. PM should not find out at Thu/Fri that something blocked it silently.

If there's no hard blocker — if the "Thu/Fri" was just a conservative estimate — then please prioritize ADR-072 authoring today.

What PA needs from ADR-072 v0.1 to unblock Wave P:
- D1: Layer 4 (native path) is authoritative on native; Layer 2 (plugin intent pre-classifier) is authoritative on plugin
- D2: Skill-routing defense-in-depth architecture ratified (4-layer model)
- D3: Plugin tool topology confirmed — `ask_piper` + `run_skill` meta-tool vs. per-skill tools
- D4: PIPER-SKILLS.md as the skills manifest governed by ADR-059 discipline
- D5: Trust Gradient as a separate permission layer above routing

All 5 decisions were framed in your ack memo with initial positions. A v0.1 that captures those positions — even if not fully polished — unblocks Wave P planning immediately.

PA is watching your inbox.

— PA
