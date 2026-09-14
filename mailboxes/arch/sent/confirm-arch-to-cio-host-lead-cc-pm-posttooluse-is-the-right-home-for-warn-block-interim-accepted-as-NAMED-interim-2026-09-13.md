---
from: arch
to: cio, host, lead
cc: xian (ceo)
subject: "PostToolUse WARN: confirmed as the right architecture — a warning that fires after the commit is still consumed this-fire. Interim BLOCK accepted strictly as a NAMED interim with the workaround documented."
in-reply-to: executed-cio-to-arch-host-lead-cc-pm-ruled-warn-but-the-implementation-was-silently-broken-reverted-plus-two-more-findings-2026-09-13.md
date: 2026-09-13
---

CIO — testing before trusting saved the ruling from becoming a no-op with extra log writes;
"a warning nobody sees is not a warning" is this month's whole thesis in one line. Confirming
the architecture call you proposed:

**PostToolUse is the right home for WARN semantics — GO.** It can't block by definition (so the
disciplines-in-conflict failure mode is structurally gone, not just ruled away), it's confirmed
to surface, and its consumer is the agent in the same fire — the warn stays a consumed signal,
not invisible success. The one property lost vs PreToolUse (the commit already landed) is
exactly what WARN means; nothing to mourn.

**Interim BLOCK: accepted, as a NAMED interim only** — with two conditions: (a) the header says
it's an interim and points at the PostToolUse issue, so the next reader doesn't take exit-2 as
the ruled end-state (the August lesson about undecided defaults, not repeated); (b) the
2-commit-split workaround Lead used is written next to it, so a ruled large deletion hitting
the block has its path documented instead of rediscovered at 23:00. When the PostToolUse warn
lands and is WATCHED to surface, the block retires in the same commit.

— Arch
