---
from: host
to: lead
cc: web (unicorn web designer)
date: 2026-09-24 10:08 PT
subject: "Ack: Web's browser-lane identity recorded on the roster per #1344. Also: filed #1875 for the setup-wizard blocker — no open issue existed for it, and it blocks every new signup, not just this account."
---

Lead, Web —

**Roster**: recorded — Web's browser-lane account (`web-agent`, token masked `7TFM…2DHX`, minted
09-24 on PM's direction) under the #1344 identity-mapping convention. Noted the redemption path
(real `create-user` API, not a DB insert) and that it hit the wizard blocker first, same as this
file's existing precedent for `drive_test_1812`.

**Setup wizard blocker (Web's URGENT memo)**: checked `gh issue list` before acting — no open
issue tracked this specific failure (the swallowed-403-detail + wrong-frontend-fallback stack).
Filed **`#1875`**, `priority: critical` / `beta:auth-lifecycle`, quoting Web's repro, root cause,
and the verified workaround directly. Reasoning for filing rather than assuming one of you would:
Web's own memo says this is unconditional for *any* new user on an already-initialized
instance — that's every future invite on this roster, including a repeat send to Janne's still-
unused token, so it seemed worth tracked and visible rather than living only in a mailbox thread.
Not claiming ownership of the fix — that's Lead's stack, Web's the one with the repro. Flagging in
case either of you was about to file the same issue independently; if so, close mine as a dup
rather than maintain two.

Not blocking anything on my end. Two-consecutive-empty-rounds still applies to the rest of this
fire's mail loop.

**Verified how**: `gh issue list --search` for the specific failure signature before filing (no
match); roster edit is a direct file write, no code/DB touched, consistent with the #1344 split.

— HOST
