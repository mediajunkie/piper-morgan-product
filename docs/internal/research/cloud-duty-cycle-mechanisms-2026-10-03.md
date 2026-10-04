# Can a duty cycle run in a cloud session? Mechanisms, 2026-10-03

**Ask**: PM via Exec (10-03): "I suspect there are ways to run a duty cycle in the cloud." Find what the cloud
container service offers for scheduled or recurring wakes, and what each can and can't do for a duty-cycle fire.
**Author**: CIO. **Contributors**: PA (first-hand session-cron data). **Status**: research. PM rules afterward;
PA's LaunchAgent stays armed until then.

Every claim is tagged with its evidence layer: **MEASURED** (we timed or observed it ourselves),
**OBSERVED** (read from live account records, not run by us), or **READ** (documentation only).

## What a duty-cycle fire needs
1. A **wake** on a schedule (and ideally on events, such as new mail).
2. **Continuity**: the next fire knows what the last one did. Today that's a warm tmux session plus the
   carry-forward and session log. The 09-27 cold start proved that carry-forward + log alone is enough
   (MEASURED, this seat).
3. **Repo write access**: commit and push to `origin/main` and run `mail-send.sh` (plain git).
4. **Liveness visibility** to the freeze-watchdog (heartbeat commits; unchanged by any of this).

## The mechanisms

### A. Session-scoped `CronCreate` (in-session cron)
- **Dies with the session**: MEASURED (PA: job gone after the 09-29 restart; `durable` is a no-op).
- **Fires late**: MEASURED (PA: 10/10 fires +30 min, about 2× the documented max-15-min jitter).
- **7-day auto-expiry; fires only when the REPL is idle**: READ.
- **Cloud fit**: only if a cloud session keeps a live REPL between fires. UNVERIFIED. **Verdict**: weakest
  option, and the reason the cohort moved to LaunchAgents.

### B. Scheduled routines (`RemoteTrigger` API / the `schedule` skill), the cloud-native candidate
- **Server-side scheduler, cron with timezone** (`CRON_TZ=America/Los_Angeles 0 8 * * *`): OBSERVED (4 live
  routines on this account, all enabled, all last runs SUCCEEDED).
- **Survives anything on our side** (no tmux, no host, no session needed): READ (by design), consistent
  with OBSERVED behaviour (the routines fired while no session was attached).
- **Lateness 5–13 min** past the cron slot: OBSERVED from `last_fired_at` on the 4 routines (08:00 → 08:13,
  19:00 → 19:09, two at +5). Inside the documented bound, and better than A's +30.
- **Each fire is a fresh session by default**: OBSERVED (`persist_session: false` on all 4; every run has a
  different `cse_…` id).
- **A `persist_session` flag exists, and the tool doc says "a routine that posts into an existing session
  adds to that session"**: READ only. **This is the open question that decides warm vs cold.**
- **Two execution targets**: cloud container (`environment_id`, no device: the two morning-brief routines)
  or **bound to a local device** (the two Dispatch-PM routines run on Claude Desktop with local folders):
  OBSERVED.
- **Event triggers**: `create_webhook_trigger` attaches e.g. a **GitHub event** that fires a routine: READ.
  **This is better than polling for us**: a push to `mailboxes/<role>/inbox/` could wake that role directly.
  UNVERIFIED.

### C. OS LaunchAgent + tmux injection (today's cascade)
- Works and is MEASURED (6 seats). **Local only**: it types into a local tmux pane, so it can't drive a cloud
  session. **Failure mode**: injected text can land in a dialog (the 09-27 wedge); Pard now withholds Enter
  and detects that.

## The real trade-off, if PA goes cloud on routines
- **Cold vs warm.** With fresh-session-per-fire (the observed default), every fire cold-loads CLAUDE.md,
  the skill and the carry-forward. That's a context-cache miss each time, at 3–7 fires a day per seat, which
  runs against today's measured burn problem (Exec 10-03: mix, not volume). If `persist_session` gives real
  continuity, that cost largely disappears. **Measure before choosing.**
- **Continuity is solved either way**: the carry-forward + session log already carried a full cold restart.
- **Repo access**: a cloud environment clones the repo per session (READ). Pushing needs the environment's
  git credentials. `mail-send.sh` is plain git, so it should work. UNVERIFIED in a cloud env.
- **Watchdog**: unchanged. Heartbeats are commits wherever they come from.

## The cheapest experiment that settles it (PA's proposal, sharpened)
One throwaway routine, cloud environment, `persist_session: true`, cron every 2 hours for one afternoon,
prompt = a no-op `DUTY CYCLE TICK` for a test role that writes one line to a scratch file and pushes.
Measure:
1. **Same session or new?** (`list_runs`: one session id, or one per fire?)
2. **Actual lag** vs cron (`last_fired_at`).
3. **Push works** from the cloud env (a commit on origin).
4. **Token cost per fire**, cold vs warm (from the run logs).

Then disable and delete it. **Cost**: a few cloud-session fires, within the one-time credit if PM has
claimed it. **It creates a scheduled resource on PM's account, so I'm asking first, not running it.**

**Verified how**: RemoteTrigger `list` (read-only) on this account this fire, with 4 routines' fields
summarized programmatically (prompts not quoted). The RemoteTrigger tool description was read in full. PA's
cron measurements are quoted from their 10-03 memo. Nothing was created, run or modified.

## Experiment results (2026-10-04): MEASURED
Routine `trig_01LdUvFVg5LQs7ouKx6jinoZ` (Haiku 4.5, cloud env `env_013USvwgAt9TXtoSh6cS989B`,
`persist_session: true`, connectors cleared), cron `0 19,21,23 * * *` UTC. **Disabled 2026-10-04
16:08 PDT** after its 3 scheduled fires. Awaiting PM's delete at claude.ai/code/routines.

| Question | Result | Evidence |
|---|---|---|
| **Same session across fires?** | **YES, a warm seat.** One `persistent_session_id` (`cse_01DCcXTRDcQCX4mhcVZYXDdV`); `list_runs` shows 1 session for 3 fires; fires 2 and 3 recalled the earlier fires' times and results; identical session id in all 3 log lines. | routine `get`, `list_runs`, the probe log on the branch |
| **Lag vs cron** | **+4 min, +1 min, +1 min** (19:04, 21:01, 23:01 UTC) | probe lines + `last_fired_at` |
| **Push from cloud env** | **Works**, to the scratch branch: 3/3 pushes succeeded (`6a4d40bbbf`, `c10557a460`, `ac70c54cab`); no PM-side grant needed | branch history |
| **Per-fire cost** | 33–43 s, 9–10 turns per fire. **Tokens: UNMEASURED** (the condensed run log omits usage) | `get_run_log` |

**How the warmth works** (OBSERVED in the run log): each fire **allocates a fresh sandbox** but
**reuses the repo clone** ("Using existing repository clones"; the branch was still checked out) and
**resumes the conversation** ("I see a resumed session"). So a cloud seat keeps both its context and its
working tree between fires, the same two properties our tmux seats rely on.

**Two findings a real cloud duty cycle must handle:**
1. **Our repo's project hooks run in the cloud session** (51 hook executions; our SessionStart hook
   regenerated a mailbox MANIFEST, leaving an untracked file). Good for parity, but every hook has to be
   cloud-safe (no Amber-only paths).
2. **The cloud environment injects its own stop hook** (`~/.claude/stop-hook-git-check.sh`) that tells the
   agent to "commit and push" untracked files. The probe correctly refused ("never edit any other file").
   **A real seat would face the same nudge every fire**, and obeying it would sweep scratch files and
   other seats' MANIFESTs into commits, exactly the broad-staging failure we guard against. Any cloud seat
   needs an explicit instruction to ignore it, or the hook needs disabling in the environment.

**Bottom line for PA's question**: a cloud duty cycle is **viable**. A routine with `persist_session: true`
gives a warm, scheduled seat with ~1–4 min lag and working pushes. Before any real seat moves: (a) measure
tokens per fire on a real tick (needs usage data, perhaps via PM's usage page for that session); (b)
handle the injected stop hook; (c) check every project hook is cloud-safe; (d) decide liveness: the
freeze-check reads git heartbeats, which a cloud seat would write normally.
