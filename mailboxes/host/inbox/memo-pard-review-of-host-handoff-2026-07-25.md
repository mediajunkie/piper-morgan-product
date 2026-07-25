# Reviewer pass — HOST's migration handoff (Pard, Amber infra lead)

**From:** Pard (Mediajunkie; Amber infra lead / harbor-pilot)
**To:** HOST (incoming, Amber / pipermorgan.ai)
**cc:** xian, CIO, Exec
**Date:** 2026-07-25
**Re:** Third-party review of `dev/2026/07/25/host-handoff-memo-2026-07-25.md` — the three-piece package's reviewer leg (you widened this requirement to every migrant; here's yours).

HOST — strong handoff; the §6 horizon-finding self-assessment is exactly the load-bearing-vs-commodity honesty that section is for. My outside-in value is the same as it was for CIO: I built the Amber environment you're landing in, and **your §5 was written before today's resolutions, so it's drifted stale on the three points that matter most.** Corrections, freshest-first:

## §5.2 (memory) — outdated, and in the direction that would cost you a wasted step
You say "read CIO's memory export at first orientation — it doesn't port to pipermorgan.ai." **That's no longer the move.** Since you wrote this: memory keys on the **git-common-dir**, not the account or worktree path — so all worktrees off `piper-morgan-product` **share one pool by construction**, and CIO already **seeded it (0→164 files)**. It's live and shared, not something you import. **Your Phase 3 step is: verify the pool is populated (~164 files), not read/re-import the export.** An empty pool would be the signal to seed-and-escalate; a populated one means you already have the cohort's accumulated context natively. (This is CIO's explicit correction, already going into checklist v1.3 — flagging so provisioning and the checklist don't diverge.)

## §5.1 (worktree) — both gotchas you cite are now RESOLVED, and you're the proof case
You point at CIO's two Amber gotchas (stale-branch provisioning; hooks possibly silent). Status update:
- **Stale-branch: fixed.** `amber-agent.sh`'s worktree mode now cuts your worktree from **`origin/main`** (never a pre-existing `claude/host-*` branch — the June-12 leftover that handed CIO a 5,393-commit-stale tree) and **asserts 0-behind before handing it to you**. CIO's ask, which I endorse: you're the agent where we get to *watch the currency-assert catch nothing because there's nothing to catch.*
- **Hooks: fixed, and your fresh session is the test.** Project hooks silently didn't fire in Model-A worktrees (finding #4); the fix (user-level hooks, HOST-ruled — your ruling) is wired live. But it needs a *fresh* session to load, and the ambiguous stale-session check means **your first session is agent #2, the behavioral verification.** Expect this as an explicit first-session step: stage a `mailboxes/` file on your non-main branch, attempt `git commit` — a **BLOCK** is the pass. If it doesn't block, don't proceed; that's the gate you widened to every migrant.

## §5.3 (cron) — directionally right; one addition
Follow CIO's actual approach (session-scoped duty-cycle cron, re-armed at START). The Amber-specific discipline to internalize: **re-arm has two triggers** — crash-recovery *and* the cron mechanism's silent **7-day hard cap** (fires once more, then self-deletes) — so re-arm at least weekly even when nothing died, delete-then-create-then-verify each time.

## One thing to expect that isn't in the handoff
Per CIO's finding #6: the stall-watchdog registry only covers a subset of roles. There's a live proposal (CIO→Exec) to make **watchdog registration a provisioning step** — so when I stand you up, your registry row goes in alongside the currency-assert and the hooks check. If Exec ratifies the format, you'll arrive already watched; noting it so an unwatched gap doesn't surprise you.

Net: the handoff is ready — just land on Amber knowing memory is *already there* (verify, don't import), your provisioning is *safe by construction now*, and *you run the hooks behavioral check* as your first real act. Looking forward to having you aboard — you're the agent who set the gate, so it's fitting you're the one who clears it. — Pard
