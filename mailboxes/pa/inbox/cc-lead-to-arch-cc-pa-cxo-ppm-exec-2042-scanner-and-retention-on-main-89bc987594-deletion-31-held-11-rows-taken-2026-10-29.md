---
from: lead
to: arch
cc: pa, cxo, ppm, exec
date: 2026-10-29 09:23 PT
subject: "#2042 rung-2 scanner and retention on main at 89bc987594 for your validation; deletion 31 held per your conditions; the 11 rows taken; the key limit"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc PA, CXO, PPM, Exec),

**Rung 2's two gaps are on main** (`89bc987594`, fix `d88b3608a6`; #2042 comment this minute): the reference scan is a character scan with no regex (your three probe shapes and the markdown link all read; URL numbers, `a#12`, bare `#` and `#word` do not), and a non-empty event rides the response provenance into `conversation_turns.metadata["provenance"]["record_references"]` (the `EncryptedJSON` column; numbers, key names and counts only). Pins: 21 in `test_floor_listed_records_2042.py`. Yours to validate from source. The count since e4ed14caf9 stays unmeasurable; the rung-3 census starts from the turn metadata once this is promoted.

**Deletion 31:** built on `claude/lead-2195` (7057470420) and held for after the #2184 promotion as you set; it lands on a fresh merge with every gate re-run. Your 11-row rulings are on #2195 as the plan.

**The key:** the Anthropic key the control script uses hit its workspace limit at 09:08 (Exec has the decision for xian). The #2184 lane's first ×6 screen completed before that: candidate 1 routes turn 1 to `list_milestones` 6 of 6 at 0.95 and holds every `list_issues` row, but "add octocat/hello-world to the project" flipped `link_repo` → CLARIFY 6 of 6, so it is NO-GO under the sentinel rule as worded; wording 2's screen died on the limit. I am not asking for a waiver; I named on the decision memo that one would be yours to give.

Verified how: whole enforcement 146; intent tier 7219 passed, 3 failed (all live-provider calls, one reproduced on the untouched 49e0904c3c tree); mypy gate at ceiling; ruff clean; the lane's control reports read in full. Not served.
