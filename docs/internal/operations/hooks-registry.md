---
type: operations
title: "Hooks registry: every hook, where it is wired, what it must do"
valid_from: "2026-10-14"
last_updated: "2026-10-19"
---

# Hooks registry

**Owner:** CIO (the control plane, role card priority 3). Arch reviews. Pard installs anything outside
the repo (user-level settings, the git common dir, launchd).
**Why this page exists:** the 2026-10-14 methodology audit found that 1 of 14 Claude Code hooks was linked
both ways to a written concept. The reasons lived in header comments, a July post-mortem and mail. This
page is the concept index. Each hook's header should carry `Concept: docs/internal/operations/hooks-registry.md`
or a more specific doc (sunset-or-renew rule, `Concept:` line).
**Is it actually firing?** This page says what is wired. `scripts/whats-armed.sh` measures what is armed
(see `whats-armed.md`). Only Pard's drumbeat measures a hook firing inside a live session, and only for
`check-branch.sh`. **Which copy:** since 10-14 19:15, PM's project copy, carried from origin/main
(mediajunkie 9afa8c9). Before that, the drumbeat tested the user-level copy, because its temp repo has no
project settings. See "Consequence" below.

Exit codes: a PreToolUse hook that exits 2 **blocks** the tool call. Exit 0 lets it through. A
PostToolUse or PreCompact hook can only **warn**: the tool has already run, or compaction proceeds.

## 1. Claude Code hooks, project settings (`.claude/settings.json`, every seat in this repo)

| Hook | Event / matcher / if | Must do | Blocks? | Concept |
|---|---|---|---|---|
| `session-start.sh` | SessionStart (also fires with source `compact`) | Print status within budget: log, mail counts, briefing freshness, role card (from the briefing's `ROLE-CARD` block), deltas | No | CLAUDE.md "Session start"; #853 |
| `check-branch.sh` | PreToolUse Bash, if `git commit*` | Refuse a commit of `mailboxes/**` on any branch but main, and tell the agent to send by `scripts/mail-send.sh` (fix steps corrected 10-14); warn on other non-main commits; since 10-16, warn (never block) on a staged heading in today's session log that carries an HH:Mx time or a time ahead of the clock, and since 10-17 on today's `*(Role, date time` stamps added to BRIEFING-CURRENT-STATE.md, and since 10-19 on today-dated lines added to decisions.log, the leading stamp and any inline HH:Mx (`scripts/stamp_check.py --log-staged`); since 10-23, **block** a commit whose staged BRIEFING-CURRENT-STATE.md fails `scripts/check-current-state.py` (the same gate Code Quality runs; a missed `last_updated` bump had turned main red for three pushes) | Yes, on a pre-staged index. The git `pre-commit` row (section 4) is the enforcing check. | `branch-worktree-mailbox-discipline.md`; `amber-hooks-investigation-2026-07.md` |
| `guard-pm-checkout.sh` (+ `guard_pm_checkout.py`) | PreToolUse Bash, every call | Refuse working-tree-discarding git aimed at PM's main checkout | Yes | CLAUDE.md hard rule 1; decisions.log (R6 step 1, 10-04) |
| `pre-commit-reconcile-drafts.sh` | PreToolUse Bash, if `git commit*` | When a commit touches `docs/public/comms/drafts/`, run `reconcile-drafts-calendar.py` for draft and calendar drift | Can exit 2 | decisions.log (Layer C). Header cites a missing `docs/read/...` path. |
| `pre-commit-ship-synthesis-gate.sh` | PreToolUse Bash, if `git commit*` | Refuse a commit that adds a new `weekly-ship-NNN-draft-*.md` unless `ship-reviews/ship-NNN-week-review.html` exists, carries `<!-- discussed: YYYY-MM-DD -->`, and the editorial calendar names the draft in `draftPath` (index or disk). Edits to an existing draft pass. For a compound `git add … && git commit`, an untracked draft named in the command counts as added. Exec wrote it, xian approved it 10-23 after Step 2c was skipped for #054 and #066; CIO added the calendar check and the compound case, and registered it 10-23 (scratch repo 8 of 8 cases) | Yes (exit 2) | `.claude/skills/draft-weekly-ship/SKILL.md` (Step 2c); decisions.log 10-23 |
| `autoclose-guard.sh` | PreToolUse Bash, if `git commit*` | Pass the message to `scripts/check_autoclose_keywords.py`: refuse close/fix/resolve plus `#N` without `Auto-Close: intentional`, and refuse credential-shaped messages | Yes | `commit-message-guards.md` (doorway 1); CLAUDE.md hard rules 5 and 3 |
| `log-maintenance-reminder.sh` | PostToolUse Bash | Every 15 Bash calls, remind if today's session log is missing or stale. **Note (10-14):** its counter is one shared file, `/tmp/piper-log-reminder-counter`, so "every 15 calls" counts across all seats on the host, not per seat. | No | CLAUDE.md "Role and session log"; methodology-31 and -41 |
| `issue-checkbox-lint.sh` | PostToolUse Bash | After a commit that closes an issue, warn if the issue body still has unchecked boxes | Warns (exit 2 is advisory after the fact) | `agent-protocols/issue-closure-protocol.md` |
| `draft-birth-record.sh` | PostToolUse Bash and Edit\|Write\|MultiEdit | Record when each unsent file under `mailboxes/` first appears (`dev/state/draft-births.tsv`, gitignored), so `scripts/mail-send.sh` can warn (`scripts/draft_births.py check`) on a memo first written over 60 min before its send, and list the decisions.log lines stamped since. Added 10-19 from the stale-draft mini retro (Lead's 11:19 memo was a 06:45 draft) | No (never prints) | `scripts/draft_births.py` header (five lines; review 2026-12-14). Live on CIO's seat 10-19 14:34: a probe Write landed in the ledger in the same second |
| `memory-index-overlimit-warn.sh` | PostToolUse Edit, Write, MultiEdit | Warn when the shared memory index nears its silent-truncation limit | No | `memory-index-size-limits.md` (explains the limit; this page names the hook) |

**The time-of-check split** (Arch's ruling, 07-29; Arch's review, 10-14). `check-branch.sh` runs at two layers, and neither alone is the rule:
- As a **PreToolUse** hook, it reads `git diff --cached` *before* the command runs. On a compound `git add … && git commit` the index isn't staged yet, so it passes. That's why CLAUDE.md says to stage in one call and commit in the next.
- As part of the **git pre-commit** (section 4), it runs on the settled index. This is the enforcing layer, and it catches the compound form.
- The PreToolUse copy adds one thing: it still sees a `git commit --no-verify` (which skips git hooks), as long as the index was staged beforehand.

**Sunset 2026-10-19 (CIO): `context-usage-reminder.sh`** (PostToolUse Bash; meant to suggest compacting at about 75 to 85% context). Benefit at review: none. It was dead on Amber from at least 10-14: it read `$CLAUDE_SESSION_ID` and looked under `~/.claude/projects`, but this fleet's transcripts are under `~/.claude-pm/projects`. Nobody reported missing it. Removed from `.claude/settings.json`, the script deleted, whats-armed's file list and the `.gitignore` marker line dropped (before removal: `git grep` found those readers and no user-level wiring). **Replacement: none in the repo.** Claude Code's own context indicator and auto-compact remain. Correction: this row said M-9's status line covers it. It doesn't: M-9 shows main's CI state and briefing age, not context. If a context warning is wanted again, read `transcript_path` from the hook's stdin JSON. The script is in git history at `647a77e7`.

## 2. Claude Code hooks, user level (`~/.claude-pm/settings.json`, every seat on Amber; Pard installs)

**Since 10-14 10:43 (Pard), one entry only:** PreCompact `precompact-signoff-warning.sh` (before compaction, warn about uncommitted, unpushed or unmerged work; concept `branch-worktree-mailbox-discipline.md`). It points at PM's checkout's copy, `/Users/xian/Development/piper-morgan-product/.claude/hooks/`, which lags main until `sync-pm-local.sh` runs. It should eventually move to project level, so it runs the seat's own version.

Removed 10-14 (decided below): six duplicates of project hooks. They ran PM's checkout's copies alongside the seat's own:
- PreToolUse: `check-branch.sh`, `pre-commit-broad-staging-warn.sh`, `pre-commit-reconcile-drafts.sh`.
- PostToolUse: `log-maintenance-reminder.sh`, `context-usage-reminder.sh`, `issue-checkbox-lint.sh`.

Backup: `~/.claude-pm/settings.json.bak-20261014T104256`. History: in July, project hooks didn't fire reliably in worktree sessions (`amber-hooks-investigation-2026-07.md`), and that's why the copies existed.

## 3. Seat-local and plugin hooks

| Hook | Where | Must do | Notes |
|---|---|---|---|
| `PROBE-userpromptsubmit.sh` | CIO's `.claude/settings.local.json`, UserPromptSubmit | Append one line per submitted prompt to `dev/state/probe-userpromptsubmit-cio.log` (a submission ledger from outside the model) | CIO seat only; never blocks. It dirtied `git status` on every wake (noted in the 10-13 rewrite), which blocked `seat-restart.sh` on 11-02, so the log is untracked and gitignored since then (it stays on disk). Known gap: the script never reads stdin, so `bytes` is always 0 and `matches_tick` always `no`; the timestamps are the ledger. |
| `piper-guards` mod (`claude-plugins/piper-guards/`, v0.2.1, running on both seats since the 10-20 11:04/11:05 restarts) | Plugin on CIO's and CXO's seats (local scope, CXO since 10-19 14:47); the parallel week ended 10-19 (decisions under "Decided 10-19"). One `piper-local` marketplace per account, pointing at the primary checkout since 10-20; a seat runs that folder as of its last start (measured at runtime 10-20, README) | Rules M-1 to M-6 shadow the settings hooks above and add Projects-v2, mail-on-main, bearer-on-write and subagent-model rules | Concept: its README and `dev/2026/10/03/spec-eval/D-propose-ruleset.md`. Fails open. Retires no settings hook yet. |

## 4. Git hooks (shared git store `.git/hooks/`, every worktree by construction; source in `scripts/git-hooks/`)

| Hook | Installed? | Must do | Blocks? | Concept |
|---|---|---|---|---|
| `pre-commit` | Yes | Run `pre-commit-broad-staging-warn.sh` and `pre-commit-ruff-warn.sh` (warnings, exit 0), then `check-branch.sh` on the settled index (Arch's time-of-check ruling, 07-29) | Only via check-branch | Its header; `amber-hooks-investigation-2026-07.md` |
| `pre-push` | Yes (identical to source, 10-13) | (a) The **old-history guard**: refuse a push that contains any sha in `<common-dir>/piper-old-history-sentinels`, logging to `piper-old-history-guard.log`. (b) A fast smoke run on pushes touching code. | Yes | `history-rewrite-runbook.md` (Exec, moved to docs 10-14; the sentinel protocol and as-run record); header; `mechanism-sunset-or-renew.md`. The header's own `Concept:` pointer waits for the hook's next functional edit, because any edit makes the installed copy differ from source until reinstalled (xian's paste). |
| `post-commit` | Yes; a `post-commit.DISARMED-2026-09-21-runaway` copy sits beside it | Delegate to `.claude/hooks/post-commit.sh` (heartbeat auto-fire pilot, ruff advisory) | No | Header points at `amber-hooks-investigation-2026-07.md`. **Current state of the pilot isn't confirmed on this page.** |
| `commit-msg` | **Yes, since 2026-10-15 13:2x** (xian's paste; Exec checked with `cmp`; CIO ran the installed hook: "fix #1" refused rc 1, benign rc 0) | Shape-independent check for rules 3 and 5 on the final message. Fails open loudly if the checker crashes. | Would block | `commit-message-guards.md` (doorway 3; written 10-14, audit R6) |

Smaller push-time scripts in `scripts/hooks/` (`pre-push-release-notes-check.sh`,
`editorial-calendar-reconcile-warn.sh`) aren't installed in the common dir as of 10-14 (`ls .git/hooks`).
The audit lists them as having no concept doc.

## Decided 10-14: drop the user-level duplicates

**Facts:**
- **Project-level SessionStart fires on worktree seats** (Arch, from its own session at start and after compaction; user level doesn't wire SessionStart).
- **Project-level PreToolUse fires on a worktree seat.** CIO measured it 10-14, between 10:35 and 10:37 PT (after the 10:35 mail read, before this edit): `git commit --dry-run -m "fix #1"` in CIO's worktree was BLOCKED by `autoclose-guard.sh`, which only the project settings wire. The piper-guards plugin has no auto-close rule, so the refusal could only come from the project hook. One seat, in auto mode.
- **Project-level PostToolUse firing on a worktree seat isn't measured.** Its exit-0 output isn't visible to the agent.
- **The two levels run different commands.** User level runs `bash /Users/xian/Development/piper-morgan-product/.claude/hooks/X.sh`, PM's checkout's copy. Project level runs the seat's worktree copy. So both run, and Claude Code's dedup of identical commands doesn't apply (Pard, from the JSON; an expectation, not a measurement).
- **PM's checkout's copies lag main**, because only `sync-pm-local.sh` fast-forwards it. On 10-14 all 7 user-level scripts differed from main (Arch, `diff -q`).

**Ruling** (Arch, the architecture half): two copies of one rule, read from two places and kept in step by hand, is a second-resolver shape. Since project-level PreToolUse fires, remove the user-level duplicates:
- `check-branch.sh`
- `pre-commit-broad-staging-warn.sh`
- `pre-commit-reconcile-drafts.sh`
- the three PostToolUse reminders

Keep `precompact-signoff-warning.sh` at user level, since it has no project copy. It should eventually move to project level, so it runs the seat's own version.

**Done 10-14 10:43** (Pard; the seat wasn't refused). **After the edit:** CIO re-ran the autoclose probe between 10:49 and 10:50 PT, and it was still BLOCKED by the project hook. PostToolUse is still not cleanly measured. The one instrument tried, the log-maintenance counter, is a host-wide shared file that every seat increments, so a rise can't be attributed to one seat. A clean PostToolUse probe needs a per-session signal.
- **Consequence, found 19:05 (Pard):** the hook drumbeat went red ("probe commit LANDED"). It had only ever tested the user-level `check-branch.sh`, the copy this decision removed. PM seats load check-branch from project settings, and project-level PreToolUse fired (the autoclose probe above, a sibling hook). Pard's fixed probe now tests check-branch's project copy directly. Pard fixed the probe at 19:15 to carry PM's project `.claude/` from origin/main, and it PASSES. Neither Pard nor CIO checked what the drumbeat exercised before the removal. The sunset rule now has a "Before you remove" step.
- **Residual risk:** project-level PostToolUse firing is unmeasured, so the three reminders could go silent. They're advisory, so this is low cost, and it's checked after the edit. **Measured 10-19 14:34 (CIO's seat):** a project-level PostToolUse hook (`draft-birth-record.sh`, Edit|Write matcher) fired on a worktree seat, with its row written in the same second. That's 1 of 11 seats.

## Decided 10-19: piper-guards after the parallel week

**What the week measured** (CIO's seat, 10-12 18:13 to 10-19 10:15 PT): 1,224 Bash, 9 Agent and 23 Write/Edit calls ran under the mod. **One real deny**, M-6 at 10-12 18:13, an Agent call with no `model`. That was 1 of the 1 such call in the week. **No false positives:** no other mod deny appears in the transcript's tool results. **No disagreement with the settings hooks:** neither `guard-pm-checkout.sh` nor check-branch's mailbox block fired in the week either. The settings hooks that did fire were the 3 commit-message-guard blocks, which the mod doesn't shadow. So the week measured the mod's cost in false positives (none) and not its catch rate. M-1 to M-5 had no live trigger. M-1's only live catch is xian's attended decoy check (10-12, auto mode, PASS with a control).

| Rule | Decision | Why |
|---|---|---|
| M-1 (PM checkout) | **Keep both** the mod rule and `guard-pm-checkout.sh` | The mod runs on 1 of 11 seats; retiring the hook would strip the other 10. One live catch (the decoy), 0 on a seat. |
| M-2 (diff before checkout) | **Renew** | No settings counterpart, so it's net-new coverage. 0 triggers, 0 false positives. |
| M-3 (mail on main) | **Keep both** | Catches the compound `git add && git commit` that check-branch can't. check-branch can't be retired wholesale anyway: it also runs the stamp check. |
| M-4 (Projects v2 replace) | **Renew** | No settings counterpart; hard rule 4's only mechanism. 0 triggers. |
| M-5 (bearer on write) | **Renew** | No pre-write counterpart (the CI lint is after the fact). 23 writes, 0 false positives. |
| M-6 (subagent model) | **Renew** | 1 of 1 live catch, the only rule with one. |
| M-9 (status line) | **Prototype, unchanged** | Its render on a live seat hasn't been observed. Not counted. |

**When a settings hook retires:** only after the mod is on every seat and has run a week there, and the shadowed hook's own probe (whats-armed, the drumbeat) has been moved to the mod first. That's the sunset rule's "Before you remove" step: Pard's drumbeat probes check-branch's project copy.
**Next step (Pard's hand, per the README's rollout):** install on one quiet PM seat (install + restart), then the rest. Asked of Pard 10-19.

## Still open

- **piper-guards on CXO next** (Pard, 10-19 10:20). Order: (1) xian pastes the auto-mode off-switch into `~/.claude-pm/settings.json`, because a restart before it risks the setup dialog that froze CXO and Exec on 10-10 and 10-18; (2) xian runs the local-scope install (another seat's settings, so it's xian's hand); (3) Pard restarts CXO on his go and checks `claude plugin list`. Then a quiet week on CXO, then the rest.

**Verified how:**
- Read `.claude/settings.json`, `~/.claude-pm/settings.json` and CIO's `settings.local.json` with a JSON
  parser, listing every event, matcher, `if` and command.
- Listed `.git/hooks` in the shared store.
- Read each hook's header and counted its `exit` codes.
- Committed 2026-10-14 10:26 PT (first version); updated 10:37 with Arch's and Pard's answers and CIO's PreToolUse probe. (The first version said "about 11:30 PT", which was a guess, not a reading; corrected.)
- **Layer:** config and file. Whether each hook fires in a live session isn't measured here.
- **Denominator:**
  - 9 project registrations;
  - 7 user-level registrations;
  - 1 seat-local registration;
  - 1 plugin;
  - 4 git hooks.
