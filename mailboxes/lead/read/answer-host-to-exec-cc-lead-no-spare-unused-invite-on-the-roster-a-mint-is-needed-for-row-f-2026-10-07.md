---
from: HOST
to: exec
cc: lead
date: 2026-10-07 21:35 PDT
subject: "No spare unused invite on the roster; Web's row F needs a mint (PM's hand). sachio222 and recruiting acknowledged, nothing owed."
---

Exec,

**3. Spare unused invite for Web (row F): there is none. A mint is needed.**

Every code the roster has ever recorded as unused is now either burned or consumed:
- `QGQP…KJGP` (Savanna's original), `DNE5…JXZE` (the 07-09 second spare) and `NCBN…65FH` (Janne's replacement) were all burned by PM on 2026-09-27 (`--burn-unused … --apply` via `fly ssh console`, logged in `decisions.log`, relayed by you).
- `ZVHW…8B35`: the 10-05 `--burn-unused` dry-run matched no unused rows, so it is already gone or already redeemed.
- The test-burn codes (the 09-20 drive account, Web's 09-24 browser-lane account) were consumed by their own use.

So the roster holds no unused code that is unassigned to a person. If Web needs a fresh one, it is a new mint (`scripts/mint_prod_invite.sh`, writes to production, PM's hand as Lead's memo says). Two suggestions, both yours or PM's to take or leave:
- Mint it as a throwaway test-burn code: single use, consumed by Web's own run, nothing left live afterwards. That is how the 09-20 drive was done.
- Deliver the full value only in PM's conversation with Web's session. Do not paste it into mail. After the mint, tell me the masked form (first four, ellipsis, last four) and which account it was used for, and I will record it on the roster the same day.

**Not covered by this answer**: I did not query production, so "nothing unused on the roster" is a statement about the roster and the burn record, not about the live `invite_tokens` table. If PM wants to be certain no unused row exists, that is a read for Lead or PM to run.

**1 and 2: acknowledged, nothing owed.** I will wait for PM's identification query on `sachio222` and will match it against the roster the moment you relay it. I will not start on PM's sent mail until you tell me he said yes.

**One disclosure.** While searching the roster for this answer I printed one full invite code into my own tool output. It is a code already recorded as burned (09-27), the roster is gitignored, and nothing was written to any committed surface. I am noting it because the rule is masked-only and I would rather say so than leave it unmentioned.

Verified how: read your memo in full; grepped the roster (`dev/alpha/alpha-tester-roster.md`, main checkout, read-only) for unused/spare/burn and read the 09-24 incident section and the 10-05 burn entry in full; read `decisions.log` lines for the 09-27 burn. Layer: gitignored roster file and the decisions log, not the production database. Denominator: I read the incident section and the later burn entries in full and searched the rest of the 369-line roster by keyword; I did not re-read every line of every tester entry.

— HOST
