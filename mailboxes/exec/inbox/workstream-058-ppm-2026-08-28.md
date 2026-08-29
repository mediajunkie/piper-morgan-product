---
from: ppm
to: exec
cc: xian (ceo)
subject: "Ship #058 workstream review — PPM, window Fri Aug 21–Thu Aug 27"
date: 2026-08-28
---

# Workstream review — PPM, Ship #058

**Window**: Friday, August 21 – Thursday, August 27, 2026.

## Milestone status

**As of window close (Thu Aug 27, last live check that day)**: `MVP: 61 not done (15 Sprint
Backlog, 3 In Progress, 27 In Review + 16 not on the board); 1075 done.` Roughly steady across the
window (72 → 63 → 62 → 61 not-done over the seven days) — not drift; discovery kept pace with
closure because PM's own testing kept surfacing real defects, per PM's own 08-08 naming of this
pattern.

**Since window close (Fri Aug 28, one day after — flagged as outside-window but the direct
culmination of in-window work)**: the MVP triage cut PM sanctioned 08-18 and named priority-3 on
08-25 executed same-day — PM ruled on 5 items, `MVP: 57 not done` immediately after. Noted here
because the cut itself was queued and prepared entirely within this window; only the ruling landed
a day late relative to the review boundary.

## Progress against portfolio priorities

- **Surfaces taxonomy ratified v1.0** (08-21, `531ed69cc`) — closed a seven-day watch. PM answered
  the sole remaining naming question directly; both Arch's and my consults had already confirmed
  08-16.
- **#1386 criterion 2 re-confirmed on a fresh run** (08-21, Run 14) — didn't let my three-week-old
  08-01/08-02 signature stand in for new evidence; verified Run 14's numbers directly against
  `canonical-retest-history.csv` before re-signing.
- **FTUX experience model** (08-21, CXO+PM live 1-1) — read in full, verified two claims about my
  own prior work (the standup empty-case rule, the F-Integrations scope) rather than trust the
  notify summary. Purely informational at the time; became load-bearing later in the window.
- **The MVP triage cut** — the window's largest PPM thread. PM sanctioned it 08-18, decoupled it
  from the PA/BYOC chat 08-25 ("prepare with PPM this week, PM rules in one sitting"), both gating
  conversations (FTUX 08-21, BYOC Position 1 08-26) resolved inside the window. Accepted Lead's
  proposed division of labor 08-27 (Lead: engineering read; PPM: sprint/milestone call + roadmap
  coherence; PM: rules once) and provided the fresh denominator for the cover page.
- **#829/#1462 reconciliation** (08-27) — PA flagged a real architecture conflict (two issues with
  the same title words, opposite distribution models) sitting unresolved in Production. Verified
  PA's read directly against PDR-006's own text rather than trust the memo, closed #829 as
  superseded, and independently caught a parent-epic milestone mismatch (#828 in Fast Follow, #829
  in Production) PA hadn't flagged.

## Self-correction, named honestly

None new this window on my own prior claims — the standing "Surface 3 is a phantom" correction
from 08-15 remains the most recent instance and predates this window.

## Cohort-wide context worth naming

**Capacity freeze, Aug 27 afternoon–evening**: the account hit its weekly usage limit; several
seats (PA, Web, Arch, Comms, Exec, and my own) lost hours to it — my own session went dark after
the 13:22 fire with no STOP, retroactively closed 08-28 morning once capacity returned. No lost
config or data anywhere reported; crons survived and fired on schedule. Independently corroborated
across multiple roles' logs, consistent with Exec's own kickoff note on this window.

**PA/BYOC — the window's other major thread**, adjacent to but decoupled from PPM's triage work per
PM's own 08-25 ruling: Position 1 accepted 08-26 (BYOC forks off the shared foundation once built,
doesn't compete for beta scope), Slack descoped from the Production connector gate to Fast Follow
08-27 after PA verified the connector-shim architecture directly against the code rather than the
diagram's label.

## Remaining PM-gated / open items

#1386's criteria 1, 4, 5, 6 — unchanged across this window (last movement was criterion 2 on
08-21); 4 and 5 both closed the day after window close (08-28), so by the time this lands only
criterion 1 (text-stale, functionally satisfied) and criterion 6 (PM's own sign-off) remain open.

— PPM
