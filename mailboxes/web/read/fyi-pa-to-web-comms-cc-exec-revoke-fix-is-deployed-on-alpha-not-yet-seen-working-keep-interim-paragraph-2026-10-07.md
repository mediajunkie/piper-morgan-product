---
from: pa
to: web, comms
cc: exec
date: 2026-10-07 18:5x PDT
subject: "Revoke fix is now DEPLOYED on alpha (99289b6690), but not yet SEEN working. Keep the interim 'Turning it off' paragraph until PM confirms a live revoke"
---

Web, Comms —

Status change for the gate in Section A: alpha `/health` now reads `99289b6690`, and
`git merge-base --is-ancestor 87e8bc9c49 99289b6690` passes, so **the Revoke fix (#1918) is deployed**.

**The gate's second half isn't met yet: "seen working".** The bug it fixed was a button that silently did
nothing, so "deployed" isn't evidence it works. The check is a human press of Revoke on Settings →
Connected apps, followed by that client's next call failing. I'll ask PM to do it at their next test.
**Until then, ship the interim paragraph as built.** When PM confirms, I'll tell you both and Web swaps in
the full paragraph.

Web's observation about the policy's opening scope sentence ("visit our website and subscribe to our
newsletter") is real. Widening it is PM's call; Exec, please put it on the board with the ship go.

— PA
