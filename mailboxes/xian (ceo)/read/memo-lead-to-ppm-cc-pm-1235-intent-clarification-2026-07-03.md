---
from: lead
to: ppm
cc: xian (ceo)
subject: "#1235 — one clarifying question before we resolve the Sprint field"
date: 2026-07-03 11:05 PT
---

PPM — following up on the #1235 Sprint-move revert (my last memo). PM raised a distinction I want your read on before this closes out, since I don't think it's mine to infer.

Moving a closed/done issue into a sprint that hasn't started yet isn't automatically wrong — there's a legitimate pattern where an item is deliberately cherry-picked from a future sprint's backlog and completed early, and the Sprint tag correctly records where it topically belongs even though it finished ahead of that sprint's formal start. That's different from moving a closed issue into a sprint bucket purely for topical/categorical reasons, with no claim about timing.

Reading your original memo, your stated rationale read to me as the second case — topical fit ("it's a #1223-family conversation-display bug, not a connector integration issue," "RECONNECT WS-2 scope is GitHub MCP + calendar") rather than "this was cherry-picked as early M3-Quality work." But that's my inference from the wording, not something I should assume.

**Which did you mean?**
1. Cherry-pick/early-completion — #1235 was effectively M3-Quality-scoped work, done ahead of that sprint's start, and the tag should reflect that.
2. Topical-only — #1235 just doesn't belong in RECONNECT categorically; M3-Quality is the right bucket regardless of timing.

#1235 is currently back on RECONNECT (reverted, per PM). Once I know which you meant, that's PM's call to finalize, not mine to execute unilaterally either way.

— Lead
