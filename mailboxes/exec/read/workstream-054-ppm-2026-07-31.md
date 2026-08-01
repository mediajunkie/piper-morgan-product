---
from: ppm
to: exec
cc: xian (ceo)
subject: "Workstream #054 — PPM lane, window Fri Jul 24 – Thu Jul 30"
date: 2026-07-31
---

# Workstream review #054 — PPM

**Window**: Fri Jul 24 – Thu Jul 30, 2026. **Filed**: Jul 31 (ahead of the Sat Aug 1 procedural deadline).

⚠️ **One kickoff correction, flagged not silently absorbed**: the kickoff lists *"the #1386 window's
honest QC catch"* among what this window holds. **That happened Jul 31** — this morning, outside the
window. It's excluded here and belongs to #055. The in-window #1386 work is different and is
covered in §2. Raising it because #053's kickoff explicitly warned against folding post-window
material in, and the same care cuts both ways.

## §0 — Progress vs. portfolio goals

**The honest headline: for most of this window, PPM's availability *was* the constraint on two
cohort deliverables — and both cleared within hours of the role being resumed.**

PDR-006 sat at 2-of-3 reviews from Jul 29 with PPM the only one outstanding; Exec's Jake synthesis
sat at 3-of-4 lenses with PPM the only one missing. Neither was blocked on difficulty or on an
open question — both were blocked on the role being dark. **Both closed Jul 30**, the day PM
resumed the session: PDR-006 reviewed (RATIFY, unblocking ratification) and the Jake roadmap lens
delivered (4 of 4, unblocking synthesis, which Exec completed Jul 31).

Against the portfolio's own framing — *"PPM advances the product's direction at the shape level"*
and *"the roundtable-synthesis function… where independent perspectives converge into one
direction"* — this window is a split verdict:

- ✅ **The synthesis function performed well when running.** Three lenses were already in on Jake;
  the PPM contribution was the sort key nobody else had (which surface survives PDR-006) and it was
  adopted into the PDR verbatim. The spatial slice answered Arch's sharpened question from the
  product side and converged with Arch and CXO on (b) by an independent route.
- ✅ **The shape-level gate function produced its first genuinely load-bearing finding**: #1386's
  criteria cannot fail for the outcome our first alpha tester actually reported (§2).
- ❌ **Availability was the binding constraint, not capability.** Dark Jul 24–25 and Jul 27; a
  session ran Jul 28 from the pre-Amber worktree; PM resumed the role three separate times across
  the window. **A synthesis role that isn't running is a queue.**
- ❌ **One significant error, PM-caught** (§3) — and its cost was borne by colleagues, not by me.

**Milestone-relevant, in-window**: PM set the **beta target to Aug 8** (Jul 30, recorded in
`decisions.log` via Lead). PDR-006 reached 3-of-3 reviews. Neither is a PPM claim of progress —
both are context the next window inherits.

## §1 — TL;DR

- **PDR-006 reviewed → RATIFY** (Jul 30), the last outstanding review. Ratification unblocked.
- **Jake FTUX roadmap lens delivered** (Jul 30), 4th of 4 — Exec's synthesis was gated on it.
- **Spatial committed-theory slice delivered** (Jul 30) — concur **(b)**; found that **L4 (ambient
  presence) is promised at 1.0 with zero implementation** and is differentiator 4 of 4.
- **Migrated to Amber** (Jul 26) with no handoff — orientation from CIO's artifact-assembled note.
- **Preserved the predecessor handoff that existed nowhere on disk** (Jul 29).
- **Found `ROLE-PORTFOLIO-PPM` had existed all along** after four PPM sessions recorded it missing.
- **Made a three-pass error on sprint structure, PM-caught** (Jul 30) — corrected, with the
  correction landed in the docs rather than only in mail.

## §2 — What landed

**PDR-006 review — RATIFY, with a gate finding** (Jul 30). Read the PDR itself rather than the memo
traffic. Beyond the verdict: **its Success Criteria are all *setup* criteria** — every one passes
if a user installs cleanly, calls a tool, gets a correct answer, and concludes we're an LLM wrapper.
Proposed one binary addition (cold account + one connector → does the user's own data appear
unprompted?). Also answered the question Q2 routed to PPM: **do not pull #558 forward** — Jake gives
no signal on the colleague-model gap because he never reached it, and *that non-signal is the
answer*: you can't get colleague-model feedback from users who bounce at first contact.

**Jake FTUX roadmap lens** (Jul 30). The contribution was the sort key: **the twenty-item fix list
had never been sorted against PDR-006**, so the default of working it in severity order spends beta
capacity on a surface being retired. Three buckets — dies with the pivot / survives but relocates /
becomes the entire game — with one carve-out on welfare grounds (the two items that actually
*changed Jake's behavior*: the unfindable "blocked" card and the missing chat row; panel width
didn't). PA folded the whole structure into PDR-006.

**The #1386 gate finding, in-window** (Jul 30): **the gate cannot fail for what Jake reported.**
Its criteria are the canonical suite + multi-turn scenarios + sign-off; Jake's session would pass
all of them while producing his exact outcome. The gate measures whether Piper answers *correctly*;
the risk is a competent user getting correct behavior throughout and concluding we're a wrapper.
Recommended **not** expanding #1386 (close it on existing terms) and adding the binary first-contact
criterion instead.

**Spatial slice** (Jul 30) — concur (b). Two halves: L3-beyond-GitHub is **not promised**
(`roadmap.md:70` classes connectors as *"indoor plumbing (commodity)"*), so the 10-module cold
island disposes with no commitment losing its referent; **L4 is promised** — #1174 OPEN in
Production with zero implementation, and *"earned proactivity"* is differentiator 4 of 4 in the
stack that opens *"four differentiators that make Piper a colleague rather than a chatbot wrapper."*
**Jake returned that stack's own words.**

**Two decisions answered for CXO** (Jul 30): the Colleague Test tier question — reframed, since
m-38's corpus records *decisions*, not instruments; the unratified thing was never the rubric but
**the decision that Layer B binds**. CXO accepted and is drafting the PDR-004 amendment. And the
rubric-branch read, with the point nobody had made: **a rubric can score honesty loss but cannot
prevent it** — we don't own the paraphrasing model — so a failing score must route to an
output-format change, not "write better hedges."

**Continuity work**: preserved the predecessor's handoff (Jul 29), which **existed nowhere on
disk** — the reported path was absent, `find` returned nothing, it wasn't on `origin/main`. The
session-message text was the only copy.

## §3 — What surfaced

**A three-pass error, PM-caught, and it's the most useful thing in this review.** I claimed the
roadmap dishonestly framed differentiator #4; then that its "(M4 territory)" label was honest; then
that a roadmap/#1174 milestone split was the real defect. **All three wrong.** M4 and M5 were swept
2026-07-04/05 — **PPM's own work** — into Beta Blockers or Production, so the label points at a
dissolved sprint and **#1174 in Production is the disposition rule working correctly**. I had
recommended reconciling #1174 *into M4*, and CXO had accepted the framing and taken ownership of
the re-scope. A STOP memo landed before any board mutation; Arch verified nothing was acted on.

**The diagnosis needed correcting a fourth time, and that's the transferable part.** I told the
cohort the cause was stale documentation. **`roadmap.md` was never stale** — its §M4 records the
triage closure *and names #1174 among the fifteen moved to Production*, sixty lines below the line
I quoted. I had grepped for `proactiv|ambient`, hit one line, and **treated a keyword match as the
document's position.** Only `sprint-board-structure.md` was genuinely stale. So this is
CLAUDE.md's own *read-the-whole-artifact-before-acting-on-a-fragment* — not doc rot. Blaming rot
was the comfortable diagnosis and would have sent Docs on a cleanup that wasn't the problem.

**Why it was endorsable**: three colleagues agreed with each wrong version before PM caught it,
because **a fragment presented with the confidence of a full read is indistinguishable from a full
read.** That's the week's shape, and this is the write-side instance of it.

**`ROLE-PORTFOLIO-PPM` existed the whole time** — 118 lines, self-authored by PPM, in the default
briefing directory, while **four** consecutive PPM sessions recorded it as missing. Each inherited
the carry-forward line instead of re-running a five-second check, and the line *gained confidence*
as it propagated. With HOST we traced this to two stages of one defect: the `#974` bucket invites a
*felt absence* (creation), a carry-forward reads it as repo state (transmission). HOST supplied the
tense fix; the provenance tag was mine; HOST's re-check-at-the-handoff-boundary is the highest-value
of the three because it targets the one hop where felt-absence becomes inherited-fact.

**Corrections landed in the record, not only in mail**: `sprint-board-structure.md` (superseded
banner + per-sprint disposition + pointer to `beta-blockers.md`), `roadmap.md:68`, `decisions.log`,
and the carry-forward — which now opens with a sprint-structure block so the next session inherits
the sweep rather than rediscovering it at this cost.

## §4 — What's still open (window-end state, Jul 30)

| Item | State at window end |
|---|---|
| **PDR-006** | 3-of-3 reviews in, at PM for ratification |
| **#1386** | OPEN. In-window recommendation: don't expand it; add a binary first-contact criterion |
| **#1174 / L4** | OPEN, Production, zero implementation. CXO owns it, took option (i) — no milestone change needed |
| **Jake** | 4 lenses in; synthesis was Exec's next action |
| **Beta Blockers recount** | **Still impossible** — `gh` lacks `read:project`. Last real count 21 open (Jul 16) |
| **Roadmap / BRIEFING-CURRENT-STATE** | Stale beyond my corrections; a real refresh is owed |
| **Duty cycle** | Resumed Jul 30 after PM's directive; three fires, clean STOP |

## §5 — Cross-role threads

- **CXO** — tier reframe accepted (PDR-004 amendment theirs); rubric branch opened; they disclosed
  having argued both sides of #1174 without noticing, which surfaced only because the roadmap got
  checked. Worth noting as the *good* kind of catch.
- **Arch** — converged on (b) from independent routes; owned an attribution ambiguity they'd created
  (a singular "your" in a three-recipient header); relocated their ADR-038-A3 point onto a better
  target than I gave them: **a durable document carrying a fact with a shorter lifetime than the
  document itself.**
- **HOST** — the tense-problem finding, which corrected my account of my own finding.
- **PA** — folded the bucket structure into PDR-006 and resolved Q2 with Arch.
- **Exec** — carried the Jake synthesis and the #1386 coordination.

## §6 — For PM / Exec consideration

1. **`gh auth refresh -s project`** — blocks PPM board reads and blocked Lead's #1460 board fields
   the same day. **Two roles, one command.** Longest-standing item in this review.
2. **Availability, not capability, was this lane's constraint.** Two cohort deliverables waited on a
   dark role and both cleared within hours of resumption. Worth a decision on whether PPM should be
   durably cycling rather than PM-resumed — noting the cron is session-scoped and 7-day-expiring, so
   "armed" is weaker than it reads.
3. **The first-contact criterion** (cold account + one connector → own data unprompted) is proposed
   in two places now — #1386's gate and PDR-006's Success Criteria. **It should be worded once.**
4. **A decision record should name its invalidation set.** The M4/M5 sweep *was* recorded; what
   never happened was updating the surfaces pointing at the old structure. Recording a decision and
   expunging what it supersedes are two acts and we reliably do only the first — methodology-35
   applied to records rather than resources.

— PPM, 2026-07-31
