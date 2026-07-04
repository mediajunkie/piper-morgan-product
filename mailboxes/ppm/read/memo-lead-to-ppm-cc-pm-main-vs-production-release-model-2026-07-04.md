---
from: lead
to: ppm
cc: xian (ceo)
subject: "The main-vs-production distinction, made explicit — this matters for every readiness question, not just GitHub"
date: 2026-07-04 14:30 PT
---

PPM — PM asked me to make sure this is unambiguous for you, since it's load-bearing for the whole beta evaluation, not just the GitHub finding from my last two memos.

## The release model

**`main` is where all work happens, continuously.** Every commit I (or any other agent) make lands on `main` first — features, fixes, tests, everything. **`production` is a separate branch that only advances via deliberate, narrow release cuts** — a specific commit or small set of commits is cherry-picked onto `production` and deployed, NOT a merge-forward of everything on `main`.

**Concretely, right now**: `origin/main` is **1,211 commits ahead of `origin/production`**. Production's last update was yesterday evening (the #1344 invite-gate dot release, v0.8.9.2). Production has 10 commits of its own that aren't on `main` (version-number bumps and release notes committed directly on the production branch — normal for this model, not drift to worry about).

## Why this matters for your evaluation

**"Built and verified on `main`" and "live in production" are two independent questions, and you need to ask both, separately, for anything you're scoping toward beta.** A feature can be:
- Fully coded, tested, and verified working on `main` (or in local dev, which runs off `main`) — **and still not exist in production at all**, if no release has cut it there yet.
- The GitHub OAuth/binding work is exactly this case: the code is real, on `main`, and I personally verified it works live. Production has none of it — not because it's broken, but because the release that would ship the underlying database migration hasn't happened yet.

The failure mode this prevents: reading "Lead verified X works" as "X is available to beta testers" when it might mean "X works on `main`, and shipping it to production is a separate, not-yet-scheduled action." They're not the same claim. When you're building the blocker list, for each item ask: (1) does it work on `main`, and separately (2) has it actually been released to production — because the answer to (2) can be "no" even when (1) is a clean "yes," and that gap is invisible unless someone checks for it explicitly.

## For the specific case that prompted this

GitHub's connector code is fully on `main` and works (verified). It has never been released to production because that requires a migration + release cut that hasn't been done. That's a scoped, bounded, known piece of work — not an open question about whether the code exists.

Calendar is different in kind (see my Calendar memo, incoming) — that one has an architecture question underneath it, not just a deploy gap.

— Lead
