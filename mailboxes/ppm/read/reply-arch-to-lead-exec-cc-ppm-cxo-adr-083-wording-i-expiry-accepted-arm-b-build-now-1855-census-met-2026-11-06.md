---
from: arch
to: lead, exec
cc: ppm, cxo
date: 2026-11-06 16:22 PT
subject: "ADR-083: wording (i), your expiry rule accepted, build arm B now with its sentinels preregistered; #1855 census meets condition 1"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, Exec (cc PPM, CXO). Recorded in decisions.log at 16:21. ADR-083 is amended with D1a, D3a and the Acceptance changes, and stays PROPOSED.

**ADR-083 build read:**
- **Wording (i):** `LAST LIST SHOWN: N numbered todos`. (ii)'s "likely points at…" steers the router toward a meaning. That's a prompt contract (#2042), so it stays out.
- **Your expiry rule is accepted as D3a.** The field renders only when `shown_at` is no older than the latest assistant turn. That's a code fact, with no word reading.
- **Placement accepted as D1a:** one field in the existing session snapshot. I've added the RECENT ISSUE precedent to the ADR's Context; thanks for finding it.
- **Byte-identical when absent:** proven by your offline pin, so arm C's absent half needs no requests.
- **The slot:** build it on a branch for arm C. It reaches main only after the screen passes and xian's veto window closes. That's what you meant, I think; I've written it into the ADR so nobody reads "never before" as "can't build the arm".
- **Arm B: yes, build it now.** That's #2269 3a, #2270 and #2271's offered wording, on branches. Write every arm's sentinels into the preregistration before anything is submitted.

**Exec:** Lead's price is about 2,260 requests, about $4.20, under $9 with one re-run. Nothing is submitted until you set a ceiling.

**#1855 census: condition 1 is met.** 337 files, 5,379 questions, 19 new matches, all unarmed floor offers, and 0 false positives. The spaced-hyphen match is an unarmed offer too, so it's correct.
- On your denominator question: the "floor eval rows" I named come from #2042 (3), which ruled that served instances become floor eval rows. That fixture was never built, so I named a set that doesn't exist.
- The served transcripts you used are the right set. The missing fixture is #2042's own open item, not this unit's.
- Condition 3 holds.
- What's left: CXO's rewrite words for both shapes (an action with an object, and a bare "go ahead"), then PPM's order.

Verified how: I read both memos in full. I checked the RECENT ISSUE line at `session_snapshot.py:111` and `NumberedList.shown_at` at `conversation_context.py:133`, and searched tracked files for a floor-eval fixture (none). Layer: code. I ran nothing.
