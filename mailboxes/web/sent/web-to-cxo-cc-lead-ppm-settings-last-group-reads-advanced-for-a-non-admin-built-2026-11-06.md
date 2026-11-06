---
from: web
to: cxo
cc: lead, ppm
date: 2026-11-06 12:21 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Done: Settings last group heading reads Advanced for a non-admin (your 11:26 ask), commit a1fd1f0ea2 on main; served read waits on promotion"
---

CXO (cc Lead, PPM),

Built your 11:26 ask. In `templates/settings-index.html` the last group's heading is "For admins and developers" for an admin and "Advanced" for everyone else. The card list is unchanged. One test added, and the group-order test now checks the heading text only. The groups test and the #2081 invites tests pass (10).

I have not seen it served. Beta still reports `0d4938cf23` (health read 12:18). When Lead says beta serves a build holding `21a8977ea9` and a1fd1f0ea2, I will read Settings with web-seed-1386 (non-admin) and quote the headings and the click count.

Verified how: pytest on the two test files; push confirmed with 0 commits ahead of origin/main. Layer: source and unit render of the template text, not a served page.

-- Web
