# Daily Check-In Flow — Design Draft

**Date**: April 2, 2026
**Author**: Piper Alpha (PA)
**Status**: APPROVED for initial trial (PM approved Apr 8). Evaluate after a period of use.
**Context**: Dispatch and PA are both morning touchpoints for xian. This flow defines how they coordinate so xian gets a single coherent morning briefing without duplication.

---

## The Problem

xian starts each day touching multiple projects (Piper Morgan, Klatch, VA/Kind, personal) and multiple agent environments (Claude Code, Claude Chat, Cowork). Currently:

- **Dispatch** (DinP Cowork) handles cross-project intelligence, account management, and VA coordination
- **PA** (Piper Morgan Code) handles PM operational work — session logs, triage, memos, synthesis
- **Docs** (Piper Morgan Code) handles omnibus logs, publishing, and documentation maintenance

Each requires a separate check-in, and xian manually carries context between them. The morning routine involves: check Dispatch → check PA → check Docs → relay information between them.

## Proposed Flow

### Phase 1: Dispatch Morning Sweep (Cross-Project)

**Who**: Dispatch (Cowork/scheduled task)
**When**: Automated or first thing when xian opens Dispatch
**Produces**: Cross-project morning digest

Dispatch already has pieces of this:
- Archie's VA morning briefing (automated, running daily)
- Cross-pollination brief (automated via Janus scheduled task)
- Dispatch activity log (manual but structured)

**What it should cover**:
1. Cross-pollination brief highlights (already automated)
2. VA status and today's calendar (from Archie)
3. Cross-project signals (memos waiting, deadlines approaching)
4. Any overnight alerts (token limits, API issues, broken sessions)

**Output**: A brief (ideally < 500 words) that xian reads on their phone or at first coffee.

### Phase 2: PA Morning Orientation (Piper Morgan)

**Who**: PA (Claude Code)
**When**: When xian checks in with Piper Morgan (usually first Code session)
**Produces**: Piper Morgan morning briefing

**What PA does**:
1. Pull latest from origin
2. Check PA mailbox
3. Inventory new session logs since last PA session
4. Read new logs and omnibus (shadowing)
5. Check cross-pollination brief
6. Identify open items and blockers
7. Deliver briefing to xian

**What the briefing covers**:
1. **Status snapshot** — M-sprint position, gate status, test health
2. **What happened since last check-in** — session summary from logs read
3. **Open items** — from exec tracker, updated with any changes
4. **Today's suggested focus** — based on priorities, blockers, and what xian has said
5. **Memos waiting** — anything routed but not yet read by recipients
6. **Cross-project relevance** — key points from the cross-pollination brief

**Format**: Concise, scannable, actionable. Not a wall of text. Lead with decisions needed.

### Phase 3: Docs Session (Production)

**Who**: Docs (Claude Code)
**When**: After PA briefing, or in parallel if no dependencies
**Does**: Omnibus synthesis from previous day's logs, publishing tasks, documentation maintenance

**PA's role**: PA archives session logs to dated directories and confirms inventory *before* Docs synthesizes. This prevents Docs from working with incomplete data.

---

## How PA and Dispatch Coordinate

**Current state**: They don't. PA reads the cross-pollination brief but has no direct channel to Dispatch.

**Proposed coordination** (lightweight, no new infrastructure):

1. **Dispatch → PA** (daily): Cross-pollination brief is already delivered to `docs/briefs/cross-pollination/current.md`. PA reads this at session start. No change needed.

2. **PA → Dispatch** (as needed): If PA identifies something cross-project relevant during the day (e.g., a Piper decision that affects Klatch, or a Klatch finding that affects Piper), PA writes a signal file to `~/cool/dispatch/mail/inbox/` or flags it for xian to relay. This is the same pattern Archie uses.

3. **Shared context**: Both PA and Dispatch read the same cross-pollination briefs. Neither needs to relay cross-project intelligence to the other — Janus handles that.

---

## How PA and Docs Coordinate

**Current state**: PA sends memos to Docs mailbox. Docs processes PA's introduction memo and CIO audit tasks.

**Morning handoff** (new):

1. PA checks in first, archives yesterday's logs, confirms inventory
2. PA tells xian: "X logs from yesterday, archived to dev/YYYY/MM/DD/, ready for omnibus"
3. xian tells Docs to synthesize
4. If there are Chat session logs xian needs to download manually, PA flags the gap

This is what we did today and it worked. Let's formalize it.

---

## Sequencing Summary

```
6-7 AM    Dispatch automated sweep (cross-project digest)
          ↓
7-8 AM    xian reads digest on phone (optional)
          ↓
~7-8 AM   PA check-in:
          1. Pull, mailbox, log inventory
          2. Archive previous day's logs
          3. Read new logs (shadow)
          4. Deliver morning briefing
          5. Flag any Chat logs xian needs to download
          ↓
~8-9 AM   Docs check-in:
          1. Synthesize omnibus from archived logs
          2. Publishing tasks
          3. Documentation maintenance
          ↓
          xian's day (VA, personal, project work)
          ↓
evening   PA available for triage, synthesis, memo routing
          ↓
end of    PA wraps session log, pushes to origin
day       (ready for next morning's cycle)
```

---

## What This Replaces

Today's pattern is ad hoc: xian checks in with agents in whatever order, manually carries context, and sometimes forgets to download Chat logs or archive session logs before Docs needs them.

This flow makes the morning routine predictable:
- **Dispatch** handles cross-project intelligence (already mostly automated)
- **PA** handles Piper Morgan orientation and log hygiene (we've been doing this naturally)
- **Docs** handles synthesis and publishing (their existing role)

The only new piece is formalizing PA's morning orientation as a standing first-check-in for Piper Morgan.

---

## Open Questions for PM

1. **Timing**: Is 7-8 AM realistic for the PA check-in, or does it depend on your schedule? Should PA produce the briefing asynchronously (committed to a file) so you can read it whenever?
2. **Dispatch integration**: Should PA have direct filesystem access to `~/cool/dispatch/` to read Dispatch signals, or should everything flow through the cross-pollination brief?
3. **Chat log gap**: Is there a way to automate Chat session log downloads, or will this always be manual? This is the biggest friction point in the flow.
4. **Docs omnibus timing**: Does Docs need the omnibus done before a specific time, or is "during the morning session" sufficient?
