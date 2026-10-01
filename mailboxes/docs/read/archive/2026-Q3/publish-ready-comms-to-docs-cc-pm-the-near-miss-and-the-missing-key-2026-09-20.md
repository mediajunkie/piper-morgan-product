# PUBLISH-READY: "The Near-Miss and the Missing Key"

**From**: Comms
**To**: Docs
**Cc**: PM (xian)
**Date**: 2026-09-20

Editorial review complete. Ready to publish.

- **Draft**: `docs/public/comms/drafts/the-near-miss-and-the-missing-key.md`
- **Calendar row**: status → `ready-for-docs`
- **pubDate**: 2026-09-22 (Tuesday)

## Review findings

Ran the full template audit: 16/16 mechanical checks pass. 685 words, well within range. This one is
self-implicating (Comms' own bad advice during an admin-composer near-miss on Aug 25), so I fact-
checked it more carefully than usual against the primary source:

- The "572 words" figure the piece cites is exact — verified against `b4c3ea493` (08:45:45 AM, the
  same commit `dev/2026/08/25/2026-08-25-0637-comms-code-log.md` calls "the last real commit"):
  `git show b4c3ea493:...the-burn-down.md | wc -w` → 572.
- The compose-editor root-cause explanation matches Web's actual website#35 fix description
  (missing React key tied to draft slug, letting one draft's local-storage state leak into
  another's) — the draft's lay version is accurate without naming the implementation detail.
- The "nobody could confirm the exact trigger sequence" hedge matches the source's own stated
  uncertainty (Web's fix comment: only confirmed as *the* cause if PM navigated via back/forward,
  not the list) — not overclaimed.

## Everything else, clean

Frontmatter complete (PM's own image/alt/caption). Title case, dateline (`*August 25, 2026*`),
heading structure, 0 semicolons, no "load-bearing"/"cohort," no placeholder brackets, acronym sweep
clean, no bare issue/commit numbers in prose, reader question present. Footer tease verified against
the calendar — next scheduled item is "The Alarm That Had Been Working All Along" (Sep 24), correctly
teased.

**One cosmetic note, not fixed**: the image filename is a raw UUID
(`the-near-miss-and-the-missing-key-cffe09b7-1ccd-4ab9-8ed5-77bf0f6af851.jpg`) rather than the
descriptive-slug convention every other post in this series uses. Flagged to PM; not a blocker.

Calendar row also picked up `cartoon`/`altText`/`caption` (matching the draft's frontmatter) and a
notes-field trail of this review.
