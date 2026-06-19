---
from: CIO (Chief Innovation Officer)
to: Lead Dev
cc: PM (xian)
date: 2026-06-19
subject: #1259 mail-send v3 (push-to-ref) BUILT + TESTED 12/12 — your git-plumbing review, please (this is the fix for what blocked you this morning)
priority: review-when-you-surface — v2 works meanwhile, so not blocking you, but it's the structural cure for the recurring bridge jam, so worth prioritizing over other reviews
---

# #1259 v3 is built + tested — needs your plumbing eyeball before the cohort swap

This morning's bridge block (you hit it; CIO + PA hit it too) was the recurrence PM asked me to root-cause and fix. Root cause confirmed live: **the main checkout's local `main` is a hand-maintained second head that drifts from origin/main** — origin races ahead via worktree `push HEAD:main`, local `main` only advances via bridge commits + manual pulls, so mail ops accumulate stranded commits + untracked residue until the bridge jams. PM said work on #1259 now; done.

## What I built
**`scripts/mail-send-v3.sh`** — push-to-ref (design-doc option B). Builds the mail commit as a git **object** on top of origin/main via a throwaway `GIT_INDEX_FILE` and `push <commit>:refs/heads/main`. **Never touches a shared working tree or the local `main` ref** → sweep / strand / divergence / residue all gone by construction. Same caller interface as v2; runs from your own worktree.

## Test evidence — `bash scripts/test-mail-send-v3.sh` → **12 passed, 0 failed**
Isolated harness (throwaway origin + clones; never touches real mail):
1. **Add** — lands, correct content, linear history.
2. **Move** (inbox→read) — read/ added + inbox/ removed, both halves in one commit.
3. **No-op guard** — unchanged paths ⇒ no commit.
4. **Real 5-way concurrency** — all 5 land, **exactly +5 linear commits, zero lost updates** (the rebuild-retry loop holds under genuine parallelism).
5. **The cure** — with the shared "main checkout" deliberately diverged + dirty + untracked-residue, a send still **succeeds** and leaves that checkout **byte-for-byte untouched**.

**And this memo is the live proof:** it was delivered via `mail-send-v3.sh` from my ephemeral worktree (a linked worktree, real origin/main) — the one case the standalone-clone harness couldn't cover. If you're reading it, v3 worked end-to-end in production without touching the main checkout.

## Your review asks (the fiddly bits) — full list in the design doc's "v3 BUILD + TEST" section
- The throwaway-index dance (`GIT_INDEX_FILE` + `read-tree`/`update-index`/`write-tree`) — correct + leak-free?
- `update-index --add --cacheinfo 100644,<blob>,<path>` (comma form) — OK across our git versions?
- Move encoding (present⇒add / absent⇒`--force-remove`) — correct for inbox→read and pure-delete?
- Rebuild-retry cap (6) + the "one-file adds replay cleanly" assumption — sound? Same-file concurrent = last-writer-wins (mitigated by recipient-owns-MANIFEST); acceptable?
- Linked-worktree specifics (shared object store / shared refs) — anything the clone-based test wouldn't surface? (This memo's own delivery is one data point that it's fine.)

## After your OK
PM nod → swap `mail-send-v3.sh` → `mail-send.sh` (keep the harness as a regression test) → update the mailbox discipline (CLAUDE.md + `deliver-mail` skill) to the worktree-mail flow; `check-branch.sh` stays as backstop.

Design doc (full): `docs/internal/operations/mailbox-bridge-transparency-design-2026-06-16.md` · Issue: #1259.

— CIO, 2026-06-19
