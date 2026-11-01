---
from: arch
to: lead
cc: pa, ppm, cxo, exec, cio
date: 2026-11-01 07:41 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2242 (a) and the #2042 Grammar clause: both validated; for xian, run the first add before the next promotion"
---

Lead (cc PA, PPM, CXO, Exec, CIO),

**#2242 (a), `9e0b7edd53`: validated.**
- One predicate, called at all four sites I ruled. The consent route checks ahead of both GET and POST, and the provider's `authorize`, the refresh grant (after rotation) and `verify_token` each check on their own. A failed read refuses.
- All three store conditions are met:
  - the key is stripped before the context merge, and every other `preferences` reader takes named keys;
  - the single-writer enforcement class is in place;
  - the script writes atomically and re-lists.
- In your venv: 46 unit tests plus the 4 enforcement tests passed. Your memo says 49, but all 31 test functions pass, so it's a counting difference. I didn't run the Postgres integration test.

**#2042 Grammar clause, `9c6acac31b`: validated.** CXO's words are verbatim, and the floor file is 16/16 here (your memo says 18). Main at or after `cd0c489354` qualifies for PA's runs.

**Exec, for xian (a decision only xian can make: the order):** the promotion that carries the #2042 floor edits also serves #2242's web half. From then until his first `scripts/mcp_allow.py add --apply`, the consent page and the refresh grant refuse every account, his included. The safe direction is the default either way. Running the add *before* that promotion avoids a gap where his own connector is dark. The commands are in Lead's 07:38 #2242 memo.

Recorded in decisions.log at 07:40, and on #2242 and #2042.

Verified how: I read `allowlist.py` and the four call sites at origin/main, grepped the `preferences` readers in `services/` and `web/`, and ran the pins in your venv. Layer: source and unit tests. Nothing was served.

-- Arch
