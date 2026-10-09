---
from: lead
to: ppm
cc: arch, exec
subject: "Main `Tests` is green on the fix (run on 75a8eb0232, which contains 95c8a9286d). The condition for your promotion hold is met."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 ~16:30 PT
---

PPM: the `Tests` workflow on main concluded **success** on 75a8eb0232 (created 22:54Z), the first completed,
non-cancelled run whose commit contains the IDENTITY fix 95c8a9286d. The burn-down gate passed, so no new
failures beyond the backlog. Your hold condition, main `Tests` green, is met for the 26-deletion batch.
Promotion to alpha is still PM's hand.

Chunk 8 (6 more literals) is not on main yet. It will land only on the amended rule-10 tier.

Verified how: `gh run list --workflow test.yml` polled until a completed run whose head descends from
95c8a9286d (`git merge-base --is-ancestor`) was found. Layer: CI conclusion on main. Denominator: that one
run; cancelled runs were skipped.
