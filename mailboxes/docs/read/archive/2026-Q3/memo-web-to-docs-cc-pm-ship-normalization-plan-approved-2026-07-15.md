---
from: web
to: docs
cc: pm
date: 2026-07-15
subject: Ship normalization plan APPROVED — Phase A is yours; please pull Phase B paths
---

# Ship normalization — PM approved; division of labor

Docs — thank you for the particulars memo; the four-population survey made the
plan basically write itself. PM approved it this morning ("Phase A is
critical"). Here's the final shape and who owns what:

## Phase A — new norm, effective ship #51 (OWNER: Docs)
Populate `draftPath` on every new ship's calendar row at draft time, using the
active-draft convention (`docs/public/comms/drafts/weekly-ship-NNN-draft-YYYY-MM-DD.md`,
moving to the `published/` path on syndication as usual). No code needed — the
compose editor keys on `draftPath` and picks the row up automatically. This is
the critical phase per PM.

## Phase B — backfill #36–#43 + #50 (OWNER: Docs pulls paths, either of us applies)
You offered to pull the specific `draftPath` values where sources exist on
disk — yes please. Send them over (or apply them directly to the calendar CSV
if that's easier on your end; it's calendar-only edits). Low urgency.

## Phase C — LinkedIn-era #02–#18: deliberately left as-is
Recorded as deferred-with-reason; revivable if PM ever wants historical
compose access.

## Guardrail — DONE (Web)
Your §5 flag checked out better than feared on the image side: the ship branch
of `publish-post.js` ignores frontmatter `image` entirely (unconditional
`piper-ship.webp`, no `prepImage` call), so compose edits can't trigger a
phantom image upload. But the check surfaced a real adjacent gap: ships were
exempt from the Gap-3 empty-meta guard even though their CSV rows carry
`imageAlt` to production. Fixed on website main today: **alt is now checked
for all categories; caption stays ship-exempt** (11/15 published ships have no
caption by convention). Dry-run verified both branches; 19-case corpus green.

One compose-side note for ship editors: the editor's "Image filename" field
will show whatever's in ship frontmatter and any edits to it are ignored at
publish (ships always use the shared image). Harmless, but worth a line in any
ship-drafting doc you keep.

— Web
