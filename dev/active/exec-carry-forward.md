# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-13 ~23:20 PT at day-close.**

## Cron
Job `83258e51`, `38 6,10,14,18,22` — 5 fires/day. Armed 09-11 06:55, expires ~09-18 → **rotate ~09-16.**
⚠️ **"CronList shows one job" means a job OBJECT exists, NOT that the schedule is live** (Lead's
catch, 09-13 — their cron was armed and correct all night and fired nothing while signed out).
**Report "one job, correct expression." Never "therefore the schedule is live." The only proof a
cron fires is a fire.**

## Weekly cycle — Ship #060
Omnibus 7/7 · 10/10 reports · **internal report delivered** · **prep complete**.
🔴 **PM ruled the internal-report discussion comes BEFORE the draft. It has not happened. The draft
has not started and should not.**
Artifacts: internal report `4af428b3-ea1e-4f02-b077-c4ce146dca72` · epic accounting
`6b09674a-2d60-46c5-807d-9952951adca0` · rollup `a0d0af86-9505-4dcf-8b22-c63017251a47`.

## Blocked on PM
1. ⭐ **The ruleset decision — parks TWO roles** (Arch: scope-guard delivery; CXO: same). Repo public,
   zero rulesets, bypass-actor path free. Highest leverage.
2. **Vercel** — Web hard-blocked on access since 09-09. 14.91/10 GB deployment storage.
3. **PA** — awaiting PM's sequencing answer before building the BYOC readiness plan.
4. **The internal-report discussion** (gates the Ship).
5. ✅ **Janne Lammi's invite token is READY TO SEND** — HOST recorded the roster row, Lead minted at
   v99, status UNUSED. Nothing needed from either; it's PM's to send.

## Epic 1 — the credibility epic, and PM worked it today
✅ **PM rotated the secrets. E2E & AAXT went RED → GREEN.** Belt now: E2E, Docker, Config Validation,
Router, Code Quality all **green**; **`Tests` is the ONLY red** — 4 consecutive failures
(23:52, 00:14, 01:53, 05:06). That's the product-failure half Lead predicted under the auth errors.
**#1687 still OPEN** (close condition = its four green on a real push; Tests was never in its
denominator — that gap is #1747's whole point).
**#1747 needs diagnosis + milestone/epic triage** (PM's ask) — ⚠️ **its own snapshot is now stale:
it recorded E2E red, and E2E is green.** Half-true; the remaining half is Tests.
**#1764 / #1765 can move in parallel** — neither depends on #1687. ⚠️ #1765's premise ("Tests green
since 09-11") **has expired** — Tests is red now. Whoever diagnoses must re-establish which.

## State at close
**9 closed today (6 MVP)** incl. #1617 + #1739 (PM cleared epic 3's floor). MVP **51 not done**
(28 Sprint Backlog, 3 In Progress, 6 In Review, **14 Product Backlog**); **1,164 done**.
⚠️ **`PLUS 1 unmilestoned` — the 3-day zero streak broke at 22:38** with `#1798`. One issue, filed
minutes ago; flag to PPM, not an alarm.

## Standing corrections on me
- ⚠️ **"No conclusion" is not "no failure."** A `gh run list` returning nothing because runs were
  *cancelled* reads exactly like clean. Widen the window before reporting.
- ⚠️ **`echo` after `||` asserts nothing.** Verify pushes by re-reading `origin/main`.
- ⚠️ **`closedAt` is UTC.** Compute in Pacific and say so.
- ⚠️ **Membership is not mention** (epic counts).
- ⚠️ **Re-check an anomalous reading once before reporting** (PM's rule). Applied 6×; changed the
  reading 3 times.
