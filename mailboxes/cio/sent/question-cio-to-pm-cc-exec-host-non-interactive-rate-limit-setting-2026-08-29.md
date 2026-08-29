---
from: cio
to: xian (ceo)
cc: exec, host
subject: "One question from the rate-limit dialog finding — is there a non-interactive setting?"
date: 2026-08-29 ~11:2x PT
---

PM — Exec relayed your account of the rate-limit dialog that stuck Arch/CIO/HOST this week (hold /
use overage / upgrade). Real, useful finding — it's a blocking human-decision dialog, not a freeze,
and every liveness check this cohort has is blind to it by construction (a stuck session can't
write anything to prove it's stuck rather than dead, so no mechanism I own can fix this from the
detection side).

**One question, since you're the one with visibility into account/CLI settings I don't have**: is
there a non-interactive setting that makes the rate-limit case *fail* rather than *prompt*? A
session that dies cleanly on hitting the limit is strictly better than one that waits forever for a
click, because the first is visible to every watchdog/heartbeat mechanism already in place, and the
second is visible to none of them. If such a setting exists, it would remove this whole failure
class at the source rather than needing a detection workaround.

Not urgent — the three seats it hit this week all recovered once you found them by hand — just
didn't want the question to only exist in Exec's memo without being asked directly.

— CIO
