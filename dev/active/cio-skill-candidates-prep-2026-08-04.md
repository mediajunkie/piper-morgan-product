# Skill-candidates review — CIO prep for the first-ever review (Aug 4)

**For**: PM + Exec (Exec maintains the doc; PM disposes). CIO looped in per PM's 2026-07-08 direction for the skill discussion itself and for cadence-alignment with the existing audits.

**Method note first, because it is also a finding**: the review procedure names **memory-eval "wanted but not found" buckets** as *signal feed #1* — *"a recurring 'wanted but not found' across roles is a skill candidate by definition."* Every role has written that bucket at wrap since #974. **Nobody has ever read them.** This prep is the first harvest.

---

## What the harvest found

**221 of 286 July–August session logs carry the bucket** — the discipline is real and near-universal (exec 32 · docs 29 · comms 24 · lead 23 · cio 21 · cxo 19 · arch 19 · ppm 16 · host 16 · pa 11). **263 distinct entries** in the last two weeks alone, across **11 roles**.

**So the feed works. The consumption never existed.** That is worth naming on its own: we built a collection mechanism, ran it faithfully for weeks across every role, and the first read is happening eight months in because a procedure finally pointed at it.

## Convergent themes — clusters appearing across 3+ roles

| theme | mentions | roles | reading |
|---|---|---|---|
| **staleness detection** | 8 | arch · docs · exec · host · ppm | *"a way to know my working tree is stale before I read from it"* (docs) · *"a consumer for `check-staleness.py`"* (arch) · stale branches (exec) · stale pointer to a dissolved sprint (ppm) |
| **verification practice** | 14 | cio · docs · host · lead · ppm | the largest cluster; substantially the m-43/m-44 family |
| **cron mechanics** | 12 | arch · cio · docs · host · pa | what the cron *is*, when it dies, how to know it is alive |
| **test/coverage** | 5 | arch · lead · ppm | concentrated in the dev lane |

## Candidate dispositions — my leans, for PM to dispose

**1. Staleness detection — FOLD, and the reason is the interesting part.**
Five roles independently asked for it. **And Arch's entry says a script already exists — `check-staleness.py` — with no consumer.** So this is not a missing capability; it is a **built-but-unwired** one. The disposition is to wire it into the surfaces that asked (working-tree read, branch sweep, pointer checks), not to build a skill.
*This is the shape I would most want PM to notice*: the most-requested thing across roles was already built and nobody had connected it. A review that only asks "what should we build?" would have missed it entirely.

**2. Verification practice — DON'T-BUILD (as a skill).**
Largest cluster, and correctly so — but it is **methodology, not procedure**. m-43, m-44 and m-45 were filed for exactly this in the last ten days, from incidents rather than from reasoning. A skill would encode as steps something whose whole content is judgment about what a check is measuring. *Escalation trigger that would reopen it*: if the same verification failure recurs after the methodology entries exist and are referenced, the gap is procedural after all.

**3. Cron mechanics — FOLD, already done, flagged so it is not re-litigated.**
Five roles asked what the cron *is*. **PA established it by elimination on 7/29** (session-scoped `CronCreate`; dies on session exit; 7-day auto-expiry; neither death emits anything), and it is now documented in the `duty-cycle-registry.tsv` header along with the consequence that the registry records **intended cadence, not a live job**. The gap was documentation, and it is closed. Recorded here so the next review does not rediscover it.

**4. Test/coverage — defer to Lead's lane.** Three roles, all dev-adjacent. Not a cross-role skill candidate.

## The candidate I would add, which came from the harvest method rather than its contents

**A consumer for the memory-eval feed.** Not a skill — a *habit with an owner*. The buckets are written faithfully by eleven roles and were read for the first time today. My own innovation agenda names the same gap independently (*"nothing consumes a review's second-order findings"*), and Ship #053 supplied the cost: a lesson sat in a filed review **eight days** before we re-learned it expensively.

**Cheapest version**: this harvest becomes a standing input to each monthly review — thirty minutes, no new tooling, and it is already someone's meeting.

## On cadence alignment (the second thing PM looped me in for)

Monthly here does **not** collide with the existing rhythms: Docs's weekly audit, the Friday Ship kickoff, quarterly sweeps. It reads the *outputs* of those rather than competing for the same evidence. **I would not add a fourth rhythm** — and note the review's own don't-overlearn principle applies to this review too.

— CIO, 2026-08-03 (prep for the Aug 4 review)
