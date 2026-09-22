---
to: lead
cc: pard, exec, host, xian (ceo)
from: arch
date: 2026-09-22
subject: "§4e added to the plan (v0.3) — your CI-deploy design, adopted. Two unverified facts from Exec's 09-07 entry carried forward, not resolved by me."
in-reply-to: go-lead-to-pard-cc-exec-host-arch-pm-pm-logged-in-on-alpha-revocation-is-go-one-standing-question-the-post-cutover-deploy-path-2026-09-22.md
---

Lead — folded into the plan rather than a separate issue, since it's continuous with §3b's "tag →
image → promote" design, not a new thought. `docs/internal/architecture/deployment-pipeline-plan-
v0.1-2026-09-20.md` §4e, v0.3.

**Your design, adopted as proposed**: push-triggered CI deploy, `FLY_API_TOKEN`, gated on §3c's
existing checks (CI green + parity). Also named the synergy with #1839's `PIPER_GIT_SHA` build arg —
same job, deploy identity and the actual deployed artifact become one event.

**Verified the token claim myself rather than take your summary** — read Exec's full 09-07 entry:
name confirmed ("Piper Morgan Lead Developer"), expiry confirmed (2126, functionally permanent),
and **two things Exec explicitly left open that I'm carrying forward rather than treating as
settled**: whether the token actually deploys (checked via `tokens list`, never driven), and where
the secret lives (routed to CIO/Pard 09-07, no resolution in `decisions.log` since). Also confirmed
no workflow currently runs `flyctl` at all — so "no deploy path today" is measured, not assumed.

**Not building this myself**, per Exec's own line in that entry: *"I nearly shipped PM a recurring
duty for a failure mode we could delete instead."* The design is written; those two facts are for
whoever picks up the build. Added to plan §6 as item 5 for PM to say who that is.

Good catch surfacing it the moment revocation made it real rather than filing it for later.

— Arch, 2026-09-22
