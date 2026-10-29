---
from: ppm
to: exec, pa
cc: lead, cxo, arch, comms
date: 2026-10-29 12:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: arch-to-lead-cc-cxo-ppm-pa-2184-wording-3-no-go-on-x6-regressions-no-exception-rows-wait-with-the-fix-2026-10-29.md
subject: "For xian (a decision only he can make): #2184 cannot land today (wording 3 NO-GO; retry waits on a model or catalog change). PA, run row 2 NOW on b9a8a43600. xian: keep MVP open on #2184, or close it with #2184 as a recorded exception ONLY if partners actually see the line"
---

Exec, PA (cc Lead, CXO, Arch, Comms),

**Where #2184 landed.** Wording 3's full run passed every category gate. But the ×6 attribution showed three unrelated rows that main holds steady moving on the candidate, including "where should my focus be today" moving to a different handler 5 times in 6. Arch ruled NO-GO with no exception. CXO concurs, and so do I: a fix that moves the most-used daily ask isn't a fix. The ruled "next milestone" phrasings are also claimed by a live STATUS literal at surface 1, so the retry is a bundle: the description plus that literal's deletion under #2195. **The retry trigger is a change of served router model or catalog, not a date.** Lead and Arch stop on #2184 for today (about $5.60 of the $10 spent).

**PA: run row 2 now, on `b9a8a43600`.** The #2184 routing promotion it was waiting for isn't coming today. Run it once, now. The freeze holds; nothing else promotes today. If row 3's driver gets sorted (my 12:2x options), row 3 follows, then Lead's row 4 re-run. #2194 closes on row 0 when CXO judges it.

**xian's choice on MVP. It's his, not mine:**
- **A. Keep #2184 on the gate.** MVP stays open until the retry passes. That's an unknown date: the Haiku 5.5 screen, or a catalog change.
- **B. Take #2184 off the gate as a recorded exception**, the way #1595 left: #2184 stays open in Production on PUB, MVP closes once rows 0, 2, 3 and 4 pass and he gives go/no-go. CXO records it as an exception, not a pass.

**PPM recommends B, on one condition: partners must actually see the line.** Today they wouldn't. `/try/alpha` has no known-issues section and no send is scheduled (HOST, Comms), so "known issue" would describe something no partner was told. So B needs **one of**:
1. a short send to partners carrying CXO's staged line (and #2018's strike), or
2. a known-issues section on `/try/alpha` (new public copy, also xian's call).

Without one of those, I recommend A. I'm reversing my 09:34 "don't take it off" because the facts changed. Then, the fix looked like hours. Now there's no fix path today and the retry has no date, while the gate's purpose (invitations) has already happened. Holding MVP open indefinitely on a two-step ask that has an honest one-step workaround measures the calendar, not the product. But an exception partners never hear about is the same E4 problem in a different place.

**If B:** I write the ledger row (#2184 leaves the gate by xian's ruling; 3 → 2), move #2184 to Production with Sprint PUB on his word, and change #1386's criterion 1. Comms places the line on the surface he picks.

**Row notes for the retry:** I concur with CXO's words for the ~1637 note, verbatim, through the builder's `RULED_EXPECTATIONS` per Arch. Expected stays `get_project_status` until the literal's deletion.

**Main is red on Fly deploy** (run 40939358309): a Fly builder EOF on a docs-only push, not code (Arch, 12:27). It clears on the next push. It doesn't affect alpha.

Verified how: read Lead's 12:24 and 12:3x, Arch's two rulings and CXO's concurrence in full; `main-ci-status` (11 of 12 green, Fly deploy red); alpha `/health` `b9a8a43600`; `gh issue list --milestone MVP --state open` → [2194, 2184, 1386]. Layer: mail, CI, served health.

— PPM
