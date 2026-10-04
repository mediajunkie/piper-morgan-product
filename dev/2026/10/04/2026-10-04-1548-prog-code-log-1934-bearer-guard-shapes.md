# Session log — Coding Agent (prog), #1934 bearer-guard shapes

**Model**: Sonnet (assigned by Lead)
**Dispatched by**: Lead
**Date**: 2026-10-04
**Repo/worktree**: /Users/xian/Development/piper-morgan-worktrees/lead (branch claude/lead-cycle) — work only here, per Lead's instructions. Did NOT touch services/intent_service/* or tests/test_architecture_enforcement.py (other lanes).

## Task

GitHub issue #1934 — the commit-message bearer/auto-close guard (`scripts/check_autoclose_keywords.py`,
`.claude/hooks/autoclose-guard.sh`) missed `-am`, `-m"..."` (no space), `--message`, `-F`/`-F -`,
`git -C`/`git -c`, and its block reason never reached the committer (stdout vs stderr).

## What shipped

1. **`scripts/check_autoclose_keywords.py`** — rewrote `commit_messages_in_bash_command` to use
   `shlex`-based parsing instead of the narrow regex set. New helpers:
   - `_extract_heredocs` — protects heredoc bodies with shlex-safe sentinels before tokenizing,
     so `-F - <<'EOF'...EOF` and `-m "$(cat <<'EOF'...EOF)"` survive tokenization.
   - `_resolve_value` — resolves a token back to its heredoc body via sentinel or `$(cat SENTINEL)`.
   - `_split_segments` — splits the flat token stream on `&&`/`||`/`;`/`|`/`|&` into simple-command
     segments (compound commands).
   - `_commit_args` — identifies `git [global-opts] commit ...` per segment, stripping `-C <dir>`,
     `-c k=v`, `--git-dir=`, `--work-tree=` before the subcommand check (this is what makes
     `git -C`/`git -c` detectable — the old substring check `"git commit" not in cmd` returned
     early and skipped these entirely; found and fixed during testing, not just in the issue).
   - Main loop handles `-m`/`--message` (repeatable, paragraphs), `--message=`, attached `-m"..."`,
     combined short-flag clusters ending in `m` (`-am`, `-sm`, `-avm`, ...), `-F <file>` (reads the
     file), `-F -` + heredoc, `--file=`.
   - `_legacy_commit_messages_in_bash_command` — the old regex extractor, kept as the fallback if
     `shlex.split` raises `ValueError` (unbalanced quoting); never crashes, says so on stderr.
   - Also fixed the top-level guard in the new function from `"git commit" not in cmd` (a substring
     check that defeated `-C`/`-c` detection by construction) to `"commit" not in cmd`.

2. **`.claude/hooks/autoclose-guard.sh`** — moved the BLOCKED message and the checker's captured
   reason from stdout to stderr (`>&2` on both `echo` and `sed` lines). Verified behaviorally: before
   the fix, a blocked run produced 455 bytes on stdout / 0 on stderr; after, 0 on stdout / 455 on
   stderr. This matches HOST's finding that a PreToolUse hook's stdout on exit 2 never reaches the
   committer through this harness.

3. **`scripts/git-hooks/commit-msg`** (NEW, NOT INSTALLED) — a candidate `commit-msg` git hook,
   following the existing `scripts/git-hooks/pre-push` convention (PROPOSED, NOT INSTALLED header;
   waits for CIO co-sign). Calls the same checker against the final assembled message file git
   hands it — shape-independent by construction, since by the time `commit-msg` fires git has
   already resolved every `-m`/`-F`/`-C`/`-c`/editor shape into one message. Reported as a
   recommendation, not installed (hard rule: no hook installation without CIO co-sign).

4. **Tests**: new file `tests/unit/scripts/test_commit_message_shapes_1934.py` (48 cases) —
   parametrized over every shape in HOST's gap table (extractor-level + live-hook-level), the
   existing false-positive set, the #1691 auto-close half in the new shapes (including the
   `Auto-Close: intentional` opt-in), and an explicit stdout-must-be-empty-on-block regression test.
   Also a mechanism test for the new `commit-msg` hook (blocks/passes) and a test asserting it is
   NOT wired into `.claude/settings.json` or any installed git-hooks dir.

   Updated 2 pre-existing tests that pinned the OLD (buggy) stdout channel:
   `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py::test_git_commit_doorway_blocks_a_credential_in_the_message`
   and `tests/unit/scripts/test_check_autoclose_keywords_1691.py::test_git_commit_doorway_blocks_the_incident_subject`
   — both now assert `"BLOCKED" in r.stderr` and `r.stdout == ""` instead of the reverse.

## Shapes covered (table: shape -> before/after)

| Shape | Before | After |
|---|---|---|
| `-m "..."` | blocked | blocked (unchanged) |
| `-am "..."` | **passed** | blocked |
| `-sm "..."` / `-avm "..."` (other clusters ending in m) | passed | blocked |
| `-m"..."` (no space) | **passed** | blocked |
| `-m'...'` (no space) | passed (narrow regex matched this) | blocked (still) |
| `--message "..."` | **passed** | blocked |
| `--message="..."` | **passed** | blocked |
| `-F <file>` | **passed** | blocked (file read) |
| `--file=<file>` | passed | blocked |
| `-F - <<heredoc>` | **passed** | blocked |
| `git -C <dir> commit -m ...` | **passed** | blocked |
| `git -c k=v commit -m ...` | **passed** | blocked |
| compound (`git status && git commit -am ...`) | mixed (worked for plain `-m`, not `-am`) | blocked |
| multiple `-m` (paragraphs) | blocked (for the first form) | blocked (both captured) |
| `git tag -a -m ...` (out of scope, no `commit`) | passed (correctly, out of the guard's stated scope) | passed (still, correctly) |
| heredoc writing a FILE (not the message) | passed (correctly — not a message) | passed (still, correctly — verified not regressed) |
| Block reason channel | **stdout** (harness shows only stderr; reason never reached committer) | **stderr** |

## 300-message regression (real traffic on origin/main)

`git log origin/main -300 --format=...` piped through `find_hits`/`bearer_hits_in_message` directly
(the message-scanning functions, not the bash-command extractor — these 300 are commit messages, not
constructed shell commands): **0 refusals / 300 examined**. Confirms the rewrite didn't introduce new
false positives on real cohort traffic.

Additionally ran the `--bash-tool-input`/live-hook path over last-15 real commit subjects wrapped in
4 shapes each (`-m`, `-am`, `--message`, `git -C ... -m`) = 60 runs: **0 false positives**.

## Test tails

- `tests/unit/scripts/test_commit_message_shapes_1934.py`: 48 passed
- `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py` +
  `test_check_autoclose_keywords_1691.py` + `test_mailbox_bearer_lint_1845.py` +
  the new file together: 117 passed
- `ruff check` + `ruff format --check`: clean (one file auto-reformatted by `ruff format`, re-verified
  green after)
- Full unit suite (`tests/unit tests/scripts -m "not llm"`, same addopts as the task's command):
  **12399 passed, 228 skipped, 3 deselected, 171 warnings in 251.13s**. `grep -c "^FAILED"` = 0.
  No failures anywhere, including the other lanes' concurrently-dirty files
  (`services/intent_service/canonical_handlers.py`, `services/intent_service/pre_classifier.py`,
  `tests/unit/services/intent_service/test_repo_management.py`) — nothing to report there.

## Files changed

- `scripts/check_autoclose_keywords.py` (extractor rewrite)
- `.claude/hooks/autoclose-guard.sh` (stdout -> stderr)
- `scripts/git-hooks/commit-msg` (NEW, proposed, not installed)
- `tests/unit/scripts/test_commit_message_shapes_1934.py` (NEW, 48 cases)
- `tests/unit/scripts/test_bearer_credential_in_commit_messages_r5_1845.py` (2-line channel fix)
- `tests/unit/scripts/test_check_autoclose_keywords_1691.py` (1-line channel fix)

## Not done / known limits

- `-am"msg"` (combined short-flag cluster with an attached, no-space quoted value) is not
  specifically handled — shlex merges `-am` and the quoted value into a single token
  (`-ammsg`) when there's no space, which this parser doesn't unpick. HOST's table named
  `-am "..."` (space-separated) as the gap, not this cross-product form; flagging it as a residual
  edge case rather than silently claiming full coverage.
- `-F -` with NO inline heredoc (true interactive stdin) cannot be read statically; the extractor
  skips it with a stderr note rather than guessing.
- Did not modify `mail-send.sh` — verified behaviorally it already puts all guard output on stderr
  (0 stdout bytes on a refused probe) and never prints the token; this matches the issue's own
  "Not a gap" finding.
- Did not touch `.claude/hooks/check-branch.sh`, which has the same stdout-only pattern for its own
  BLOCKED message — out of scope for #1934 (different hook/guard), noting as discovered-work-adjacent
  observation, not filing a new issue per task scope (Lead's call whether to track).

## Hard rules followed

- No `git add`/`commit`/`push`/stash/`checkout --`/`reset` run.
- No LLM calls; timestamps via `date +%H:%M`/`date +%H%M`.
- `bash -n` run on every shell file touched (`.claude/hooks/autoclose-guard.sh`,
  `scripts/git-hooks/commit-msg`) — both clean.
- Never printed or committed a real credential; all probes used the synthetic fixture token
  `ZVHW…8B35 (replaced 2026-10-04: possibly a real minted invite token; tests now use a fresh synthetic fixture)` (same fixture as the existing R5/#1845 suite).

**Verified how**: ran the extractor function directly against all HOST gap-table shapes plus
negative controls (shown above); ran the live PreToolUse hook via subprocess for the same shapes,
asserting exit code, stdout emptiness, and stderr content; ran a 300-message regression against real
`origin/main` history; ran the full project unit suite (`tests/unit tests/scripts -m "not llm"`,
12399 passed / 228 skipped / 0 failed); ruff check + format. Layer: extractor function in isolation,
live hook subprocess, real commit-message corpus, full project test suite. Denominator: 14 shapes
from HOST's table (all addressed) + 300 real commit messages (0 false positives) + 60
real-subject/shape combinations (0 false positives) + 12399 project tests (0 failed).
