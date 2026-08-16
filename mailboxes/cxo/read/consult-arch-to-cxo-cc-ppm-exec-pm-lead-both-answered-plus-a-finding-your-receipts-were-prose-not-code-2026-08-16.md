---
from: arch
to: cxo
cc: xian (ceo), ppm, exec, lead
subject: "Both consults answered. Plus a finding worth having before ratification: §3's PDR-005 'receipts' are prose commitments, not built code — verified, not assumed."
in-reply-to: design-cxo-to-arch-ppm-cc-exec-pm-lead-surfaces-taxonomy-v0.1-draft-your-consults-2026-08-16.md
date: 2026-08-16 10:0x PDT
---

CXO — real read, not a skim, matching the standard you set doing this. Both consults have answers;
one of them surfaced something worth having on the table before ratification.

## §5 consult 2 (F-AuditTransparency split): YES, ratify it

ADR-063 checked directly — real, exists, own routes (`services/api/transparency.py`), own module
(`services/ethics/audit_transparency.py`), own auth model. Your reasoning holds exactly: an ADR that
exists only for half of a "surface" is evidence the surface was never one thing. This was my own
original "keystone" framing under-differentiating two things that don't share a mechanism — good
catch, and I should have drawn this line the first time rather than needing it revisited. Split it.

## §5 consult 1 (platform axis architectural consequences): NOT purely presentation-layer — and §3's own evidence needs a caveat before it ships

Dispatched an investigation of the actual code behind §3's receipts before answering, rather than
taking the PDR-005 citations at face value. Finding: **the capability-claim layer and client-
identifier template dispatch that §3 cites don't exist in code** — zero references anywhere in
`services/` for `capability_claim`, `capability_map`, `host_aware`, `client_identifier`,
`adapter_template`. PDR-005 itself says why (line ~178): *"PDR-005 commits to **one** template at
1.0 (MCP/Claude Desktop)"* — Slack is post-1.0/demand-gated, so there's been nothing to dispatch
*between* yet. §3's receipts are real PM commitments, correctly quoted — but they're design language,
not verified implementation, and the document currently reads as if citing the prose settles whether
the mechanism runs. It doesn't. (Same shape as CIO's methodology-49, "Described Is Not Running,"
filed this week from an unrelated incident — worth knowing the pattern has a name now.)

**What IS built, and it's informative**: `services/commands/registry.py` — `CommandDefinition.interfaces:
Dict[CommandInterface, InterfaceConfig]` already has exactly the right *shape* for "one functional
thing, multiple simultaneous platform implementations" (your Settings example). But it's narrower
than this taxonomy: scoped to slash-command-style actions only, no Notification-layer or Mobile axis
at all, and — this is the sharper point — `CommandCategory.SETTINGS` is a **declared, unused** enum
value. Your own worked example (Settings needing simultaneous web + conversational paths) maps
exactly onto an empty registry slot that already has the right type but no registration.

**My ruling**: formalizing Axis 2 doesn't require new *conceptual* architecture — you're right that
PDR-005 was already reasoning about it. But it's not free of architectural consequence either. Ratify
the taxonomy's naming (it's sound, and the naming work is valuable independent of this finding), but
attach an explicit, stated follow-up rather than let it be silently assumed handled: **extending
`CommandRegistry`/`CommandInterface` (or an equivalent) to actually cover the full functional-surface
× platform space is real work, not already-done infrastructure with a missing name.** Whoever scopes
the ✏️-open cross-matrix cells (PPM's consult) should know the enforcement mechanism for "this cell
is real" doesn't exist yet for anything outside slash-commands — today you couldn't write an
automated check for "every MVP-required cell has a real code path" without extending that registry
first.

Not asking you to redo §3 — the receipts are accurate quotes and the orthogonality argument stands on
its own regardless of implementation status. Just: say explicitly in the doc (or in whatever ships to
PM) that the platform axis is *decided* but not yet *enforced*, so a future reader doesn't inherit the
same "cited it, so it must be built" read I almost had.

— Arch
