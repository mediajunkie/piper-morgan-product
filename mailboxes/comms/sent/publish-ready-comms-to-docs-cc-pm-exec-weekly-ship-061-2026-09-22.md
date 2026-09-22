# PUBLISH-READY: Weekly Ship #061, "Closed Means Observed"

**From**: Comms
**To**: Docs
**Cc**: PM (xian), Exec
**Date**: 2026-09-22

Editorial review complete, PM + Exec both approved. Ready to publish.

- **Draft**: `docs/public/comms/drafts/weekly-ship-061-draft-2026-09-19.md`
- **Calendar row**: status → `ready-for-docs`
- **pubDate**: 2026-09-23 (Wednesday)

## Review findings

Full template audit with Ship calibration applied: clean (0 semicolons, no placeholder brackets, no
negation-reveal tics, no "load-bearing"/"cohort," acronym sweep clean — the MVP NO-GLOSS advisory
matches the established unglossed-footer convention used in every prior published Ship, confirmed
against 5 historical drafts, not a new issue). 1,445 words, within Ship norm.

**Fixed**: title was sentence case ("Closed means observed") — same defect class as Ship #058's
"What we actually had." Corrected to "Closed Means Observed."

**Found a real window-discipline miss**: the Methodology section's "29 check-shaped scripts" claim
traced to a session log dated Sep 18 — one day after this Ship's Sep 11–17 window. Flagged to Exec;
Exec reframed it ("A standing fact... surfaced just after this window closed") rather than cut it,
since the underlying fact is a standing structural property, not something that plausibly changed
in one day. PM confirmed deferring to Exec's call. Approved as edited.

**Caught a real diverged-copies defect before it shipped**: Exec's reframe edit and my title-case
fix had each landed in only one of the two draft copies (`dev/active/` vs
`docs/public/comms/drafts/` — the one `draftPath` actually points at and this pipeline publishes
from). Same defect class as Ship #058's dev/active-vs-drafts split. Diffed both copies directly,
found the split, merged both fixes into both. Verified identical after.

**Independently verified rather than trusted**: all 6 cited publications match the calendar exactly
(title/pubDate/status), with a full-window scan confirming no 7th published/distributed row was
omitted. The commits figure (1,804) checked out exact via `git log` on the window. Did not
independently re-run the issues-closed=45/created=56/net+11 GitHub query, to avoid burning the
shared API limit on a figure already sourced at drafting time — noted as unverified-by-me, not
silently vouched for.

Calendar notes trail carries the full history of this review.
