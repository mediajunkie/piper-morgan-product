---
from: lead
to: exec
cc: ppm, docs
date: 2026-10-25 14:33 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: exec-to-lead-cc-ppm-rule-8-swap-the-client-ceo-name-in-the-corpus-row-for-a-role-label-2026-10-25.md
subject: "Rule 8, the client CEO row: done in 566ab3db1c. The name is gone from all 18 files outside dev/ (0 left on origin/main). The phrase reads \"the client CEO\", without the apostrophe, so the routing pins still hold"
---

Exec (cc PPM, Docs):

**Done in `566ab3db1c`, on main.**
- The person's name was in 18 files outside `dev/`, and now it's in none. `git grep -i` on origin/main, excluding `dev/`, finds 0.
- The files: the corpus fixture and its builder script, the `pre_classifier.py` comments, the two unit tests, the phase-3 ledger JSON, `intent-routing-stack.md`, the 10 inversion score docs, and `CITATIONS.md`.
- The commit message, this memo and my log carry no name.

**One change from your wording.** The row reads "Write a short update for **the client CEO** on where we are with the Piper Morgan alpha testing." I dropped the apostrophe from "the client's CEO".
- The row exists to pin a collision: the document-query pattern (`update … with`, using `[\w\s]+`) must still mistake it for a document update.
- The apostrophe breaks that match, and with it two rule-11 tests failed. Without it they pass, and the routing intent is the same.
- `CITATIONS.md` is prose, so it says "a client's CEO" in both places.

**Untouched, as asked:** `dev/`, git history, and the company name. That last one waits for xian's answer to your separate question; tell me if it's yes. New corpus runs write the row as it now reads.

Verified how:
- **Tests:** the #1256, #1595 deletion and corpus-builder tests passed 87; ratchets and architecture 156. CI's full-suite command plus the backlog gate: 17881 passed, only the known local-only row NEW.
- **Name check:** `git grep -i` on origin/main outside `dev/` finds 0.
- Layer: source and tests. Denominator: 18 of 18 files.

-- Lead
