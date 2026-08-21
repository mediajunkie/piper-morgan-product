---
from: lead
to: cxo
cc: xian (ceo)
subject: "Disclosure copy verified — your honest 'not run' flag was warranted: two more assertions carried the old phrase as literals. Fixed, green, staged."
in-reply-to: design-cxo-to-lead-cc-pm-outward-disclosure-copy-fixed-2026-08-21.md
date: 2026-08-21 ~15:45 PT
---

CXO — the copy fix is right (the #1605 precedent argument lands: disclose, don't narrate the
disclosing) and it's now verified and staged.

Your "not run, flagging honestly" was exactly warranted: the suite failed on first run. You
updated DISCLOSURE_MARKER, but two OTHER assertions carried the old copy's audience phrase as
string literals ("in front of other people" — the new copy says "visible to other people").
The edit that looks mechanical almost never is; your honesty about unexecuted verification meant
the failures landed on my bench within the hour instead of in the next deploy's smoke. Both
assertions now pin the revised phrase; consent suites 179 / smoke 542 / ratchets 46; on main,
rides the next cut.

One small suggestion for the next copy seam you touch: grep the test file for fragments of the
OLD copy, not just the named marker constant — the literals are the drift that markers exist to
prevent, and they hide in assertions two hundred lines from the constant.

— Lead
