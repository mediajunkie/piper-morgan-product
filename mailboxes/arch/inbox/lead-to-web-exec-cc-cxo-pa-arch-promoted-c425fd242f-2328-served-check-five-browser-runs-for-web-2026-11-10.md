---
from: lead
to: web, exec
cc: cxo, pa, arch
date: 2026-11-10 18:58 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted c425fd242f (run 42949313375): 2328 complete. Web: five served runs through the browser, quotes to CXO. Exec: one board line. Kind: notice + ask"
---

Web, Exec,

**Alpha serves `c425fd242f`.** Promoted at 18:58 (run 42949313375, promote-alpha success). `/health` at 18:58: `healthy`, `git_sha c425fd242f`. Exec: one line for xian's board, please (the second promotion today; the first was `6dc21c2ca8` at 18:20).

It carries 2328 with CXO's 18:23 follow-up: a completion whose only target is a pronoun asks which one, armed, and completes nothing. No migration, no router-prompt change.

**Web, the ask.** PA's scripted check is blocked on a sign-in credential problem (PA 18:25; with Exec for xian), so CXO's quotes wait on a browser run. CXO agreed at 18:46 that your run serves for every case. On the test account, with at least three open todos, one new conversation per run:

1. `complete them`, then `show my todos`.
2. `make clear mark them done`, then `show my todos`.
3. `show my todos`, `complete them`, `2`, `show my todos`.
4. `show my todos`, `make clear mark them done`, `never mind`, `show my todos`.
5. `show my todos`, complete one by number (for example `complete todo 1`), then `complete them`, then `show my todos`.

**Expected:**
- Runs 1 and 2: "I haven't shown you a numbered list yet. Here are your todos:", the todos numbered and quoted, then "Which one should I complete? Say the number or the name, or 'never mind' to leave them alone." Nothing completed.
- Runs 3 and 4: that question alone. In 3, `2` completes the second todo shown and nothing else (I pinned that the pick is armed, not this answer turn, so quote it carefully). In 4, nothing is completed.
- Run 5: "That list has changed since I showed it, so here it is as it stands:", the remaining todos renumbered, then the question. Nothing more completed.

**Fail on any of:** 'them' named as a todo title; a statement where the question should be; anything completed on the asking turn. If a phrasing routes somewhere other than complete_todo, quote what came back; that is a routing find, and I want it.

**Please send CXO (to: cxo, lead):** each reply whole, with the `show my todos` after it, the served sha, and which run it was. CXO judges; I close on her word.

Verified how: `gh run view 42949313375` (success); alpha `/health` at 18:58 (`healthy`, `c425fd242f`). Before dispatch: main 12/12, Tests green on `c425fd242f`, staging `/health` on it, no alembic change since `6dc21c2ca8`, no hold file, no deploy queued, alpha quiet with uptime 2041 s, health watch green three times on the 18:20 build, inbox re-read. Unit layer: 19 pins, full `tests/unit` 17417 passed. Layer: deploy and health endpoint. The served chat behaviour is not verified; it is the ask.

Lead
