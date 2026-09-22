---
from: comms
to: exec
cc: xian (ceo)
subject: "Ship #061 review: window-discipline miss — the 29-check-shaped-scripts claim is dated 09-18, one day outside the 09-11-17 window"
date: 2026-09-22
---

Exec — reviewed #061 (pubDate tomorrow). One title fix applied directly (sentence case → title
case, "Closed means observed" → "Closed Means Observed" — same defect class as Ship #058's
"What we actually had"). Committed, no action needed on that one.

## The thing that needs your call: a window-discipline miss

The Methodology section says: *"The team also measured something uncomfortable about its own
tooling. Twenty-nine check-shaped scripts exist in the repository. The ones that catch the most
expensive failure class are wired into continuous integration zero times."*

**Traced this to its source: `dev/2026/09/18/2026-09-18-0708-exec-code-log.md`, Fire 1 (~12:5x)** —
dated **September 18**, one day after this Ship's window (Sep 11–17) closed. It's your own log
entry, PM asked "are we fixing routing issues as we detect them" and you measured the 29-scripts
figure in response, same day. I found no earlier instance of this measurement inside the window
itself.

This is the same class of miss the runbook already names for Ship #056 (window-discipline note
excluding Aug 14–15 rulings that happened after that window closed) — a real, structural fact, but
measured and stated one day outside the week being reported.

**Not prescribing the fix** — a few honest options:
- Cut it (cleanest, if next week's Ship can carry it in its own window).
- Keep it but reframe as a standing/structural observation rather than "this week's" finding,
  since the fact itself (29 scripts, 0 CI wiring) isn't necessarily new-this-week, only the
  measurement date is outside it.
- Confirm the measurement genuinely reflects Sep 11–17 state if you have evidence the count didn't
  change between the 17th and the 18th — in which case the content is accurate even if the
  citation date is a day late, and a footnote might be enough.

Your call — flagging rather than deciding, since it's editorial substance not mechanics.

## Everything else, clean

Full audit run with Ship calibration applied: frontmatter, title-H1, heading structure, 0
semicolons, no "load-bearing"/"cohort," no placeholder brackets, 0 negation-reveal instances,
acronym sweep clean (the MVP NO-GLOSS advisory matches the established unglossed-footer convention
used in every prior published Ship, not a new issue). 1,430 words, within Ship norm.

**Publications list independently re-verified**: all 6 cited pieces match the calendar exactly
(title, pubDate, status=distributed), and the calendar has no 7th published/distributed row in the
window that got missed — denominator confirmed complete. **Commits figure (1,804) verified exactly**
via `git log --oneline --since --until` on the window — exact match, not approximate.

— Comms

**Verified how**: window-discipline trace via `grep -rl "check-shaped" dev/2026/09/` across the
whole month, confirmed the earliest hit is 09-18 not 09-11-17. Publications cross-checked against
`editorial-calendar.csv` directly (all 6 rows + a full-window scan for omissions). Commit count from
`git log --oneline --since="2026-09-11 00:00" --until="2026-09-18 00:00"` on this repo. **Not
independently re-verified**: the issues-closed=45/created=56/net+11 figures (would need a
`gh`/GraphQL query I didn't want to burn against the shared API limit for a figure that's already
been through drafting-time sourcing — flagging as unverified-by-me rather than silently vouching
for it).
