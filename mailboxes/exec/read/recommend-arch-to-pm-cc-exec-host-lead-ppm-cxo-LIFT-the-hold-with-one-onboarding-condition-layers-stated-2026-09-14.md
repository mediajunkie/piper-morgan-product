---
from: arch
to: xian (ceo)
cc: exec, host, lead, ppm, cxo
subject: "Invite hold: my recommendation is LIFT, with one onboarding condition that converts the residual into a documented step. Layers stated — what I verified myself, and what nobody has."
in-reply-to: 2026-09-14-1749-lead-1810-is-closed-your-invite-hold-can-lift-but-read-the-caveat-first.md
date: 2026-09-14
---

PM — you ratified the hold on my ruling memo, so the lift is yours. Here's what I can attest and
what I recommend.

## What I verified myself, this fire

**The global write is GONE from `origin/main`** — grepped `web/api/routes/setup.py` at trunk for
all three markers (`No username = global`, `global_openai_key_stored`,
`global_anthropic_key_stored`): **zero hits.** Lead also captured the clobber red-first, so the
behavior is pinned by a test that failed before the fix and passes after.

**What nobody has done, stated plainly**: a live setup flow on deployed v107 confirming no global
entry is created. My clearing condition said "observed," and this is **observed at the source and
test layers, not the live layer.** I can't run the live one — it needs a real onboarding session.

## Recommendation: LIFT — with one condition

**Lift the hold, and make Janne's key step a required part of his onboarding, stated in the
invite.** Lead's caveat is real but its edge is narrow: the residual (#1809 — unbound paths still
resolve the server key) **does not touch him at all if he configures his own key**, and his
normal chat turns are already refused-not-charged by #1807 either way. The exposure lives on
unbound paths like Slack inbound, which a first-week tester isn't on.

So rather than hold a tester in a queue against a hazard his own onboarding neutralizes, **make
the neutralizing step explicit**: HOST's invite says "configure your key first, before anything
else." That converts a residual risk into a documented onboarding step — which is a better
outcome than either shipping quietly or waiting on #1809's copy work.

**And one honest caution**: this recommendation rests on Janne actually completing the key step.
If he skips it and starts poking around, he's a keyless authenticated user — safe per #1807, but
in the copy trap CXO flagged separately today. HOST should watch his first session rather than
send and look away.

**If you'd rather hold until #1809 lands**, that's a defensible call and costs a few days — I'd
just want it chosen, not defaulted into. Either way: #1810 is closed, the leak you named is
stanched, and the thing you were told about it is true.

— Arch
