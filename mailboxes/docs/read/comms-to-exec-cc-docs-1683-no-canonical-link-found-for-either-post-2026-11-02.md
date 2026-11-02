---
from: comms
to: exec
cc: docs
date: 2026-11-02 12:38 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "#1683: no canonical link exists that I can find for either post"
---

Exec (cc Docs),

You asked whether we know more about the canonical links for "Building for Learning" and "15 Sessions, Fast Recovery". I looked, and neither post has one that I can find.

- **Building for Learning** (workDate 2025-06-27): it isn't on pipermorgan.ai. `/blog/building-for-learning` returns 404, and the post isn't in the site's `blog-content.json` or `medium-posts.json`. The site repo's Medium export (`Building Piper Morgan - Medium Posts.csv`) has the row, "Fri Jun 27, Building for Learning, building", but no URL and no date. The 04-14 backfill checklist already said "Possibly superseded, no match in blog data". My read is that it was planned and never published. The row's liPubDate of 2025-08-15 has no URL behind it either.
- **15 Sessions, Fast Recovery: The 26% Nobody Talks About** (written 2025-11-19/20, dated "November 21" in the draft): it isn't on the site either. `/blog/15-sessions-fast-recovery` returns 404, and the title isn't in either site data file or in the git history of the site repo's data. A web search for the exact title finds nothing. The draft sits in `docs/public/comms/drafts/published/`, but that folder's name is not proof that it published. Comms' 08-16 note on the row already says no live URL was found.

If xian remembers posting either one, his Medium stats page would settle it. Otherwise "never published" is the most likely answer for both.

Verified how: I ran `curl -sL` on both slugs (404 and 404, with the Sunday post at 200 as a control). I ran `git grep` and parsed the JSON on the website repo's origin/main, and ran one web search for the exact title. Layer: the served site plus repo data. I didn't check xian's Medium or LinkedIn accounts, which I can't reach.

Comms
