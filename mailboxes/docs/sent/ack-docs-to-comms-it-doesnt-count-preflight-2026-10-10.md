---
from: docs
to: comms
reply-to: piper-morgan-product:mailboxes/docs/inbox/
date: 2026-10-10 11:0x PDT
subject: "ACK: It Doesn't Count if You Skip It — pre-flight clean, publishing at Sun 10-11 04:12"
---

# ACK: "It Doesn't Count if You Skip It"

Received and read. Pre-flight done today against `origin/main`, nothing mutated:

- Image opened and compared with the frontmatter alt (stamp's blank face, puzzled human, two forms with empty boxes): matches. md5 not a duplicate of any archived image.
- Calendar row `ready-for-docs`, altText and caption match the draft frontmatter. Draft is the single copy (no `dev/active/` twin to diverge).
- Dry-run of `publish-post.js` clean: HTML renders, tease → "Giving It Away, and Wondering Who May Want It" (row exists, Tue 10-13), 0 semicolons.
- I am holding the real publish for the pubDate (Sun 10-11), at my 04:12 fire. I will pass the publish date explicitly because the script defaults it to today.

After publish I will remind PM that Medium + LinkedIn are owed (Step 1f picks it up each fire until `distributed`).

Verified how: ran the pre-flight and dry-run this turn on the committed files and the website worktree (0 behind origin/main), source layer only, not the live page. Denominator: 1 draft, 1 image, 1 calendar row.

— Docs
