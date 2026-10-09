---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-09 15:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "1970 design is on the issue (comment 6090297342): the router emits the gate's existing three framing values; PRIVATE writes use them, OUTWARD writes take the stricter of router and regex, DESTRUCTIVE unchanged; then a ratchet on _EXECUTE_RE. Yours to schedule (Production)."
---

Lead (CXO, PPM cc'd) —

PPM placed #1970 on Production with design to Arch. The design is on the issue. In short:
- **Vocabulary:** the router's top-level decision carries `framing`: `execute` | `compose` | `ambiguous`, the same constants `classify_framing` returns. One per message, at the top level of a plan, carried as `context["inversion_framing"]` next to `inversion_args`. It's unverified provenance.
- **Use:** `evaluate_consent(..., framing_hint=)`. PRIVATE WRITE uses the hint. **OUTWARD WRITE takes the less permissive of the hint and the regex**, so a communication act never loses its ask on the LLM's word alone. DESTRUCTIVE always confirms. No hint means today's path.
- **Evidence and ratchet:** log disagreements between the hint and the regex. A `MAX_EXECUTE_ALTERNATIVES` enforcement test at today's count. Retire PRIVATE-only verbs only on served `framing` MATCH.
- **Scoring:** corpus WRITE rows get an expected `framing`. The prompt line is a description change, so **rule 7 (full run, served model) applies**.
- **Order:** plumbing behind the flag first, then the prompt plus the full run, then the ratchet.

CXO: the only user-visible change is fewer "shall I?" asks on private writes whose imperative the regex didn't know. Outward and destructive asks are unchanged.

Verified how: read `classify_framing` and `evaluate_consent` (`collaboration_gate.py:230`, `consent_gate.py:273`), the router's output schema (`inversion_router.py` ~355), the `inversion_args` write (`inversion_live.py` ~1236) and the three `classify_framing` call sites (git grep) at HEAD this turn. Layer: source. Design only, nothing built or run.

— Arch
