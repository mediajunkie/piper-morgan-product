---
to: xian (ceo)
cc: exec, lead, pard, host, ppm
from: arch
date: 2026-09-20
subject: "Deployment pipeline plan v0.1 — on origin/main for your ruling. Four questions, one thing I'd take now, and a finding: we already paid for staging tooling that cannot run."
in-reply-to: tasking-exec-to-arch-cc-pm-pard-lead-host-ppm-define-a-real-deployment-pipeline-pm-top-priority-droplet-costs-money-2026-09-20.md
---

# Plan v0.1 — `docs/internal/architecture/deployment-pipeline-plan-v0.1-2026-09-20.md`

On `origin/main`. **Nothing built**, per Exec's scope note — this is the written plan you asked to
rule on. Cover note only; the plan is the artifact.

## The one-sentence diagnosis

**The build system and the release marker have been tracking different things, and nothing could
answer "what is running" without SSH — so the pipeline didn't fail, it was never observable enough
to fail loudly.**

`docker.yml` builds on **`main`**. The branch meaning "released" is **`production`**. Nothing
connects them. That's why *"I'm not sure what version is on alpha"* was an unanswerable question
rather than a lookup — and how `production` drifted ~4,195 commits without anyone's alarm going off.

## Two findings you'll want regardless of how you rule

🔴 **We have already paid for staging tooling that nothing can run.** `docker-compose.staging.yml`
and `scripts/deploy_staging.sh` exist — but **`.env.staging` does not, and neither does an
`.example`**, and the script requires it at line 12. No deploy workflow invokes any of it. So
"add staging" would be buying the same thing twice. **Present is not live** — the same shape as a
hook that looks configured and never fires.

✅ **Alpha is genuinely current, in the sense that matters.** `main` is 24 commits ahead of
`production` — but **0 of those touch product code**; they're docs and mailbox traffic, including
mine from this morning. The tag `v0.8.12.0` resolves to exactly `origin/production`. I checked that
last one specifically because an annotated tag's `rev-parse` returns the tag object, not the commit,
and reporting a mismatch that wasn't real would have been a manufactured scare.

## The one thing I'd take now, ahead of your ruling

**Expose version + git SHA on `/health`.** It already returns 200 unauthenticated. Lead had to SSH
into the container to read `/app/VERSION`.

**Every gate in the plan depends on cheaply answering "what's deployed" — a promotion gate that
can't read the current version isn't a gate.** It's small, reversible, and it turns this month's
recurring confusion into a `curl` the attention rollup can carry automatically. **Say the word and
I'll take it; I haven't, because it's code and you asked for a plan.**

## Four questions (plan §6)

1. **Vocabulary**: adopt **environment** (`local`/`staging`/`prod`) vs **stage** (alpha/beta/GA) as
   permanently separate words — and **retire the `production` branch**? Right now "alpha" is both an
   audience and a host, and "production" is both an idea and a git ref. Under the split, **opening
   beta becomes an access decision rather than a migration.**
2. **The droplet, which is your money call**: **(A)** keep it as `prod`, add staging on Fly (we
   already pay for Fly) — cost unchanged, least disruption; or **(B)** collapse onto Fly and end the
   droplet spend — real migration work, and today's deploy showed the bind-mounted `uploads/`, redis
   and chroma are exactly the sharp edges. **My lean is A now, revisit B once the pipeline is
   boring** — B's savings are real but one-time-costly, and your current pain is *not knowing what's
   deployed*, which A plus the `/health` change fixes immediately and B doesn't fix faster. ⚠️ **I
   don't have the cost numbers; you do.**
3. **May I take the `/health` version surface now?**
4. **"Unless someone tells me something more pressing"** — taking that as the invitation Exec said it
   was: **I don't think anything is.** One flag: **#1818 and #1823 are both mid-build and both touch
   first-contact experience**, so if beta opens soon they compete for the same week as this.

## What I did not do

**I did not re-derive Pard's thread.** Theirs is archaeology and immediate unblocking; mine is the
forward design. They meet at *what happens to the droplet*, which is question 2 — **Pard, flag it if
you read that seam differently.**

⚠️ **I also did not carry Exec's "alpha runs 0.8.10.14, deployed July 16" into the plan.** Lead's
report landed while the tasking was in flight and alpha is now **v0.8.12.0**, verified in-container.
Not a criticism of Exec — it's an instance of the thing the plan is about: **the deployment facts
went stale inside a few hours, and the only reason anyone noticed is that a human happened to SSH in.**

**Verified how**: every "exists" claim checked in-repo this morning — `VERSION`, tags resolved to
commits, `docker.yml`'s trigger block, `deploy_staging.sh:12`'s env dependency, and the absence of
`.env.staging` tested by file existence. Drift measured (`git rev-list --count` = 24; product-path
`git diff --name-only` = **0**). **Layer: repo state, static. Denominator: 4/4 deploy-release scripts
opened, 1/1 build workflows read, 0/3 live hosts touched** — I hold no credentials for the droplet,
Fly, or Vercel, so every claim about what is *running* is Lead's SSH read cited as theirs.

— Arch, 2026-09-20
