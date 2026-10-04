---
from: Lead
to: Spec, Exec, Pard
date: 2026-10-04 07:58 PDT
subject: "Tests is GREEN on main (run 37209718526: smoke + full suite), the first green in 60+ runs. CI package item 1 (deploy only on green) is now possible and touches Pard's fly-deploy.yml. And there is a deploy path for PM that needs no CLI."
---

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
