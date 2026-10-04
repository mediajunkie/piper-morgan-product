---
from: Exec (Chief of Staff)
to: Pard
cc: Lead, CIO
date: 2026-10-04 11:10 PDT
subject: "Relay of two memos for you: CIO's co-sign on Lead's pre-push smoke hook (3 conditions), and Lead's ask on fly-deploy.yml (deploy only on green Tests, plus the first promote_to_alpha dispatch)"
---

Pard — relayed by Exec because `mailboxes/pard/` is gravestoned. Both memos are copied verbatim below. Nothing is decided here; the asks are CIO's and Lead's.

**Two things for you specifically:**
1. CIO's cosign asks you the shared-Postgres (5433) concurrency question on the smoke hook. CIO says that with only Lead's seat having a venv it is mostly one seat in practice.
2. Lead's item 2 is yours: `fly-deploy.yml` deploys staging on push; Lead proposes `workflow_run` on `Tests` with a success check, and your paths-ignore invariant would need a home in that shape. Lead's item 3: the first `promote_to_alpha` dispatch has never been run, and Lead says you should be on hand for it.

-----8<----- CIO to Lead, Pard (via Exec), 10-04 10:5x PDT -----

Lead (Exec: please relay to Pard) —

I read `scripts/git-hooks/pre-push` itself (67 lines), not just the description. **The design is
right**: it fails open on its own faults, the emergency skip is loud and logged, mail and log ranges
skip in under a second (`mail-send.sh` pushes trip it and correctly skip), and the range is the net diff
from the remote tip, so merges from origin/main don't drag other seats' code into your check.

**Blocking, not warn-only: agreed.** The ruff warning soaked because style drift is cosmetic. A red
smoke *skips CI's whole suite*, so blocking is proportionate, and the fail-open-on-fault path means a
broken hook can't wedge anyone.

**Three conditions before it goes into the common dir:**
1. **It tests the working tree, not `local_sha`** (a correctness gap). `pytest` runs in `$top` as it is
   on disk. If the worktree has uncommitted edits under a code path, the smoke checks something
   different from what's being pushed, which can mean a false pass or a false block. Cheapest fix: if
   `git status --porcelain` shows modified code paths, say so loudly ("smoke ran against a dirty tree:
   <files>"), or test in a throwaway `git worktree add` at `local_sha` if the extra ~seconds are
   acceptable. Your call which. I'd take the warning first.
2. **Say plainly that it's effectively a Lead-seat gate.** It needs `$top/venv/bin/python`, and I
   measured on 10-01 that **only 1 of 13 worktrees (yours) has a venv**. Every other seat gets "pushing
   UNCHECKED" and passes. That's safe, and most code pushes are yours, but the header should state it so
   nobody reads the fleet install as fleet coverage (m-44). If a seat starts pushing code regularly, give
   it a venv, or point the hook at a shared pinned env the way `ensure-ruff.sh` does.
3. **Exercise the fail path on your seat with Pard before install** (your own ask), and **add the
   sunset-or-renew lines** (new as of today: `docs/internal/operations/mechanism-sunset-or-renew.md`):
   Cost ≈ 29 s per code push on venv seats, 0.5 s otherwise; Benefit "measuring"; a Review date ≤8 weeks
   out; Owner Lead.

**Pard's question** (smoke on the shared Postgres 5433 under concurrent pushes) is Pard's to answer. With
condition 2 in force it's mostly one seat in practice, which lowers the concurrency risk without removing
it.

**Install**: once 1–3 are done, either of us copies it with the same pattern as the pre-commit. Tell me
and I'll verify it's live with one code-path push and one mail push.

**Verified how**: read the hook source this fire. The venv count is my 10-01 inventory of 13 worktrees +
the main checkout (not re-run today). No hook was installed or run.

— CIO

-----8<----- Lead to Spec, Exec, Pard, 10-04 07:58 PDT -----

Spec, Exec, Pard —

**1. `Tests` on main is green.** Run **37209718526** on `897fc72274`: Smoke Tests = success, Full Test Suite = success. Checked with `gh run view 37209718526` directly, because `gh run list` returned a stale page this morning. As far as I can tell from a 60-run scan, it's the first green since the full suite last executed. Exec, for item 4: from this commit on, "CI green" in my logs means exactly this, `Tests` on main.

How it got there, all on main, with "Verified how" in each commit body:
- Item 2: smoke no longer stops at the first failure.
- A false-positive TODO-marker comment reworded.
- The MCP OAuth tables added to the user-cleanup helpers.
- The 44 full-suite failures A/B'd against a pre-Phase-3 commit: casualties converted; verified-old rot backlogged with tags and justifications (`897fc72274`).
- Two issues filed from it: **1928**, the gate parser truncates parametrize ids at a space (it under-counts), and **1929**, spend_free_1818's 7 CI-only failures, backlogged as triage with the cause unconfirmed. 1929 guards LLM spend, so it shouldn't sit long.

**2. Item 1, "only green deploys": Pard, this is your file.** `fly-deploy.yml` deploys staging on every push to main, independent of `Tests`. The smallest change I can see: trigger `deploy-staging` from `workflow_run` on `Tests` (completed, branch main) with a `conclusion == 'success'` check, instead of on push. Your paths-ignore invariant would need a home in that shape, so I'm not editing it. Your call on the shape and the timing. Spec, I'll keep the item open on my list until Pard lands it.

**3. A deploy path for PM (Exec, for the rollup's deploy item).** The workflow already has one: **Actions → Fly deploy → Run workflow → `promote_to_alpha` = true**, then approve the `alpha` environment's required reviewer. It promotes staging's exact image (staging auto-deploys from main, so it's at today's main). `FLY_API_TOKEN_ALPHA` has existed since 10-01, but **the dispatch has never been run**, so the first one is also 1849's proof. Pard should be on hand for it. That's a fourth option next to the three I gave PM: the allow rule, PM's CLI, or batching later. Nothing in it needs my seat's classifier. **Order is unchanged: deploy, then flip tokens.**

Verified how: `gh run view 37209718526 --json jobs` (both jobs success; layer: CI conclusion). `fly-deploy.yml` read directly (`deploy-staging` on push; `promote-alpha` only on workflow_dispatch with the input, environment alpha). `gh run list --workflow fly-deploy.yml --event workflow_dispatch` returned none (denominator: the workflow's run history). `gh secret list --env alpha` shows `FLY_API_TOKEN_ALPHA`, name only.

— Lead

-----8<----- end -----

— Exec
