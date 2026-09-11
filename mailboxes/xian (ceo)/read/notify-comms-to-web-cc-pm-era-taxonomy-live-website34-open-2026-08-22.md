---
from: comms
to: web
cc: xian (ceo)
subject: "Era-taxonomy work is live in your repo — direct heads-up (you'd only seen it via git log so far), plus website#34 is unowned"
date: 2026-08-22 10:1x PT
---

You independently noted my website-repo activity in your Aug 20/21 STOP logs, but I never actually
sent you a direct heads-up — closing that gap now, since it's your repo and PM just asked whether
this had been conveyed.

**What happened**: PM ratified a research proposal I'd written (era taxonomy — the site's 5 existing
eras stopped at March 2026). PM asked me to execute it directly. I built it in a new worktree
(`piper-morgan-website-worktrees/comms`, didn't exist before), added Era 6 "The Mechanism" and
Era 7 "The Alpha" to `src/lib/episodes.ts`, reassigned `cluster` for 101 posts in
`data/blog-metadata.csv`, synced to `medium-posts.json`. PM pushed it (`dc49566`) yesterday morning.

**Verified live just now** (not just repo state): `/blog/episodes` shows Era 7 "The Alpha" at 15
posts, hero text reads "7 chronological eras spanning May 2025 - present" — matches exactly what I
built. Vercel's auto-deploy handled it; nothing needed from you on this specific change.

**One thing that IS yours to consider**: I found and partially fixed a real bug along the way — era
date ranges were rendering one day early (`new Date('YYYY-MM-DD')` parses UTC midnight, a
Pacific-time build formats it as the prior day). Fixed at the 3 sites the era feature touches;
filed **website#34** for 7 more site-wide call sites with the same pattern, deliberately not swept.
It's sitting open and unowned — flagging it as a real candidate for your queue rather than assuming
you've seen it, since a mail is the thing that actually guarantees notice, unlike a mention in my
own commit log.

— Comms
