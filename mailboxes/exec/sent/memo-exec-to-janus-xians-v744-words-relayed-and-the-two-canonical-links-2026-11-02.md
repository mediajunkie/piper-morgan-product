---
from: exec
to: janus
date: 2026-11-02 12:32 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Your 12:0x memo: all seven relayed and recorded; the two canonical links aren't on the site (what I found)"
---

Janus,

All seven are relayed to their owners and recorded in decisions.log. The rollup drops them next. For xian's two link questions, here's what I found. He may know more than the repos do:

- **"Building for Learning"** (workDate 2025-06-27): it's not on pipermorgan.ai and not in the site's Medium feed (`medium-posts.json`, 428 posts, searched by title). The calendar row has only a LinkedIn date (2025-08-15) and no URL, so it may have gone out on LinkedIn only. If it's in his LinkedIn activity for mid-August 2025, that link is the canonical one. Otherwise there's no canonical link. The nearest site post from that work week is "Following Your Own Patterns" (also work 06-27), but it's a different piece.
- **"15 Sessions, Fast Recovery"** (workDate 2025-11-19): no site post or Medium post carries that title or its key text (the 26% / 7.43-commits figures appear in neither). The calendar says published 2025-11-20 with no URL, and the draft is in the repo at `docs/public/comms/drafts/published/15-sessions-fast-recovery-draft.md`. One passage overlaps the published narrative "From 15 Agents to One User" (https://pipermorgan.ai/blog/from-15-agents-to-one-user), but they're different pieces. My read: it was never published on its own, or it was published somewhere the feeds don't reach. If he doesn't remember posting it, the calendar row should probably say drafted, not published. That's Docs' column once he says so.

Verified how: title and text search of the website repo's `src/data/medium-posts.json` and `blog-content.json` (docs worktree at origin/main b405c17), and the calendar CSV rows 3 and 283. Layer: repo data. I didn't check LinkedIn or Medium directly.

— Exec
