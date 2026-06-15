# PPM Migration Handoff — paste into the OLD-account PPM session (LIVE today)

**Author**: CIO (supervising the wave) · **Date**: 2026-06-15 · **For**: PM to paste into the old-account PPM session when ready to close it. Same shape as the PA/HOST/Comms/Docs/Web handoffs. **NB: PPM is mid-session today** (it has a `2026-06-15-0642-ppm-code-opus` log) — this is pasted into a *live* session, so the priority is capturing in-flight threads in the continuity surface before close, not just a quiet shutdown.

---

PPM — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), on **Sonnet** (your tier per the role-model map — a model change from your current Opus; bundled with the account move, like the others). You're a discipline lead (like Arch/CXO), not a supervisor — CIO runs the wave; you just hand off your own state cleanly. (Keep clear: you are **PPM, the Principal Product Manager** — distinct from **PA, Piper Alpha**, PM's product assistant. Don't let new-PPM inherit PA's lane.)

1. **Capture in-flight threads FIRST, then update continuity.** Because you're live mid-session, the load-bearing step is making sure new-PPM can resume *exactly where you are*. PPM's state lives in the **session log** (there's no `ppm-carry-forward.md`). Capture in your session-log day-close:
   - **Today's Fire-0 deliverables and their send-state** — for each of the three, record whether the memo was actually written + committed + pushed to `origin/main`, or is still owed: (a) PPM explicit response to Lead's history-sidebar **flattening 4 questions** (BLOCKING Lead → CXO cc PM); (b) PPM **ack + M-placement for #1216** provenance field (→ Lead cc CXO, PM); (c) **ADR-066 v0.2 m-38 tier-discipline check** (→ Arch). Don't let new-PPM re-do a sent memo or skip an unsent one — state each explicitly.
   - **Open standing items** (carry the full list): the **roadmap v18.1/v19 fold** owed to PPM (per Docs' sprint-structure reconciliation — RECONNECT + D1 are new sprints; M4 entry now active); **#683** (Lead-gated), **PDR-005 Docs swap** (Docs-owned), **#5 Multi-Agent** lane unclear, **#967** (edges 1/2/5 deferred), **#1166** roadmap slot (M4 entry active), **#1185** M5.
   - **New entity-model lane ownership** — you were designated the **object-model / entity-model lane owner** for the history-sidebar-IS-radar-Layer-2 resolution and for the **#1217 People-network Layer-2 entity** capability. Note where that work stands so new-PPM owns it without a gap.
   - **Sprint reality** as you understand it (per Docs): M2 ✅, M3 ✅, next **M4 (Trust + Learning)**, then RECONNECT, D1, **M5 (final, Jul 4 MVP beta)**.

2. **Close your log (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-15 -->` marker. (The cycle log is optional scratch now — no formal close needed. The session log is THE record — don't let it lapse across the migration.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id). NB: your 6/15 START already deleted a stalled cron (`acf26b74`) — if `CronList` shows nothing, that's fine; just confirm clear. The new session arms a fresh CronCreate cron (see the bootstrap — the scheduled-task approach was tried + suspended 6/14).

4. **Commit + push EVERYTHING to `origin/main`** — run + read each:
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now
   ```
   PPM especially: make sure none of today's response memos or the session-log day-close is stranded on the `claude/upbeat-dubinsky-c2b572` branch. Mailbox memos go to `origin/main` via the bridge per discipline.

5. **Report back**: continuity recap (1-line) + the **send-state of the three Fire-0 deliverables** (sent vs. owed) you're handing off + crons clear (`CronList`) + the **actual output** of `git log --oneline main..HEAD` (empty is correct). Then stand by for PM to close + reopen.
