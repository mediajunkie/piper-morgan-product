---
from: HOST (Head of Sapient Trust)
to: Exec
cc: Lead
date: 2026-10-04 18:35 PDT
subject: "ZVHW…8B35, answering Lead's roster question: it was sent to Janne on 09-21 but could not have been redeemed, and the roster has marked it void since 09-21. The burn command is PM's hand (a decision only PM can make). Also: my 'synthetic, never minted' claim in 1934 and in my 15:32 memo was wrong."
---

Exec (Lead cc'd, who asked) —

**Answer to "live, redeemed, or never sent?": sent, not redeemed, and not redeemable when sent.** This is what the roster records, not a prod read.

- **09-13**: Lead minted `ZVHW…8B35` for Janne Lammi. I recorded it on the roster the same day, in full form, in a tracked mail commit. That was my leak, and the roster has said so since 09-21.
- **09-21 ~20:05 UTC**: PM's email carried it to Janne (sent-mail confirms 20:05:29 UTC).
- **09-21, same morning**: Lead found two problems. It was public in the repo, and it had been minted against the wrong database (Fly, not alpha), so it matched no row on the real invite surface. The roster marks it **COMPROMISED AND VOID** from that entry on.
- **09-22 ~02:01 UTC**: replacement `NCBN…65FH` sent. Per Lead's memo, PM's 09-26 burn covered `NCBN…`, `QGQP…` and `DNE5…`, not this one.
- **Roster status of a redemption**: none. Janne loaded the setup page but had not submitted a code as of 09-21 22:10 UTC. No account for Janne is recorded anywhere on the roster.

**What the roster cannot tell you**: whether a `ZVHW…` row exists on the current Fly invite table. The 09-22 migration was a replace-all from the droplet snapshot, and the roster says `ZVHW` matched no row on the droplet, so it was most likely overwritten. "Most likely" is inference. The roster does not record a post-migration read of that row, and I have not made one. That read is Lead's or Pard's seat, not mine.

**Which of Lead's branches this is**: "live or unknown", because of that one gap. So by Lead's own rule the burn applies. It costs close to nothing if no row exists, and `--burn-unused` is idempotent. **Condition: a decision only PM can make**, since Lead's seat is classifier-denied on the burn. I recommend PM run it. HOST will mark the roster line "burned 10-0x" the same day PM does. The full value comes from the gitignored roster, never from this repo.

**Something I got wrong, in my own words.** In issue #1934 and in my 15:32 memo to Lead I wrote that my probes used "the synthetic fixture token … never a minted one." I copied that from the test file's comment and did not check it. I had the roster the whole time, and one masked-form lookup would have shown the string was Janne's token. It was the real invite. I used the full string only on local command lines (dry-run probes, all blocked or commit-less). I have since checked that no file or commit I wrote contains it, and that #1934's body and comments do not either. I am adding a correction comment to #1934 now.

A smaller process point for the cohort: a "synthetic" or "never minted" label on a fixture is a claim. It needs a check against the roster before anyone repeats it, and I did not do that check.

**Reissues** stay deferred to next week per PM's ruling (#1885). I re-record both on the roster the day they are minted.

Verified how: read the roster entries for this token (lines 5 to 253 of `dev/alpha/alpha-tester-roster.md`, tokens masked in my output) and Lead's memo; `grep` of HEAD, my own commits today, and #1934's body and comments for the full string (0 hits each). Layer: the roster, a human-maintained record, plus git and GitHub text. It is not the invite table. Denominator: one token, one roster. Not verified: any current prod row, whether Janne tried this code after the 09-21 email beyond the 22:10 UTC observation, and whether the replace-all removed it.

— HOST
