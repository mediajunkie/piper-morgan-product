# GitHub Actions: Workarounds for a Run Stuck in `queued` for 12 Days

Research compiled 2026-05-27 for stuck Tests workflow run #25923061467 on `mediajunkie/piper-morgan-product`.

## TL;DR — the most promising workaround to try first

**Disable GitHub Actions at repo settings level, wait ~30–60 seconds, then re-enable.** Multiple community threads and a March 2026 DevOpsil article report this is the strongest "kill from above" tactic that does not require GitHub Support: `Settings → Actions → General → toggle Actions off, save, toggle back on`. The toggle clears the queued state at the repo level because GitHub treats it as a re-initialization of the Actions surface for that repo. This is the only non-API path that has any reported success against a run that already returns HTTP 500 on both `cancel` and `force-cancel`.

If that fails, the second-best self-serve move is an **empty commit to `main`** (`git commit --allow-empty -m "retrigger" && git push`). Multiple users in Discussion #147604 confirm this "wakes up" the scheduler and either unsticks the queue or at least drops the stuck run as a side effect of resynchronizing the workflow definition. This is also the documented fix for the *separate* scheduled-workflow drop symptom.

Everything beyond those two requires either a destructive repo operation (archive) or GitHub Support intervention. The 500 errors on `cancel`/`force-cancel` are a known infrastructure-level failure that only GitHub can clear from the backend.

## Ranked workarounds (1-5) with citations and risk assessment

### 1. Disable/re-enable Actions at repo Settings level — LOW RISK, BEST FIRST TRY

`Settings → Actions → General → "Disable actions" → Save → toggle back to "Allow all actions"`. Reported to clear queued state for the repo. DevOpsil article (March 2026) calls this out explicitly, and search results across multiple community threads cite the same recipe. **Risk**: brief window where no workflows can run for the repo. Side effect: may force pending Pages deployments to redeploy. Reversible in seconds.

### 2. Empty commit to default branch — LOW RISK, GOOD SECOND TRY

`git commit --allow-empty -m "retrigger workflows" && git push`. Confirmed working by multiple users in Discussion #147604 ("I created another PR and merged it and now my workflows are running again"). Also the GitHub-staff-recommended fix for the *related* scheduled-workflow throttle-drop symptom — which we are almost certainly also experiencing given the May 13 simultaneous drop of all six scheduled workflows. **Risk**: none. Generates one trivial commit.

### 3. Delete (`git rm`) the workflow file `.github/workflows/tests.yml`, commit, push — MEDIUM RISK, UNDOCUMENTED

GitHub docs do not state what happens to queued runs of a workflow whose definition file is removed from the default branch. No community thread surfaced a confirmed report of this working. Theoretical mechanism: the orchestrator may garbage-collect runs whose workflow no longer exists. **Risk**: medium-low — easily reversible (`git revert`), but if it doesn't work you've created an extra commit cycle. Worth trying *after* #1 and #2 fail. If you try this, restore the file in the same PR/branch so you don't leave the test suite undefined.

### 4. Force-cancel via `gh` CLI rather than raw API — LOW RISK, ALREADY LIKELY EXHAUSTED

`gh api -X POST /repos/mediajunkie/piper-morgan-product/actions/runs/25923061467/force-cancel`. Same endpoint as raw `curl`, but `gh` sometimes injects different headers and goes through a different rate-limiting bucket. Worth one re-attempt with `gh` specifically if not already tried that way. **Risk**: none. **Likelihood of success given prior 500s**: very low — the 500 is from the backend, not the wrapper.

### 5. Repository archive → unarchive — HIGH RISK, LAST RESORT BEFORE SUPPORT

Discussion #68327 documents that archiving can leave runs stuck *worse* than before, and unarchiving doesn't reliably clear them. Archiving also makes the repo read-only mid-operation, which interferes with other agent work. **Risk**: high — disruptive, slow to reverse, may worsen the symptom. **Recommendation**: do not do this; open a Support ticket instead.

## Likely root cause of the throttling-suppression

The repo is showing two correlated symptoms that almost certainly share a cause:

1. Scheduled workflows simultaneously stopped firing on 2026-05-13 (six workflows at once)
2. A specific run from 2026-05-15 is stuck in `queued` and uncancellable

GitHub documents that **"scheduled events can be delayed during periods of high loads of GitHub Actions workflow runs, and if the load is sufficiently high, some queued jobs may be dropped"** (Troubleshooting workflows docs). Multiple community threads in early-to-mid 2026 reference a server-side change that was rolled back, with GitHub staff stating *"any commit pushed to the default branch will resync the impacted scheduled workflows."*

The most consistent explanation: the repo's workflow-state cache on GitHub's side got into a wedged state, possibly from a May 13 platform-wide rollout. The scheduler stopped delivering `schedule` events to this repo, and one push-triggered run from May 15 landed in the queue before the orchestrator could pick it up — and now neither the scheduler nor the cancel path can act on it because both touch the same wedged state.

This is consistent with the 500s: a 500 from GitHub's API on a normally-idempotent operation almost always means a backend service in an unrecoverable state for a given resource. The DELETE returning 403 (not 500) on a non-terminal run is *expected* behavior per GitHub docs (you can only delete `completed` runs), not a permission issue — adding the `workflow` scope didn't help because the rule is state-based, not scope-based.

## What to tell GitHub Support if a ticket is needed anyway

Suggested ticket body:

> **Repo**: `mediajunkie/piper-morgan-product`
> **Stuck run**: ID `25923061467` (Tests workflow, `queued` since 2026-05-15T14:23Z, 12 days)
> **API attempts**: `POST /actions/runs/25923061467/cancel` → 500. `POST /actions/runs/25923061467/force-cancel` → 500. `DELETE /actions/runs/25923061467` → 403 (expected: run is non-terminal).
> **Correlated symptom**: all six scheduled workflows on this repo simultaneously stopped firing on 2026-05-13 and have not resumed. Suggests repo-level scheduler state is wedged.
> **Self-serve attempts**: disable/re-enable Actions, empty commit, workflow-file delete — please confirm before we escalate further.
> **Ask**: clear stuck run `25923061467` from backend queue + restore `schedule` event delivery for this repo.

Reference Discussions #143045, #196717, #196720 as prior cases of the same symptom pattern.

## Citations

- [GitHub Community Discussion #143045 — Confirmed Incident: workflows stuck in queued](https://github.com/orgs/community/discussions/143045)
- [GitHub Community Discussion #196717 — Actions/Pages stuck and cannot be cancelled](https://github.com/orgs/community/discussions/196717)
- [GitHub Community Discussion #196720 — force-cancel returns HTTP 500](https://github.com/orgs/community/discussions/196720)
- [GitHub Community Discussion #147604 — Why is my workflow stuck in queued state](https://github.com/orgs/community/discussions/147604) (empty-commit workaround confirmed by multiple users)
- [GitHub Community Discussion #51458 — Action stuck queued 24h+](https://github.com/orgs/community/discussions/51458) (new PR merge as workaround)
- [GitHub Community Discussion #176347 — Stuck workflow runs, unable to cancel](https://github.com/orgs/community/discussions/176347)
- [GitHub Community Discussion #159946 — Stuck "Queued" but CLI/API say "Completed"](https://github.com/orgs/community/discussions/159946)
- [GitHub Community Discussion #68327 — Cancel workflows before archiving](https://github.com/orgs/community/discussions/68327)
- [GitHub Community Discussion #185373 — Scheduled workflows not firing (private repo)](https://github.com/orgs/community/discussions/185373) (GitHub staff: push to default branch resyncs)
- [actions/runner Issue #3872 — workflow stuck queued, cannot be cancelled](https://github.com/actions/runner/issues/3872)
- [GitHub Docs — Troubleshooting workflows](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows) (scheduled-event-drop under high load)
- [GitHub Docs — Deleting a workflow run](https://docs.github.com/en/actions/managing-workflow-runs/deleting-a-workflow-run) (only `completed` runs deletable)
- [DevOpsil — Fix GitHub Actions Workflow Stuck in Queued (2026-03-30)](https://devopsil.com/articles/2026-03-30-github-actions-workflow-stuck-queued-fix) (disable/re-enable + empty-commit recipe)
- [DEV Community — Unfreezing Your GitHub Actions](https://dev.to/devactivity/unfreezing-your-github-actions-troubleshooting-stuck-deployments-and-protecting-your-git-repo-2adh)
- [DevActivity — Cron Delays Community Insight](https://devactivity.com/insights/github-actions-cron-delays-a-community-insight-into-engineering-workflow-scheduling/)
