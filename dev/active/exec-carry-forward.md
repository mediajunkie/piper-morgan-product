# Exec (Chief of Staff) — carry-forward

**Rewritten 2026-09-10 ~21:15 PT at day-close.**

## Cron
Job `52fb898d`, `32 8,20 * * *`, armed 09-07 21:03, expires ~09-14 → **rotate at a 09-12 fire**
(window opens then; several fires available, no urgency).
⚠️ **PENDING PM RULING: my cadence is 2 fires/day while every other role runs 6.** I am silent
09:05→20:32 by construction and the belt flags me BELT-INVISIBLE for it. PM saw the gap and asked
about it; I proposed 6× and PM has not ruled. **Do not change unilaterally.**

## Blocked on PM — three, all verified live 09-10
1. **Vercel dashboard access.** Web is hard-blocked: no CLI, no token, no dashboard. Repo has **no
   `vercel.json` and no `.vercel` dir** — the integration is account-side and deploys on GitHub
   push, which is why Web can deploy and cannot see billing. **Nothing changed; there was never a
   credential.** PM options given: read the dashboard themselves · invite Web as Viewer · read-only
   token via `KeychainService` (`_api_key` suffix trap).
2. **Bot path onto protected main.** Verified config: required PR reviews ON, **bypass allowances
   NONE SET**, enforce_admins OFF (which is why PM's pushes work and the bot's don't). Fix: add
   `github-actions[bot]` to the bypass allowlist. Settings → Branches → `main` rule.
3. **Flywheel v3 ratification.** Text published as artifact for PM
   (`dev/active/flywheel-v3-layer2-text-2026-09-10.md` — published Arch's actual text, not a
   re-presentation). Reports itself complete, no open slots. **On ratification the workstream
   CLOSES.**
- **Q5 also unruled** (verified: 0 matches in decisions.log). HOST advises ruling after the intake
  step has mileage. v3 has a slot for either answer.

## PM's testing queue
**7 In Review**, round prepped: `dev/active/in-review-test-round-2026-09-10.html` — 2 conversations,
~12 min. **#1617, #1651, #1632 PM failed live 09-09**; Lead shipped fixes, so they are real re-runs.

## Trajectory
**17 MVP closed in 3 days** (4 Mon · 9 Tue · 4 Thu) vs 7–11 per WEEK during the collapse.
MVP 45 not done (35 Sprint Backlog, 3 In Progress, 7 In Review); 1,133 done; zero unmilestoned.
⭐ **The cause-factoring proved itself**: 3 of today's 4 closes (#1631/#1650/#1694) are ONE contract
— the convergence flagged 09-09 morning. The grouping predicted which items share a fix.

## Awaiting others
Web (Vercel, blocked on PM) · Arch/CIO (scope-guard delivery, blocked on PM) · Lead (carry-forward
refresh — flagged 09-10; their session log is excellent) · PPM/Arch (epic order in use).

## Standing corrections on me
- ⚠️ **`closedAt` is UTC.** Evening-Pacific closes land next-day. Every closure figure must be
  computed in Pacific — this inflated one figure and double-counted another this week.
- ⚠️ **Killed my own In-Progress watchdog proposal**: 9 issues closed Sprint Backlog → Done without
  touching the column. Replacement: days-since-last-closure + backlog trend.
- ⚠️ **Verify at the layer where the thing happens, not where the schema says it should.**
- ⚠️ **Ask once is not ask.** A question unanswered is not answered.
