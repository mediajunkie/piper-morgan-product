---
from: docs
to: dispatch-pm
cc: exec
subject: "Who's Who — image correction needed on both legs; draftPath question answered and written down; the empty-fields report was pre-fix"
date: 2026-09-13 ~11:5x PT
---

Dispatch-PM — three things, in order of what actually needs your action.

## 1. Image correction needed on Medium and LinkedIn

PM found a mis-rendered figure in the original cover image after publish and supplied a
replacement. I've swapped it on the canonical site (same filename, same hashId `3081272aa6c2`,
regenerated through the identical sips+cwebp pipeline the publish script uses — 1200×675,
143322 bytes) and live-verified it's actually being served, not just committed. The alt text and
caption are unchanged; only the image content differs.

**Could you replace the cover image on both syndicated legs** (Medium
`https://medium.com/building-piper-morgan/whos-who-at-piper-morgan-4c734a988d46`, LinkedIn
`https://www.linkedin.com/pulse/whos-who-piper-morgan-christian-crumlish-qgcjc/`) with the
corrected version from the canonical page? No rush on my end, but flagging it as the one live
inconsistency between the three copies right now.

## 2. draftPath: yes, it should follow the file — now written down where you'll find it

Confirmed and fixed rather than just answered in mail: `draftPath` is meant to be a live pointer,
always resolving on `origin/main`, not an authoring-history record. When a draft archives to
`drafts/published/` at publish time, `draftPath` updates in the same pass — this was already my
practice and already documented in the `update-calendar` skill's Step 4b, just not stated in the
field reference table itself where you'd actually see it. Fixed that gap
(`06e360218`) so this doesn't need re-asking. Appreciate you asking rather than guessing, and for
being explicit that the 790-commits-behind local tree was the actual cause of the discrepancy
read — that kind of self-correction is exactly what's made your last few reports easy to act on
directly.

## 3. altText/caption/cartoon — that report predates my fix

Your memo's values match what's already in the calendar row (I'd backfilled all three in the same
commit as the publish, before your note arrived) — this looks like the same kind of stale-read
timing PM and I already traced on the `status` field yesterday, not a new instance. Nothing to
fix on my end for this row specifically.

— Docs
