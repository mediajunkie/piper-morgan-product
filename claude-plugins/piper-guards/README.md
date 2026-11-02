# piper-guards (R6 step 6)

The cohort's guard hooks, ported into one Claude Code **mod** (a plugin with a hooks module). The plan is stage 7 of
`dev/2026/10/03/spec-eval/D-propose-ruleset.md`: port M-1 to M-6 and M-9, run each mod rule alongside its settings
hook for one week, then retire the hooks. **Status 2026-10-12 (CIO), v0.2.0: M-1 to M-6 implemented, M-9 prototyped. Installed on CIO's seat only (local scope, xian 17:02); live after a restart (M-6 blocked an unset-model Agent call at 18:13, the same call ran at 17:1x before it). Side-by-side week 10-12 to 10-19.** **10-19 review (CIO):** 1 real deny (M-6) and 0 false positives in 1,224 Bash, 9 Agent and 23 Write/Edit calls. No settings hook retires yet (the mod runs on 1 of 11 seats). Per-rule table: `docs/internal/operations/hooks-registry.md`, "Decided 10-19". Next: Pard, one quiet PM seat. Rollout lesson: each seat needs the install **and** a restart.

| Rule | What it does | Settings hook it shadows | State |
|---|---|---|---|
| M-1 | Refuses working-tree-discarding git aimed at PM's main checkout | `.claude/hooks/guard-pm-checkout.sh` | ported; 3 tests pass |
| M-4 | Refuses `gh api` calls carrying `updateProjectV2Field` + `singleSelectOptions` (full replace of a Projects v2 option list) | none (prose rule + skill `assign-sprint-safely`) | new; 3 tests pass. Can't see a query passed by file (`-F query=@q.graphql`) |
| M-2 | Denies `git checkout <ref> -- <paths>` / `git restore --source=<ref> <paths>` when `git diff HEAD --stat -- <paths>` is non-empty; prints the stat. Override: put `diff-reviewed` anywhere in the command | none (prose rule, SCOPE is not DIRECTION) | done; 3 tests (parser pure; hook with `process.run` stubbed). Plain `git checkout -- <path>` (no ref) is not covered |
| M-3 | Denies `git add`, `git mv` or `git rm` of a `mailboxes/` path (mv and rm added in v0.2.2, #2251), or `git commit -a/--all` while `git status --porcelain mailboxes/` is non-empty, on any branch but main; says use `scripts/mail-send.sh`. Parses the command string, so the compound `git add && git commit` is caught | `.claude/hooks/check-branch.sh` (reads the index before the add runs) | done; 4 tests (parser pure; hook with `process.run` stubbed) |
| M-5 | On Write/Edit under `mailboxes/`, `docs/`, `dev/`: writes the NEW content (`content` / `new_string`) to a temp file, runs `python3 scripts/mailbox_bearer_lint.py --files <tmp>`, denies on exit 1. Fails open if the script or python is missing | CI `mailbox_bearer_lint.py` (backstop) | done; 2 tests with the linter stubbed. The real script was run by hand on a fake token (exit 1) and a masked one (exit 0). An Edit is judged on `new_string` only, with no baseline |
| M-6 | Denies an `Agent` tool call with no `model` (a `fork` is exempt: it can't take one) | none (prose rule, CLAUDE.md dispatch tier) | done; 1 test |
| M-9 | Status line `CI main: green/red · briefing Nd`, via `$.ui.status`, refreshed at session start and at most every 10 minutes on a Bash call, never awaited. **0.2.1 (10-19):** the CI word comes from `scripts/main-ci-status.sh`'s summary line (every push workflow, about 30 s), falling back to the newest success/failure per workflow in the last 100 runs. 0.2.0 read one run of any workflow and showed its `status` ("completed" on CXO, Pard 10-19) | log-maintenance and context reminders | prototype: text builder tested; the `gh` / `git log` refresh path is untested live. Log staleness not built (role unknown to the mod) |

**Needs CLI ≥ 2.1.287** (mods are on by default from there; the fleet is on 2.1.296 per Pard's 10-12 record).

- Check: `claude plugin validate claude-plugins/piper-guards`, then `cd claude-plugins/piper-guards && claude plugin test`.
- Try on one session: `claude --plugin-dir claude-plugins/piper-guards`. `/plugin` shows `1 mod active · piper-guards`.
- Turn off: drop the flag, or `/plugin` → disable, or `"disableAllHooks": true`. The settings hooks still run either way.

**Order** (docs, mods/events): managed PreToolUse hooks, then mod `tool.call` hooks, then project PreToolUse hooks,
then permission rules and mode, then `tool.check` mods. A `tool.call` deny that never calls `next` stops the call
before the rules and the auto-mode classifier. **Not yet measured on a live seat**: CIO's sandboxed live test was refused
by the auto-mode reviewer on 10-12. The first live check is the canary seat (Pard).

**Fails open** on its own error (`.catch` passes the call on), so a bug can't wedge a seat. The settings hook stays
behind it during the parallel week.

Cost: string parsing per Bash call; M-2 and M-3 run `git` only when the command parses as a match; M-5 runs python3 per Write/Edit under the three trees; M-9 runs `gh` and `git log` at most every 10 minutes. Benefit: none yet: measuring. Review: 2026-12-01. Owner: CIO (rules), Pard (install).

## Attended live check (for xian; 2 minutes; nothing installed)

Purpose: confirm that a mod's `tool.call` deny holds in **auto mode** on a real seat. The docs imply it; nobody has
measured it. Two seats' reviewers refused to set this up unattended (CIO and Pard, 10-12), so it's a paste for xian.
**Harmless if the guard fails**: the only command the agent runs is `git stash` on a clean throwaway repo.

No paste block in this README contains a `#` comment: interactive zsh treats `#` as an argument unless
`interactivecomments` is set (10-12, Janus). Notes go in the prose around a block.

**1. In your own terminal** (not inside a Claude session), make a decoy repo and a plugin copy pointed at it:
```bash
T=$(cd "$(mktemp -d)" && pwd -P)/pg-check && mkdir -p "$T" && cd "$T"
git init -q decoy && echo x > decoy/a.txt && git -C decoy add a.txt && git -C decoy -c user.name=t -c user.email=t@t commit -qm init
cp -R ~/Development/piper-morgan-worktrees/cio/claude-plugins/piper-guards ./pg
sed -i '' "s#/Users/xian/Development/piper-morgan-product#$T/decoy#" pg/.claude-plugin/plugin.json pg/hooks/register.js
grep -c "$T/decoy" pg/.claude-plugin/plugin.json pg/hooks/register.js
grep -c piper-morgan-product pg/.claude-plugin/plugin.json pg/hooks/register.js
```
The first `grep` should print 1 for each file, the second 0 for each. (The copy comes from CIO's worktree because your checkout hasn't pulled `claude-plugins/` yet. The path is rewritten
in both the manifest default and `register.js`'s fallback, so the result doesn't depend on how userConfig reaches a
`--plugin-dir` session. `pwd -P` matters because the mod compares paths as text and doesn't resolve symlinks; Pard
caught both, 10-12.)

**Result 2026-10-12: PASS** (xian, 09:36; the mod blocked `git -C decoy stash` in auto mode; `git -C decoy stash
list` empty, read by Janus at 09:52). **Control: the command ran** ("No local changes to save", xian ~09:58), so the
mod, not the auto-mode reviewer, did the blocking. The steps stay here for the next seat.

**2. Test run, in auto mode, from `$T`:**

Before you start, two things that bit the first run (Janus, 10-12):
- On Amber, `claude` may not be on a plain terminal's PATH, so the block below uses the full path `~/.local/bin/claude`.
- Over `ssh amber`, the session can start "Not logged in" (its header reads "API Usage Billing") because ssh can't
  read the login keychain. Prefer a tmux window on Amber, where the seats already run signed in. Otherwise run
  `security unlock-keychain ~/Library/Keychains/login.keychain-db`, then start again. Don't run `/login`: it
  hasn't been checked against the seats' shared sign-in. Check the header no longer says "API Usage Billing"
  before going on.

```bash
~/.local/bin/claude --plugin-dir ./pg --permission-mode auto
```
Run `/plugin`. **Stop here unless it shows `1 mod active · piper-guards`.** If it doesn't, the result is
"didn't load" (tell Exec that), not a FAIL. If it does, press Esc to leave `/plugin`, then type:
> Run exactly this one command and show me its output: `git -C decoy stash`

**Pass**: the tool result contains `BLOCKED by piper-guards M-1`, and `git -C decoy stash list` (in your terminal)
is empty. **Fail**: the agent reports `No local changes to save`, which means the command ran past the mod.

**3. Control, same place, no plugin:** a new terminal starts somewhere else, so first `cd "$T"`, then
`~/.local/bin/claude --permission-mode auto` with the same prompt (same sign-in check as step 2). Expected: it runs and
prints `No local changes to save` (or the reviewer stops it, which is also worth noting: a refusal there would mean
the reviewer, not the mod, was doing the work in step 2).

**4. Clean up:** `rm -rf "$T"`. Tell Exec pass or fail (one line); CIO and Pard take it from there.

## Installing on a seat (local scope; Pard's design, 2026-10-12)

Local scope writes to `.claude/settings.local.json` in the worktree it is run from, which is gitignored, so the
install reaches that one seat only and survives a relaunch with no launcher change. Not user scope: the PM seats
share `~/.claude-pm`, so a user-scope install would reach every PM seat at once. Marketplace: `piper-local`
(`claude-plugins/.claude-plugin/marketplace.json`). The marketplace is one per account and each `marketplace add` re-points
it, so every seat adds the same source: the primary checkout, which follows main by fast-forward only and that no seat
works in (Pard, 10-20). For CIO's seat, in your own terminal:

```bash
cd /Users/xian/Development/piper-morgan-worktrees/cio
export CLAUDE_CONFIG_DIR=/Users/xian/.claude-pm
~/.local/bin/claude plugin marketplace add /Users/xian/Development/piper-morgan-product/claude-plugins --scope local
~/.local/bin/claude plugin install piper-guards@piper-local --scope local
~/.local/bin/claude plugin list
```

To load a new version: land it on main, let `scripts/sync-pm-local.sh` fast-forward the primary checkout, then
restart the seat. The status line after the restart is the check; `plugin list` and the install entry are not (see
"Measured 10-20" below).

The last line should list `piper-guards`. The running session may need a restart to load it; check `/plugin` in
the seat's pane shows `1 mod active · piper-guards`. To back out:

```bash
cd /Users/xian/Development/piper-morgan-worktrees/cio
export CLAUDE_CONFIG_DIR=/Users/xian/.claude-pm
~/.local/bin/claude plugin uninstall piper-guards@piper-local --scope local
```

Measured 10-20, at runtime (Pard's restarts of CXO at 11:04 and CIO at 11:05): **with a directory source, a seat
runs the source folder as it is at session start.** Both status lines read `CI main: green`, which is 0.2.1's word (0.2.0
had shown `pending` and `in_progress`), while CXO's entry in `installed_plugins.json` still said 0.2.0 with a
`cache/…/0.2.0` path. So the install entry and the cache are stale metadata, not what runs. CIO's disk-only reading that
morning, that the cache is what loads, was wrong. **The evidence of what a seat runs is the status line after a
restart**, not the install entry, the cache or `plugin list`. Also measured: the `piper-local` marketplace is one per
account, and each `marketplace add` re-points it (CXO's 10-19 install had pointed it at CXO's worktree). Since xian's
10-20 paste it points at the primary checkout, so every seat runs the primary checkout's copy (main, once `sync-pm-local.sh` has fast-forwarded it) as of its last start. Still not measured: whether userConfig's `pm_checkout` reaches an installed plugin
(the `register.js` fallback is the same path on Amber, so the result is right either way). The mod fails open, so
a seat checks that its status line still shows the `piper-guards:` segment:
otherwise "no blocks" can't be told from "not running".
