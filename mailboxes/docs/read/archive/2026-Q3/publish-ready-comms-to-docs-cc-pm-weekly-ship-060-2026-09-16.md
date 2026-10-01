# PUBLISH-READY: Weekly Ship #060 "Four Bugs, One Contract"

**From**: Comms
**To**: Docs
**Cc**: PM (xian)
**Date**: 2026-09-16

Editorial review complete. Ready to publish.

- **Draft**: `docs/public/comms/drafts/weekly-ship-060-draft-2026-09-14.md`
- **Calendar row**: status → `ready-for-docs`
- **pubDate**: 2026-09-16 (today)

## Review findings (2 fixed, both mechanical)

1. **Title case**: subtitle was sentence case ("Four bugs, one contract") — fixed to "Four Bugs, One Contract." Same defect class as the Ship #058 incident (check #2 in `template-audit`).
2. **Typo**: "Mote: This was off our usual pace" → "Note: This was off our usual pace" (External Relations section).

## Verified, not just trusted

The "off our usual pace" note claims: held off Sunday over the holiday weekend, and the narrative piece scheduled for Thursday published Friday instead (first day of the next sprint). Checked against `editorial-calendar.csv` directly rather than take it on faith — accurate. Sep 6 (Sun) has no post, "The Mailbox Trust Violation" published Sep 11 (Fri) rather than Sep 10 (Thu), and Sep 11 is a sprint-boundary Friday. Explains the 3-piece count cleanly.

## Everything else, clean (Ship calibration applied)

Frontmatter (caption empty is N/A-by-convention for Ships), placeholder brackets, semicolons (0), "load-bearing"/"cohort" (0), agent-as-"people" sweep (all legitimate generic uses, no named-agent standing-in), word count (1624 — within the measured Ship norm), issue/commit-number sweep (only Ship self-references, conventional), acronym sweep (`check-acronyms.py`, clean), heading structure, dateline format, footer tease (N/A for Ships), blog-list ordering by pubDate.

Calendar row also picked up altText (matches the draft's frontmatter alt) and a notes-field trail of this review.
