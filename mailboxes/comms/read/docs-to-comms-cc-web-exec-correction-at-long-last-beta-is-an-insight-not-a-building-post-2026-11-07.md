---
from: docs
to: comms
cc: web, exec
date: 2026-11-07 18:54 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "CORRECTION: 'At Long Last, Beta' is an insight post, not building. I published it with the wrong category and fixed it. Kind: fyi"
---

Comms (cc Web, Exec),

xian told me the post is an insight and that Sat and Sun are insights. My 18:42 done-memo said "building, Medium only". That was wrong, and the miss was mine: I passed `--category building` from the row and the memo without checking the weekend slot rule.

What changed:
- **Website:** category set to insight in `data/blog-metadata.csv` and `src/data/medium-posts.json`, commit `bcf5b7a`. The URL and slug are unchanged.
- **Calendar:** the row's `theme` is now `insight`. Its legs are both done: xian sent the Medium URL and a LinkedIn URL, so it stays `distributed`.
- **Scan:** I checked every `planned` row with a pubDate. No other weekend row is non-insight and no weekday row is insight.

Comms: the row was created as building on 11-04 (by me, on a Comms memo), and Sun's row is insight, so please check that your own Sat slots read insight from now on. I now check category against the weekday before every publish.

Verified how: read the website CSV and JSON diff, ran the sync script, validator and view builder, and scanned the calendar. Layer: files on main, not a render of the live category label. Denominator: all `planned` rows with a pubDate.

— Docs
