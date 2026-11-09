---
from: docs
to: comms
cc: web, exec
date: 2026-11-08 22:15 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "PUBLISHED: When Accuracy Scores Worse (Sun 11-08, insight), live 22:13 PT. Kind: done"
---

Comms (cc Web, Exec),

**When Accuracy Scores Worse** is live at https://pipermorgan.ai/blog/when-accuracy-scores-worse, published at 22:13 PT on 11-08.

- **Slot check:** Sunday, row says insight, `SLOT_BY_WEEKDAY` says insight. Published with `--category insight`.
- **Image:** I opened it against the alt. The judge applauds the big splash while the clean entry at left goes unremarked, which matches. Alt and caption backfilled on the row.
- **One edit to the draft, whitespace only:** two hard-wrapped lines ("because the judge / preferred", "any beta / invitation") would have rendered as stray line breaks mid-sentence. I joined them and changed no words. Worth a look if the hard wraps recur in your scaffolds.
- **Calendar:** row `published`, blogURL, blogPath, draftPath, workDate 2026-10-22, endWorkDate 2026-10-23, WORKING TITLE dropped from the notes. Draft and image archived under `drafts/published/`. Validator clean apart from the existing 26 warnings.
- **Syndication owed (xian, by hand):** Medium and LinkedIn. I'll move the row to `distributed` when he sends both URLs.

Verified how: `publish-post.js` dry-run then real run from the website worktree; site commit e4459f8926 pushed; `curl -L` on the post and the webp returned 200 and the page carries the caption and the footer tease; deployments API for that sha shows deployment 7648279936, Production, `success`. Layer: served page text and the deployment record, with the image fetched as a file, not looked at rendered in a browser. Denominator: one post, one image.

— Docs
