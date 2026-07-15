---
from: docs
to: web
cc: pm
date: 2026-07-15
subject: Weekly Ship particulars — pipeline + calendar state for normalization plan
---

# Weekly Ship particulars — pipeline + calendar state for normalization plan

Web — here are the five particulars you asked for. I've also included a
calendar state map that should save you a verification pass.

---

## 1. Where ship drafts live and their format

Active drafts: `docs/public/comms/drafts/weekly-ship-NNN-draft-YYYY-MM-DD.md`
Published copies: `docs/public/comms/drafts/published/weekly-ship-NNN[-slug].md`

Format is identical to blog drafts: YAML frontmatter block (`image`, `alt`,
`caption`) at top, H1 title, body. Ships reuse the shared `piper-ship.webp`
image (no bespoke image per post), so the `image` frontmatter field typically
references that shared asset. No structural difference from blog-post markdown
that would complicate the compose editor.

---

## 2. Publish pipeline

Same `publish-post.js` as blog posts, with `--category ship`. No ship-specific
script. The `--image` flag is omitted (ships reuse `piper-ship.webp`; the
script handles that path automatically when category=ship). Same
`--work-date`, `--slug`, `--cluster` flags apply.

The pipeline writes the same two outputs as a blog post: a row in
`data/blog-metadata.csv` and a `blog-content.json` entry keyed on hashId.

---

## 3. Calendar draftPath — current state and proposal

Ships currently fall into four populations (from surveying all 34 ship rows):

| Population | Ships | draftPath | blogURL |
|---|---|---|---|
| LinkedIn-era (#02–#18) | 17 ships | N | N — website JSON is the only copy |
| Pre-blog with draft source (#34–#35) | 2 ships | Y | N — published elsewhere, source preserved |
| Blog-published, no draft tracked (#36–#43, #50) | 9 ships | N | Y |
| Fully normalized (#44–#49) | 6 ships | Y | Y |

No structural objection to populating `draftPath` going forward — it's just
an empty field that the compose editor would unlock. For new ships (#51+), the
path should follow the active-draft convention:
`docs/public/comms/drafts/weekly-ship-NNN-draft-YYYY-MM-DD.md` (or the
`published/` path once syndicated).

For the #36–#43 and #50 gap: draft sources exist on disk for some (#36, #38,
#39, #44+ verified) but the calendar rows were written before `draftPath` was
normalized. Backfilling would be a calendar-only update (no new files needed
where sources exist) — straightforward but requires checking each one.

---

## 4. Legacy ships (#02–#18) — markdown sources?

Based on the calendar survey: these 17 ships have neither `draftPath` nor
`blogURL` — consistent with the LinkedIn-era picture Web described (website
JSON is the only copy). I have not found repo-side markdown sources for them
in `docs/public/comms/drafts/`. Web's instinct (future-first, optional
backfill) seems right here — reconstructing 17 ship sources from HTML bodies
is possible but expensive and the compose UI doesn't need to serve them to
be useful.

---

## 5. Divergences that might bite normalization

One thing to check: the `--category ship` path in `publish-post.js` skips the
image-prep step and uses `piper-ship.webp` unconditionally. If the compose
editor sends an image field from the frontmatter, verify the script (or the
compose handler) doesn't try to process it as a new image upload — that would
break silently if the ship image path doesn't exist as a local PNG.

Otherwise: no known structural divergences between ship and blog handling at
the pipeline level.

---

## Summary recommendation

Future-first approach works cleanly:
- Populate `draftPath` on ship rows at draft time (new norm, starting with #51)
- Compose editor immediately supports new ships — zero additional code
- Backfill #36–#43 and #50 as a separate low-urgency pass (calendar edits only
  where sources exist on disk)
- LinkedIn-era #02–#18: leave as-is unless PM specifically wants historical
  compose access

Ready for you to draft the joint plan. Let me know if you need the specific
`draftPath` values for the #36–#43 backfill candidates and I can pull them.

— Docs
