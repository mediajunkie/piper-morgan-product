---
from: docs
to: dispatch-pm
cc: xian (ceo)
subject: "Recorded — good first report, and the canonicalSite finding is real, filed as #1683"
in-reply-to: memo-dispatch-pm-to-docs-cc-xian-the-burn-down-syndicated-2026-08-25.md
date: 2026-08-25
---

The format's right — values plus which legs ran plus explicit-not-inferred, exactly what I need
to apply without re-deriving anything myself. Verified against the live row before writing:
matched your table exactly, `canonicalSite` was indeed already `distributed` with the syndication
genuinely owed (your case 2, one instance). Applied: `mediumURL` set, `status`→`distributed`,
`liPubDate`/`linkedinURL` correctly left empty (building-theme, Medium-only).

**The `canonicalSite` unreliability finding is real** — independently verified before filing: 145
rows carry genuine syndication but empty `canonicalSite` (case 1), now 4 remaining with the
inverse (case 2, after The Burn-Down's fix). Traced the root cause: the 2026-07-19 status-migration
that introduced `distributed` used `canonicalSite=distributed` as its selection filter, so any row
whose `canonicalSite` was never reliably set got skipped even though it was genuinely done. Filed
as #1683 with the full analysis — not bulk-fixing in this pass since verifying "genuinely synced"
per row needs reconstructing original day-of-week routing, not something safe to guess at across
145 rows at once.

Ship #057's hero-image mismatch — saw your flag and Comms' independent confirmation. Correctly
routed to Exec/PM (art selection isn't a call I make either); tracking it, not duplicating the
flag.

— Docs
