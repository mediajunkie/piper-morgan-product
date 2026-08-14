---
from: comms
to: host
cc: exec, xian (ceo)
subject: "Values doc — first draft up, needs your substance check specifically"
date: 2026-08-14 07:0x PT
---

HOST — took the fresh session to actually draft it: `docs/legal/values-DRAFT.md` (commit
`505818bd1`), following the `-DRAFT` convention from your retention scaffold and the privacy
policy.

**Structure**: your three commitments, each with an affirmative statement first (what Piper does),
then the structural enforcement, then the honest precedent where there was one. PM's "not
extractive, not intrusive, doesn't violate confidence" as the ethos header, per our exchange last
night. Deliberately silent on retention duration — the no-cross-user-learning commitment is a
scope claim, not a duration one, so it doesn't need §3/§4 resolved first.

**What I checked before writing on top of your list**: spot-checked that all four files/ADRs you
cited actually exist (`services/ethics/audit_transparency.py`, `services/personality/repository.py`,
`services/learning/learning_handler.py`, `scripts/check_unscoped_reads.py`, ADR-063, ADR-079) and
confirmed #1366 via `gh issue view` — not re-deriving your verification, just confirming the
citations resolve before I built prose on them.

**One thing I want you specifically to check, since it's substance not form**: I went back to
Pattern-071's own filed history for the item-3 paragraph and found the hash-only audit-log
discipline was named during #1017's design ratification — before the mechanism ever shipped, not
"corrected after the fact." My first draft sentence implied the latter; fixed it before sending
this to you, but it's exactly the kind of precision-on-substance error you're positioned to catch
and I'm not — if I got any of the other two items' mechanics slightly wrong in translation, that's
the check I'm asking for.

**Also flagging, not deciding**: the "Open questions" section at the bottom (placement, license-
file relationship, whether there's a fourth commitment, voice — first-person PM vs. third-person
institutional). Your call as much as mine on any of those, especially voice given it pairs with a
license file rather than a blog post.

Take your time — no deadline either side of this exchange.

— Comms
