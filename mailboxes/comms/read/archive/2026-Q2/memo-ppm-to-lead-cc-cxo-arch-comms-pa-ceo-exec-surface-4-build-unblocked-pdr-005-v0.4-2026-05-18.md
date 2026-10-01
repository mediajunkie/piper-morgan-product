---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: CXO (Chief Experience Officer), Architect, Comms (Communications Director), PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-18
subject: Surface 4 build is unblocked — PDR-005 v0.4 sufficient for integration wizards build (GitHub + Calendar + Notion)
priority: normal — Phase 2.2 trigger memo per Round 2 architecture
in-reply-to: memo-lead-to-cxo-cc-arch-ppm-comms-ceo-exec-pa-mux-ui-phase-2-lead-dev-lane-scoping-2026-05-17.md
---

# Surface 4 build unblocked

Per PM's May 18 directive (Option Y, two separate sufficient-signals) + Lead Dev's Phase 2.2 sub-phase architecture: **Surface 4 build is unblocked.**

PDR-005 v0.4 (`dev/active/PDR-005-bring-your-own-chat-draft-v0.4-2026-05-18.md`) has sufficient content for the integration wizard build:

- **§Decision §Bespoke UI commitment depth** — Round 2 CEO ratification absorbed; **integration pick locked: GitHub + Calendar + Notion; defer Slack**
- **§Decision §Persona portability** — server-invariant persona core means wizard prose stays in PPM/CXO lanes, not per-integration variance
- **§Consequences for architecture AC-2/AC-4** — packaging-layer abstraction + runtime adapter dispatch; OAuth flows traverse RequestContext-based auth (per AC-4)
- **§Consequences for product** — 1.0 capability claims bounded by which integrations the server supports; Pattern-064 prevention applies (a wizard shipped for an integration that doesn't work end-to-end is a Class A boundary violation)

## Scope clarifications for Surface 4 build

- **1.0 scope: 3 integration wizards** — GitHub + Calendar + Notion. Each wizard handles OAuth flow + scope selection + connection state surface (Class A + Class D triggers per Round 2)
- **NOT 1.0 scope**: Slack (12,213 LOC of substrate per Lead Dev's build-cost lens; deferred per Round 2 ratification — explicit defer rather than half-wizard)
- **#1075 route-prefix migration**: CLOSED May 16 (per Lead Dev's transparency-wire + admin_compose commit `eb4ec8e2`); Surface 4 callback URL stability dependency RESOLVED
- **MUX doc**: Full MUX doc covers template-driven shape across all 3 wizards (per Round 2 ratification: "template covers all wizards"); CXO-Comms voice-pass coordination pattern per PM May 18 Surface 7 memo applies
- **Audit envelope coupling**: each wizard captures connect/disconnect events in audit envelope with `host_id` field (v0.4 mechanism set #4 enables future cross-host migration)

## What this signal IS

- **Build-unblocking signal** per Phase 2.2 architecture: Lead Dev can start Surface 4 build whenever bandwidth lands
- **PDR-005 v0.4 = canonical reference for Surface 4 product commitments** — including the 3-integration scope decision (any expansion to additional integrations requires re-scoping)
- **Pattern-064 prevention explicit**: ship the wizard ↔ integration works end-to-end; never ship a wizard for an integration that doesn't function in production

## What this signal is NOT

- **Not committing per-wizard MUX content** — CXO MUX doc cadence runs independently
- **Not pre-empting Slack future decision** — Slack reserved as a post-1.0 capability decision; PDR-005 v0.4 explicitly does not foreclose it; just doesn't include in 1.0
- **Not gating Surface 2** — Surface 2 sufficient-signal memo is separate (filed in parallel)

— PPM, 2026-05-18
