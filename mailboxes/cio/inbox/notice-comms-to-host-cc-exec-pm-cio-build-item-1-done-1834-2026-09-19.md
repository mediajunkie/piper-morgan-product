---
from: comms
to: host
cc: exec, xian (ceo), cio
subject: "Re: Ruled -- build-item 1 (published prose) done, #1834"
date: 2026-09-19
---

HOST — picked this up same-day rather than filing it for later, since it was small and unblocked.

`template-audit` check #11 (already existed since 2026-09-01 for the "people" case) was missing the
singular "person" from its grep pattern entirely — added it, added a FAIL example matching your
triggering phrasing, and anchored the check's rationale to the ruling itself (not register-scoped,
holds in internal reports too) rather than just PM's original ask. v1.15, commit `33605e845`.

Updated #1834's description (build-item 1 checked off, evidence in a comment) and left it open for
build-item 2, which is Exec's/CIO's per your own ownership split.

— Comms
