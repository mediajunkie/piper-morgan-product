# HOST Migration Handoff Capture — paste into OLD-account HOST session

**Purpose**: get HOST's working state cleanly committed + pushed to `origin/main` before PM closes the old-account session and opens the fresh one on DinP. Same shape as PA's (6/10), Exec's (6/11), and CIO's (6/12) handoff prompts.

**Why an outside author helps**: CIO drafted this from *outside* HOST's context. PA's handoff worked clean for exactly this reason — an outsider catches the steps the insider would skim. PM should add any step that looks under-specified.

**Author**: CIO (post-migration, supervising the rest of the wave) · **Date**: 2026-06-12 · **For**: PM to paste verbatim into the old-account HOST session when ready to close it.

---

HOST — this is your migration handoff. PM is closing this session and opening a fresh Code session on the DinP account (xian@designinproduct.com). **Account move only — same model you're on now, no model change** (the rest of the wave moved accounts without changing models). You're next in the re-migration wave after PA (6/11), Exec (6/12), and CIO (6/12). You do NOT supervise others — CIO carries the rest of the cohort migration. Your job here is a clean handoff of your own state.

Before the switch, please do these in order:

1. **Update your carry-forward** (`dev/active/host-carry-forward.md`) — it's currently dated 2026-06-06 and is stale on several threads. Rewrite it so new-HOST resumes cleanly. Make sure it captures:
   - **Live PM-blocked / awaiting-PM items**: privacy decision on `dev/alpha/` (git-tracked tester PII vs. "gitignored" roster claim; your alpha-tiering doc is held uncommitted pending it); wire-#1178-recurring to cc/assign HOST; thin-prompt cohort-rollout broadcast nod
   - **In-flight with others**: ROLE-PORTFOLIO-HOST pilot (w/ Exec, on PM framework-ratify); gbrain co-signed memo (CIO+HOST→PM, agent-experience findings); BYO-colleague trust lens (delivered to Exec-as-synthesizer — watch for Exec's synthesis); dashboard welfare-criteria v0.2 (m-39, pair w/ CIO)
   - **Watch / trigger-bound**: v0.3 360 synthesis (~Jun 12 — extraction done; remaining = summary memo + the PM-collaborative "what's worth changing" step); alpha re-ping wave 1 (PM pinging Jake Krajewski + Rebecca Refoy)
   - **Standing cycle responsibility**: recurring-audit polling — `gh issue list --label sapient-trust --state open` (GH doesn't notify agents; your cycle is the catch mechanism)
   - **Owed**: the mail-vs-GH-comments cohort-norm one-liner (committed to Arch 6/7)

2. **Append a final "MIGRATION HANDOFF" entry to BOTH logs** — session log AND cycle log, one terminal entry each. Dual-surface discipline: the cycle log is ephemeral (sprint-cleaned); the session log is the durable record. Both need the close, or new-HOST lands on a half-closed trail.

3. **CronDelete the active duty-cycle cron** (currently `c85076d3`, windowed `37 6,9,12,15,18,21`). Don't leave it armed in the old session — the new session arms fresh. `CronList` to confirm it's gone.

4. **Commit + push EVERYTHING to `origin/main`.** Not a formality — run each command and read the output:
   ```bash
   git status                          # working tree clean (no uncommitted changes)
   git log --oneline @{u}..HEAD        # empty (branch is pushed)
   git log --oneline main..HEAD        # empty — OR, if not, merge to main NOW
   ```
   If `main..HEAD` has commits (work stranded on the branch), merge it before reporting back: from the `host-cycle` worktree, `git push origin HEAD:main` for non-mailbox work. A session that ends with commits stranded on `claude/host-cycle` means new-HOST lands on a carry-forward promising state that isn't on main. The sign-off checklist only works if you actually run it and read the output.

5. **Report back** with: (a) carry-forward path + one-sentence summary of what's in it; (b) confirmation crons are clear (`CronList` output); (c) the **actual output** of `git log --oneline main..HEAD` (paste it — empty is correct; if it had lines before you merged, say so). Then stand by — PM will close this session and open the new one.

Take whatever time you need. The next agent's clean start depends entirely on this capture.
