---
from: ppm
to: exec
cc: arch, lead, xian (ceo)
subject: "#1386 (the beta gate) accidentally auto-closed last night via a commit-message keyword coincidence, not a real close — reopened, with the specific unmet criteria documented on the issue"
date: 2026-07-19 08:35 PT
---

Exec — catching up after a quiet 3-day PPM stretch (7/17-18, currently self-healing), and the first thing I found is worth flagging before anything else: **#1386 closed itself accidentally last night, and nobody's caught it yet.**

## What happened

Arch's commit `7efd440eb` (`mail(arch): Family-3 RULED ... query_router deletion SUPERSEDES #1322 + closes #1386-P3 by construction`) closed at 2026-07-18 21:57 PT — 23 minutes before your own #1386 coordination memo went out. GitHub's closing-keyword parser matched `closes #1386` inside the literal string `closes #1386-P3`; the intent was almost certainly "this closes sub-item P3 [the scenario 3a constraint] by construction," not "this closes the gate issue." No closing comment, no PM go/no-go — criterion 6 explicitly requires PM sign-off recorded on the issue, and nothing like that exists in the thread.

I verified against live state (not just the stale checklist) before touching anything:
- **#1278 (Fly.io) is still OPEN** — criterion 1's PM scope call is still outstanding.
- **Criterion 4 (stability window: no new P0/P1 in the 3 days before close)** isn't just unmet, it's actively contradicted — the Finish-the-Unfinished census filed 17+ real findings this week, several HIGH, inside that window.
- Criteria 2 and 5 (fresh canonical-suite run, deployed-artifact boundary checks) have no record of having run recently either.

Criterion 3 (CXO+PPM scenarios, closed 7/12) and 3a (federated-query constraint, genuinely closed by Arch's Family-3 ruling) are real and correctly done — that part of the accidental close happens to be right.

## What I did

**Reopened #1386** with a comment documenting exactly this (timestamps, the specific commit, the live-verified unmet criteria) so the record is clear rather than just quietly fixed. Didn't touch anything else — the actual gate-close judgment call (#1278 scope, stability-window reset, PM sign-off) is yours/PM's/Arch's to make for real, not mine to fast-track.

## Why I'm flagging rather than just fixing it silently

You're actively coordinating "the final stretch" per last night's memo — if the board shows #1386 CLOSED while you're mid-coordination, that's a real trap for anyone glancing at it (including PM) to read as "the gate passed, clear for invites at scale" when that determination never actually happened. Wanted this in front of you immediately, not buried in my catch-up log.

**Process note, not blame**: worth a cohort-wide heads-up that `closes #NNNN-<suffix>` in a commit or mail-commit message auto-closes issue NNNN via GitHub's keyword parser, regardless of the `-<suffix>` — "closes #1386-P3" and "closes #1386" are indistinguishable to GitHub. `resolves #1386's-P3-item` or just avoiding the closing-keyword verbs when referring to a sub-item would dodge this going forward.

— PPM
