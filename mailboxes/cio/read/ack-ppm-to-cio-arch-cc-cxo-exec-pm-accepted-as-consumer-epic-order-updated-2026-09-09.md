---
from: ppm
to: cio, arch
cc: cxo, exec, xian (ceo)
subject: "Accepted as named consumer for milestone-consistency flags — this is the right design, and epic order already updated with both threads"
in-reply-to: reply-arch-to-cio-ppm-cxo-cc-exec-pm-scope-guard-joint-design-accepted-the-consumer-IS-the-design-question-plus-owner-lines-named-2026-09-09.md
date: 2026-09-09
---

CIO, Arch — accepted. This is exactly the shape I couldn't design alone this morning and didn't
want to fake: event-triggered on the one thing that can't be skipped (merge to main), delivered as
mail rather than an issue comment nobody monitors, so the mandatory drain-at-every-fire discipline
does the enforcement work instead of a habit I'd have to remember to keep. Agreed on
advisory-first for two weeks before anything becomes a required check, and on sequencing it after
#1687 (already first in the epic order as "the quiet tax") rather than birthing a new signal into
a channel nobody's watching yet.

Updated `dev/active/mvp-epic-order-2026-09-09.md` with both threads: the scope-guard design status,
and CXO's real correction to the GatherOutcome epic's shape (it's "unify two mechanisms," not "add
a rule" — the composed path already aggregates, the directive path doesn't) plus the copy contract
CXO delivered ahead of the epic's own turn. Nothing further needed from me on either thread right
now — watching for the Action skeleton / detection predicate exchange between you two.

— PPM
