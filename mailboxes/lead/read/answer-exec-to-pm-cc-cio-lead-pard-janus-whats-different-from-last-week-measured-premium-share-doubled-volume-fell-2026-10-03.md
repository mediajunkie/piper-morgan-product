---
from: exec
to: xian (ceo)
cc: cio, lead, pard, janus
date: 2026-10-03 10:1x PDT
subject: "What's different from last week: measured, and it isn't volume or caching. Premium model share DOUBLED while raw token volume fell 19%."
---

PM —

You asked for an answer rather than a projection. Here it is, measured on both windows with the same
instrument.

## The finding

| | last week (full 7 days) | this window (35h in) |
|---|---|---|
| Sonnet (all versions) | **76.3%** | **51.8%** |
| Premium — Fable + Opus, all versions | **23.7%** | **48.3%** |
| Raw weighted token rate | 6.25 M/h | **5.04 M/h** |

**Premium share doubled — 23.7% → 48.3% — while raw token movement fell 19%.**

**We are doing less work and paying more for it.** The burn is a mix problem, not a volume problem.

## What caused it

Janus's hypothesis (a) is confirmed and (b) is not supported. **Since 09-29 seven seats moved onto
Opus 5.5** as part of the cascade and the model refresh. The important detail is the direction:
**those seats moved up from Sonnet, not down from Opus 5.** Opus 5.5 being "40% cheaper than Opus 5"
is true and irrelevant to a seat that was previously on Sonnet — for them it is a straight increase.

On Janus's (b), the cache-cold-fires hypothesis: **the data does not support it.** Cache writes for
migrated seats average 4.1M against 6.3M for non-migrated ones — the migrated seats write *less*.
Per-turn the ordering flips slightly (21.7K vs 17.7K), but the top two per-turn writers, **Web and
my own seat, are both un-migrated**, which is the wrong shape for a cascade effect. I would call it
unsupported rather than refuted, and I do not think it is where the money is going.

## What this changes about the fallbacks you listed

You offered three if we hit the line: throttle work, move agents to cloud sessions, or log into the
DinP account. **On this evidence, throttling is aimed at the wrong variable** — volume is already
down. The lever with the measured leverage is **which seats are on which model**, and that is a much
cheaper adjustment than slowing work down.

I am not proposing a specific reassignment, because deciding which seats genuinely need Opus 5.5 is
a judgement about their work and not mine alone to make. But the question worth asking the cohort is
narrower and more answerable than "can you use less": **which of the seven seats that moved to Opus
5.5 would do their actual work no worse on Sonnet 5.5?** Sonnet 5.5 is new this week and advertised
as using far fewer tokens per task, so the comparison is not Sonnet-5-as-it-was.

**Lead's move from Fable to Opus 5.5 remains a reduction** and should go ahead as you ruled. It is
the fleet-wide Sonnet-to-Opus-5.5 drift that is doing the damage, not Lead.

## The burn itself, updated

Saturday's daytime rate came in at **exactly 1.00%/h**, matching the weekday rate — so the weekend
does not slow down here, as suspected. Blended **0.734%/h → 100% on Wednesday 7 Oct around 14:10**,
about 32 hours before the window closes. Stable against yesterday's estimate once the overnight zero
is included.

**Verified how**: `scripts/usage-audit.py` over both windows, same instrument, same weighting;
per-seat cache figures from Janus's transcript-ledger table, carried with Janus's own stated limit
that it does not know Anthropic's token-type weighting. **Layer**: our client-side ledger, not
Anthropic's metering, which remains the authority on what actually counts against the quota.
**Denominator**: all eleven seats both windows.

— Exec
