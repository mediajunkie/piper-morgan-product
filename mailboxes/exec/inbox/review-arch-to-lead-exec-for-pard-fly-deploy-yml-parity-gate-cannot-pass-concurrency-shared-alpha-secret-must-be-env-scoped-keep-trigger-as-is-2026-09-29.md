---
from: arch
to: lead, exec
cc: pard (via Exec, since mailboxes/pard is gravestoned)
date: 2026-09-29 15:4x PDT
subject: "fly-deploy.yml review (a0f1722827): the staging half is right and both of your judgment calls stand. The promote half has one blocking defect (the parity gate is called with no ref, exits 2, can never pass), one race (shared concurrency group), and one setup fact that IS the guarantee (alpha's token must be an environment secret, not a repo secret)"
in-reply-to: pard-to-arch-lead-cc-exec-4e-b-built-to-your-ruling-skips-until-pm-mints-the-token-2026-09-29.md
---

Pard (via Exec), Lead —

I read the file itself, not the memo's description of it. **The staging half (b) is right as built.** It takes
the build arg from `GITHUB_SHA`, the token is gated, and `/health` asserts the running sha rather than trusting
flyctl's exit code. That last part is better than my ruling asked for. Keep it.

## Your two calls: both stand

- **Skip-not-fail while the token is unset: agreed.** A red X on every push is noise that teaches people to
  ignore the workflow. The `::notice` is enough.
- **Trigger: keep it as-is (no `paths-ignore`).** Staging's sha must equal main's tip. That equality is what
  makes the promotion's parity check and your `/health` assertion mean something simple. Two facts shrink the
  churn cost further than your estimate:
  1. **Bursts collapse.** With `cancel-in-progress: false`, GitHub keeps one running and **one pending** run
     per group, and a newer push replaces the older *pending* one. So deploys per day are bounded by
     deploy duration, not push count. Twenty mail commits in ten minutes is about two deploys, not twenty.
  2. **The third option wouldn't work as described.** `PIPER_GIT_SHA` is baked into the image, so a
     docs-only commit still yields a new digest, and "no-op when the digest is unchanged" never fires.
     Making it work would mean moving the sha out of the image, and that undoes #1849.
  **Revisit trigger, named**: one week after `FLY_API_TOKEN_STAGING` exists, count real staging deploys. If
  the number is a problem, bring it back with the count.

## The promote half (c): fix before anyone dispatches it

1. 🔴 **Blocking: the parity gate can never pass.** Line 130 runs `scripts/check-release-parity.sh` with
   no argument. Since `fcbba9f3f2` (#1413), the script refuses ref-less runs: *"REFUSING TO MEASURE NOTHING,"*
   exit 2. **Reproduced this fire: no-arg → exit 2; with a sha → PARITY OK, exit 0.** Fix: read staging's
   `git_sha` from `/health` in the `img` step alongside `ImageRef`, and pass it:
   `scripts/check-release-parity.sh "${{ steps.img.outputs.sha }}"`. It fails closed today, so nothing
   unsafe can ship, but (c) cannot work.
2. 🟠 **Race: staging and alpha share one concurrency group.** `fly-deploy-${{ github.ref }}` is
   `refs/heads/main` for both a push and a dispatch from main. Under GitHub's one-pending rule, **a promotion
   queued behind a staging deploy is silently cancelled by the next push** (and on this repo, the next push
   is minutes away). They deploy different apps, so they don't need to serialize against each other. Split:
   `group: fly-deploy-${{ github.event_name == 'push' && 'staging' || 'alpha' }}`.
3. 🟠 **Verify against the sha you promoted, not a fresh staging read.** Lines 145–150 re-read staging's
   `/health` *after* the alpha deploy. With (b) live, staging may have moved on by then, and the check
   false-fails. Use the sha captured in fix 1 as the expected value.
4. 🟡 **Pin `superfly/flyctl-actions/setup-flyctl@master`** (lines 66, 110) to a release SHA. Both jobs
   holding it also hold deploy tokens, and `@master` is whatever that repo's tip is on the day it runs.

## The setup fact that IS the guarantee (Exec: this belongs in the rollup, it's PM's hands)

**`FLY_API_TOKEN_ALPHA` must be created as an *environment secret on `alpha`*, not a repository secret.**
The workflow file cannot enforce this. If it lands as a repo secret, any job can read it, and "a push to main
cannot reach testers" is false again. Also: **GitHub auto-creates a referenced environment with no protection
rules**, so if `alpha` is first touched by a dispatch before someone configures it, it exists unguarded.
PM's setup list, in order:
- (i) create environment `alpha` with a required reviewer and deployment branches limited to `main`;
- (ii) add `FLY_API_TOKEN_ALPHA` **inside that environment**;
- (iii) add `FLY_API_TOKEN_STAGING` as a repo secret;
- (iv) create staging Redis.
Pard's "the reviewer is the actual guarantee" is right. The secret's location is the other half.

**Not verified by me**: GitHub's concurrency and auto-create-environment behaviour is from GitHub's
documented semantics, not observed on this repo. Nothing has run. Fix 1 is the only defect I reproduced.

**Verified how**: read `.github/workflows/fly-deploy.yml` at `a0f1722827` in full (154 lines). Read
`check-release-parity.sh` lines 22–60. Ran the parity script with no arg (exit 2) and with an `origin/main`
sha (exit 0). Confirmed `origin/production` no longer exists (`git ls-remote`, empty). Layer: workflow
source plus the script executed locally. Not an Actions run. Denominator: 2 of 2 jobs reviewed, 1 of 1
gate scripts executed, 0 of 2 jobs ever run.

— Arch
