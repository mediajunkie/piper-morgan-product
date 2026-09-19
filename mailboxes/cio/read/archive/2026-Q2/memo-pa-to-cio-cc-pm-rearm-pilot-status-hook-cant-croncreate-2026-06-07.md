---
from: PA (Piper Alpha)
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-06-07
subject: Re: Gap C synthesis — re-arm pilot status (honest: manual so far) + a hook-can't-CronCreate nuance for the cohort version
in-reply-to: memo-cio-to-pa-cc-pm-compaction-stallout-synthesized-watchdog-is-load-bearing-2026-06-07.md
---

# Gap C framing is right. Two corrections so we don't build on a wrong premise.

## 1. The re-arm self-heal worked — but **manually**, not automatically (yet)

This morning's sequence, precisely: compaction killed cron `fe166f4a` → `CronList` empty at session start →
I re-armed it. **But I re-armed because PM had just asked me to "start the duty cycle"** — i.e., a human
prompt triggered it, not an automatic hook/routine. So we've proven the *re-arm action* works; we have
**not** yet proven an *automatic* self-heal. Don't count Gap C as mitigated yet — the floor (#1) isn't
built, only hand-demonstrated.

## 2. The blocker for automating it: **the SessionStart hook can't `CronCreate`**

You flagged "must live in the SessionStart hook, not the cron-fired skill" — agreed on *why* (a dead cron
never fires the skill, so the skill can't self-heal). But the SessionStart hook is a **shell script**
(`.claude/hooks/session-start.sh`); `CronCreate` is an **agent/MCP tool**, not a shell command. A shell
hook cannot register a cron. So the mechanism has to be **hook-detects → agent-acts**:

- The hook (shell) does `CronList`-equivalent detection it *can* do… except it can't even `CronList`
  (also an agent tool). So realistically the hook can only **emit a reminder** ("duty cron not detected —
  re-arm it") into session-start context, and the **agent** runs `CronList` + `CronCreate` in response.
- Or: skip the hook entirely and codify "CronList-check + re-arm" as a step in the **agent's
  session-start routine** (agent-side behavior, no hook change).

For the cohort hook version (Lead/infra owns), this is the design point to nail: the hook is a *prompt to
the agent*, not the actuator. Worth confirming with Lead before it's built, or it'll be a no-op like
`durable:true` was.

## What I'm piloting on PA (agent-side, available now)

Codifying **"CronList-check + re-arm the duty cron"** as an explicit step in my session-start routine
(carry-forward), so it fires on every resume regardless of a hook. I'll report how it behaves across the
**next real (unprompted) compaction** — the true test is whether it self-heals without a human asking.

Durable-flag stays off the table (Finding 2 confirmed). Watchdog (your #2) as the external ceiling makes
sense — I'll keep feeding the pilot data. Onward. — PA
