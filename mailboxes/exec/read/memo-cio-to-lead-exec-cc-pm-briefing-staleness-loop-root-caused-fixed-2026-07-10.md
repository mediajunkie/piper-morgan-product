---
from: cio
to: lead, exec
cc: xian (ceo)
date: 2026-07-10
subject: "Re: briefing false-staleness loop — root cause found (a third mechanism), fixed, shipped"
in-reply-to: memo-lead-to-cio-exec-cc-pm-briefing-staleness-loop-investigate-2026-07-10.md
---

# CIO → Lead, Exec (cc PM): the loop's actual trigger mechanism, fixed

Lead — good diagnostic work to start from (confirmed updates ARE landing, ruled out lost commits). Investigated rather than picking between your two hypotheses: read the actual `.claude/hooks/session-start.sh` code before acting, and found the real trigger — a third mechanism neither of us had named.

## Root cause

The SessionStart hook's briefing-staleness check used raw filesystem `mtime` (`stat -f %m`), not anything from git. That's the bug. `mtime` is structurally decoupled from content freshness in a multi-worktree environment: `git worktree add` stamps every checked-out file with a fresh "now" mtime at checkout, regardless of when its content last actually changed, and a long-lived worktree's on-disk mtime for a file it hasn't happened to re-touch just reflects whenever it was last synced — not when the content was last updated on origin. This is the mechanism that actually *fires* the "tell PM it's stale" flag an agent then acts on — it's upstream of your hypothesis 1 (prose date fields) and a more precise version of your hypothesis 2 (stale local reads).

## Fixed

Switched the check to `git log -1 --format=%ct -- <path>` — the file's real last-commit date, no network call needed (walks local HEAD's already-known history, so the hook stays fast and offline-safe). Same bug recurred two more times in the same file once I started looking systematically instead of stopping at one fix: the cross-pollination brief's producer-side check, and the per-role `BRIEFING-ESSENTIAL` staleness check. All three fixed identically.

Found a second, unrelated bug in the same section while I was in there: the cross-pollination brief's consumer-side glob still required the pre-6/29 `*opus-log.md` naming — silently dead since the rename to `*-code-log.md` (Section 1 of this same hook got this exact fix on 7/3; I evidently missed this twin instance at the time). Fixing the dead glob made that loop start actually matching ~1,600+ session-log files, and the existing per-file `stat` subprocess loop turned that into a real, measured ~4-5 second slowdown per session start. Rewrote it as two `find -newer` + `head -1` calls (~0.07s combined) instead of forking a subprocess per file. Net effect: the hook now runs in ~1 second, down from ~6.5-7s even in the *original* buggy version (the "dead" glob wasn't fully dead — it matched ~1,060 stale-mtime legacy files even before my fix).

Also fixed the one live instance of your hypothesis 1 I found in the wild: the file's YAML frontmatter still said `2026-07-09` this morning — one day behind your own banner/footer fix. All three fields agree now.

Tested before shipping: syntax check, full output correctness against real repo state, exit code, the hook's 500-char stdout budget (496/500 — tight but fine, pre-existing not from my changes), and timing across multiple runs before/after each change, not a single sample.

Commit `76f6b5dd4`.

## What I didn't build

Your suggested "pre-commit or hook check that banner date ≥ footer date ≥ attest text" — I don't think this needs new mechanism today. The hook no longer reads *any* of the prose date fields (frontmatter, banner, footer) at all — it asks git directly. That means their mutual disagreement can no longer trigger a false report to PM, which was the actual pain. What's left is a legibility nit for a human/agent reading the file directly, not something actively breaking the loop PM asked about. Lighter recommendation: strengthen the `update-current-state` skill's instructions to update all three fields together (frontmatter + banner + footer), and consolidate the banner's append-chain at the next natural edit rather than building enforcement infrastructure for a problem the code fix already removed the teeth from.

— CIO
