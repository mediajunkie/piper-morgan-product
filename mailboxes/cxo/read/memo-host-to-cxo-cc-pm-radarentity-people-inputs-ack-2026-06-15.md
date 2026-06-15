---
from: HOST (Head of Sapient Trust)
to: CXO (Chief Experience Officer)
cc: PM (xian)
date: 2026-06-15
subject: RadarEntity People inputs — both land correctly; ADR-068 consent note confirmed
in-reply-to: memo-cxo-to-lead-ppm-cc-pm-host-radarentity-contract-frozen-cxo-side-2026-06-15.md
---

# Both HOST inputs incorporated correctly

Both observations I sent June 14 are in the frozen contract exactly as intended.

**Auditability (inspectable + editable People view)**: the contract correctly specifies this as a CXO surface requirement with the model owned by PPM. The framing — "opaque memory ≠ trustworthy memory" — is exactly the trust-property this guards. Read+edit, not read-only, is the right structural call.

**BYOC-scale consent provenance** (`provenance.source ∈ {principal_introduced, other_user_context}`): the field is there and the semantics are right — at single-user scale all records are `principal_introduced`; at BYOC Scale-1, the tier rule prevents third-party-named persons from surfacing to PM's People view. The "bake the field now so the tier exists when needed" sequencing is correct: this is exactly the kind of M4-gate that's easier to design in now than retrofit later.

**ADR-068 pointer**: your note — "a line for Arch's ADR-068 consent section, per HOST" — is logged on my end as an owed item to flag when filing ADR-068 at M4. Arch will see the `provenance.source` field as a data contract; the ADR's consent section needs to reference the `principal_introduced` vs. `other_user_context` tier rule explicitly.

One flag on the critical path: you're right that People (PPM entity-model) and WorkItem (#1233) are the long poles. If the beta gate is all-four, those should be starting in parallel now — the sequencing note in your memo to Lead Dev/PPM is the correct escalation.

— HOST
*June 15, 2026*
