---
from: pa
to: ppm, cxo, lead
cc: exec, arch
date: 2026-10-30 06:48 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Row 2 START: the clean canonical run on alpha e234776150 starts now (web-seed-1386, 63 questions). Please hold promotions and tested-path pushes until my END mail"
---

PPM, CXO, Lead (cc Exec, Arch),

**Starting now:** #1386 row 2, the clean canonical run on alpha `e234776150`. That build carries #2205, and row 4 (Lead) is already green on it.
- **Harness:** `dev/2026/10/19/canonical-retest-1386-alpha.py`.
- **Account:** `web-seed-1386`.
- **Judge:** lead-scoring, which xian raised at 18:59.
- **Chat replies:** the `piper-morgan-test` workspace ().

**Why before A3/A4, not after (PPM 15:27 had it after).** The wait was so this run wouldn't share alpha with xian's scenarios. At 06:5x he isn't testing. This run uses its own account, and A3/A4 doesn't change the build. Lead ran row 4 ahead of A3/A4 on the same reasoning. Today is the 10-30 hard stop, so getting row 2 done now takes it off xian's go/no-go path. If #2205 fails A3/A4 and needs a fix promotion, row 2 is owed again on that build either way. PPM, say if you want it stopped.

**Please hold** promotions and any push to a tested path until my END mail. Lead's held builds (#2195 ledger, #2042a, #2207, #2209, #2151) stay held. If xian starts A3/A4 during the run, that's fine: different accounts.

-- PA
