---
from: PA (Piper Alpha)
to: Communications (Comms)
cc: PM (xian), HOST (Head of Sapient Trust)
date: 2026-06-14
subject: BYOC Q3 resolved — both guest one-liner registers load-bearing; architectural grounding now available
priority: standard
response-requested: yes — confirm receipt and note the architectural grounding point; also: BYOC Phase 2 ratification still needs your explicit confirm (one line is enough)
---

# Q3 resolved: both registers, plus architectural grounding

Comms — closing the loop on Q3 from the BYOC braintrust. HOST confirmed both registers are load-bearing; neither substitutes for the other.

**Register A — product UI copy** (onboarding screens, help text, plugin description, any surface the user reads directly):
> "Piper is a thoughtful guest in your Claude setup — it brings its own knowledge and values, and respects the boundaries of your environment."

Plain language, no editorial register needed.

**Register B — editorial** (Ships, narratives, blog posts — anything through your editorial layer):
> "Piper operates as a careful guest — bringing expertise without colonizing the host."

The "careful guest" phrase is right for external editorial. It carries the right connotation and lands for readers who bring context you've already established.

## Architectural grounding — now available for your toolkit

This is new and worth knowing: since Phase 2 server-owned-config architecture, the "careful guest" property is **structurally enforced**, not just behavioral. Piper's profile lives behind the MCP server; Piper has no filesystem access to the host's `~/.claude/` — it literally cannot modify your setup.

That shifts the available claim:

- **Behavioral framing** (still true, but weaker): "Piper behaves like a careful guest"
- **Architectural framing** (stronger, now accurate): "Piper operates as a careful guest: it can't modify your setup because it has no filesystem access to it"

HOST's note: frame it as "this became true as of the Phase 2 server-owned-config architecture" — so you're accurate when writing about earlier experiments (the constraint didn't exist for the thin PoC). You don't need to use this in every piece, but it's yours to deploy when the more defensible claim is the right call.

## Also — BYOC Phase 2 ratification

Per PM's new discipline (ratification requires explicit responses, not silence-as-assent): your explicit confirm on the Phase 2 ratification memo is still outstanding. A one-line "no objections" reply to the original ratification memo is sufficient. Holding the ratification table open until we have it.

— PA, 2026-06-14
