---
from: PM (xian) — drafted by PPM at PM direction
to: Lead Developer
cc: CXO, PA, Architect, exec (Chief of Staff)
date: 2026-04-26
subject: Phase F flag-flip decision — DO NOT AUTHORIZE; ENABLE_ETHICS_ENFORCEMENT remains false in docker-compose.yml
priority: high
response-requested: Lead Dev — acknowledge and hold the flag-flip; continue #1002 + #1003 work toward eventual re-evaluation
status: PM decision (authoritative)
---

# Phase F Flag-Flip Decision — DO NOT AUTHORIZE

## Decision

**`ENABLE_ETHICS_ENFORCEMENT` remains `false` in `docker-compose.yml`.**

The Phase F flag-flip is **not authorized** at this time. Lead Dev: please hold the flag in its current state. No production change. Continue the #1002 and #1003 scoping/fix work; Phase F can be re-evaluated when that work resolves and follow-up evidence sharpens the picture.

## Basis

PM accepted PPM's Phase F flag-flip recommendation v2 (`memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v2-2026-04-26.md`), which was grounded in Lead Dev's #1003 AC#1 diagnostic result.

**The load-bearing evidence**: Lead Dev's `flag=false` diagnostic comparison run (#1003 AC#1, ~11 seconds of compute) showed the response on S1 r2 is byte-identical between `ENABLE_ETHICS_ENFORCEMENT=true` and `=false` — same intent classification, same `floor_hit`, same absent boundary fields, same response shape. The flag is observably inert for this harassment-vector input on this code path.

**The product framing** (refined per Lead Dev's caveats):
The right read is not "the flag is theater across the board." It's **"the flag works for some BoundaryType categories and not for others, and the variance isn't documented."** S2 demonstrated PROFESSIONAL boundary engagement with a full audit envelope (`boundary_type: professional`, `decision_id: bd_1777168526167`); S1 r2 demonstrated HARASSMENT non-engagement on the same code-path family. Activating the flag without documenting and addressing that asymmetry would assert coverage we know we don't have for at least one BoundaryType.

**Why this is conservative, not perfectionist**: shipping `ENABLE_ETHICS_ENFORCEMENT=true` is a public-facing assertion that the ethics infrastructure is engaging on boundary-adjacent input. We have empirical evidence that it isn't engaging on at least one canonical boundary class. The cost of holding is one config-line that stays as it already is. The cost of authorizing prematurely is a Pattern-045 manifestation specific to ethics — gate passes, tests pass, infrastructure isn't doing the work, and we wouldn't know until something visibly bad happens or someone independently audits the audit envelopes.

## What this decision does NOT mean

- **Not a verdict on Phases A–D.** Those work. S2 demonstrated the BoundaryEnforcer infrastructure functioning correctly for PROFESSIONAL.
- **Not a permanent block on Phase F.** As soon as #1002 + #1003 resolve and follow-up evidence (the additional 2–3 harassment vectors Lead Dev mentioned, plus Architect scoping) sharpens the picture, the flag-flip can be re-authorized. The default is "blocks-flip-until-scoped," not "blocks-flip-permanently."
- **Not a verdict on the floor LLM's response quality.** The floor produced a 9/9 (CXO) / 8/9 (PPM) response on S1 r2 even without infrastructure engagement. The floor's general competence is real and valuable; it's also the masking signal that made this gap detectable only by running the diagnostic.
- **Not a closure of the C-axis rubric reconciliation** (separate thread, `memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md`). That work continues independently.
- **Not a closure of Phase E.** Phase E gate closes cleanly on the rubric verdict (all three scenarios PASS per the Apr 26 PPM/CXO scoring exchange). Phase E was always about *can the system produce colleague-level decline behavior on boundary-adjacent input*; it can. Phase F is the separate question of *does activating the flag cause that behavior*; the diagnostic answered that with "no, at least for harassment vectors via this code path."

## What's asked of each role

| Role | Action |
|---|---|
| **Lead Dev** | Acknowledge this decision and hold `ENABLE_ETHICS_ENFORCEMENT=false`. Continue #1002 + #1003 scoping/fix work in coordination with Architect. When convenient, run 2–3 additional rephrased harassment vectors through the r2 code path (~5 min compute) to confirm whether the no-op generalizes; report results. No timeline pressure. |
| **Architect** | Continue #1002 + #1003 scoping. The diagnostic result is decisive on activation today; your scoping is decisive on the fix shape and whether re-authorization can happen via a small patch or requires structural work. Both inputs needed before the flag-flip is reconsidered. |
| **CXO** | No new asks. Standing voice oversight on any production decline responses (when activation eventually happens) per the predecessor's framing. Continue C-axis rubric reconciliation thread when bandwidth allows. |
| **PA** | Situational awareness. If you see ethics-related signals in cross-pollination work or operational rhythm that bear on this decision, route them through normal channels. |
| **PPM** | Update Phase F recommendation memo when follow-up evidence (additional vectors, Architect scoping) lands. Track #1002 + #1003 to closure. |
| **Exec** | Add to open-items tracker as a held decision pending #1002 + #1003 resolution. |

## What re-opens this decision

PPM v2 named three update paths:

1. **AUTHORIZE WITH DOCUMENTED GAPS** if 2–3 additional rephrased harassment vectors *do* fire the BoundaryEnforcer (S1 r2 was an edge case, not a pattern), AND Architect scoping confirms the gap is bounded and documentable, AND a `known_pathological` tag is filed for the gap.
2. **CONTINUE TO HOLD** with refined understanding if 2–3 additional vectors confirm the no-op generalizes, AND Architect scoping reveals the fix is structural enough that the hold should remain in force until the structural fix lands.
3. **DO NOT AUTHORIZE — broader than thought** if S2-style flag-off comparison shows PROFESSIONAL (or other categories) also have flag-independent behavior despite their audit envelopes showing engagement.

Default in absence of update is the current decision: HOLD.

## Audit trail

- Phases A–D context: `memo-2026-04-23-from-lead-to-ppm-cc-cxo-pa-phase-e-sign-off.md`
- Phase E run results: `memo-2026-04-25-from-lead-to-ppm-cc-cxo-pm-pa-phase-e-run-results.md`
- PPM finding response → #1002 + #1003 escalation: `memo-ppm-to-lead-cc-pm-cxo-pa-arch-phase-e-finding-response-2026-04-25.md`
- Phase E S1 r2 results → exposed #1003: `memo-2026-04-26-from-lead-to-ppm-cc-cxo-pa-phase-e-s1-rerun-results.md`
- #1002 scoping request to Architect: `memo-2026-04-26-from-lead-to-arch-cc-ppm-pm-cxo-pa-1002-bypass-scoping.md`
- #1003 issue: [GitHub #1003](https://github.com/mediajunkie/piper-morgan-product/issues/1003)
- #1002 issue: [GitHub #1002](https://github.com/mediajunkie/piper-morgan-product/issues/1002)
- PPM/CXO scoring exchange: `memo-ppm-to-cxo-cc-pm-pa-lead-arch-exec-phase-e-scoring-exchange-2026-04-26.md`
- C-axis rubric reconciliation thread: `memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md`
- PPM Phase F recommendation v1 (pre-diagnostic): `memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-2026-04-26.md`
- Lead Dev #1003 AC#1 diagnostic result: `memo-2026-04-26-from-lead-to-ppm-cc-cxo-pm-arch-pa-exec-1003-diagnostic-result.md`
- PPM Phase F recommendation v2 (post-diagnostic): `memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v2-2026-04-26.md`
- **PM decision (this memo)**

---

— PM (xian), via PPM, 2026-04-26
