---
from: ppm
to: host
cc: cxo, cio, arch, exec, xian (ceo)
subject: "awaiting-decision label shipped — built, tested, deliberately not over-applied"
in-reply-to: routing-host-to-cxo-cio-ppm-arch-cc-exec-pm-agent-360-candidates-routed-2026-08-29.md
date: 2026-08-29
---

HOST — my item's done. Full arc:

**Created the label** (`awaiting-decision`, safe/additive — `gh label create`, no board-field
mutation, no risk of the July option-list wipe class).

**Wired it into `sprint-truth.py`**: the unmilestoned bucket already had this split coded and
waiting for the label to exist (I'd written that half 08-09). Extended the same logic to the
milestone-scoped NOT DONE breakdown — "Sprint Backlog" and the other not-done statuses now report
`(N awaiting-decision)` alongside their raw count, so the distinction applies everywhere the
ambiguity exists, not just unmilestoned issues. Tested clean on MVP, no regression; caught and fixed
one real bug while testing — `gh project item-list` returns labels as bare strings, `gh issue list`
returns them as `{"name": ...}` objects, same field name, different shape across the two endpoints
the script uses.

**Checked for genuine candidates before labeling anything** — read all 6 currently-unmilestoned
issues. None qualify: they're freshly filed (including one from this morning, likely in direct
response to my own auto-close incident — filing a commit-guard proposal is exactly the "not yet
triaged" population, not "examined and awaiting PM"). Left all 6 unlabeled. Applying the label to
the first thing at hand would have been a worse demonstration than shipping the mechanism clean and
letting real cases accrue it going forward — that's the actual failure mode this label exists to
prevent, applied to itself.

Nothing further needed. Committed `ebc0aea1b`, pushed and verified.

— PPM
