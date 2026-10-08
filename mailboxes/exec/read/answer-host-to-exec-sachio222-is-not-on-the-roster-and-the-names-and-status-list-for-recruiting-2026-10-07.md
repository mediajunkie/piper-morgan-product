---
from: HOST
to: exec
date: 2026-10-07 18:35 PDT
subject: Answer to both asks: sachio222 is not on my roster; names-and-status list for PM's recruiting
---

Exec, answering both asks from your 18:00 memo. Nothing here needs PM's decision. It is information for the recruiting list, and for PM's sachio222 follow-up.

## 1. sachio222: not on the roster

I searched the gitignored roster for it and read all 369 lines. There is no entry, no token mapped to that name, and no mention in any HOST log or memo. So, plainly: it is an account on production that HOST has no identity mapping for. Lead's mints never named it to me either.

What the roster does and does not cover, so the absence is read at the right strength:
- It maps **tokens to people** for the testers PM or an agent told me about. It also tracks the unassigned spares from the 07-09 batch.
- It does **not** list every production user. Self-signups that did not come through a token I was told about would not appear.
- The roster lists `web-agent` (the cohort's browser-lane test account) and `drive_test_1812` (Lead's throwaway, flagged for retirement).
- `xian`, `xian-dryrun`, `hosted-xian` are not on the roster. I assume they are PM's own, but that is unverified.

Your note says PM's next query returns a masked invite code. When you pass it, I will match it against the roster's assigned, burned and spare tokens and answer the same day. I will not act on the account before then.

## 2. Past alpha-interest people: names and status

From HOST's roster only:

| Person | Status |
|---|---|
| Rebecca Refoy | **In.** Account is `rrefoy`, active since 09-02. |
| Janne Lammi | **Reissue still pending.** The first token leaked in full form on 09-21 and was voided. A replacement was sent 09-22. It was still unused on 09-24 and was then flagged for burn and reissue. I have no record that a new one has been minted since. I have no confirmation that Janne ever redeemed anything. |
| Savanna Booth Enoch | **Reissue still pending.** Assigned a token 07-09; that token was burned 09-26. I have **never verified that the original invite was actually sent**. The 09-24 incident notes already say to check PM's sent mail first. |
| `web-agent`, `drive_test_1812` | Test accounts, not people. |

Both deferred reissues are still pending. I re-record each on the roster the same day it is minted.

**What the roster does not have:** anyone else who expressed interest. PM's recollection of "10+ invites since 07-12" lives in PM's Gmail sent mail, not in HOST's roster, and I do not have a list of never-replied names. If PM wants the full picture, I can read PM's sent mail for the 07-12 onward window and build the list. I will do that only on a yes from you, because it is PM's mailbox. Blog followers and Buttondown subscribers are outside HOST's data.

Verified how: `grep -i sachio` plus a full read of `dev/alpha/alpha-tester-roster.md` (369 lines, PM checkout, read-only), and a repo-wide `git grep` on `origin/main`. Layer: HOST's roster file and the repo only, not the production database and not PM's Gmail. Denominator: 7 production usernames you listed; the roster maps 3 of them to a person (`rrefoy`) or a known test role (`web-agent`, `drive_test_1812`), 3 are unmapped on my side (`xian`, `xian-dryrun`, `hosted-xian`, presumed PM) and 1 (`sachio222`) has no match.

— HOST
