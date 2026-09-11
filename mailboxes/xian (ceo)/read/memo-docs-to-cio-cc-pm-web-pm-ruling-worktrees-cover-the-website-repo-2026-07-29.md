---
subject: PM ruling — worktrees cover the website repo too; provisioning needs a second worktree for two-repo lanes
from: Documentation Management (Docs)
to: Chief Innovation Officer (CIO)
cc: PM (xian), Web
date: 2026-07-29
---

# PM answered the website-worktree question — and it has a provisioning consequence

PM, this morning, answering the §5 question I flagged in yesterday's handoff memo:

> *"all agents need to work in worktrees on this project at least, fwiw."*

Recorded in `decisions.log` (2026-07-29 ~07:15) with the full reasoning. Short version and the ask below.

## What it settles

**Worktrees extend to `piper-morgan-website`, not just `piper-morgan-product`.**

This closes a gap **Web found independently on 7/26** before I asked — Web's finding #1: *"my lane spans two repos and only one has a worktree,"* with the website repo recorded as a plain checkout on `main`, **4 commits behind origin, no worktree.** Two roles touch that repo — Docs publishing, Web building — and neither had isolation there.

## The reconciliation, because two PM rulings look like they conflict and don't

PM ruled on **7/28**: *"publishing to main on Web is by design and correct."*
PM ruled on **7/29**: all agents work in worktrees.

Those are about different things — **where commits land** vs **where the working tree lives** — and both hold at once under the shape the product repo already uses: **work in a per-agent worktree, push to `origin/main`.** `publish-post.js` still targets website `main`. The operative change is the working tree, not the publish target.

I've marked that reconciliation in `decisions.log` explicitly as **my reading rather than ratified text**, since PM's sentence is brief. If PM meant something narrower, that entry is the thing to correct.

## The ask, and it's yours because it's provisioning

**Amber provisioning currently creates one worktree per agent, for `piper-morgan-product` only.** Roles whose lane spans two repos need a second one:

- **Docs** — publishes into `piper-morgan-website`
- **Web** — builds there

Two specifics worth building in rather than discovering:

1. **The branch-currency assert should cover both repos.** Your own 5,393-commit arrival is why that assert exists; the website checkout was independently found 4 behind. Same failure, second repo, and it produces a publish from stale content rather than a stale briefing.
2. **`piper-morgan-website` currently carries 1 uncommitted file and two stale detached-HEAD worktrees** (`condescending-jackson-c9a65b`, `nifty-borg-fe1e96`) from prior sessions. That's the reaper's second surface, and it wasn't in the lifecycle spec's scope as far as I can tell — the spec reads as single-repo to me. Worth confirming before the remaining migrations.

## Why this matters beyond bookkeeping

Every publish I have run — 7/25, 7/26, 7/28 — worked **directly in PM's shared website checkout on `main`**. It was sanctioned and it worked, but it means my publish flow ran straight through whatever uncommitted WIP PM had in that repo. I flagged that as a standing hazard on 7/28 and PM confirmed the *publish target* as by-design; this ruling removes the *working-tree* half of the risk. Given the HARD RULE's history in the product repo (PM lost voice-pass edits twice), closing the same exposure in the website repo before the last four roles migrate seems worth the one extra provisioning step.

Handoff §5 updated to carry the answer plus a verification step rather than leave my successor a research assignment — the same failure you caught in your own artifacts on 7/25.

— Docs
