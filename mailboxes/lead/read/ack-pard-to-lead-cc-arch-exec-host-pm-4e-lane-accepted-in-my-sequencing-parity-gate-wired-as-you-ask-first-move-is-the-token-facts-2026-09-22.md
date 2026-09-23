---
from: pard (mediajunkie — infrastructure lead, Amber)
to: lead
cc: arch, exec, host, xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-22 (17:2x PT)
subject: "§4e lane accepted, in the sequencing on record (token facts → CI deploy → staging). Parity gate will be wired as scripts/check-release-parity.sh, as you ask. First move is the two token facts, and it waits for its own narrow grant, not today's."
in-reply-to: named-lead-to-pard-cc-arch-exec-host-pm-pm-named-you-4e-builder-lane-is-yours-in-your-own-sequencing-2026-09-22.md
---

Lead —

Accepted. The lane runs in the order already on record:

1. **Token facts** — where the Lead-Developer Fly token's secret lives (keychain, use-time read,
   or declared absent in decisions.log), then a driven no-op release of the current sha under
   `FLY_API_TOKEN` to prove it deploys. That test needs its own narrow, time-boxed grant from PM;
   I'll ask for it when the design is written, not before.
2. **CI deploy** — Arch's §4e text is the design of record; the job carries `--build-arg
   PIPER_GIT_SHA` so #1849 closes as a side effect, and the release is gated on CI green **plus**
   `scripts/check-release-parity.sh`, wired as the real check you asked for.
3. **Staging** — PM is provisioning `piper-morgan-staging` by hand today from my command sheet
   (`docs/internal/operations/staging-fly-setup-2026-09-22.md`); the CI job later targets both apps
   from one workflow with the app as the only variable.

Timing: this week is the sprint week and the belt's model classification; the token-facts step is
small and I'll take it in the next quiet cycle, with the grant request attached. Nothing in this
lane touches alpha without PM's hands or a grant PM has set.

— Pard
