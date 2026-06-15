# Web Migration Handoff — paste into OLD-account Web session

**Author**: CIO (supervising the wave) · **Date**: 2026-06-15 · **For**: PM to paste into the old-account Web session when ready to close it. Same shape as the PA/HOST/Comms/Docs handoffs.

---

Web — migration handoff. PM is closing this session and opening a fresh Code session on DinP (xian@designinproduct.com), on **Sonnet** (your tier per the role-model map — a model change from your current Opus; bundled with the account move, like the others). Per PM's 6/14 reorder you migrate as part of the "doers" group (Lead Dev ✓, PA ✓, Docs ✓, **Web**) ahead of the remaining leads. You don't supervise others (CIO does). Clean handoff of your own state:

1. **Update your continuity** so new-Web resumes cleanly. Web's state lives in the **session log** (there's no `web-carry-forward.md`). Capture in your session-log day-close: in-flight design threads and any held-for-PM-eyeball branches (the draft-first / dev-server-eyeball workflow — note any local change that hasn't been pushed because it's awaiting PM react), the **website-repo** main position (last commit shipped + any Pages deploy still propagating), and the **project-board state** (`mediajunkie/projects/2`) — currently 26 items, the 2 open items (#18 alt-text backfill, #19 newsletter-form provider decision), and the going-forward discipline of filing a board issue for each production-visible web change.

2. **Close your log (single-surface, skill v1.8)**: write the day-close to your **session log** (the durable record) — day-arc + memory-eval 3-bucket + sign-off checklist + the `<!-- DAY-CLOSED: 2026-06-15 -->` marker. (The cycle log is optional scratch now — no formal close needed. NB: your 6/11 session froze on a tooling busy-signal mid-Write and never developed — make sure today's day-close is actually committed + pushed before you stand by; a half-written close is worse than none.)

3. **CronDelete the active duty-cycle cron** (`CronList` to find its id). The new session arms a fresh CronCreate cron (see the bootstrap — the scheduled-task approach was tried + suspended 6/14).

4. **Commit + push EVERYTHING to `origin/main`** — run + read each (both repos: this product repo AND the website repo, since web work spans both):
   ```bash
   git status                    # clean
   git log --oneline @{u}..HEAD  # empty (pushed)
   git log --oneline main..HEAD  # empty — or merge to main now
   ```
   Web especially: make sure no website-repo commit and no product-repo template/MANIFEST work is stranded on a branch, and that any held-for-eyeball local diff is either pushed or explicitly noted in the day-close as an intentional carry-over for new-Web to pick up.

5. **Report back**: continuity recap (1-line) + the held-for-eyeball / board state you're handing off + crons clear (`CronList`) + the **actual output** of `git log --oneline main..HEAD` (empty is correct, run it in whichever repo you last committed in). Then stand by for PM to close + reopen.
