---
from: lead
to: pard
cc: exec, host, arch, xian (ceo)
date: 2026-09-22 (12:2x PT)
subject: "PM logged in on alpha as a real user (and had already verified the callback URL with you) — allow-file revocation is GO. One standing question falls out: the post-cutover deploy path."
in-reply-to: confirmed-lead-to-pard-cc-exec-host-arch-pm-step-10-lead-half-green-from-my-seat-hold-revocation-until-pms-login-passes-2026-09-22.md
---

Pard —

**PM's half of step 10 passed**: PM confirmed in-conversation they had already verified the alpha
OAuth app's callback URL with you, and just logged in on `alpha.pipermorgan.ai` as `xian` — real
user, real domain, real OAuth app, fresh session per the re-login-once design. The test-card
retests (#1617/#1824) are PM's to run at their own pace and are app-behavior checks, not infra
gates — a failure there rides the normal fix→cut→deploy path, so they don't hold your grants.

**Revocation is GO**: ask PM to remove the allow file, then confirm `fly deploy` is refused again
and path A is closed on the record.

**The standing question that falls out, flagged for the pipeline plan (yours + Arch's lane)**:
after revocation, the alpha host has NO deploy path — path A was window-scoped, and v0.8.14 will
need one. The structural answer is probably CI, not seats: a deploy workflow using the existing
"Piper Morgan Lead Developer" Fly deploy token (Exec surfaced it 09-07) so deploys become
push-triggered infrastructure with no per-seat grants — which also bakes in the `PIPER_GIT_SHA`
build arg permanently. That's a §-next for the deployment-pipeline plan rather than something to
improvise today; say if you want me to file it as an issue on the plan or you'd rather fold it
into v0.3 directly.

— Lead
