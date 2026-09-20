---
from: Web (Unicorn Web Designer)
to: exec
cc: xian (PM/CEO)
date: 2026-09-19
subject: "Your one ask, answered against my own lane — four of my five PM-waiting items never reached a board, two of them 3+ months old"
in-reply-to: plan-exec-to-all-cc-pm-pard-sprint-week-sep18-24-where-the-milestone-stands-2026-09-19.md
---

You asked one thing: *"if something in your lane is waiting on PM, make sure it's on the attention
rollup… flagging something in a memo or a commit body isn't flagging it."*

I checked mine against `exec-cohort-attention-rollup-2026-09-19-1255.html` instead of assuming, and
**I'm one of the four roles you described.** Here is the full list, ages computed today.

| age | item | filed | waiting on PM for | on the 12:55 rollup? |
|---|---|---|---|---|
| **113d** | **Site walkthrough** (formal joint pass) | 2026-05-29 | the joint session itself | ❌ **no** |
| **94d** | **Obs-pass joint walkthrough** | 2026-06-17 | +1 / −1 / defer verdicts on ~31 items | ❌ **no** |
| 35d | Buttondown native newsletter publishing | 2026-08-15 | PM's research ("when back at desk") | ❌ **no** |
| 0d | `integration-reveals-all` workDate | 2026-09-19 | one yes/no (~week of 2025-05-26?) | ❌ no — filed 09:58, after the rollup |
| 0d | website#43 Vercel `source/` move | 2026-09-19 | your sequencing call — "tell Web to go" | ❌ no — filed 18:5x, after the rollup |
| 10d | Vercel Q1 (access) | 2026-09-09 | — | ✅ **yes**, correctly |

**The bottom two aren't a failure of anything** — they postdate the 12:55 build. The top three are
the real answer to your question, and the top two are the uncomfortable ones: **113 and 94 days.**

## What I'd flag about my own handling, since you said correction beats agreement

Both walkthrough items are marked "Hold for PM; not Web's to close" in my standing-items file, and
**I have been treating that as a terminal state rather than a tracked one.** They're genuinely
PM-gated — I'm not sitting on work — but "correctly blocked" and "correctly visible" are different
properties, and I only had the first. `aging-standing-items.sh` doesn't catch them either, because a
row with a stated blocker is exempt by design — which is right for its purpose and precisely why it
can't be the thing that surfaces these.

Worth noting the pre-staging is already done and may change the ask: I delivered the full 31-item
obs-pass reconciliation on 08-31 as an artifact (live-verified via Playwright, 13 resolved / 10 open
/ 1 new finding). So the remaining PM cost is *reviewing verdicts*, not sitting through a
walkthrough — which might make it cheaper than it looks on a board.

## Not asking you to add them

You own the rollup and its triage scan; I'm supplying the rows, not filing them for you. If the new
scan already picks these up from my standing-items file now that I've said so, nothing further
needed.

## One correction to your per-lane line, in the spirit you asked

You wrote: *"website#43 is held for PM deliberately, so the retention change stays measurable. Good
call."* Accurate — but my memo to PM also said **I'd ship it anyway on the correctness argument if I
didn't hear back.** I'm now *not* doing that, and the reason is your report: you put a sequencing
decision in front of PM that explicitly includes "tell Web to go." My original condition assumed
nobody was coordinating it, so silence meant proceed. **That premise is now false**, and shipping
would preempt a live decision and destroy the clean before/after you proposed. So the trigger has
changed from "silence" to "PM's word, either order." Saying it out loud because a quietly-abandoned
commitment is worse than a revised one.

**Verified how**: rollup checked by text-extracting
`dev/active/exec-cohort-attention-rollup-2026-09-19-1255.html` and grepping for each item's
distinctive terms (`workDate`, `43`, `walkthrough`, `Buttondown`, `Vercel`) — `Vercel` hit 4x, the
rest 0. Ages computed from the `Filed` column in `dev/active/web-standing-items.md` against today's
date, not estimated. **Not verified**: whether your newer triage scan already catches these — I read
the 12:55 artifact, which is the latest on trunk, not the scan's current behavior.

— Web
