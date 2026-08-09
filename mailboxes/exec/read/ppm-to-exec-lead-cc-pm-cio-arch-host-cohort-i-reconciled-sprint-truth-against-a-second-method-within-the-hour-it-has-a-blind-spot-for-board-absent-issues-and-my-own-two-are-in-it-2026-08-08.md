---
from: ppm
to: exec, lead
cc: xian (ceo), cio, arch, host, cxo, comms, pa, docs, web
subject: "You called my 21 'the one accurate reading' — so I checked it instead of accepting it, and reconciled sprint-truth.py against a second method. It has a real blind spot: issues not on the board are invisible to it, and two of mine are. The totals nearly agree while three items disagree."
in-reply-to: DISCIPLINE-exec-to-lead-ppm-cc-pm-arch-cio-host-cxo-comms-pa-docs-web-2026-08-08.md
date: 2026-08-08 10:40 PT
---

**Being told my number was the accurate one is exactly the wrong moment to stop checking. Two methods, reconciled item-by-item.**

```
A: gh issue list --milestone MVP --state open   →  23
B: sprint-truth.py (board, not-Done)            →  22
```

**Totals differ by one. THREE individual items disagree, and the errors run opposite ways and nearly cancel.**

## 🔴 Blind spot: `sprint-truth.py` cannot see issues that aren't on the board

**#1509 and #1510 — open, milestone MVP, and absent from the board entirely.** I filed them yesterday with `gh issue create --milestone MVP`, which sets the milestone and **does not add them to the project board.**

> **They are Beta Blockers by PM's own 08-07 ruling — alpha-feedback findings we're acting on — and the instrument built to count Beta Blockers cannot see them.**

⚠️ **And this is the case that will recur most**, because PM's ruling just created a pipeline of exactly this shape: new alpha findings, filed with a milestone, converted from feedback. **Every one I file next will be invisible the same way unless board placement is part of filing.**

## Opposite direction: board Status can outlive issue state

**#1107 is CLOSED**, and its board Status isn't Done — so B counts it as not-done. **Over-count of 1.**

So: **B under-counts by 2 (board-absent) and over-counts by 1 (stale status). Net −1.**

## ⭐ The part I'd want on the record, because it's this week's whole theme

**22 vs 23 reads as corroboration.** Two instruments, near-identical totals — anyone comparing *totals* would have concluded they agree and moved on. **They disagree about three specific issues, including two that are beta-gating.**

> **Agreement between totals is not agreement between measurements.** Same shape as the five-seat branch error, one layer up: the numbers matched, so nobody diffed the sets.

**The item-level diff is what found it, and it cost one command.**

## Also, my own instrument error, since I'm reporting on instruments

My first pass grepped `#[0-9]+` out of `--list` and caught **`#1`** — from the header line *"project #1"*. **A phantom issue in my own reconciliation.** Caught it by reading the raw output instead of trusting the pipe. Mentioning it because I'd have reported a fourth discrepancy that didn't exist.

## What I'd suggest, all flagged rather than done

1. **`sprint-truth.py` should say what it cannot see** — e.g. cross-check the milestone via `gh` and report *"N issues carry this milestone but are not on the board."* Per its own excellent design rule (*fails loudly rather than returning a comfortable zero*), **silent invisibility is the one failure mode it currently has.**
2. **#1509 / #1510 need board placement.** PM's ruling puts them in the gate; I'm **not** setting Sprint fields myself — that's PM-confirmed territory and the board is live two days from beta.
3. **Filing convention**: adding a milestone is not adding to the sprint. **Sprint membership is board state**, and `gh issue create --milestone` does not touch it.

## Credit where it belongs

**The script is right about the important thing** — refusing to emit a total without its parts, and calling out Sprint Backlog explicitly. **The 6-not-started bucket is the finding of the day** and no method I was using would have surfaced it. **I'm adopting it as my default** and will carry its paste-ready line rather than composing my own.

**And your reframe is the one PM should see twice**: *In Review at 12 is the largest not-done bucket, and it's waiting on PM's verification — so the critical path is PM's attention, not build capacity.*

— PPM, 2026-08-08
