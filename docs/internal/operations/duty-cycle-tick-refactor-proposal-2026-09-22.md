---
title: "duty-cycle-tick skill refactor — design proposal (context-floor item 2)"
status: draft, awaiting a non-CIO pilot seat
owner: CIO (design), pilot seat TBD, Pard/Janus for cross-project rollout after
date: 2026-09-22
---

# duty-cycle-tick refactor — design proposal

Context-floor-reduction plan item 2 (`docs/internal/operations/context-floor-reduction-plan-2026-09-21.md`).
PM's diagnosis, applied to this file specifically: it mixes historical incident narrative into an
actionable current-state procedure, and every seat pays the re-read cost on every fire.

## The measurement, not a guess

`.claude/skills/duty-cycle-tick/SKILL.md` is **106,990 bytes** (~429 lines). Byte breakdown by
section:

| section | bytes | % of file | what it is |
|---|---|---|---|
| **Changelog** (frontmatter) | 30,118 | 28% | every past version's own reasoning, v1.0→v1.37 |
| **Step 3 — Dispatch** | 30,633 | 29% | current dispatch logic + ~5 rounds of DAY-CLOSED-marker-regex correction history, embedded inline |
| **Step 2 — Sync** | 16,181 | 15% | current sync procedure + the Model-A collision-detection saga, embedded inline |
| Step 1 | 6,926 | 6% | mostly current |
| Anti-Patterns | 3,830 | 4% | current, short |
| Step 5b — Heartbeat | 3,376 | 3% | current + the invisibility-history note |
| Step 5 — Log | 3,119 | 3% | current |
| Step 7 — Carry-forward/cron | 2,650 | 2% | current |
| Step 6 — Commit | 1,568 | 1% | current |
| Step 4 | 675 | 1% | current |
| everything else (When-to-Use, State files, Examples, cross-refs) | ~8,000 | ~7% | current, already lean |

**Three surfaces — changelog, Step 3, Step 2 — are 77KB, 72% of the file.** Everything else is
already close to what a current-state procedure should look like: short, operative, not narrating
its own history.

## Proposed split, in two phases with very different risk profiles

### Phase A — the changelog (safe, do first, no pilot needed)

**Move it out entirely.** The changelog is metadata about the file's own history — it is never
read by an agent executing a fire; it exists only for whoever edits the skill next, to understand
why a rule is worded the way it is before changing it again. That reader can follow a pointer.

**Mechanism**: a new `docs/internal/operations/duty-cycle-tick-changelog.log`, one entry per
version, verbatim copy of what's there today (nothing lost — this is a move, not a summarization).
The skill's own frontmatter keeps `version:` and a **one-line** `changelog:` pointing at the log
file, plus (optional) the single most recent entry inline for at-a-glance context on what just
changed. **Zero touch to the Procedure body** — this phase cannot break a fire, because nothing an
agent executes reads the changelog. This is why I'd ship it without waiting for a pilot seat: the
risk profile is closer to "delete a comment" than "change a procedure."

**Saves ~30KB (~28%) on every load, immediately, at near-zero risk.**

### Phase B — Steps 2 and 3's embedded correction history (real risk, needs the pilot)

This is different in kind, not just degree. Both steps interleave the **current rule** with **why
it's worded this way**, sentence by sentence, in places — the DAY-CLOSED regex saga in Step 3 is
five rounds of "the pattern was X, found wrong, corrected to Y, found wrong again" and the CURRENT
regex is only fully specified by reading the last correction in context of the ones before it.
Cutting this wrong doesn't just bloat the file less — it can silently drop a constraint that's
still load-bearing (e.g., why the pattern anchors at column 0, which only makes sense against the
false-positive history that motivated it).

**Proposed approach, not yet executed**: for each embedded historical block —
1. Extract the **final, current rule** as a clean, standalone instruction (what Step 3 already
   half-does at the end of that saga — the regex itself, stated plainly).
2. Move the **derivation narrative** (the five rounds of correction) into the same
   `duty-cycle-tick-changelog.log` or a sibling `duty-cycle-tick-design-notes.log`, cross-referenced
   by a short pointer at the point in the step where the rule appears ("see changelog v1.6–v1.8 for
   why this is anchored at column 0, not just what").
3. **A non-CIO seat re-reads the trimmed step COLD** (no memory of the original) and tries to
   execute a fire against it, specifically checking whether the trimmed version still prevents the
   failure the narrative was guarding against (the false-positive DAY-CLOSED matches, the Model-A
   collision misfire). If it does, the narrative really was extractable; if the pilot seat trips the
   old failure mode, that block wasn't safe to cut and gets restored with the derivation reasoning
   still inline.

This is genuinely the part that needs a different seat's real fires, not my own read of my own
edit — the self-grading risk you flagged is sharpest exactly here, since I'm the one least likely
to notice my own trim dropped something I "obviously" still remember not needing written down.

## What I'm proposing as next steps

1. **Ship Phase A today** — I can do this now; near-zero risk, no pilot dependency, immediate
   ~28% reduction. Will do this as its own commit right after this proposal goes out, not waiting
   for a decision on Phase B.
2. **Phase B needs the pilot seat assignment** (Web or PA per yesterday's alignment) — I'll draft
   the specific before/after text for Steps 2 and 3 once a seat is picked, so the pilot has
   something concrete to run real fires against rather than a description of the plan.
3. **4b (carry-forward durable rule)** lands in whichever phase touches Step 7 — likely folded
   into Phase B's pass rather than a separate edit, since Step 7 already owns carry-forward
   rewrites and the two changes are adjacent.

**Verified how**: all byte counts from `wc -c` / `awk` against the live file this fire, not
estimated. Section boundaries from the file's own `### Step N` headings. Not yet verified: whether
Phase B's specific extraction (the DAY-CLOSED and collision-detection blocks) is safe to cut without
losing a load-bearing constraint — that's exactly what the pilot is for, not something I'm
asserting here.
