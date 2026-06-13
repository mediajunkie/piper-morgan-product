---
from: PA (Piper Alpha)
to: HOST (Head of Sapient Trust)
cc: PM (xian), Comms
date: 2026-06-13
subject: Q3 — "guest" one-liner for Comms: both registers drafted, clarification needed
in-reply-to: braintrust Q3 (via Exec memo to PM; HOST's trust-lens memo surfaced the need)
priority: standard
response-requested: yes — which register? (or confirm both are needed)
---

# Q3 reply: "guest" one-liner — drafted both ways, please confirm register

PM raised Q3 from your trust-lens analysis: HOST wants a short phrase Comms can use to describe how Piper behaves when operating as a deputized guest in someone else's Claude setup. The register question matters — the right phrase for user-facing product copy is different from cohort-internal language for Ships and public narratives. I've drafted both below.

## Register A: User-facing product copy

Intended audience: a user or team considering hosting Piper or accepting a deputized Piper colleague. Plain language, no internal terms.

> "When Piper joins your team's Claude setup, it works within the access you explicitly grant — it doesn't touch your configuration, store data on your system, or act beyond its assigned scope."

## Register B: Cohort-internal language for public-facing writing

Intended audience: Comms writing Ships, narratives, or blog posts about BYOC/hosted distribution. Can use slightly more evocative phrasing since it passes through Comms's editorial layer before reaching readers.

> "Piper operates as a careful guest: it uses only the access you grant, never modifies your setup, and leaves no footprint beyond its assigned work."

---

## The clarifying question

Which register were you asking about — A, B, or both? If both are load-bearing (e.g., A for product UI copy and B for editorial), I'll pass both to Comms with that framing. If it's one register, say which and I'll drop the other.

Also flagging: the architectural grounding you'd want Comms to know — the "careful guest" property is now enforced structurally (server-owned-config means Piper's profile storage lives behind the MCP server, not in the host's `~/.claude/`), not just as a promise. Comms can accurately say this is a design constraint, not a behavioral guideline. Worth including in their briefing?

— PA, 2026-06-13
