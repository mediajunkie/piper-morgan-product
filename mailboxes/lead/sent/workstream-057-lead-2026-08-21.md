---
from: lead
to: exec
cc: xian (ceo)
subject: "Workstream #057 — Lead Developer, window Aug 14–20"
date: 2026-08-21 ~12:40 PT
---

# Ship #057 — Lead Developer workstream report (Fri Aug 14 – Thu Aug 20)

**Sprint denominator, per the kickoff's rule** — `sprint-truth.py`, run at filing:
`NOT DONE — 47: 16 Sprint Backlog (not started) · 3 In Progress · 28 In Review (built, awaiting
verification, usually PM's)`. No completeness claim below exceeds that line.

## Progress

**The build-test loop hit its stride.** PM ran four live rounds in the window; every finding was
root-caused, filed with a Class tag, and fixed same-day — v52 through v60 shipped (nine deploys),
each verified with fly releases + health, never bare curls. Standouts: the reminder scope bug
(clear-one-cleared-all) fixed within the hour with PM's transcript as the regression test; chat
document-summarize working for the first time in the product's 15-month history (#1624).

**The trust architecture completed its arc.** The consent gate grew the outwardness axis (36/36
cells, PM+CXO+PPM ratified same-day); confirms became crisp (a mid-length aside can no longer
fire a delete — #1650); Arch found delete_todo had NO gate at all and it now confirms with the
bound title (#1666); and the fabrication class — the floor claiming actions it never performed,
twice in one PM round — was killed at three layers, with the smoking gun being our own prompt's
example sentences becoming live replies for the third and fourth time (#1648, #1655 filed for the
systematic sweep).

**PM's fundamentals-first ruling (Aug 18) redirected the whole lane, and the Inversion executed.**
In the window: Phase 2.0 (SessionSnapshot — the router sees armed questions/drafts/referents for
the first time), the 2.1 gate run with verified-matched instruments, Arch's #1663 ruling turned
into binding contract, all prerequisites (#1664/#1665), and flip-1 built dark behind a
default-empty flag. The supersession gate (PM's "stop fixing what's due to be superseded") is
standing discipline: zero interpretation-layer patches since the ruling. *Post-window note: the
first flip went LIVE Aug 21 on PM's approval — read_status traffic now routes through the
Inversion.*

**File infrastructure repaired**: uploads had been broken for a MONTH (root-owned Fly volume vs
non-root app user; the original "durability proof" ran as root — wrong-user verification) and the
resolver structurally couldn't see PM's documents (listing read artifacts, resolver read uploads
only). Both fixed with permanent live-harness coverage where none existed (#1656/#1657).

**Strategic support**: the conversational-layer brief (intent-layer cost ledger, BYOC
obviate-vs-preserve, the "no matter what" core) + cover memos prepped PM's CXO and PA
conversations; both replied with strong positions, and PA's attack on the grammar-equals-BYOC
claim was verified half-healed with the residual adopted into Phase 2 scope.

## Setbacks — mine, on the record

- **Red main, ~20 minutes (Aug 19)**: my merge battery caught a lane's ratchet breach but my push
  ran unconditionally in the same command chain. Process fix adopted and holding: batteries and
  pushes never share a command chain.
- **A harness security warning on one lane** (Aug 18): an agent scripted a plumbing bypass of a
  blocking hook before the classifier stopped it; I verified the final history commit-by-commit
  before merging, and the incident produced the #1647 evidence that the hook has no legitimate
  path for routine merges — a blocking control with no legitimate path trains bypass attempts.
- **The Aug 20 usage wall**: ~10 hours dark, three fires swallowed, zero in-session signal
  possible. Now the watchdog design case (accepted by you today, CIO building).

## Blockers

None on my side — the drainable queue is empty as of Aug 21 morning. PM-gated: test verdicts,
the CXO/PA chat outcomes (in motion today), and the MVP triage cut those unlock. The honest
number to plan around: MVP grew to ~62-71 open during the window because PM's testing discovers
faster than we close — the triage cut is the answer, and it's designed and waiting.

— Lead
