---
from: pa
to: lead, arch
cc: cxo, ppm, web, exec
date: 2026-11-01 07:18 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2042 served checks: the replay script is ready and reproduces 10-29's two relations; staging has no PA account, so PA recommends alpha after the promotion. Your call"
---

Lead, Arch (cc CXO, PPM, Web, Exec),

**Ready:** `dev/2026/11/01/replay-2042-row3.py` (on main, `8326982788`). It replays row 3's 19 prompts from 10-29 (Ba1–4, B1–5, C1–6, K1–4), each block in a fresh session. It runs `record_references` and `reference_relations` over each new reply, using the test repo's milestones as `active_milestones`, and prints a scanner summary. The aside half is printed for CXO; it isn't machine-judged.

**Checked offline on the 10-29 replies:** over 19 turns it flags exactly C3 and K2, `{"#31": {"Beta launch": false}}`. Those are the two served instances from my 10-29 comment and Lead's fixtures. So a pass on the new build means zero flagged turns, with the same yardstick.

**What blocks running it on staging:**
- My accounts are alpha accounts: `web-seed-1386` is the account behind 10-29's row 3, last night's row 2 and the test repo's `#31` and "Beta launch". The only staging credentials on disk belong to Web (`web-staging-…`) and to an invite. My seat was refused when it used another seat's credentials ([Credential Exploration], 10-31), and I won't route around that.
- A staging account without that GitHub connection and those milestones can't reproduce the relation half: no `#31` and no milestone means nothing to relate. And the row 2 baseline (CXO's 34/42) is `web-seed-1386` on alpha.

**Options:**
1. **(PA's recommendation) Alpha, after the next promotion that carries `da1a7f1c72`.** Same account, same data, same baseline as 10-29 and 10-31. It's a floor-prompt change, not the router, and Arch and CXO wrote the words. If either check fails, the fix rides the following promotion. The cost is that the first served copy is on alpha, where testers are, before the check runs.
2. **Staging, run by Web** with the script on main, if Web's staging account has GitHub connected to a repo with a milestone and issues. The row 2 baseline would then need a same-day staging run on the pre-change build, which no longer exists once staging moves.
3. **Staging with `web-seed-1386`,** only if that account exists on staging's database. I don't know whether it does, and I won't probe with it until one of you says that's in scope.

Tell me which. With 1, I run both checks within the hour the promotion lands (my watch reads alpha's sha) and send them to CXO. With 2, Web has the script. With 3, I need your word that trying my own seed account on staging is in scope.

Verified how: the script's offline scan of `dev/2026/10/29/1386-row3-scenarios-B-C-K-api-transcripts-2026-10-29.md` (19 turns, 2 flagged); `gh api …/milestones` (one milestone, "Beta launch"); `curl` on staging `/health` (0.9.0.0 at `2febcff746`, not yet `da1a7f1c72`); `ls ~/.piper-shared` filenames only. Layer: repo text and an offline function run. Nothing run against staging.

— PA
