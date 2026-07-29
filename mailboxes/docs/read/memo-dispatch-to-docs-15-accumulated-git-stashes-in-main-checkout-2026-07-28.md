---
from: Dispatch (via xian)
to: docs
subject: "Housekeeping — 15 accumulated git stashes in PM's main checkout, some back to early May. Review, drop the safe ones, come back on anything ambiguous."
date: 2026-07-28
---

# 15 accumulated git stashes in the main checkout

Docs — while syncing PM's local `main` with `origin/main` this morning (local was 33 commits behind; fast-forwarded clean, no conflicts), the session noticed `/Users/xian/Development/piper-morgan/piper-morgan-product/` is carrying **15 git stashes**, the oldest from May 5. They look like accumulated residue from a range of agents' sessions over the last three months — rebase carryovers, "foreign WIP at session start" set-asides, and a couple of genuine WIP stashes.

**They were left completely untouched during the sync.** Nothing here has been dropped, applied, or inspected beyond `git stash show --stat`.

## The ask

1. **Review what's actually in these 15 stashes.**
2. **Drop the ones that are clearly safe** — stale scratch, work superseded by since-merged commits, duplicates of changes already applied. You don't need to check back for those; just clean them up and note what you dropped.
3. **For anything ambiguous, or anything that might hold real unmerged work — do NOT drop it.** Evaluate it and come back with a recommendation (apply to a branch? extract to a file? hand to the originating role? drop after all?). PM would rather carry a stale stash another week than lose an agent's unmerged work.

Same principle as the git HARD RULE in CLAUDE.md and the "pause before any irreversible action" pattern: `git stash drop` has no undo path once the reflog expires, and "this is probably just disposable scratch state" is not the same as verified-disposable. When unsure, the narrow reversible move — `git stash show -p` first, or `git stash branch` to park it — beats being wrong.

⚠️ **A hazard specific to this cleanup**: stash indices **renumber on every drop**. `stash@{7}` becomes `stash@{6}` the moment you drop `stash@{0}`. Resolve each stash to its stable SHA (`git rev-parse 'stash@{N}'`) before you start dropping, and work from SHAs — or drop strictly highest-index-first. Working top-down by index while the list shifts underneath you is how the wrong stash gets dropped.

Also note this is **PM's live working checkout, not a worktree** — PM edits prose there and saves without committing in real time. Do the inspection read-only, and don't run anything that touches the working tree (no `git stash pop`/`apply` into a dirty tree, no `git stash -u`, no broad `checkout --`). If you need to apply a stash to look at it, do it in your own worktree from the stash SHA.

## Current stash list

Captured 2026-07-28 from the main checkout. Dates are the stash's own commit date; diffstat is `git stash show --stat`.

| # | Date | Description | Diffstat |
|---|------|-------------|----------|
| `stash@{0}` | 2026-07-27 05:40 | On main: pre-existing stale local modifications, not mine, set aside while fixing my own commit mistake | 9 files, +203 / −32 |
| `stash@{1}` | 2026-06-20 07:31 | WIP on claude/magical-jackson-40fc80: 43385d5bb feat(#1289): swap standup-skill to honest engine, retire MorningStandupWorkflow | 1 file, +3 |
| `stash@{2}` | 2026-06-19 21:04 | WIP on main: e43cd5310 mail(janus→exec): open meta-rollup channel — CEO-hat rollup request + inbox conventions | 616 files, +416 / −36,417 |
| `stash@{3}` | 2026-06-16 14:27 | On main: cio-rescue-main-monday-dup | 1 file, +7 |
| `stash@{4}` | 2026-06-14 15:14 | WIP on main: bef514989 mail(cxo): relay PM #1217 confirmation — people/agent network map = Layer-2 People entity; routed PA/PPM/HOST | 1 file, +4 / −4 |
| `stash@{5}` | 2026-06-14 15:14 | WIP on main: bef514989 mail(cxo): relay PM #1217 confirmation — *(identical description to `{4}`, same timestamp, different content)* | 3 files, +45 / −20 |
| `stash@{6}` | 2026-06-02 19:11 | WIP on main: d843c8bbe mail(cio): triage PPM adoption-complete + Comms offset-confirm to read/ (absorbed; reflected in tracker) | 3 files, +4 / −7 |
| `stash@{7}` | 2026-05-19 06:57 | On main: pre-rebase carryover (not mine; will discard after verifying) | 45 files, +294 / −3,009 |
| `stash@{8}` | 2026-05-17 10:50 | On main: foreign comms WIP at sync | 1 file, +3 / −3 |
| `stash@{9}` | 2026-05-17 06:54 | On main: foreign WIP at May 17 session start | 29 files, +143 / −981 |
| `stash@{10}` | 2026-05-16 13:01 | On main: foreign WIP before sync 13:02 | 3 files, +35 / −124 |
| `stash@{11}` | 2026-05-16 07:14 | On main: foreign WIP at May 16 session start | 13 files, +130 / −82 |
| `stash@{12}` | 2026-05-15 07:05 | On (no branch): rebase-recovery-stash-mux | 2 files, +34 / −7 |
| `stash@{13}` | 2026-05-15 06:27 | On main: host-session-log-pending | 1 file, +31 |
| `stash@{14}` | 2026-05-05 14:03 | On claude/869-project-config-ia: claude/869 agent WIP — left after PA recovery 2026-05-04 | 3 files, +74 / −64 |

## Things worth noticing before you start

- **`stash@{2}` and `stash@{7}` are enormous deletions** (−36,417 and −3,009 lines). Almost certainly artifacts of stashing a dirty tree against a far-behind `main` — i.e. the "deletions" are files that existed upstream but not locally at stash time, not deliberate removals. **Treat with extra care and confirm that read before dropping**, because if either one *does* hold real content it'll be buried under thousands of lines of noise.
- **`stash@{4}` and `stash@{5}` share an identical description and timestamp but hold different content** — likely a double-stash during one session, not a true duplicate. Diff them against each other rather than assuming one supersedes the other.
- **`stash@{7}`'s own message says "not mine; will discard after verifying"** — the verification apparently never happened. That's a candidate for exactly the "evaluate and recommend" bucket rather than an assumed drop.
- **`stash@{13}` (host-session-log-pending) and `stash@{1}` (#1289 standup-skill)** are the two most likely to contain real content someone intended to keep. `{13}` is +31 lines of what sounds like an unsaved session log; `{1}` references a specific issue. Check whether that work landed on `main` some other way before deciding.
- Several are labeled "foreign WIP" — meaning the agent that stashed them didn't recognize the changes as their own. Per the self-attribution note in CLAUDE.md, "foreign" in a stash description is a *guess*, not a finding; the content may well be that same agent's pre-compaction work.

No deadline on this — it's hygiene, not a blocker. But it's been accumulating since early May, so sooner beats later before the reflog makes recovery harder on anything that turns out to matter.

— Dispatch, on behalf of xian
