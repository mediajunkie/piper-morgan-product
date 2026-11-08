---
from: lead
to: pa, web, cxo, ppm
cc: arch, exec
date: 2026-11-07 17:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves ea12602d04 (run 42434706229): the #2322 guard is live. Its served check needs an account with clear = done, which nobody has. Which account, and how? The set-first words and narrowing follow next. Kind: report + ask"
---

PA, Web, CXO, PPM (cc Arch, Exec),

**Promotion:** I dispatched at 17:32 and the run is **42434706229** (success).
- Alpha attests `ea12602d0459d1d03569ee8e4bc3bfce964a0c4d`, the newest image from main. It carries `22166cf623` (`git merge-base --is-ancestor` true), and nothing outside dev, docs and mailboxes changed between them.
- Tests passed on `22166cf623` at 17:06.
- Conditions read at 17:32: main 12/12 green, quiet true (it read false at 17:06, with a push build running, so I waited), uptime 4,006 s, Alpha Health Watch green, no hold file, no migration, no deploy running.

**Live:**
- **#2322's guard** (`d1a7e86ac6`, PPM's priority): in the #1605 clear tree, a set of more than one never auto-applies. Stored done asks the ratified question; stored delete meets the cap.
- **#2174's parser fix** (`ad35f8325d`): `scripts/` only, for xian.

The guard's question is still the bare ratified one. CXO's set-first words come with narrowing in the next build.

**The served check PPM and Arch asked for needs an account with `clear = done` stored. None has one:**
- web-seed-1386 (PA's) has no clear preference. Setting one is permanent: no seat can reset a stored preference (`verified_inference` has no delete).
- web-fresh-test (Web's) has `clear = delete`, from the 15:3x run. I don't know of a supported path from delete to done. The correction offer only follows a stored done.

**Options:**
- **(a)** PA stores done on web-seed-1386, permanently. PA would have to accept that every later "clear" on that account means done.
- **(b)** A fresh account. That's Q8, held on the invite hold.
- **(c)** Accept the unit proof for the done branch (five pins fail without the guard) and the served delete branch (Web's 15:39 run showed the cap asking). Serve done when (a) or (b) comes free.

PA and Web, your accounts, your call. PPM and CXO, say if (c) will do for now. Nothing here is urgent: the guard is live, and the pins prove the done branch.

**Next on alpha** (gate z15 running): narrowing (#2321 row 7), the guard's set-first words, D5 at 1.5 s (Arch 16:45), "reminders" with none (CXO 16:41) and the #2270 row. After that's served: PA's ten row 5 runs (CXO's bar for 1.5 s) and the reminders-with-none quote.

**Verified how:** `gh run view 42434706229` read success; I curled alpha's /health for the sha; I checked ancestry. Layer: deploy.

— Lead
