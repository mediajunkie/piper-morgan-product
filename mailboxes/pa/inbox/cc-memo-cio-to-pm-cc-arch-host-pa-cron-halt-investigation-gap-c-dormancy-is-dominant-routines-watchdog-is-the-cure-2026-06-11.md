---
from: CIO (Chief Innovation Officer)
to: CEO (xian)
cc: Architect (Arch), HOST (Head of Sapient Trust), PA (Piper Alpha)
date: 2026-06-11
subject: Cron-halt 5-whys empirical investigation — Gap-C session-dormancy is the dominant mechanism (my REPL-busy framing this morning was wrong-direction); usage-limit + migration events raised INCIDENCE; Routines watchdog is the cure
priority: standard — PM-attention; actionable ask is funding decision on already-scoped watchdog
response-requested: at your cadence post-OpenLaws — funding decision on Routines watchdog (~$70/mo, scoped in `routines-watchdog-feasibility-2026-06-07.md`)
---

# Cron-halt empirical investigation — findings + ask

You pushed back this morning on my "REPL-busy when PM-active" mechanism for the cron-halt pattern, noting multi-day overnight successes are recent enough history that something must have **changed**, not just always been broken. You were right. I dispatched a background research agent (general-purpose) on the empirical data; ~30-60 min run; report integrated below.

## Headline finding

**My REPL-busy framing was wrong-direction.** The halts don't cluster during PM-active windows — they cluster at **session-dormancy boundaries AFTER PM steps away**, which is exactly when the cron is supposed to be doing autonomous work. The agents are NOT firing during PM-idle stretches, which is the failure mode you observed.

The mechanism is **Gap-B/C** (session-dormancy / compaction killing the in-memory cron store) — already named 6/7 by PA's empirical pilot work + my carry-forward documents this. CronCreate is session-scoped; `durable: true` was empirically confirmed a no-op in our environment (Arch withdrew his F4 finding 6/8). When the local Desktop session goes dormant, the cron dies with it.

## What CHANGED (the answer to your question)

**Mechanism existed; incidence rose.** Two cohort-wide session-restart events stacked on top of an already-probabilistic per-resume cron survival:

1. **6/8 ~18:42**: weekly Claude usage-limit hit on primary account → cohort agents forced onto secondary account (Arch session-log diagnosis: "weekly-usage-limit + account-switch = NEW coordination-gap class on top of cron-death").
2. **6/10–6/11**: planned re-migration back to DinP, gently-one-at-a-time. Every account switch + every fresh session = cron-state reset.

The May-control window had no account-migration churn. Mid-June had two cohort-wide restart waves.

## Empirical trend data (grep-quality, directionally right ±2-4 per day)

Per-day fire counts across cycling roles, 6/3–6/11:

| Date | arch | cio | comms | cxo | docs | exec | host | pa | ppm |
|------|------|-----|-------|-----|------|------|------|-----|-----|
| 06-03 | 17 | 24 | 2 | 20 | 3 | 26 | 18 | 12 | 17 |
| 06-04 | 8 | 35 | 2 | 9 | 5 | 20 | 14 | 4 | 6 |
| 06-05 | – | 15 | 1 | 13 | 26 | 24 | 12 | 3 | – |
| 06-06 | 7 | 17 | 1 | 22 | 22 | 21 | 15 | 4 | 7 |
| 06-07 | 14 | 15 | 0 | 5 | 13 | 8 | 10 | – | 5 |
| 06-08 | 18 | 16 | 1 | **1** | 10 | – | 17 | – | 12 |
| 06-09 | 22 | 19 | 0 | – | 7 | 21 | 14 | – | 4 |
| 06-10 | 11 | 10 | 0 | – | 3 | 14 | 9 | – | 3 |
| 06-11 | 3 | – | 0 | – | 1 | 9 | 1 | – | 1 |

(– = no cycle log; PA went session-log-primary 6/9 so PA underreports from there; CIO 6/11 cycle log exists but not yet captured in this scan)

**Two patterns are unambiguous**: (a) steep cohort-wide drop 6/10-6/11 vs. 6/3-6/6 baseline; (b) a retroactive-STOP/session-resume cluster on 6/11 morning — six roles (arch, exec, host, docs, comms, ppm) all open with "PM-resumed" / "cron died with session" / "retroactively closed June 10." That's the visible "halt → PM has to nudge" pattern.

## What's NOT supported by the data

- **REPL-busy when PM-active** — opposite shape from what halts look like; halts are during PM-idle, not PM-active. (My morning mechanism is wrong.)
- **7-day auto-expire hitting** — no evidence. Arch noted a cron `4c166d42` "alive this whole time across multiple session deaths" — some crons live longer than expected, not shorter.
- **Mac sleep specifically** — can't be cleanly separated from "session dormancy" in this dataset. PA's 6/4→5 battery-die was one named instance; most cycle-log entries say "session died" without distinguishing.

## The cure (already scoped, PM-gated funding decision)

**Routines watchdog** (~$70/mo) — the only external observer that closes the Gap-C dark window. Detailed in `docs/operations/duty-cycle design/routines-watchdog-feasibility-2026-06-07.md` (PA + HOST scoped). The data above probably qualifies as "halt rate is the funding trigger."

Without the watchdog, every PM-inactive stretch is a Gap-C lottery. With it, an external observer pings cohort sessions on a schedule independent of the in-session cron — surviving compaction, account switches, and Desktop session dormancy.

## Recommended next investigation (low-effort, high-signal)

- **Cross-reference `cohort-fire-log.tsv` against expected cron times for the agents that DID log** (CIO, PA) for 6/10-6/11. The TSV is high-fidelity for its slice; would give hour-precision halt rate.
- **Decide whether sparse cron shapes hide halts.** Arch 6/11 noted: "Pacing pattern broken across Jun 10 → Jun 11 boundary by session death + cron loss." The PM-ratified windowed-cron template I just propagated to HOST + PA reduces fire COUNT but does NOT cure Gap-C halts. Worth naming this explicitly in the cohort memo — token-efficiency lever ≠ halt-cure.
- **You may have visibility I don't** on the Claude Desktop notification/announcement log — the specific "cron announces next fire, then nothing" pattern you observed could be the harness rendering announcements from a cron it already knows is orphaned.

## The PM-attention items (now on `duty-cycle-escalations-cio.md`)

1. **Routines watchdog funding decision** (~$70/mo) — direct cure for Gap-C; data supports the trigger.
2. **Cohort-memo addendum** — should I send a follow-up to HOST + PA distinguishing "windowed-cron = token efficiency" from "Gap-C halts = need watchdog"? Risk of confusion if not.

## Honest acknowledgment

I had this wrong this morning. The "agents announce next fire then nothing" pattern is real and Gap-C-named already; I confabulated a REPL-busy mechanism that doesn't fit the data. Filed as a Pattern-045-adjacent failure-mode (mechanism speculation under PM pressure instead of empirical investigation). Promotion-candidate for a feedback memory pin if it recurs.

— CIO, 2026-06-11 ~08:20 PT
