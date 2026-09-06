---
from: comms
to: exec
cc: xian (ceo)
subject: "Workstream review #059 — Comms. Window Aug 28–Sep 3. Narrative front closed 24 days in one push, two Ships/beats published, three self-corrections, and one real miss that survived four review layers."
date: 2026-09-04
---

# Workstream review #059 — Communications

**Window**: Fri Aug 28 – Thu Sep 3, 2026. Filed same morning as kickoff.

*`scripts/sprint-truth.py` not run — this report makes no completeness/progress claim about the GitHub sprint or build queue; the claims below are about publishing cadence and editorial verification, a different denominator entirely (calendar-CSV-derived, cited directly below).*

`ROLE-PORTFOLIO-COMMS.md` §2 refreshed as part of writing this review (was Aug 4/9, now Sep 4) — the table below tracks the refreshed version.

---

## §0 — Progress against portfolio goals

| Portfolio line | Verdict | Evidence |
|---|---|---|
| **Building narrative cadence** | **ADVANCED — the window's biggest single event** | The Aug 4 portfolio flagged the queue running dry after Aug 18 as the one item I held with a real date behind it. **That stall is fully resolved.** The narrative front had sat at Aug 8 (Beat 6) for 24 days; closed to Aug 31 in one Sep 1 push — 7 new beats drafted, each fact-checked against primary sources via dedicated subagent research, calendared front to back (Sep 10 through Oct 1). Beat 4 ("A Sender-Impersonation Bug, Four Days Before Beta") published + Medium-syndicated Sep 1. Beat 5 ("Repetition Isn't Convergence") published + Medium-syndicated Sep 3. Two insights also published in-window: "The Orphan Migration" (Aug 29), "Two of Me" (Aug 30). Queue now sits at 8 building beats + 5 insights, all `drafted`, healthy runway to Oct 3. |
| **Editorial mechanism upgrades** | **ADVANCED** | `template-audit` v1.5→v1.12. Two new checks, both paid for by a real miss — see §1. `continue-narrative` v1.0→v1.1: a chronological-order-only rule and an under-sampling caution, both added the same day I made and had to correct the exact mistakes they now prevent. |
| **Weekly Ship pipeline** | **ADVANCED, with a real miss worth naming** | #058 reviewed, tightened at PM's request (1,891→1,856 words — a genuine duplication removed, not padding cut for its own sake), published + LinkedIn-syndicated. The published title shipped sentence-case; see §1. |
| **Verification discipline** | **ADVANCED — the whole window's throughline, see §1** | Three self-corrections owned same-day, one real miss that survived my own gate, one instance of checking a whole surface rather than trusting a single fix. |
| **BYOC marketplace positioning** | **SPLIT, both halves moved** | Listing copy remains correctly held — PM's ESSENCE ruling (ratified Aug 30, ahead of schedule) confirmed MCP stays in Production and gates public beta; PPM separately found the hosted-MCP surface has 0/15 acceptance criteria and doesn't exist in runnable form. The marketplace *narrative* — a distinct artifact — moved: PM picked Angle B on a 24-day-open question Sep 1, drafted same day, calendared Oct 3. |
| **New this window — ChicagoCamps talk prep** *(not yet in the portfolio, added as a note)* | **NEW** | Full script (~2,350 words, 3 acts matching PM's sent abstract) + slide plan drafted Aug 29, including extracting real house style from the surviving Rosenverse-talk archive images rather than guessing at it, and finding 2 of the needed slide images already exist and can be reused (one a genuine thematic callback, not just convenience). PM reviewing this week. |

---

## §1 — Verification discipline: three corrections, one miss, one full-surface check

This window's real throughline, and it's mostly about my own record rather than what I caught in others' work.

**Three self-corrections, each owned the same day it was made:**

1. **Aug 29 — asserted a negative without checking it.** Told PM "I don't have email access" when asked to help plan a conference talk. PM pushed back directly ("I'm pretty sure you do have MCP access... did you try?"). I hadn't. Ran `ToolSearch` properly — the claim turned out to be correct, but it had been asserted from assumption, not verified, when it was made. The gap was in *how* I answered, not the answer itself.

2. **Aug 30 — filled in a column that wasn't mine, then told an external party the wrong rule.** Resolving a Dispatch-PM syndication-backlog thread, I wrote `mediumURL`/`linkedinURL`/`liPubDate`/`status` on two calendar rows and told Dispatch-PM "Comms is the sole hand-editor" of the calendar. Docs corrected me directly. Re-read `.claude/skills/update-calendar/SKILL.md` rather than take anyone's word for it — confirmed the actual convention (ratified Jul 29) is multi-writer by column, and I'd written exactly the four columns Docs owns. No data conflict (different rows), but a real boundary miss, compounded by generalizing it into bad guidance for someone outside the team. Corrected both Docs and Dispatch-PM same-fire; saved a durable memory on the general lesson.

3. **Aug 30 — flattened a caveat into a false ship condition.** Synthesizing three colleagues' BYOC research into a v4 listing-copy draft, I compressed CXO's own honestly-stated caveat ("I have not attempted an upload myself") into a hard "ship condition" that implied more certainty than the source had. Web's live test then hit a *different* bug than the one my condition named — my fix wouldn't have caught what actually broke. CXO caught the flattening; I retracted the "ready to ship" framing the same day, before it reached PM as final. (The thread kept moving after that on its own — PPM found the deeper structural problem, and CXO went through two more rounds correcting their own interim positions — but the retraction was mine to make and I made it same-day.)

**One real miss that survived my own gate:** Ship #058 published with a sentence-case title ("What we actually had") against a corpus that's 100% title case across the 8 most recent Ships and 10 most recent narratives/insights. It passed Exec's draft, PM's own voice pass, my `template-audit` run, and Docs' independent post-publish audit — four layers, all reading for sense, none checking case. PM caught it after publish and fixed it directly. I added title-case verification to the audit the same day (folded into the existing title check), tested against the actual defective title, the corrected title, and a 10-title false-positive sweep before calling it done.

**One instance of not stopping at the first fix:** Beat 5's own audit caught a stale footer tease — teasing Beat 6, when the calendar's actual next-scheduled item had shifted to an interleaved insight. Rather than trust that single correction, I verified the whole forward chain (18 pubDate-ordered items) with a script instead of eyeballing it, and found 8 more footers broken the same way — a uniform off-by-one from an older insights batch getting interleaved into the beats slate after most footers were already written. Repaired all 9 (across 8 files, spanning Sep 6 through Sep 27), re-verified the full chain clean end to end. Same discipline the title-case check came from, applied one day later: a suspected pattern gets checked across its whole surface, not patched at the one instance found.

**The pattern across all five**: this window's verification work was mostly aimed at my own output, not just what crossed my desk. Two of the three self-corrections were caught by someone else and owned once named; the miss was caught by PM after four layers including mine missed it; the one clean win (the chain check) is the same instinct that produced the miss's fix, one day later, applied proactively instead of reactively.

---

## §2 — The footer-chain repair, in brief

Worth a closer look as this window's cleanest instance of a check earning its keep beyond the single defect it was built to catch.

Beat 5's footer-tease check (a mechanical part of `template-audit`, itself only two days old) found one broken link: the piece teased "More Than Anyone Ever Reported to Me," but the calendar's real next-scheduled item was an older insight that had been given an earlier slot sometime after the footer was last written. The fix was a one-line change. Before treating it as isolated, I ran the same check against the entire forward-scheduled queue — 18 items, Sep 3 through Oct 3 — rather than assume the rest were fine because this one had just been fixed.

8 more links were broken, every one skipping exactly one slot ahead of its rightful target — the same interleaving cause, recurring silently across three weeks of already-drafted material. The tell that confirmed it as one uniform defect rather than scattered drift: each broken file happened to be holding the *correct* tease text for the file one slot downstream of its actual target, meaning the whole chain had shifted by one position at some point and nothing had propagated the correction. Fixed by shifting the existing (already-accurate) copy down the chain one slot at a time, writing fresh copy only for the two links with no donor text available, and resolving one placeholder that had been sitting open in "Described Is Not Running" since Aug 29 waiting for its rightful target to finally get scheduled. Re-verified the full chain script-clean end to end after.

Nobody asked for a full-chain audit. The prompt was one broken link on one piece publishing that day.

---

## §3 — Commitments

**Fulfilled**: two narrative beats + two insights published, all four Medium-syndicated · one Weekly Ship reviewed, tightened at PM's request without cutting substance, published + LinkedIn-syndicated · the 24-day narrative-front stall fully closed, 7 beats drafted and fact-checked in one push · two `template-audit` versions shipped from real misses, each verified against actual controls before calling it done · `continue-narrative` gained a permanent fix for a mistake I made and corrected the same day · a systemic 9-link footer-chain defect found and repaired across 8 files · three self-corrections owned same-day rather than left standing · a full self-verification pass on `BRIEFING-ESSENTIAL-COMMS.md` (fixed a broken reference and two real misconceptions the doc had been propagating) · ChicagoCamps talk script + slide plan delivered.

**Outstanding**: **8 building beats + 5 insights**, all `drafted`, awaiting PM's voice-pass + art — the queue is healthy but nothing in it moves without PM. **Series structure (era split + blog-index featuring)** — raised by PM Aug 2, genuinely open, PM/Web's call. **ChicagoCamps talk** — script delivered, PM reviewing this week; a dry-run window (~Sep 1-5) was mentioned and hasn't surfaced yet, watching for it. **website#35** — root cause found and fixed in code independent of confirming the specific incident; PM watching for recurrence, not actively pursued further.

---

## §4 — Window shape

No capacity events this window (unlike Aug 21-27's usage-limit outage) — six fires most days, no gaps, nothing stranded.

The shape worth naming: **this was a window where the corrections outnumbered the catches.** Most weeks I report what I found in someone else's or my own prior work; this one, three of my own real-time claims needed correcting the same day I made them, one defect got past my own gate entirely, and the one unambiguous win (the footer-chain check) came from applying the exact same "check the whole surface" instinct that had just closed the title-case gap the day before. Worth saying plainly rather than only reporting the wins: the corrections are what the discipline is actually for, and this window had more of them than usual.

— Comms
