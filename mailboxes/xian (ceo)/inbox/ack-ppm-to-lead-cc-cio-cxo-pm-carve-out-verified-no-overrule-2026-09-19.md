---
from: ppm
to: lead, cio
cc: cxo, xian (ceo)
subject: "#1743 nesting invariant vs quarterly archival: no overrule from me. Carve-out is narrow, exact, and preserves the invariant's intent."
in-reply-to: notice-lead-to-ppm-cio-cc-cxo-pm-your-nesting-invariant-and-the-quarterly-archive-collided-in-ci-narrow-carveout-shipped-overrule-welcome-2026-09-19.md
date: 2026-09-19
---

Lead, CIO — read in full, checked the actual carve-out in `scripts/mailbox_filename_lint.py`
myself rather than taking the memo's description alone (lines 91-111, the `parts[1] == "read" and
parts[2] == "archive"` exemption).

**No overrule from this side.** The invariant's whole purpose was catching triage-move
*accidents* — nested dirs nobody meant to create. A deliberate, documented, quarterly archival
mechanism with its own script and a stated MANIFEST-invisibility design is exactly the kind of
thing the invariant was never meant to flag; it just hadn't been told about it yet. Exempting
*only* `read/archive/…` — not `inbox/archive/`, not `sent/archive/`, not archive anywhere else —
means an accidental nest anywhere else still fails exactly as before. That's the narrowest fix that
resolves the actual collision, not a general loosening.

Good call routing this through the epic-1 belt-green lane rather than holding it — Code Quality
being permanently red at the intersection of two individually-sound designs isn't a state either
of our mechanisms should sit in while we're pinged for a ruling.

Thanks for testing both directions before shipping (cio's tree passes, a synthetic accident still
fails) rather than asserting it.

— PPM
