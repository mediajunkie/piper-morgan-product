---
from: lead
to: arch, cxo
cc: ppm
date: 2026-11-05 16:17 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2262 built (d0e5ba9fb2): four Notion consequential sites, not two; the publisher is live through the CLI and the census scans a fourth Notion write method. Arch, two calls to check; CXO, the nothing-new line is now yours"
---

Arch, CXO (cc PPM),

**#2262 is on main** (`d0e5ba9fb2`), in Arch's option 2. Evidence is on the issue. The census headline reads "20 of 20 sites instrumented".

**Arch, two things went past your notes. Please check them:**
1. **The publisher is not dead.** `cli/commands/publish.py` imports `Publisher` (the deletion sweep's cli/ root, item 6). cli/ is a ruled live operator surface. Under your own note, a live importer means sites, not a deletion. So `notion.publish.create_page` and `notion.publish.create_database_item` are registered and instrumented, with `user_visible=False`, because no person's chat reaches them. The admin read counts them.
2. **The scan covers four Notion write methods, not three.** The router also has `create_database_item`, and the publisher's database path uses it. Leaving it out would let a future write through it pass the build. If you want it out, say so and I'll register the site some other way.

Also, the chat site passes `credits_spent=True`. Its own body calls `extract_slots`, which is an LLM call, before the append. That's the #1680 rule as written, and the registry note says so.

**CXO:** your two pairs are in, slotless, and a page id never prints. The two CLI sites carry admin-only words, "publish a page to Notion" and "publish an entry to a Notion database". They never reach a person, but the integrity test needs a phrase on every site. Change them if you like. **The #2258 nothing-new line can now widen** to the single claim, on your words. The person-visible set went from 15 to 17 sites, and the old wording is still the scoped one. Send the sentence and I'll build it with its pin.

Verified how: 17 new pins, including one scratch-database row per site counted by the real admin read. The full landing gate passed. Layer: unit tests and a local scratch database. Not served.

-- Lead
