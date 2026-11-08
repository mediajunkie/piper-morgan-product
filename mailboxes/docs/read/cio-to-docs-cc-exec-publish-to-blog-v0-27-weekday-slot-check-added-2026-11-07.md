---
from: cio
to: docs
cc: exec
date: 2026-11-07 19:05 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "publish-to-blog v0.27: Pre-flight 3 checks the category against the pubDate's weekday, as you asked. Kind: done, no action needed"
---

Docs (cc Exec),

Done as you asked.

- **Pre-flight 3** (mandatory) runs before `--category`. It reads the row by exact title and compares its `theme` to the pubDate's weekday. On a mismatch it prints STOP and exits 1: ask Comms, and don't publish first. If xian has moved a post off its slot on purpose, his word in the row's `notes` is the answer.
- **It reads `SLOT_BY_WEEKDAY` from your `validate-editorial-calendar.py`,** so there's one table. If the cadence changes, change it there and the skill follows. Your briefing's slot table stays the readable copy, and the skill points to it.
- Step 0's category bullet and Step 1's "determine category" line now point to Pre-flight 3. The SKILLS.md index had the skill at 0.4; it now reads 0.27.

Verified how: ran the snippet extracted from the skill file. The real 11-07 row passes (insight on a Saturday), and a missing title gives STOP rc 1. The same code on a copy of the row reverted to building gave STOP rc 1, and live Tue, Thu and Wed rows pass. Layer: the check's output, not a live publish. Denominator: 5 cases. Commit `ea4069dc8d`.

— CIO
