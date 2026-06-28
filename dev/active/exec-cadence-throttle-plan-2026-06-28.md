# Cadence throttle plan — run lean through Wed Jul-1 ~9pm (quota reset)

**STATUS: EXECUTED 2026-06-28 12:35** (PM-approved; Exec cron cut 6x→2x `7007f7f7`; cohort broadcast sent to 10 roles `47b12470b`) (Exec, 2026-06-28 12:15 PT; awaiting PM approval → then Exec broadcasts).
**Context**: PM at ~25% weekly quota; resets **Wed Jul-1 ~9pm PT**. Largest draw = autonomous duty-cycle fires (many agents × 6/day), much unconsumed midweek while PM's attention is elsewhere. Aligns with Janus's "run lean through Wed" proposal. Goal: avoid PM provisioning a 2nd paid account just to keep unwatched cycles running.

## The tiers (through Wed 9pm; restore normal after reset)

| Tier | Roles | Action | Why |
|---|---|---|---|
| **IDLE** (suspend cron; resume on-demand or at Wed reset) | **HOST, CXO, PPM** | CronDelete until Wed | No active in-window deliverable: HOST 0 sapient-trust open + M4 work post-RECONNECT; CXO M4 work post-RECONNECT; PPM just shipped roadmap/sprint-list/People one-pager, standing items all gated. |
| **SLOW (~2×/day, AM+PM)** | **Arch, Docs, PA, Comms, Exec(me)** | reduce own cron to 2 fires | Slow-burn/on-call: Arch rulings landed (on-call for RECONNECT Qs); Docs omnibus → once daily; PA sprint-recovery wrapping; Comms idle after arc proposal lands; Exec is PM-engagement-driven, not cron-driven. |
| **KEEP (trim to ~3×/day)** | **Lead, CIO** | reduce to ~3 fires | Lead actively shipping RECONNECT WS-2 / Option C (#1322) — the consumed critical-path work. CIO working the liveness cure (cure-(a) failed → scoping off-machine (b)). |
| **KEEP (off-cron)** | launchd watchdog | unchanged | Liveness safety net; low draw; needed *more* while idled roles can't self-wake. |

## Execution (on PM approval)
1. **Exec cuts its own cron immediately** (lead by example): `32 6,9,12,15,18,21` → `32 8,20` (2×/day).
2. **One broadcast memo to the cohort**: each role reduces its OWN cron on its next fire to its tier target (agents control their own crons; Exec can't reach into their sessions). Single message, not per-role.
3. **Restore**: after Wed Jul-1 9pm reset, broadcast "resume normal cadence."

## Caveat
Idled roles won't self-wake (in-process cron suspends with the session); they resume on PM prod or at the Wed broadcast. Acceptable for a 3-day low-consumption window. The watchdog still nudges if a *kept* role stalls.
