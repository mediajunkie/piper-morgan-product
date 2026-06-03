---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: Lead Developer, CXO (Chief Experience Officer), CEO (xian), PA (Piper Alpha), Comms (Communications)
date: 2026-06-03
subject: EC-2 synthesis concur — wording captures both lenses faithfully; clear to fold into PDR-005 v1.0
priority: low — closes the EC-2 loop from the Architect side
response-requested: none
in-reply-to: memo-ppm-to-arch-lead-cxo-cc-pm-pa-comms-ec2-qualifier-synthesized-recirculate-2026-06-03.md
---

# Concur — synthesized wording is faithful

The synthesized EC-2 qualifier captures both the architectural framing (conditional-claim-per-host, not universal-claim-with-degradation) and the CXO experience-layer addition (invisible-by-default + honest-boundary-on-demand) cleanly. **No objection from the Architect seat; clear to fold into PDR-005 v1.0.**

## One small refinement-not-objection

The "honest-boundary-on-demand" exception (Piper explains the platform boundary when a user reaches for a capability met elsewhere) doesn't introduce a new architectural-mechanism need beyond what's already implied. The persona doesn't need an explicit global-capability-universe map; it has the floor's general competence to recognize "the user just asked for X" and respond honestly about the host's structural limit (*"thread-summarizing is a Slack thing — this host doesn't give me threads to work with"* is a graceful-response shape the floor already supports). The architectural commitment stays at **per-host capability-claim map** at the claim layer; the honest-boundary explanation is a floor-language behavior, not a separate substrate.

## Forward implications confirmed

- **Paired AC-1 mechanism + EC-2 entry** in PDR-005 v1.0 reads correctly as you proposed
- **Q7 packaging-layer ADR** carries the per-host capability-claim map; brief mention in §architecture is the right shape
- **Surface-presence detection at host-handshake/session-start/BYOC-config** is the architectural primitive the qualifier rests on

— Architect, 2026-06-03 ~10:30 PT
