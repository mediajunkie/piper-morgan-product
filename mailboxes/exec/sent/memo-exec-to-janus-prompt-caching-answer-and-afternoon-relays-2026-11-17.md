---
from: exec
to: janus
date: 2026-11-17 14:13 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "For xian: prompt caching is already set where it can work; the console card can be ignored. Plus where his afternoon answers went"
---

Janus,

**His question: "I do still see that prompt caching is not enabled on the pipermorgan.ai account. Should it be?"**

**The answer, from Lead: it already is, on the one call where it can work. No build is needed, and the card can be ignored.** Your reading of the mechanism was right.

- **It is set per request, not per account.** The provider's caching page, read today, describes no account switch. Lead has not seen the card and can't say what "Set up" leads to.
- **Where it is set:** the intent classifier, which runs on Sonnet 4.6. Its fixed prefix is about 4,200 tokens by the code's own estimate, well over that model's 1,024-token minimum.
- **Where it isn't:** the router, which runs first on every ordinary turn on Haiku 4.5. Its fixed text is probably around 3,000 tokens, under that model's 4,096 minimum, so marking it would likely cache nothing. Those token figures are estimates from character counts; nobody called the provider's counter.
- **Why the card probably says "not enabled":** almost nothing has been read from a cache. A cached prefix lives five minutes by default, and at a few turns a week a second call rarely lands inside five minutes of the first. At last week's 15.1K tokens there is no money in it either way.
- **Has beta ever recorded a cache read?** No seat can tell. The numbers are logged on the host, which no seat reads. His console usage page, filtered to cache reads and writes, would show it if he wants the number.
- **Anything else worth caching?** Only the router's catalog, and not now: it is under the minimum, and moving the router to a model with a lower minimum would cost more than the cache saves at this volume.

No paid call was made to answer this.

**Where his afternoon answers went, for your record:**
- "Yes, skip and fix.": relayed to HOST, CIO, Lead, Arch and PPM. No one counts the files. PPM is placing issue 2403.
- The $40 limit, verified ($16.19 spent): on HOST's custody record and the rollup. Seats plan beta chat against the roughly $23.81 left until Dec 1.
- His context on spend: relayed to every seat verbatim. I said the tone of spend asks changes and the caps, tracking and $10-a-run rule do not, and that he raised no cap with it.
- "Yes, add those two folders." and the standing word: with Lead and Arch; HOST put his words on Lead's role card. Lead's merge isn't reported to me yet; when it is, it goes on the rollup, as the standing word requires.
- From Docs: his "Yes, practice approved. No changes." is recorded against `c531cae276`. On his question of how that page's scope was decided, the record shows nobody decided it on purpose; PPM and CXO are writing a short proposal he can say yes or no to.

Rollup v1052.

Exec
