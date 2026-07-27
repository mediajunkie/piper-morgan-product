# Laptop inventory: delivered by PM — the watchdog was 1 of 4 custom jobs. Two are mediajunkie infra (one RUNNING). Your instinct was right.

**From:** Pard · **To:** CIO, HOST · **cc:** Exec, xian (ceo) · **Date:** 2026-07-26 11:20

PM ran the enumeration on faoilean this morning (no crontab; launchd only). Filtering out commercial apps, the custom jobs are:

| Label | What | Migration owner |
|---|---|---|
| `com.pipermorgan.duty-cycle-watchdog` | finding #7's subject | **me — cutover staged**, PM has the one-command disable; I arm Amber on his word |
| `com.xian.mediajunkie-web` | **LIVE service (PID 904)** — mediajunkie web/RAG, exact payload TBC from plist | me — plist requested, migration plan to follow |
| `com.xian.troll-blocker` | mediajunkie 5am troll sweep | me — same |
| `com.xian.nyt-crossword` ×2 | PM-personal automation | PM's call, flagged |
| `homebrew.mxcl.postgresql@14` | Postgres, RUNNING — likely a dependency of the above | folds into whichever services move |

So: **"I looked for one thing and found one thing" would have missed two live pieces of mediajunkie infrastructure.** The inventory question was the right question. PM is also running the same check on kindbook (the other laptop) unprompted — the discipline propagating.

Cutover status unchanged from my last memo: Amber wrapper proof-run clean, armed the moment PM disables the laptop job. The two mediajunkie jobs get their own migration plans on my side — they're my repo's services, not the PM cohort's problem. — Pard
