# Building-narrative slate proposal — Beats 24–28 (work span Jul 16–28)

**From**: Communications · 2026-07-29
**Method**: `continue-narrative` v1.0 → `building-narrative-method.md` §5
**Status**: candidates for PM's steer. **Nothing drafted, no calendar rows created yet** — per the continuation discipline, slate shape is PM's call before drafting (same handling as the Jul 16 slate).

---

## Where the front actually is

**The front = 2026-07-15**, *The Architect's Own Trap* (covers Jul 12–15, pubDate Aug 18).

Established by sorting `theme=building` rows on **source-work-period**, not pubDate, and **counting beats only** — insights don't move the front (§1.3). Verified: no drafted beat covers any day after Jul 15, and the orphan check is clean (0 drafts without a calendar row). So **Jul 16–28 is genuinely open at the beat level**, and it is contiguous with the front — this advances, it does not backfill (§1.2).

Omnibus coverage for Jul 16–28 is **complete, 13 of 13 days**, so this assessment reads sources rather than reconstructing.

## The structural problem this solves

| Track | State |
|---|---|
| **Building narrative** (Tue/Thu) | Aug 11, Aug 13, Aug 18 — then **empty**. |
| **Insight** (Sat/Sun) | Continuous through Sep 19. |

The building track **runs dry after Aug 18** while insights keep publishing every weekend. Five beats fill the next five Tue/Thu slots — **Aug 20, Aug 25, Aug 27, Sep 1, Sep 3** — carrying the narrative into early September.

## Verdict

**A beat has emphatically taken shape — five of them.** This is a slate, not a single next beat, and it wants tightening (§1.4: draft long, then tighten). It is also the strongest run of material since the alpha-launch arc, because the whole span has one spine: **the team turned its attention from the product to its own instruments, and found the instruments lying.**

That spine is *already load-tested* — Ship #053 "The Invariant Held" (Jul 17–23) draws on the middle of it, and m-44 was formally filed on Jul 27. The narrative can tell it in story order without inventing a frame.

---

## Beat 24 — Jul 16–18 · *"More Than Half of It Was Lying"*

**Through-line**: they set out to delete dead code and discovered the bigger problem was code that *faked success when reached*.

The Finish-the-Unfinished sprint went from PM ratification to a met acceptance gate in about two days — a census froze the backlog (254 broad-except handlers, 39 unscoped reads, 9 stale stubs, 78 todo markers), guards went live, 18 P0s closed. Then Jul 18's Tier-3 batch ruled on 16 modules in 6 families, and Arch named the through-line the day it landed: **more than half was fabrication-removal, not dead-code cleanup — code that lies when reached.** The batch's sleeper was a flag-gated live simulation quietly blending fake results into real ones. The `# nie-ok:` mechanism was born to distinguish a silent-zero stub (a regression) from a reviewed loud stub (an improvement).

**The turn**: Jul 17's pre-flight check caught a classifier `NameError` that would have silently degraded *every* primary classification to a fallback default. A four-line import fix. It never reached beta.

**Why it earns a slot**: it's the origin of the honesty theme the rest of the slate pays off, and it has a clean single-sentence hook.

## Beat 25 — Jul 19 · *"The Sunday That Held Everything"*

**Through-line**: one Sunday carrying a restoration, a data-loss scare, and the end of a forty-run losing streak.

All eleven roles came back for the first time since a Jul 13 reauth event had killed crons for three to six days — most ran self-heal passes before touching new work. Mid-session, a push-retry that reused a stale snapshot silently reverted three files of a colleague's already-landed work; a *different* role found it, the author root-caused and restored it, and a durable rule was written — all inside one session, across four roles. The same day, CI's smoke gate went green after **40+ consecutive red runs**, four root causes cleared in one sustained pass. And Ship #052 was collected, cross-verified and drafted while PM was away.

**Why it earns a slot**: the highest-density day in the span (its omnibus is 575 lines), and the data-loss recovery is a genuinely tense, human story with a clean resolution. It's also the beat that most directly shows the team catching *itself*.

## Beat 26 — Jul 20–23 · *"The Burn-Down"*

**Through-line**: one role, largely alone, took a chronically-red pipeline from 40-plus consecutive failures to green — and the drain kept coughing up real production bugs as a byproduct.

CI went fully green for the first time in the repo's visible history. The #1452 harness was designed-to-green in a day, and then the waves ran: 634 → 570 → 272 → 105, every removal CI-arbitrated rather than assumed. Six real product fixes surfaced *because* of the drain, not as separate work — a keyless documents surface silently 404ing, a usage-cap middleware dressing downstream errors up as capacity limits in production, a loop-bound Redis pool, an embedding constructor that 500'd an entire feed. Beta reached v28.

**The turn, and it's the good kind**: Jul 22, the role doing all of this **lost the entire day to a fifteen-hour session freeze.** That's what made the migration decision concrete rather than theoretical.

**Possible split**: this could be two beats (the burn-down; the freeze that forced the move). My read is it's stronger as one — the freeze lands harder as the interruption inside a triumph than as its own piece. **PM's call.**

## Beat 27 — Jul 24–25 · *"Moving House"*

**Through-line**: relocating a ten-role team to a new machine *and a new account*, and discovering mid-move that several safety nets had never once fired.

PM sharpened the risk from "path" to **"account"** — a path change orphans content that still exists, a different account can't see any of it — and that reframing changed the mitigation. Three portability boundaries got named as genuinely distinct: account-scoped, repo-scoped, device-scoped. Worktree isolation was ratified over a shared checkout on the strength of three real collision incidents inside ninety-six hours.

Then the first two roles actually crossed, and both **verified their successors were alive and working before standing down** rather than taking it on faith. Seven findings landed that day, six of them the same shape: a mechanism reporting success while covering less than it appeared to.

**The line the whole slate turns on**: *a safety net you haven't seen fire is a claim, not a mechanism.* And then that rule got applied to itself — twice, in the same day, by the people who wrote it.

## Beat 28 — Jul 26–28 · *"Clear Is Not a Measurement"*

**Through-line**: the pattern got a name, and then kept turning up **inside the fixes written to cure it.**

A hook that appeared to gate mailbox commits was found to bypass silently in the one command shape everybody actually uses. The investigation is the story: **every rival hypothesis was run down and refuted by the agent who had proposed it**, before the real mechanism was identified — a check reading the index *before* the command that populates it had run. Then m-44 was filed: an "all clear" is emitted identically whether a check measured and found nothing, measured the wrong thing, measured part of its space, or never ran at all — **and the false clear is the dangerous one, because an error gets investigated and a clear gets trusted.**

The instances arrived faster than the fixes. The freeze-watchdog was **alerting on compliance** — the registry assumed a live cycle commits every fire, the procedure tells agents *not* to commit on a quiet hold, so a correctly-executed quiet fire was invisible by construction and one role was flagged three times while demonstrably alive. A watchdog sat dead for two and a half hours because two apostrophes inside awk comments terminated its program, while it logged `all-quiet` with correct-looking denominators. An outside report of "no commits in 24 hours" turned out to be a read of the wrong git ref; there had been 179.

**Why it closes the slate**: it's the payoff. Beat 24 found code that lied; Beat 28 finds the *instruments* lying, names the class, and is honest that the naming didn't stop it.

---

## What I'd want PM to steer

1. **Five beats, or four?** Beat 26 could split, or Beats 27+28 could merge into one migration piece. My recommendation: **five as listed**, with 26 kept whole.
2. **Slot assignment**: Aug 20 / Aug 25 / Aug 27 / Sep 1 / Sep 3 if all five, in story order. Narrative ordering rule says walk the backlog forward by `workDate`, so the sequence is fixed by the work, not by strength.
3. **Titles are placeholders.** *"More Than Half of It Was Lying"* and *"Clear Is Not a Measurement"* are the two I'd fight for; the rest are working labels.
4. **One caution worth stating up front**: every claim above is sourced from the **omnibus digests**, not yet from primary per-role logs. That is exactly the layer where adjacent-number contamination has bitten this series three times — real numbers attached to the wrong event. **Each beat gets a primary-source fact-check at draft time**, and I expect that pass to move some details.

## Footer-chain note

The current chain ends at *The Architect's Own Trap* (Aug 18). Adding this slate means wiring Aug 18 → Beat 24 and chaining forward through Sep 3. Front-advances-don't-backfill: no published post gets re-pointed.

---

# REVISION — 2026-08-01, applying PM's A-plot discipline (§1.5)

PM, 2026-08-01: *"resist the idea that everything has to make it in… sometimes you really have to pick and choose what the actual story is."* Re-read my own proposal against that, and **one beat fails badly, one is soft, three hold.** The honest finding is that I wrote a digest and called it a slate in at least one place.

## The test applied, beat by beat

**Beat 24 — Jul 16–18. HOLDS.**
**A plot, one sentence**: they set out to delete dead code and found that more than half of it wasn't dead — it was faking success when called.
**B plot**: the pre-flight check that caught a classifier error which would have silently degraded every classification.
**Cut**: the ADR-079 owner-scoping contract, the census numbers (254 handlers / 39 reads / 9 stubs / 78 todos), the sprint's gate mechanics. All real, none serves the A plot. → *insight track or Ship*.

**Beat 25 — Jul 19. ⚠️ FAILS. This is the digest.**
I described it as *"a Sunday carrying a restoration, a data-loss scare, and the end of a forty-run losing streak"* — **that's three A plots in a trenchcoat**, and the title I gave it (*"The Sunday That Held Everything"*) is the comprehensiveness impulse announcing itself.
**Re-cut — A plot**: a push-retry shortcut silently reverted a colleague's already-landed work; a *different* role noticed; the author root-caused and restored it; a durable rule came out of it — all inside one session. That's tension, discovery, resolution, and it's about the team catching itself.
**B plot**: the cohort coming back from a multi-day cron death, which is the *setting* for the above rather than a story of its own.
**Cut and moved**: the 40-run CI streak — it isn't a B plot here, it's **Beat 26's A plot** and was double-counted. Ship #052's coordination → the Ship itself.
**Retitle needed**: something naming the actual story, not the day's fullness.

**Beat 26 — Jul 20–23. HOLDS, and gets stronger.**
**A plot**: one role, largely alone, took a chronically-red pipeline from 40-plus consecutive failures to green — and the drain kept coughing up real production bugs as a byproduct. *(Now cleanly its own, with the streak no longer split across two beats.)*
**B plot**: the fifteen-hour session freeze that made the migration concrete.
**Cut**: the per-wave backlog numbers beyond the arc, the six product fixes enumerated. Name two, drop four.

**Beat 27 — Jul 24–25. SOFT — needs a sharper A plot.**
As proposed it was *"relocating a ten-role team and discovering safety nets had never fired"* — two stories again, and the migration half is procedural.
**Re-cut — A plot**: the rule that came out of it — *a safety net you haven't seen fire is a claim, not a mechanism* — and the fact that it was **applied to itself twice within the same day**, by the people who wrote it.
**B plot**: PM's path-vs-account reframe, which changed the mitigation.
**Cut**: the three portability boundaries, worktree-isolation ratification, the provisioning specifics. → *Ship*.

**Beat 28 — Jul 26–28. HOLDS. Strongest of the five.**
**A plot**: the pattern got a name, and then kept turning up **inside the fixes written to cure it**.
**B plot**: every rival hypothesis being refuted by the agent who proposed it.
**Cut**: the watchdog-alerting-on-compliance case and the wrong-git-ref case — pick **one** as the worked example, not both.

## What the discipline changes

**Still five beats, not four.** I tested merging 24+25 and 27+28 and both merges make the problem worse — they'd produce exactly the everything-fits-together artifact PM is warning against. **The fix isn't fewer beats, it's less inside each one.**

**One double-count found**: the 40-run CI streak was doing work in both Beat 25 and Beat 26. That's the specific mechanism by which a slate inflates — material that serves two beats gets written into both, and neither cut it because it was genuinely relevant to each.

**Expected effect on length**: the cuts above are roughly a third of the material I'd have drafted. Given the measured data (§1.5) — that span does *not* predict length — cutting here should land these near the 1,000–1,300 target rather than the 1,400–2,000 the last few months have produced, **without touching the span**.

## Still PM's call

Unchanged from the original proposal: **five or four**, the titles, and the spine. The revision above changes *what goes in each beat*, not the sequence or the dates (Aug 20 / 25 / 27 / Sep 1 / 3). **Beat 25 needs a new title** either way — its current one is the symptom.
