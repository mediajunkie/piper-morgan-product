---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: CXO (Chief Experience Officer), Architect, Comms (Communications Director), PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-18
subject: Surface 2 build is unblocked — PDR-005 v0.4 sufficient for per-conversation privacy build
priority: normal — Phase 2.2 trigger memo per Round 2 architecture
in-reply-to: memo-lead-to-cxo-cc-arch-ppm-comms-ceo-exec-pa-mux-ui-phase-2-lead-dev-lane-scoping-2026-05-17.md
---

# Surface 2 build unblocked

Per PM's May 18 directive (Option Y, two separate sufficient-signals) + Lead Dev's Phase 2.2 sub-phase architecture: **Surface 2 build is unblocked.**

PDR-005 v0.4 (`dev/active/PDR-005-bring-your-own-chat-draft-v0.4-2026-05-18.md`) has sufficient content for the per-conversation privacy build:

- **§Decision §Persona portability** — variance hierarchy locked (zero tolerance for capability/ethics; ≤5% tone)
- **§Decision §MCP server scope** — privacy semantics + cross-client memory continuity sub-surface obligations (Surface 1 + Surface 6 implications captured)
- **§Decision §Bespoke UI commitment depth** — Round 2 ratification absorbed; per-conversation privacy for 1.0; per-message reserved post-1.0
- **§Consequences for architecture AC-1/AC-4** — adapter-template parameterization + runtime dispatch; privacy toggles flow through RequestContext
- **§Consequences for product** — Pattern-064 prevention applies at product layer (privacy toggle that "appears registered" but doesn't change behavior fails loudly)

## Scope clarifications for Surface 2 build

- **1.0 scope: per-conversation `is_private` toggle** with UI surface; existing data-model `is_private` flag is the substrate
- **NOT 1.0 scope**: per-message privacy granularity (schema migration + cascade rules + per-turn UI) — reserved post-1.0 expansion path
- **MUX doc**: Class A + Class D triggers; full MUX doc warranted per Round 2; CXO-Comms voice-pass coordination pattern per PM May 18 Surface 7 memo applies
- **Audit envelope coupling** (#1018 Phase 2): privacy toggle write captures in audit envelope; cross-host audit semantic deferred but `host_id` field commitment from v0.4 mechanism set #4 enables future migration without breaking changes

## What this signal IS

- **Build-unblocking signal** per Phase 2.2 architecture: Lead Dev can start Surface 2 build whenever bandwidth lands
- **PDR-005 v0.4 = canonical reference for Surface 2 product commitments** — any future PPM iteration (v0.5+ absorbing CXO §experience) refines voice/experience details, not the build-relevant decision rules above

## What this signal is NOT

- **Not gating CXO MUX doc drafting** — CXO + Comms voice-pass cadence runs independently per Round 2 ratification
- **Not committing voice prose** — voice work runs alongside build via CXO→Comms→CXO-review iteration pattern
- **Not gating Surface 4** — Surface 4 sufficient-signal memo is separate (filed in parallel)

— PPM, 2026-05-18
