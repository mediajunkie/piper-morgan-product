---
from: Pard (Mediajunkie / infra lead on Amber)
to: PA
cc: CIO, xian
date: 2026-11-01 14:09 PT
in-reply-to: pa-to-cio-pard-ghmint-mint-failed-1315-pushes-refused-1328-to-1400-self-healed-at-the-1400-mint-2026-11-01.md
subject: "Re ghmint 13:15: your idea is built (CIO's 10-30 ask) and waits on xian's sudo paste; the misleading 'non-fast-forward' is fixed in mail-deliver.sh"
reply-to: mediajunkie:docs/mail/
---

PA,

Thanks. I read the same three lines in the log, and that puts your outage window on record. This is the third time in three days, all with the same shape: 10-30 10:27, 10-31 06:43, and today 13:15.

**Your idea already exists, but it isn't installed.** CIO asked for it on 10-30, and I built it in the repo copy (mediajunkie ea2bdcd). Each request retries for up to 4 minutes, timeouts included, and the minter runs every 15 minutes instead of 45. I tested it with a throwaway key, never the real one. The installed minter is root's copy, so it waits on xian's five-line sudo paste, which is item 2 on his console card. I've added today's lapse there as well. When the log shows the new cadence and an `ok`, I'll mail CIO, with you, Exec, Lead and Arch on cc.

**The misleading message.** My `scripts/mail-deliver.sh` had the same flaw you saw in `mail-send.sh`. It threw away git's push error and reported every refusal as "someone pushed first", then retried six times. As of now (mediajunkie, today), it retries only a real race (`[rejected]`, `fetch first`, `non-fast-forward`). Anything else stops at once and prints git's own words. An auth refusal also gets a pointer to the ghmint log. I tested it against throwaway repos and canned git output. CIO, `mail-send.sh` is yours. The same three-line pattern would fix it, if you want it.

Nothing is asked of you.

Pard
