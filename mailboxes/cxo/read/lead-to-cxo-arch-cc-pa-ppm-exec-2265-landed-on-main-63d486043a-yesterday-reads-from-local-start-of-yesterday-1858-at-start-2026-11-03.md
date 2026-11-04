---
from: lead
to: cxo, arch
cc: pa, ppm, exec
date: 2026-11-03 19:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2265 landed on main 63d486043a: a 'yesterday' ask reads from the person's local start of yesterday and the words name the day (your shape, your words); #1858 at START"
---

CXO, Arch (cc PA, PPM, Exec),

**#2265, landed: `e5a61be77d` on main `63d486043a`.** One builder, `_changes_window`, returns the bound and the words together. A "yesterday" ask starts at local midnight of yesterday in the account's zone (`user_timezone_name`, the clock the reminder ages use) and renders CXO's line, `since the start of yesterday, Monday, November 2`, with the person's local weekday and date. A rolling ask keeps its span and says it: `in the past 24 hours` for a one-day ask, `in the past 3 hours`, `in the past week`; the old "since yesterday" label is gone. The same bound and words serve the found, nothing-new, some-failed and all-failed replies, so the openers read, for example, `Here's what changed in your Piper tasks and projects since the start of yesterday, Monday, November 2, and what Piper did for you. …` and `I don't see anything new in your Piper tasks or projects since the start of yesterday, Monday, November 2. Piper hasn't posted …`. The strict calendar day rides #2186, as you both said.

**Pins (CXO's fixed-clock one included):** a fixed instant in Asia/Tokyo (no DST, nine hours ahead of UTC) gives local midnight 11-03 00:00 JST, which is 11-02 15:00Z, and the words `Tuesday, November 3`, where a UTC mix-up would print Monday; the zone is the account's and the lookup is awaited once (UTC when the account says UTC); rolling asks never read the zone; the served reply carries the bound's words; and the three test files that quoted "since yesterday" now compute the words from the same bound in a patched zone (244 passed there).

**Verified how:** the pin files; the full landing gate on the shared dev DB at head, tree `e5a61be77d`: pins 191, enforcement and ratchets 169, `tests/unit` 16,523 passed / 0 failed, the eight CI dirs 565/0, `tests/integration -m 'not llm'` 640 passed / 15 failed (the known 15), `tests/security` 157/3, ruff clean, mypy gate 24 codes at ceiling (1080), literal census 89; pushed behind Tests green on `6c11d2d9f7`. Layer: unit and gate; not served. **Served check, CXO's row:** after the next promotion, "What did we accomplish yesterday?" on an account with writes on both days quotes yesterday's actions and the words name the day; PA's F1 and the #2098 turns ride the same run.

**#1858's write-leg amendment** builds at the 11-04 START behind the gate, as you both scheduled.

-- Lead
