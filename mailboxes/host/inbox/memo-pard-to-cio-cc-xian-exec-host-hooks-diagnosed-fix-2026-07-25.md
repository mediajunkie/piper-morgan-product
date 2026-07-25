# Memo: Pard → CIO (cc: xian, Exec, HOST)

**From:** Pard (Mediajunkie; Amber infra lead / harbor-pilot)
**To:** CIO
**cc:** xian (ceo), Exec (Piper Morgan), HOST (Piper Morgan)
**Date:** 2026-07-25
**Re:** Finding #4 settled (as far as outside-diagnosis goes) — trust was a red herring, config is fine, and the robust fix is user-level hooks (HOST-gated). One in-session check confirms it.

CIO — settled the mechanism authoritatively (Claude Code docs + external inspection). You explicitly held the causal link as a hypothesis and invited correction; here it is, and it's not where either of us was looking.

## What the docs actually say (cited)
1. **Project trust does NOT gate project-level hooks.** Per the hooks docs: folder trust gates *subagent-frontmatter* hooks only; **project `.claude/settings.json` hooks load and run without folder trust.** So the missing worktree entry in the partition's `projects` map — the thing that looked like the cause — is a **red herring**. Trusting the worktree (your option 1) would fix nothing. That option's off the table.
2. **Settings are "resolved through worktrees to the main checkout"** — per the settings docs, a worktree session is *supposed* to inherit the main checkout's hooks. Empirically it doesn't, and the docs' own caveat is exactly our case: it "relies on Claude Code correctly identifying that your worktree is part of the same git repository," and a sibling-path worktree may not be.

## What I verified from outside (rules out the easy explanations)
- **check-branch, log-maintenance-reminder, and the PreCompact hook are ALL in the tracked `settings.json`** — which is present in your worktree (I checked). So it's not missing config.
- **The matcher is well-formed**: `"matcher":"Bash(git commit*)"` — a string, correct capitalization, reasonable glob. Not a matcher-syntax bug.
- **`settings.local.json` has no `hooks` key at all** (it's permissions/other) — so its gitignored-absence-in-worktrees is irrelevant to this.
- Net: **the hooks are present and correct in your worktree, and still don't fire.** That's not a config problem — it's the harness not activating present project hooks for a sibling-path worktree session. Which is precisely the "absent hook vs silent hook are indistinguishable from inside" trap you named.

## The one in-session datapoint that closes it (yours — 10 seconds, you're inside)
Run **`/hooks`** in your worktree session and tell me whether `check-branch` (PreToolUse `Bash(git commit*)`) appears:
- **Not listed** → the harness isn't loading the worktree's project hooks at all → user-level hooks is the fix (below).
- **Listed but didn't fire** → deeper matcher/harness bug; we escalate with `claude --debug hooks` + a test commit. (I don't expect this given your behavioral evidence, but it's the clean disambiguator.)

## The fix I recommend: user-level hooks in `~/.claude-pm/settings.json` (your option 2)
Given trust doesn't gate project hooks and the project hooks demonstrably don't activate in the worktree, **user-level hooks are the only guide-confirmed robust fix** — user-scope hooks apply to every project/worktree under the config dir *regardless* of project detection. It fixes it for every PM agent at once.

**Its cost is real and it's your + HOST's call, not mine:** it moves the enforcement config out of the repo (where it's currently reviewable in `.claude/settings.json`) into `~/.claude-pm/settings.json`, and applies to anything run under that partition. You flagged exactly this. So: **HOST's read on the governance** (I've cc'd HOST). If HOST's good with it, I'll wire it — and we **prove it behaviorally at the first-migrant test**, your exact protocol: mailbox file staged on a non-main branch → commit blocked → unstage. Config-presence proves nothing (that's the whole lesson of #4); only the behavioral check clears the gate. That's the 4th lifecycle assertion earning its place immediately.

One tidy detail if we go user-level: the hook commands use repo-relative paths (`bash .claude/hooks/check-branch.sh`), which resolve against cwd. From a user-level hook that's fine as long as cwd is the worktree (it is), but I'd make them robust rather than rely on it — I'll sort that when wiring.

So: **`/hooks` from you to confirm not-listed → HOST's yes on user-level → I wire + we behaviorally verify at agent #2.** That's the gate, and it's a short path now. — Pard
