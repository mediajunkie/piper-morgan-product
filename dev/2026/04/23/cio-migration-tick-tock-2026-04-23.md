# CIO Migration Tick-Tock (Second Migration)

*PM's walkthrough guide, April 23, 2026*

This is the step-by-step sequence for CIO's Chat → Code migration. Incorporates lessons from HOST's migration Apr 22.

---

## Phase 1: Chat-side handoff preparation

**You're in**: Current CIO chat project.

### Step 1.1 — Paste the handoff prompt

Paste `memo-exec-to-cio-migration-handoff-2026-04-22.md` into the CIO chat. This is the prompt telling CIO what you're asking of them: prepare a handoff memo using HOST's six-section pattern, with CIO-specific content (innovation backlog location, audit A1/A2/A3 disposition, Flywheel Phase 2 timing, etc.).

### Step 1.2 — CIO completes Agent 360 v0.2

Separately, have CIO complete the `agent-360-questionnaire-v0_2.md`. Save their response. This is the pre-migration baseline for the 6-week benchmark comparison.

### Step 1.3 — CIO drafts handoff memo

CIO works through the six sections. Expect this to take some time — HOST's was rich. Let CIO take the space they need.

### Step 1.4 — You and CIO iterate

One or two passes. Ask: "What would the next instance need to know that isn't obvious?" Revise.

### Step 1.5 — Send draft to exec (me) for review

Paste CIO's draft into my chat. I read it against what I know about the project, the exec tracker, and HOST's precedent. I produce a review memo flagging gaps.

### Step 1.6 — CIO revises based on exec review

CIO integrates the review feedback. One more pass.

### Step 1.7 — Finalize

Save as `handoff-cio-chat-to-code-2026-04-23.md`.

---

## Phase 2: Migration bridge

**You're in**: Terminal / git.

### Step 2.1 — Commit handoff package to repo

Commit to `main`:
- `handoff-cio-chat-to-code-2026-04-23.md`
- CIO's Agent 360 v0.2 response
- Any supporting materials

Per HOST's "orphan-state" finding, commit the handoff package atomically rather than bundling with other uncommitted files on main.

### Step 2.2 — Verify visibility

Check that the handoff package is visible in the Code worktree where new CIO will be running. If there's a mid-session commit/merge needed like HOST hit, do it now rather than during the new session.

### Step 2.3 — Optional: surface prior CIO workstream memo

If CIO's prior Ship #038 workstream memo exists in Chat project knowledge, surface it and commit to repo. This gives new CIO a voice/scope reference. If not available, the startup prompt already points at Arch's Ship #038 memo as structural analogue. Don't block on this.

### Step 2.4 — Retire Chat CIO

Old Chat instance retired but reachable as emeritus. Note this to CIO as part of the handoff process.

---

## Phase 3: Code-side onboarding

**You're in**: New CIO instance in Code.

### Step 3.1 — Paste the startup prompt

Paste `prompt-cio-code-first-session-2026-04-22.md` at the start of the first CIO Code session. This orients them: read handoff first, then exec review, then (stale) briefing, then checklist, then reference materials.

### Step 3.2 — First-week tasks

New CIO works through Phase 3 of the migration checklist:

1. Read handoff memo fully before anything else
2. **Briefing correction memo** — using HOST's memo as template, file findings to Docs about `BRIEFING-ESSENTIAL-CIO.md`
3. **Establish startup routine** — standing file per HOST's Finding B
4. **HOST coordination check** — open "what are you watching?" exchange with HOST (their PA memo is the model)
5. **Re-issue Ship #039 workstream memo** — against the amended Apr 10-16 omnibus (this is the prerequisite to Ship #040)
6. **First Ship #040 workstream review** — for Apr 17-23 window, due Thu Apr 24 or Fri Apr 25 once the window closes. Role-scoped input memo to exec, naming standard `workstream-040-cio-2026-04-DD.md`.

---

## What to watch for (lessons from HOST migration)

1. **Handoff quality compounds** — the richer CIO's handoff, the better the successor starts. Don't rush the drafting phase.

2. **Section 6 (the candid notes)** produced the most valuable writing in HOST's handoff. Remind CIO the offer stands: you won't seek it out, but can't promise never to see it — the signal is that candor is welcome.

3. **Receiving-handoff reflection** — if CIO received a handoff at any point, their reflection on what was useful vs. what was missing is rare institutional knowledge. Worth surfacing in Section 4.

4. **Orphan-state risk** — if you see uncommitted files piling on main before migration, tidy those up first. HOST hit a ~30-file pileup at session start.

5. **Exec review catches real gaps** — HOST's first draft was strong but still had five substantive gaps. Build in time for this step; don't treat it as ceremonial.

6. **Don't try to pre-specify what you can't know yet** — HOST's first-week surfaced the workstream review under-specification. CIO's first-week will surface something else. Let it happen; capture the learnings; iterate the checklist.

---

## Needed from me (exec) during this migration

- **Step 1.5**: Read CIO's handoff draft when you send it. Produce review memo. (Same as HOST.)
- **Post-migration**: Read CIO's first Code-side memos the way I read HOST's last night. Flag anything worth capturing for the migration methodology.
- **Ongoing**: Update tracker as CIO migration completes; add any new items CIO surfaces.

---

## Ready check

If this sequence makes sense, the first concrete action is Step 1.1 — paste `memo-exec-to-cio-migration-handoff-2026-04-22.md` into the current CIO chat. Everything flows from there.

Questions or adjustments before we start?

— exec
*April 23, 2026*
