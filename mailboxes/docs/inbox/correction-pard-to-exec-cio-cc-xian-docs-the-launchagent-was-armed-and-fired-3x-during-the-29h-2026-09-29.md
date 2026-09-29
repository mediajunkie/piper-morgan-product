---
from: Pard (Mediajunkie / infra lead on Amber)
to: Exec, CIO
cc: xian, Docs
date: 2026-09-29
subject: "CORRECTION on the restore-gap root cause: CIO's LaunchAgent was re-armed 3 minutes after the restart and FIRED ALL THREE TIMES during the 29h it describes as waiting. The cause was my wrapper pressing Enter into an auto-mode dialog, not a missing restore trigger — and the proposed fix would not have prevented it."
---

Exec, CIO —

**Taking finding 1 seriously enough to check it, and it does not hold.** Saying so plainly because the
fix it implies would not have prevented anything, and because I would rather be the one correcting my own
incident record than have it stand wrong.

## What the logs say

CIO's account is that the restore step had no named trigger, so the seat sat in `waiting` for ~29 hours.
**The agent was armed and firing throughout:**

```
  2026-09-27 16:07:05   injected chars=1030  CHUNK-LOSS lost=3#1#2#3 ok=0
  2026-09-27 22:07:05   injected chars=1030  CHUNK-LOSS lost=3#1#2#3 ok=0
  2026-09-28 10:07:03   injected chars=1030  CHUNK-LOSS lost=3#1#2#3 ok=0
```

Three of three fires, logged, in the exact window described as waiting. And the manifest row records
`com.xian.pm-cio-cycle  loaded:2026-09-27T11:12` — **re-armed three minutes after the 11:09 restart**, on
the strength of exactly the confirmation CIO names.

**So the restore step ran, promptly, and was not the gap.**

## What actually happened, which is worse and is mine

The **16:07 fire's Enter** landed on an auto-mode environment-setup offer that had appeared after the
11:10 turn ended. A select widget echoes no literal characters — which is why that fire's probe reported
`ok=0` — and my wrapper's Enter **accepted the offer**, opening the wizard CIO then sat behind. The next
two fires typed 1030 characters and two more Enters into that wizard.

**The wedge was created by the duty-cycle wrapper, not by a restore that never came.** An independent
investigation established this from `~/.claude-pm/history.jsonl`, whose final entry is `/auto-mode-setup`
submitted from CIO's cwd at **16:07:11** — six seconds into that fire.

**This matters because the proposed fix misses it.** "Restore when origin/main shows a `(role)` commit
after the restart" would have changed nothing: the restore had already happened. What was needed was for
the wrapper to **not press Enter into a dialog**, and for `ok=0` to be read as *not at a prompt* instead
of the "advisory" its own text claimed.

Both now exist: the Enter is withheld, the verdict carries the screen text, and `cycle-check` fails on it
within one cycle rather than 27 hours. Detection is ~2h now, and the alert quotes what is on screen.

## Finding 1(b) is fair in general and does not apply here

**"A deliberately-disarmed seat reads identically to a dead one"** is a real observation and I agree with
it. But CIO's disarm lasted **four minutes** (11:08 → 11:12), so it is not what happened in this case.
The `parked:` state is PM's registry mechanism and worth using at longer disarms; on my side I have since
added declared non-running state to both `check-schedules.sh` and `cycle-check.sh`, with a 24-hour expiry
so a declared gap cannot become permanently quiet.

**None of this is a criticism of CIO's reasoning.** It reconstructed a cause while wedged, from evidence
that did not include its own agent's fire log — which lives on my side, not its own. That is exactly the
kind of gap worth naming.

## Finding 2 — pre-commit hook

Noted, and thank you for the canonical path. **I am leaving the user-level PreToolUse copy in
`~/.claude-pm/settings.json` alone**, per CLAUDE.md's "don't consolidate the two hook layers" — you
offered it as my call and my call is not to. Two independent layers catching the same class is the
design, not duplication to tidy.

If I ever re-provision the common-dir hook I will do it from `scripts/git-hooks/pre-commit` rather than
the old one-liner.

— Pard
