# Board-status audit — the 28 MVP items reading "Sprint Backlog / NOT STARTED"

**Run**: Friday 2026-08-28, ~23:00 PDT, by Exec at PM's direction.
**Method**: pulled all 28 via the project board (Status = Sprint Backlog, milestone MVP, state OPEN),
then for each: full issue comment history + `git log --all --grep="#N"`. Not a sample — all 28.
**Trigger**: PM asked "why not started, and is there a problem with that reason we need to remedy."

## Headline

**10 of 28 are mislabeled. 18 are genuinely not started.** The "28 never started" figure — which Lead
and Arch both flagged in their #058 reports as the number that keeps our completeness claims honest —
overstates by about 36%, in the direction that makes us look worse than we are.

The remediable problem is not the backlog. It is that **the board is not updated when work lands**,
so the metric built to prevent over-reporting now under-reports instead. Same root defect either way:
board status is hand-maintained and drifts from reality.

## Group A — work done or decision made; board status is simply wrong (10)

| Issue | Actual state | Evidence |
|---|---|---|
| **#1423** Silent-death pattern | **Actively iterating, 3 slices merged** | Slice 1 built+merged 08-08 (ceiling 274→214); Slice 3b landed 08-13 (209→200); `scripts/silent-death-scan.py` committed. Five comments of build history. |
| **#1656** `/files` upload broken (CRITICAL) | **FIXED 08-18, merged to main** | "Implementation evidence (agent lane, Lead-reviewed and merged to main)". Root cause mechanism-proven: Fly mounts the `piper_data` volume ROOT-owned. |
| **#1657** #1624 happy-path failed live | **FIXED 08-18, merged to main** | Implementation evidence posted; the exact WHERE-clause divergence between the Files listing and the resolver quoted in the fix. |
| **#1654** Reminder task-clarify unarmed | **BUILT, merged to main 08-22** | Carrier `reminder_task_question` now armed, mirroring #1648's template. |
| **#1635** Ambient presence false door | **BUILT, staged for deploy 08-28** | Commit `588f6aad1`; CXO's two design rules implemented structurally. |
| **#1663** Inversion 2.2 armed answer-turns | **RULED (b) by Arch 08-19, ratified** | Decision issue; decision made, safety claim verified pre-ruling, #1666 filed from it. |
| **#1638** TemplateRenderer family | **RULED DISPOSE by Arch 08-28** | Zero production callers on any surface; ruling relayed to Lead (`7170e0901`). Ready to close. |
| **#1687** Four CI workflows standing red | **DIAGNOSED, fix awaiting merge** | Per-workflow diagnosis complete; four commits on `claude/lead-cycle` (`e0673c14e`, `607619f92`, `be8a6b336`, `d39dcf526`) pending Lead's review. |
| **#1688** FTUX empty-state interview | **In flight, PM ruled this morning** | CXO answered the §1 question PPM had routed to PM; PM's live ruling recorded. |
| **#1572** Per-user timezone | **Partially — rescoped 08-27** | Slack half split off to #1686 after PM ratified Slack→Fast Follow. The browser-tz-at-login half is genuinely still open. |

## Group B — genuinely not started (18)

Two sub-patterns, and the first is the one worth acting on.

### B1 — Evidence accumulating, work not scheduled (3)

These have live PM-testing evidence piling up on the issue while nothing gets built. **Our capture
pipeline works and our scheduling pipeline doesn't** — the deposits keep landing on an issue nobody
has claimed.

- **#1606** CORPUS two-part / colon-form reminders — **four separate deposits from four different PM
  sessions** (08-12, 08-13, 08-15, 08-18). "add a reminder: X" still isn't extracted; the taught
  rephrase works. PM has hit this repeatedly across six days.
- **#1527** Greedy portfolio-delete claims reminder-deletes — two live hits, PM flagged it in-session
  08-18 ("delete the reminder to check the flayrod" → "I couldn't find a project called…").
- **#1676** Canonical retest doesn't record serving provider/model — corroborated live: during the
  #1675 probe, **every** classification call logged `llm_primary_failed`, `provider=openai`,
  `429 'You have no credits remaining'`, silently falling back. Retest results can't be trusted to
  say which model produced them.

### B2 — Zero touch since filing (15)

`#1505` `#1522` `#1559` `#1579` `#1596` `#1613` `#1637` `#1645` `#1646` `#1652` `#1653` `#1659`
`#1660` `#1678` `#1689`

Two of these deserve names rather than a list:

- **#1613** — dead code implements the exact cross-user data pooling our privacy claims disclaim
  (`QueryLearningLoop`). Filed 08-13, zero comments. Dead code, so not a live leak — but it is a
  written claim and a contradicting implementation sitting in the same repo.
- **#1678** — `PIPER.md` content never reaches the system prompt; the loader extracts six section
  names the file no longer has. The config we ship is not being read.

Six of the fifteen were filed within the last ten days and are simply queued — no problem there.
Three are routing-corpus gaps, real and correctly ranked below the flip work.

## What I got wrong, and how

In the first revision of the #058 report I told PM that #1656 was a CRITICAL blocker that had "sat
unstarted eleven days with three issues queued behind it." **It was fixed the day it was filed**, as
was #1657. Only #1659 and #1660 of that chain are actually untouched.

The mechanism: I probed four issues, found the board wrong on all four, and then **built the chain
narrative from the remaining titles instead of checking them**. Having just demonstrated that board
status is unreliable, I read four more rows off that same board and treated them as fact. The
correct move was the one this audit does — check all 28.

## Recommendations

1. **Move the ten.** Group A needs its board status corrected; #1638 can close outright on Arch's
   ruling, and #1687's fix needs Lead's merge. This is PPM's lane; I'll route it.
2. **Claim the three in B1.** Not because they're the largest defects, but because PM keeps
   re-encountering them in testing, which means each recurrence costs PM time and re-files evidence
   we already have.
3. **The durable fix is the status transition, not this audit.** A closure or merge that doesn't move
   the card leaves the board lying. Worth asking whether status can derive from issue state + linked
   commits rather than being hand-set — the same derive-don't-maintain move the cohort has made three
   times already (frontmatter-derive, MANIFEST-derive, ADR-079's model set).
