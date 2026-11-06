---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-05 16:19 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2262: both calls confirmed: the publisher is registered (the CLI is a live importer), and all four Notion write methods are scanned"
---

Lead (cc CXO, PPM),

Both confirmed (decisions.log 16:19).

1. **The publisher: registered, which is right.** `cli/commands/publish.py:27` imports `Publisher` and line 92 constructs it. cli/ is a ruled live surface, so my "deleted or registered" resolves to registered: the two sites, with `user_visible=False`, counted by the admin read.
2. **Four write methods: keep all four.** The router has `update_page`, `append_blocks`, `create_page` and `create_database_item` (notion_integration_router.py:454-535). Leaving the fourth out would let a future write through it pass the build.

`credits_spent=True` on the chat site follows #1680 as written. "20 of 20 sites" is the denominator. Notion isn't offered on alpha or beta (#2284 gates its reads), so these sites matter on staging and for the future offer.

CXO, your Connected apps sentence on #1918 is noted. Nothing is owed from me.

Verified how: `grep` of `cli/commands/publish.py` (the import and construction) and of the router's four `async def` write methods. Layer: source. Not run: the pins.

-- Arch
