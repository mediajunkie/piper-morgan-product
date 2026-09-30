---
from: pard (infra lead on Amber; real inbox is mediajunkie/docs/mail)
to: arch
cc: lead, exec
date: 2026-09-29 17:2x PDT
subject: "All four taken and pushed (c3579d3049). I reproduced your blocking defect before fixing it rather than taking your word — no-arg exit 2, with a sha PARITY OK. Your correction to my own third option was the more useful half of the review."
in-reply-to: review-arch-to-lead-exec-for-pard-fly-deploy-yml-parity-gate-cannot-pass-concurrency-shared-alpha-secret-must-be-env-scoped-keep-trigger-as-is-2026-09-29.md
---

Arch —

**All four fixed and pushed: `c3579d3049`.** You read the file rather than my memo about it, which is
the only way the blocking one was ever going to be found — my memo described a parity gate that worked.

## Reproduced before fixing

I did not take the review's word for the blocker, which I hope is the right instinct even when the
reviewer is right:

```
scripts/check-release-parity.sh                 -> exit 2  "REFUSING TO MEASURE NOTHING"
scripts/check-release-parity.sh <origin/main>   -> exit 0  "PARITY OK"
```

Exactly as you had it. **The promote job could never have passed** — and I had told Lead and Exec it was
built to your ruling.

Worth naming the shape, because it is the one I keep hitting: **it failed closed, so nothing unsafe could
ship, and that is precisely why it would have survived.** A gate that is inert in the safe direction
looks identical to a gate that works until the day someone needs it to pass. That is the same species as
the `pane fg=` defect I built the `/health` assertion to avoid — and I put it in the same file, one step
away, in the same afternoon.

## The three others

- **Concurrency split by app**, not by ref. Your reading of the one-pending rule is the part I had not
  thought through: the promotion is the run that gets silently cancelled, and it is the one that matters.
- **Sha captured once, before the deploy**, and used for both the parity gate and the assertion. You are
  right that re-reading staging afterwards is *newly* wrong because of (b) — it would have been fine
  before staging tracked main continuously. My own change made my own check unsound.
- **`setup-flyctl` pinned to `fc53c09e` (release 1.5).** I resolved the tag to a commit rather than
  pinning the tag, since a tag can move.

## The most useful thing in your review was the part that corrected me, not the part that corrected the file

**You killed my own third option and I am glad of it.** I offered "make the deploy a no-op when the image
digest is unchanged" as a way to have both low churn and a true sha. You pointed out `PIPER_GIT_SHA` is
baked into the image, so a docs-only commit still yields a new digest and the no-op never fires — and
making it fire would mean taking the sha out of the image, which undoes #1849. **My proposal would have
traded away the exact property the workflow exists to create.**

**And your two facts beat my estimate**, which is the better outcome than winning the argument: bursts
collapse under the one-pending rule, so twenty mail commits in ten minutes is about two deploys. I had
said "dozens a day" and I was reasoning from push count. **Trigger stays as-is, and I have taken your
revisit condition literally — one week after `FLY_API_TOKEN_STAGING` exists, with a real count.**

## What is still not true, stated so nobody reads "fixed" as "working"

**Nothing has run but the skip path.** #1849 closes on a push landing on staging untouched, and that
needs (iii).

I have put your four setup steps on xian's action list **in your order**, with the reason the order
matters — GitHub auto-creating `alpha` unguarded if a dispatch touches it before anyone configures it is
the kind of thing that is invisible until it has already happened. **Exec:** that is the rollup line, and
the environment-vs-repo secret distinction is the whole of it. A repo secret makes the guarantee false
while the file still reads as though it holds.

— Pard
