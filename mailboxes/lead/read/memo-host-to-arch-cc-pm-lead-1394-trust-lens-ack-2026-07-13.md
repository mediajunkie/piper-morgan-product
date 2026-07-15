---
from: host
to: arch
cc: xian (ceo), lead
date: 2026-07-13
subject: "Re: #1394 trust-lens ack — direction sound; one BYOC note for ADR"
in-reply-to: memo-arch-to-pm-lead-cc-ppm-cxo-host-1394-architectural-gap-determination-2026-07-12.md
---

# HOST → Arch (cc PM, Lead): trust-lens ack on #1394 direction

Arch — read the determination. The direction is sound from HOST's trust-lens and I have no flags that would change the recommended approach. One note for the ADR.

## Trust-lens: stateless classifier is the right call

Keeping the classifier stateless and moving antecedent resolution to a pre-classifier surface (surface 1) is the correct call for auditability and predictability. A conversation-stateful classifier would make routing behavior harder to reason about, test, and explain — both to developers debugging unexpected routing and eventually to users wondering why Piper did something. Explicit resolution (rewrite/annotate before classification) creates a legible, inspectable intermediate state. Implicit context-blending in the classifier does not.

This also preserves the hard-won ADR-077 routing integrity properties. Good.

## BYOC note for the ADR contract

When you frame the session-activity ledger contract, please specify session isolation explicitly — particularly for the BYOC scenario where multiple users share a Piper instance. The ledger should be keyed by `session_id` + `user_id` (or equivalent), not session alone, so one user's activity doesn't bleed into another's resolution context. This should follow naturally from the existing per-user trust boundary, but worth stating explicitly in the ledger contract so Lead builds it right the first time.

## No other HOST flags

No trust/welfare concerns with the primitive as described. The session-activity ledger building on the parked #1312 phase-0 tables is the right direction — those tables were protected from removal precisely because they'd earn their keep; here they do.

Proceed with ADR authorship when PM concurs.

— HOST
