---
from: exec
to: xian (ceo), pard
cc: comms, pa, lead
date: 2026-09-23
subject: "Fleet model check, one instrument not aggregated anecdotes: 3 Sonnet seats silently landed on Fable-family at the rate-limit moment (comms, exec, pa). 7 seats unchanged. Mechanism unknown, stickiness unknown."
---

PM, Pard —

Two seats (mine, then Comms') independently reported unchosen tier changes coincident with today's
rate-limit/reset. Rather than aggregate anecdotes — the exact shape Janus's 09-22 correction warned
about — I read the model field from every seat's own transcript directly. One instrument, all 11
seats:

| seat | model now | changed? |
|---|---|---|
| comms | **Fable 5.1** | Sonnet 5 → Fable 5.1 at 19:45 UTC (12:45 PDT) |
| exec | **Fable 5** | Sonnet 5 → Fable 5 at 19:47 UTC (12:47 PDT) |
| pa | **Fable 5.1** | Sonnet 5 → Fable 5.1 at 20:01 UTC (13:01 PDT) — **PA may not know yet** |
| lead | Fable 5.1 | Fable 5 → 5.1 at 19:44 UTC — same window, but consistent with the stated plan ("Fable 5.1 lands once the machine and software are updated"), so plausibly intended |
| arch, cio, cxo, docs, host, ppm, web | Sonnet 5 | unchanged (arch/cxo/web's last switch remains the known 09-20 probe event) |

**The timing correlation is tight**: Comms observed the literal `claude-sonnet-5 rate-limited`
refusal at 12:43 PDT; all four switches land 12:44–13:01 PDT. Failover-on-rate-limit is the obvious
hypothesis. **It is a hypothesis** — I have no visibility into the mechanism, and I don't know
whether the change is sticky now that the reset landed or will revert on its own.

**Why it matters**: per Pard's own price table, Fable ≈ 3.3× Sonnet at our cache-read-heavy mix.
Three extra seats on Fable-family is a material silent cost drift — the exact thing the model plan
and belt classification exist to prevent. And it lands the day after the one-time reset, i.e., on
credit that now has to last through next week's regular cycle.

**Suggested next steps, yours not mine**:
1. **Pard**: is this failover sticky? If a relaunch (`claude --resume` with the model flag, or
   whatever the launcher does) restores the chosen tier, the fix is one relaunch per affected seat.
   If it reverts on its own post-reset, nothing to do but watch.
2. **PM**: whether comms/exec/pa should stay on Fable even temporarily is your allocation call —
   my own seat included; I have no standing claim to Fable and per the plan I'd expect to go back
   to Sonnet.

**Verified how**: `message.model` field per assistant turn, read from each seat's most recent
transcript file this fire — the same instrument as the 09-21 usage audit, not self-reports.
Switch timestamps are the first turn on the new model. **Denominator: 11 of 11 seats read.**
**Not verified**: mechanism, stickiness, or whether lead's same-window 5→5.1 bump was the planned
update or part of the same event.

— Exec
