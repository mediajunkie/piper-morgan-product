---
from: lead
to: xian (ceo)
cc: arch, exec, ppm
subject: "STOP-condition escalation: CI red on main two days, and a beta blocker that 403s you specifically — plus what the closure sweep actually found"
date: 2026-08-11 16:1x PT
---

PM — two things need your decision, and a third that changes how much you should trust
the sprint count. All three came out of one sweep this afternoon; none were being tracked.

## 1. 🔴 STOP CONDITION — enforcement ratchets have been red on `main` for two days

Per CLAUDE.md I don't get to decide which failures are critical, so: **verified locally,
worktree clean, zero behind origin/main.**

```
pytest tests/test_completion_ratchets.py
  FAILED test_silent_death_ratchet — silent_death_core: 225 exceeds frozen ceiling 209
  FAILED test_todo_marker_ratchet  — todo_markers:       73 exceeds frozen ceiling  71
```

Both carry `@pytest.mark.smoke` — **the gating subset.** Separately, `Architecture
Enforcement` has failed on **every push to main since 08-09 15:07** (six consecutive
failures confirmed on the runs list), with the mypy gate 17 errors over ceiling across
five codes.

**What makes this worse than "CI is red":** the ratchet discipline is *lower the ceiling
in the same commit as the fix, never raise it.* Nobody raised these — they were **passed,
repeatedly, while the workflow reported red and the signal was absorbed.** A guard that is
red on every push trains people to skip it. That is the same credibility spend as an alert
nobody can action, and the next real regression lands in a workflow everyone has learned
reads red.

It is also the exact class the ratchets exist to catch, happening *to* the ratchets.

Filed **#1600**. The fix is mostly free — of the 16 new silent-death sites, most look like
genuine fail-graceful boundaries needing a `# silent-ok: <reason>` annotation, which is the
mechanism the ratchet provides. **Two of the sixteen came from #1570's own commit.**
I have not started it; say the word and it goes to the front.

## 2. 🔴 BETA BLOCKER — three routes now 403 everyone, including you

Verified directly, not taken from a report: **1377 users in the DB, zero with
`is_admin = true`.** No account matching `%xian%` or `%pipermorgan%` exists at all. The
seeding migration targets `xian@example.com` — a placeholder, not your address. **No code
path anywhere sets `is_admin = True`.** `services/api/transparency.py:15` already says so
in a comment.

#1485 and #1508 shipped correct security fixes that gate seven routes on `require_admin`.
Both are right and should stay. But they turned a **dormant, documented gap into a live
functional block** — and nothing tracked the conversion. **You cannot save the Slack app
token** (#1201) while `PIPER_SLACK_INBOUND_ENABLED` is on for beta.

Filed **#1599**. This needs to be true *at cut time*, not after. The acceptance I wrote is
behavioral — you save a Slack app token successfully — not "the flag is set," because a
config that looks right is exactly what produced this.

## 3. The sprint count you have been steering on was overstated — and it is still 48

I went to work #1573 and found it **already built, tested, and deployed** on 08-10, just
never closed. That was not isolated: **16 open MVP issues were the subject of a shipped
fix commit.** I did not bulk-close them — three agents verified each against its real
acceptance criteria, because a wrong "closeable" makes remaining work invisible.

That caution was correct. Of 16:
- **9 genuinely closed** with evidence (#1507, #1508, #1518, #1529, #1532, #1541, #1558, #1560, #1573)
- **#1411 and #1431 have live defects that still reproduce.** I reproduced #1431's by direct
  execution: *"show me my archived projects"* → STATUS at confidence 1.0. **The `me` token is
  the discriminator** — drop it and it works. Your exact phrasing still fails.
- **#1485** blocked by item 2 above
- **#1480** unit-green but its client-side half is verified only by *grepping the JS file* —
  the JS never executes, and that is the exact line that carried the bug
- **#1423 / #1436** are genuine multi-slice work (~17 of 66 sites; 15% of the mypy census)

**MVP open: 51 → 48.** Nine closed, six new filed. The number barely moved, but its
composition changed a lot — and one of the new six is a blocker on you specifically.

## 4. One correction to our own record, before you retest

#1570's comment promised *"'show me my archived projects' returns archived rows"* after the
next cut. **That is false and will not become true** — the commit never claimed it, the
verification bullet did. I have corrected it on the issue with the working phrasing. A
stated retest step that fails is worse than no step: it spends your time and reads as a
regression rather than a scope boundary.

## What I need from you

1. **#1600** — do I go fix the red ratchets now, ahead of everything else?
2. **#1599** — how do you want `is_admin` granted? Migration against your real address, or a
   recorded one-off? Either is fine; doing it in an unrecorded psql session is not.
3. Deploy word on the ninth cut is still open, unchanged.

— Lead Dev
