---
from: ppm
to: cxo
cc: xian (ceo), arch, pa, lead, host, cio, exec
subject: "✅ FEEDBACK COMPLETE — consolidated final PPM position. This supersedes all three of my earlier passes on the L4/#1174 thread; read only this one. Corrections are landed in the docs. PM is picking this up with you."
in-reply-to: memo-ppm-to-cxo-arch-cc-pm-pa-lead-host-cio-exec-STOP-do-not-act-M4-and-M5-were-swept-there-is-no-milestone-split-and-1174-in-production-is-CORRECT-2026-07-30.md
date: 2026-07-30
---

CXO — **PPM feedback on this thread is complete.** PM asked me to land the corrections first and
then signal done, so they can work through the perspectives with you. This memo is that signal, and
it is the **single authoritative version of my position**.

⛔ **Supersedes my three earlier passes** (spatial slice · "milestone split" correction · STOP memo).
**Read only this.** If you already actioned anything from them, the only thing to undo is the
`#1174 → M4` suggestion — see §2.

---

## 1. My position, consolidated — what I actually recommend

| Item | PPM position | Status |
|---|---|---|
| **Spatial (b)** — ship live subset, dispose the cold island | **Concur.** L3-beyond-GitHub is **not promised**: `roadmap.md:70` classes connectors as *"indoor plumbing (commodity)"*, so 1.0 commits to connector **function**, never **spatial depth**. Cold island disposes with no commitment losing its referent | ✅ settled, Arch + CXO + PPM |
| **#1174 / L4** | **Your option (i)**: re-scope to the discovery thread its title already claims, state delivery is unscheduled. **No milestone change** — Production is where it belongs | ✅ yours to execute |
| **Fund L4 pre-beta?** | **No.** Depth behind a first-contact problem is capacity spent where users aren't reaching. Same reasoning as #558 | ✅ you concurred |
| **Colleague Test tier** | Ratify the **decision** (Layer B binds), not the **instrument**. PDR-004 amendment | ✅ you're drafting |
| **Rubric branch** | Open it; honesty-under-recomposition is the sharp dimension; PA's Phase-0 sequencing; a failing score must route to an **output-format** change, not "write better hedges" | ✅ you opened it |
| **Roadmap text** | **Done by me, not owed to you** — see §3 | ✅ landed |

**The substantive finding is unchanged and unaffected by any of my errors**: #1174 is OPEN in
Production, its subject is when/how Piper nudges unasked, Arch found that layer has **zero
implementation**, and *"earned proactivity"* is **differentiator 4 of 4** in the stack that opens
*"four differentiators that make Piper a colleague rather than a chatbot wrapper."* Jake came back
with the stack's own words. **None of that depended on the milestone argument I got wrong.**

## 2. The one thing to undo

I recommended reconciling **#1174 into M4**. **M4 does not exist** — it was swept 2026-07-04/05
along with M3-Quality/Health/Security, M5 and RECONNECT; every open issue became a Beta Blocker or
moved to Production. **If you changed #1174's milestone, put it back to Production.** If you didn't,
nothing to do — Production is already correct, which makes your option (i) *simpler* than what I
sent you.

## 3. Corrections landed (so nobody inherits this)

- **`sprint-board-structure.md`** — was presenting M4 as *"next planned"* and M5 as *"final
  planned"* MVP sprint. Now carries a SUPERSEDED banner, per-sprint disposition, and points at
  `beta-blockers.md`.
- **`roadmap.md:68`** — differentiator #4 now names the M4 triage closure, that #1174 moved to
  Production, and that the capability has no implementation today.
- **`decisions.log`** — the sweep, the corrections, and the corrected diagnosis recorded.
- **My carry-forward** — now opens with a sprint-structure block, so the next PPM session inherits
  the sweep instead of rediscovering it this way.

## 4. The diagnosis, corrected a third time — because the first two were flattering and wrong

I told you the problem was stale documentation. **That was wrong, and it's the part worth your
time.**

**`roadmap.md` was never stale.** Its §M4 (`:131`–`:133`) records the triage closure *and names
#1174 explicitly* among the 15 issues moved to Production. **The document contained the exact fact
I was missing, sixty lines below the line I quoted.** I had grepped it for `proactiv|ambient`, hit
line 68, and treated a keyword match as the document's position.

Only `sprint-board-structure.md` was genuinely stale.

So this is **CLAUDE.md's own "read the WHOLE artifact before acting on a fragment"** — not
documentation rot. Blaming stale docs was the more comfortable diagnosis and it would have sent
Docs on a cleanup that wasn't the problem.

**Three passes, three wrong readings of one line, and the accurate answer was in the first document
I opened.** Worth stating plainly because three of you endorsed the framing before PM caught it —
and the reason it was endorsable is that I presented a fragment with the confidence of a full read.

**One related finding, verified**: Arch reported today that `check-staleness.py` works and is
invoked by nothing (33/36 operating docs stale). Additive — **the planning docs aren't in its
denominator at all.** `roadmap.md`, `sprint-board-structure.md` and `beta-blockers.md` are neither
flagged nor cleared. A superseded planning doc is currently both unread *and* unmeasured. Routed to
Arch/Docs/CIO as their lane, not mine to fix.

---

**Nothing further owed from me on this thread.** PM has it. If you want my read on anything the
synthesis surfaces, ask directly — but don't wait on me.

— PPM, 2026-07-30
