# Comms Migration Handoff — paste into OLD-account Comms session

**Author**: CIO (supervising the wave) · **Date**: 2026-06-13 · **For**: PM to paste into the old-account Comms session when ready to close it. Same shape as PA/Exec/CIO/LD/HOST handoffs.

---

Comms — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), on **Sonnet** (your tier per the role-model map — a model change from your current; bundled with the account move, like PA's). You're next in the re-migration wave after HOST. You don't supervise others (CIO does). Clean handoff of your own state:

1. **Update your continuity surfaces** so new-Comms resumes cleanly: `dev/active/comms-open-topics.md` + `dev/active/comms-standing-items.md` (Comms's state lives there — there's no `comms-carry-forward.md`). Capture: live editorial/publishing threads, the building-narrative position (next beat / waiting), any in-flight Ships/posts, the adaptive-interval pilot status, and anything awaiting PM.

2. **Close your logs (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-13 -->` marker. (The cycle log is optional scratch now — no formal close needed.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id). New session arms fresh.

4. **Commit + push EVERYTHING to `origin/main`** — run + read each:
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now (git push origin HEAD:main for non-mailbox)
   ```

5. **Report back**: continuity-surface paths + 1-line summary; crons clear (`CronList`); the **actual output** of `git log --oneline main..HEAD` (empty is correct). Then stand by for PM to close + reopen.
