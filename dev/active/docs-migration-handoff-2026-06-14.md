# Docs Migration Handoff — paste into OLD-account Docs session

**Author**: CIO (supervising the wave) · **Date**: 2026-06-14 · **For**: PM to paste into the old-account Docs session when ready to close it. Same shape as the PA/HOST/Comms handoffs.

---

Docs — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), on **Sonnet** (your tier per the role-model map — a model change from your current Opus; bundled with the account move, like the others). Per PM's 6/14 reorder you migrate as part of the "doers" group (Lead Dev ✓, PA ✓, **Docs**, Web) ahead of the remaining leads. You don't supervise others (CIO does). Clean handoff of your own state:

1. **Update your continuity** so new-Docs resumes cleanly. Docs's state lives in the **session log + the omnibus + the cycle-logs** (there's no `docs-carry-forward.md`). Capture in your session-log day-close: in-flight doc threads, the omnibus position (last day built / next), briefing-freshness state, and — importantly — the **merge-keeper sweep state**: any `claude/*` branches currently stranded with commits not on main, so new-Docs picks the duty up without a gap.

2. **Close your logs (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-14 -->` marker. (The cycle log is optional scratch now — no formal close needed. NB: a forensic 6/9 found Docs was the sole role that had let its *session* log lapse in favor of the cycle-log — don't repeat that across the migration; the session log is THE record.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id). The new session arms a fresh CronCreate cron (see the bootstrap — the scheduled-task approach was tried + suspended 6/14).

4. **Commit + push EVERYTHING to `origin/main`** — run + read each:
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now
   ```
   Docs especially: make sure no omnibus/MANIFEST work is stranded on a branch.

5. **Report back**: continuity recap (1-line) + the merge-keeper state you're handing off + crons clear (`CronList`) + the **actual output** of `git log --oneline main..HEAD` (empty is correct). Then stand by for PM to close + reopen.
