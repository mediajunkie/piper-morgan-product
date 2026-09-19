# Usage-per-account capture — the standing action, written down

**Author**: Lead. **Filed**: 2026-09-19 (standing action taken 09-15; PM reaffirmed same day:
"track more granularly as a rule"). **Status**: PROPOSAL — a capture to make the commitment
concrete, not a ratified design. Shared with Dispatch per the file-drop protocol.

## Why this exists (the incident, and what it showed)

2026-09-14: 48 subagent dispatches from one seat silently inherited the dispatcher's top tier
(Fable) and exhausted a **shared** account ceiling — two roles that dispatched nothing were
refused service and went dark (Exec's analysis memo 09-14; Janus's memo same day). Two durable
gaps that model-pinning policy alone does not close:

1. **Attribution**: when a shared ceiling is hit, nothing records which seat consumed what.
   The 09-14 attribution took a forensic reconstruction after the fact.
2. **Disambiguation**: a ceiling-refused seat is indistinguishable from a dead or signed-out
   one — the freeze-watchdog's standing blind spot ("silence has ≥3 indistinguishable causes").
   Janus's 09-14 alert triage would have been one lookup instead of an investigation.

Per Janus 09-14: the remedy conversation already includes "xian … is adding a daily per-account
usage check." This capture gives that check a durable, machine-readable home so it feeds the
mechanisms that need it, instead of living in PM's head.

## Proposed shape (minimal, deliberately)

One TSV, repo-tracked alongside the heartbeat surface: `dev/heartbeats/usage-per-account.tsv`

```
date	account	pct_of_ceiling	reset_date	source	note
2026-09-19	<account-A>	42	2026-09-21	xian-manual	after wave-2 arrivals
```

- **One row per account per reading** (daily cadence per the Janus memo; more often near a
  known ceiling). Append-only.
- **`pct_of_ceiling`** (or raw tokens if the surface shows them) — whatever the authoritative
  usage page actually displays; capture what is read, don't derive.
- **`source`** — who/what read it (`xian-manual`, `dispatch`, `pard`). Honest provenance over
  automation ambition: a hand-pasted daily row is fully sufficient for both gaps above.

## Who writes, who reads

- **Writer**: whoever has visibility into the account usage surface. Today that is xian
  (account-level), possibly delegable to Dispatch (Desktop-side) if it can read the usage page.
  Piper seats **cannot** self-report this — a seat refused at the ceiling can't write anything,
  which is exactly why the capture must come from outside the refused set (same structural
  argument as the freeze-watchdog's "watcher outside the frozen set").
- **Readers**: the freeze-watchdog / whoever triages a silence alert (row lookup: was the
  account near ceiling when the seat went quiet?); Exec's rollups; dispatch-tier policy audits.

## What this capture needs and does not have (named, not guessed)

- **Seat→account mapping.** I do not know which seats share which account — the 09-14 incident
  proves sharing exists (two non-dispatching roles paid), but the topology is xian's/Pard's
  knowledge. The TSV is useless for disambiguation without it; a one-time
  `account ⇥ seats` companion block (bottom of the same file) would carry it.
- **Where the authoritative number is readable**, and whether Dispatch can read it. Dispatch's
  answer determines whether `source=dispatch` is possible or this stays a daily manual row.
- **Cadence confirmation** — daily is Janus's stated remedy; near-ceiling days may warrant more.

## Explicitly NOT in scope

Automated enforcement, per-request token metering inside Piper (that's app-level, different
layer), or any change to the model-pinning discipline (already standing policy in CLAUDE.md).
This is a bookkeeping surface: cheap to write, structurally outside the failure it observes.

**Verified how**: incident facts from Exec's 09-14 analysis memo and Janus's 09-14 memo (both in
lead/read/ at origin/main), re-read this session; the seat→account topology and usage-surface
questions are stated as unknowns, not assumed. Layer: document synthesis — no live probe of any
usage surface was made (I have no access to one; that's the point of the design).
