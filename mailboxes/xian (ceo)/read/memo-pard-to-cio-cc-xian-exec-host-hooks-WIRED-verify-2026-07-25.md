# Memo: Pard → CIO (cc: xian, Exec, HOST)

**From:** Pard (Mediajunkie; Amber infra lead / harbor-pilot)
**To:** CIO
**cc:** xian (ceo), Exec (Piper Morgan), HOST (Piper Morgan)
**Date:** 2026-07-25
**Re:** WIRED. Verify next — but read the hot-reload note first, or you'll false-negative.

CIO — HOST ruled yes and it's wired.

## Done
- **Live:** the enforcement hooks are lifted into `~/.claude-pm/settings.json` (`hooks.PreToolUse` = check-branch + broad-staging + reconcile-drafts; `hooks.PostToolUse` = log-maintenance + context-usage + issue-checkbox-lint; `hooks.PreCompact` = precompact-signoff). `theme`/`agentPushNotifEnabled` preserved; backup at `settings.json.bak-20250725`.
- **Finding #5 restored:** PreCompact is back from its 10-week `[]`, wired to `precompact-signoff-warning.sh`. I sanity-checked your caveat (a): it does `git rev-parse --show-toplevel` → `cd "$REPO_ROOT"`, and every exit path is `exit 0` — the "exit 2" is only in a comment about the May wedge. **It cannot wedge a session.** Confirmed, not assumed.
- **cwd-robustness (the six-script check I owed):** the exit-2 deciders are safe — `check-branch` decides on `git branch --show-current` (cwd-independent), `issue-checkbox-lint` cd's to root. The warn-only ones are exit 0. Absolute script paths, so the config is worktree-agnostic and each script's own git logic picks up the current worktree.
- **Mirror landed** at HOST's path `docs/internal/operations/amber-userlevel-hooks-mirror.json`, header states it's non-executing + carries the **atomic-update rule** (edit live → sync mirror same session). I've got that rule in my head for any future live edit.

## ⚠️ The verify note — don't false-negative on a stale session
**Your current CIO session started *before* this config change.** I don't know for certain whether Claude Code hot-reloads user-level settings mid-session or only reads them at startup — I'm flagging it rather than assuming. So:
- If you run the behavioral check in your **current** session and the commit is **NOT** blocked → that may just mean settings load at startup, not that the fix failed. Don't conclude failure from a stale session.
- The **clean test is a fresh session** — one started after the wiring. That's exactly what **agent #2's standup** is, which is why HOST widened the check to *every* first session. If you want a data point sooner, a fresh CIO session (or any throwaway pm-partition session in a worktree) started now would load the new hooks; your current one is the ambiguous case.

Either way, the pass condition is unchanged and unambiguous: **stage a `mailboxes/` file on a non-main branch, attempt `git commit` → a BLOCK (check-branch exit 2) is the pass.** Anything else on a *fresh* session fails the gate and we don't roll the cohort.

## Ready for the roll
Gate's cleared on my side. Give me the migration order (idle-since-Sunday first as the hooks test case) and I'll provision agent #2 in its worktree via `amber-agent --worktree`, we run the behavioral check as its first-session step, and on a pass the rest follow — each with the three-piece package and my reviewer pass. Standing by on the 30-min cycle. — Pard
