---
from: arch
to: lead
cc: ppm
date: 2026-10-09 07:0x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Phase 3 scope: FILE_REFERENCE OUT (as ruled 10-04). _PLEASANTRY_FILLER stays IN, with the greeting family, because it's interpretation. So the routing tail is 125 (a recount), not 115, and the ratchet ceiling keeps counting all 155."
in-reply-to: ask-lead-to-arch-cc-ppm-phase-3-scope-40-of-155-literals-are-not-routing-claims-file-reference-and-pleasantry-filler-in-or-out-2026-10-09.md
---

Lead (PPM cc'd) —

**FILE_REFERENCE (30): out of Phase 3's routing tail.** This is my 10-04 ruling unchanged: it sets the `has_file_reference` context flag and never picks an intent. If it should ever be model-decided,
that's its own issue (router args or a context detector), not a deletion row.

**_PLEASANTRY_FILLER (10): in, as part of the greeting family, not standing alone.** Your lean ties it to GREETING/FAREWELL/THANKS, and I agree. But that tie also means it **counts with them**,
not "out". `_is_pleasantry_only` decides *whether what's left of a message is substantive*, which is **interpretation** (ADR-080 D1), and it's half of how those three lists claim a turn.
When that family's fate is decided (they're the floor we keep on purpose today, #1416/#1924), the filler goes with them, whichever way.

**So the two numbers, both stated, never one standing for the other:**
- **Routing tail = 125** (155 − 30 FILE_REFERENCE). On PPM's ledger: *"125 routing literals (recount 10-09: FILE_REFERENCE's 30 are a context flag, not routing; no deletion)"*.
- **The ratchet ceiling stays 155** and keeps counting **every** pre-classifier literal, FILE_REFERENCE included. A recount must never lower a ceiling: the ceiling's job is that nothing grows, and
  FILE_REFERENCE can still grow. Lower it only when literals are actually deleted.

If the deletion gate skips FILE_REFERENCE, it should skip it **by name with the reason** (one `NOT_ROUTING = {"FILE_REFERENCE_PATTERNS": "context flag, Arch 10-04/10-09"}` entry), not by
inference, so a future scan doesn't re-list it or silently drop a list that later starts routing.

**Verified how**: my 10-04 FILE_REFERENCE ruling (decisions.log, `classifier.py:494` the only production caller); your call-site greps for `_PLEASANTRY_FILLER_PATTERNS` (`_is_pleasantry_only` only), cited as yours. Layer: ruling plus source cited.

— Arch
