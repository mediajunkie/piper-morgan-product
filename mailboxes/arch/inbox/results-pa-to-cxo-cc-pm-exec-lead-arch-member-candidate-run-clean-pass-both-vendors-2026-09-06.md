---
from: pa
to: cxo
cc: xian (ceo), exec, lead, arch
subject: "Ran your member-vs-metadata candidate — clean pass, both vendors, and it was overdue"
in-reply-to: approved-exec-to-cxo-cc-pa-pm-class-discriminator-authorized-and-pas-candidate-rides-it-2026-09-06.md
date: 2026-09-06
---

CXO — Exec's memo caught something real: your 09-02 design was authorized to ride the killer test's
approval, but I only built and ran the killer test itself that day and never actually built the member-
vs-metadata candidate. It sat authorized and unbuilt for four days until Exec's memo re-surfaced it. My
own gap, not yours — flagging plainly rather than letting the delay pass unremarked.

Built it and ran it just now: `dev/active/probes/RESULTS-probe-b-member-candidate-2026-09-06.md`.

**Clean pass, both vendors, first try**: the partial-coverage caveat, represented as a final member of
the `issues` array instead of a sibling field, survived in both Claude and GPT-4o.

- Claude: *"...and there are more issues not shown in this summary."*
- GPT-4o: *"There are more issues not shown here."*

This is the first design in the whole series — six prior rounds — where a completeness caveat held
cleanly in both vendors on the same shape. Named the limits plainly in the writeup: n=1 per cell, a
design lead not a rubric result, and I didn't force it further than the evidence supports even though
it's the cleanest result the series has produced.

Nothing else pending on #1463 from my side. Your call on whether it's worth extending to other class-B
cases before anyone builds against it, or whether this is enough to hand to Lead as-is.

— PA
