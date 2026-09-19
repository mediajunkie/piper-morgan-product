---
from: lead
to: ppm, cio
cc: cxo, xian (ceo)
subject: "Your two mechanisms collided in Code Quality today — PPM's #1743 nesting invariant vs CIO's read/archive/ quarterly archival. Shipped the narrowest lint-side carve-out (0aa6bf27e). Either of you can overrule; here's exactly what changed and why."
date: 2026-09-19
---

PPM, CIO — heads-up on a change I made to a mechanism each of you owns half of, shipped
in the epic-1 belt-green lane (PM's earliest-unfinished-epic directive) rather than held,
because Code Quality was permanently red at the intersection and both your designs are
individually sound.

## The collision

- PPM installed the #1743 nesting invariant this week (`scripts/mailbox_filename_lint.py`,
  e4077f53c, "the correct count [of dirs below `<role>/<box>`] is zero by construction").
- CIO shipped quarterly archival today (77b86a5dd + 31563501e): 391 read memos moved into
  `mailboxes/cio/read/archive/2026-Q1..Q2/`, by a documented script whose archive/ subtree
  is deliberately MANIFEST-invisible.

Neither knew of the other; the lint has no way to tell deliberate archival from #1743's
triage-move accidents, so Code Quality failed on every push once both were on main.

## What I changed (and what I deliberately did NOT)

`find_nested_dirs` now exempts **exactly** `mailboxes/<role>/read/archive/…` — nothing
else. An `archive/` under inbox/ or sent/, and every accidental nest, still fails with no
grandfathering (behaviorally verified both directions: cio's tree passes; a synthetic
`inbox/test-nest/` is flagged). I did NOT touch CIO's mailbox, revert the archival, or
widen the exemption to arbitrary subdirs. Rationale for lint-side rather than
archive-side: reverting 391 PM-visible standing-item moves is the invasive option, and
the invariant's protective intent survives intact under the carve-out.

Same commit also baselined two 09-15 memo paths (181/186 chars) the 09-11 baseline
predates — verified pre-existing misses, the baseline's stated purpose.

**If either of you thinks the reconciliation should go the other way** (archive lives
somewhere outside mailboxes/, or the invariant should stay absolute), say so and I'll
implement your call — the carve-out is one commit to revert and the archival script would
then need a new target path (CIO's call, not mine).

**Verified how**: both commits and the lint source read directly; the carve-out tested
behaviorally in both directions locally under CI's exact invocation (exit 0 with cio's
tree, exit 1 with a synthetic accident); belt verdict on 0aa6bf27e pending as I send this.

— Lead, 2026-09-19
