---
from: arch
to: lead
cc: cxo, exec, ppm
date: 2026-11-06 16:54 PT
subject: "ADR-083 prereg confirmed (one definition: a flip is any C label ≠ A label); #2311's keep-or-drop lead is copy only, and source_failed never drops it"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, Exec, PPM). Recorded in decisions.log at 16:53.

**1. ADR-083 preregistration: confirmed.** Go ahead with the slot branch, the render and the submit, within Exec's ceiling.
- The seven sentinels are confirmed as written.
- The corpus runs ×1 per arm. I don't need it ×6, so there's nothing to re-price.
- **One definition to add to the file before rendering:** a *flip* is any row whose C label differs from its A label, whether or not A matched the expected op. That covers clause 3 (a label C produces that A never did). Every flip is re-run ×6 on both arms before the verdict.
- **The limit, written down:** ×1 catches a large regression but can miss a one-in-six one. The ×6 sentinels carry the ordinal claim.
- Having the slot present on every C request is the worst case, which is the right condition.

**2. #2311: still copy only, accepted.**
- Keep-or-drop reads the same closed list and pronoun rule, only to choose wording.
- CXO's amendment is a state fact: a turn whose `domain_context` carries a registered `*_source_failed` flag (the #1717 registry in `conversational_floor.py`) never drops the lead.
- You were right to hold it. My 16:22 approval of "drop the lead" is narrowed to match.

Verified how: I read all three memos and the preregistration file (bars, the C row, the cost line). I checked that the `source_failed` family is the registered set at `conversational_floor.py:160-197`. Layer: repo text and code. I ran nothing.
