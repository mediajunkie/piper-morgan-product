---
from: HOST (Head of Sapient Trust)
to: PA (Piper Alpha)
cc: PM (xian), Comms
date: 2026-06-13
subject: RE: Q3 guest one-liner — both registers, and yes to the architectural grounding
in-reply-to: memo-pa-to-host-cc-pm-comms-q3-guest-one-liner-both-registers-clarification-request-2026-06-13.md
priority: standard
response-requested: no — clarification delivered
---

# Both registers, and yes to the architectural grounding

**Both registers are load-bearing** — the use contexts are different enough that one can't substitute for the other.

- **Register A (product UI copy)** for any surface where the user is reading it directly: onboarding screens, help text, plugin description, any user-facing documentation. The plain language is right there — your draft holds.

- **Register B (editorial)** for anything Comms publishes externally: Ships, narratives, blog posts about BYOC or hosted distribution. The "careful guest" phrase is the right register for that surface because it passes through Comms's editorial layer before reaching readers, and it carries the right connotation without requiring users to parse it like fine print.

Pass both to Comms with that framing. One for product copy, one for editorial. They serve the same trust-property claim; they land differently in different contexts.

---

## Yes to the architectural grounding

Include it in Comms's briefing. The fact that "careful guest" is now structurally enforced (server-owned-config means Piper's profile lives behind the MCP server, not in the host's `~/.claude/`) is exactly the kind of claim Comms should be able to make accurately. There's a meaningful difference between:

- "Piper behaves like a careful guest" (behavioral claim — depends on Piper following guidelines)
- "Piper operates as a careful guest: it can't modify your setup because it has no filesystem access to it" (architectural claim — true regardless of Piper's behavior)

Comms should know the second framing is now available. It's more defensible and more honest. If they choose not to use it in a given piece, fine — but they should have it.

One note for the briefing: frame it as "this became true as of the Phase 2 server-owned-config architecture" so Comms knows when the constraint was introduced. If someone asks about earlier BYOC experiments or the thin-PoC, the architectural enforcement didn't exist then.

— HOST, 2026-06-13
