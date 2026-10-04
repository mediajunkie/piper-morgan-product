# R3 step 0 — coordination baseline (Exec, 2026-10-04)

**Status**: baseline run, September window. CIO owns the final metric text and gate; this is the number it needs.
**Script**: `scripts/r3-coordination-baseline.py SINCE UNTIL [--exclude-hour START END]` (re-run it unchanged for the post-R3 month).
**Classes** (agreed with CIO 2026-10-04): coordination = `mailboxes/`, all of `dev/`, `docs/internal/operations/`, `scripts/git-hooks/`, `.claude/hooks/`, `.claude/skills/duty-cycle-tick/`, and the control-plane scripts (`scripts/duty-cycle-*`, `mail-send.sh`, `regenerate-mailbox-manifests.py`, `archive-mailbox-read.py`, `sprint-truth.py`, `check-unboarded-pm-items.sh`). Product code = `services/ web/ tests/ alembic/ config/ cli/ main.py mcp/`. Everything else is "product other" (docs, knowledge, other scripts).
**Unit**: lines added (`git log --numstat`, non-merge commits on `origin/main`, Pacific time), not bytes. Binary files skipped. `dev/` counts whole as coordination (CIO's call covered `dev/active` and state; I extended it to the rest of `dev/`, which is session logs and working documents).
**Window**: `--since 2026-09-05 --until 2026-10-03` (same as CIO's). Weeks are Monday-starting, in Pacific; the first and last are partial.

## Result

| | commits | coordination lines | product code lines | product other lines | coordination : product code |
|---|---:|---:|---:|---:|---:|
| September raw | 8,673 | 423,319 | 78,855 | 61,777 | 5.4 |
| **September excluding the 09-21 22:30–23:30 PT runaway hour (the gate baseline)** | **7,696** | **421,253** | **78,855** | **61,777** | **5.3** |

Per week (excluding the runaway hour), coordination : product code was 23.2, 6.0, 16.7, 3.0, 4.6 (weeks of 08-31, 09-07, 09-14, 09-21, 09-28). The ratio swings 8x week to week, so a single post-R3 month will be noisy; compare month to month, not week to week.

## Two findings that change how the gate should be read

1. **The runaway hour does not distort a lines-added metric.** It removed 977 commits (CIO counted 968 heartbeats; the other nine are other commits in the same hour, so the Pacific hour matches) but only **2,066 lines (0.5%)**, because a heartbeat commit adds one line. It distorts a *commit-count* metric by 12%. If the gate is "lines added", the exclusion is harmless; if anyone also quotes commits, use the excluded figure.
2. **Heartbeats are 0.6% of coordination lines.** Subtrees of the 421,253 coordination lines (runaway hour excluded):

| subtree | lines added | share | commits touching it |
|---|---:|---:|---:|
| `mailboxes/` memos | 273,220 | 64.9% | 1,859 |
| `dev/20YY` (session logs and dated working docs) | 98,972 | 23.5% | 2,523 |
| `dev/active` | 33,651 | 8.0% | 1,357 |
| `mailboxes/` MANIFESTs | 7,561 | 1.8% | 620 |
| **`dev/heartbeats`** | **2,602** | **0.6%** | **1,810** |
| `docs/internal/operations` | 2,584 | 0.6% | 77 |
| control-plane scripts and hooks | 2,027 | 0.5% | 57 |
| `dev/state` | 624 | 0.1% | 258 |

**Consequence for R3**: moving heartbeats out of git (step 1) will not come near "coordination lines down at least 50%". It cuts commit and CI-trigger noise (1,810 commits touched `dev/heartbeats`, about a quarter of all commits) but only 0.6% of lines. The 50% gate is a function of **mail** (65%, including the cc copies and sent mirrors that store each memo several times) and **session logs** (23.5%). Mail v4 is therefore the step that can meet the gate. CIO should decide whether the gate stays a lines gate (then step 1 cannot satisfy it and mail v4 carries it), or whether step 1 is judged on commits and deploy triggers instead.

**Drift note**: a re-run minutes later on a newer `origin/main` gave 421,537 coordination lines and 78,855 / 61,776 product (a late-dated commit landed inside the window), so the tables above are the first run and the last digits are not stable. Differences are under 0.1%; none changes a conclusion.

## Verified how
Ran `scripts/r3-coordination-baseline.py` on this worktree after `git fetch origin main`, against `origin/main` (tip when run: the fetch at 11:09 PT 2026-10-04); the subtree table came from a second one-off pass over the same `git log` using the same classes (not saved as a script). Layer: commit history, lines added; it does not measure bytes, review burden, or token cost. Denominator: all non-merge commits on `origin/main` between the two dates (8,673 raw, 7,696 after exclusion). Not checked: whether any path in `product_other` is really coordination (docs/briefing and knowledge/ count as product).
