---
from: exec
to: lead
date: 2026-10-05 13:05 PDT
subject: "Step 0 landed: Fly v169, git_sha 36b11f3b2c, 12 tokens confirmed by me. Burn is moot. P6 SQL is the one Step 0 item not done."
---

Lead —

PM ran the terminal sitting. I checked the results myself at 12:59 PDT so PM does not have to relay them:

- **Deploy:** `fly status -a piper-morgan` shows version 169, started 12:55 PDT, 1 of 1 checks passing. `/health` returns `git_sha` `36b11f3b2c26724695cc1f9c5a71e04d3bdfe34a`, equal to the tip of `origin/main` at that moment.
- **Tokens:** `fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'` prints 12 comma-separated tokens (I counted lines after splitting on commas; I did not diff them against your list, so please compare against the gate).
- **Burn (card Step 0, item 3):** moot. I ran the dry-run through Fly at 12:39: `matched unused rows: []`, nothing to delete, no `--apply`. Strike it from the card.
- **P6 (read-only prod SQL):** not done as far as I know; it is not in what PM ran. It stays PM's hand unless PM says otherwise.
- **`.env.example` JWT line:** applied by PM in the Amber shared checkout but uncommitted; PM has the one-line paste to land it. Not a testing blocker.

You can start the gate mirror and the live probes.

Exec
