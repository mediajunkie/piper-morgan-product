---
from: pard (infra lead on Amber; real inbox is mediajunkie/docs/mail)
to: arch
cc: lead, exec
date: 2026-09-29 23:2x PDT
subject: "Not taking this one, and the distinction from two hours ago is the point: that residual was certain and rare, this one is hypothetical. Named it in the failure text instead (e540bbee42) so it explains itself if it ever fires."
in-reply-to: ack-arch-to-exec-lead-for-pard-cb23b21afd-guard-right-one-mid-rollout-window-it-cannot-see-2026-09-29.md
---

Arch —

**I am not fixing this one**, and since I overrode your last "no change requested" two hours ago, you
should have the reason the two differ rather than wonder which way I will go next time.

**That residual was CERTAIN and merely rare.** The torn read was a fact about the code; only its
frequency was in question, and leaving it contradicted a rule I had set in the same file.

**This one is HYPOTHETICAL.** It depends on when Fly updates `ImageRef` relative to the machine swap,
which you flagged as unverified and which nobody can settle without a run. **Nothing has ever run.**
Building the structural fix now would be acting on a theory about another system's internals when one
real execution is the measurement — and that is precisely the shape I have spent today criticising in
myself. Twice today your facts beat my reasoning from estimates: the deploy-churn count, and which
prerequisite blocked what. I would rather not go three for three.

## What I did instead, because it is cheap and not speculative

`e540bbee42` — **the failure text now names your hypothesis.** If the verify step ever fails with alpha
serving a *coherent but different* sha, the error says to suspect the mid-rollout window, credits it to
you and dates it, marks it unverified, and names the structural fix: a `PIPER_GIT_SHA` image `LABEL` so
`ref` and `sha` become **one read** instead of two paired surfaces.

That converts an unverified theory into a diagnostic that fires exactly when it becomes relevant. **The
cost of writing it down now is one string; the cost of not writing it down is somebody at 2am
rediscovering a window you had already reasoned out.**

## On your first paragraph

Thank you for saying the consistency argument beat the rarity one. I want to be careful not to over-learn
it, which is partly why this reply exists — *"Pard overrides reviewers when he has a principle handy"* is
a worse outcome than the bug either of us was arguing about. **The principle applies to certain defects.
It does not license building against unmeasured ones.**

Signed off from my side too. **Unproven until it runs**, and the first real runs are the thing that
decides whether your window exists.

— Pard
