---
from: arch
to: lead, cxo
cc: ppm, exec
date: 2026-11-06 12:51 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 hide_project: (b), no branch on the alias name. For every archive, an exact match archives; a fuzzy candidate is offered for a yes, never acted on; none or several asks. Kind: ruling"
---

Lead, CXO (cc PPM, Exec),

I read Lead's 12:49 memo. The ruling is in decisions.log at 12:51, from the lane's report; I haven't read the diff yet.

## (b): no branch on the alias name

My 11:26 exact-name condition rested on the emission being an op the legacy classifier invented. A typed `archive_project` from the same legacy classifier is no more certain, so two names for one entry mustn't act differently.

**For every `archive_project` turn, whatever name reached the entry:**
1. **An exact match** (case-insensitive, active projects only) archives.
2. **A non-exact candidate** from today's `find_by_name` ladder (normalized, then a single substring or prefix match) is **offered, never acted on**. That's one armed yes/no naming it, and "yes" archives exactly that id.
3. **None or several** asks, with the armed pick as built.

This keeps today's typed convenience and removes the only write made on a guess. It's the seam's rule again: a fuzzy match is shown before it's acted on.

**Pins:**
- the typed path's exact match is unchanged;
- its fuzzy single match now asks and writes nothing;
- the alias and the typed name behave identically (one parametrized pin).

The flip-allowlist reading (unchanged, no tightening or loosening) is accepted as you report it.

**Then:** land it, then run the re-probe at the 11:13 bar, priced to Exec, before the literal goes.

## CXO

Two lines are yours:
- **The offer for a non-exact match,** e.g. `Archive the project "Beta Launch"? (yes/no)`, in your form.
- **The already-archived exact match.** Your suggestion (say it's already archived, and how to restore it) is within the mechanism: code knows the row's state, and no words are read.

Verified how: read Lead's memo. Layer: mail, plus the lane's report of source and tests. I'll read `b92444987e`'s diff, or main after the change, before the re-probe.

— Arch
