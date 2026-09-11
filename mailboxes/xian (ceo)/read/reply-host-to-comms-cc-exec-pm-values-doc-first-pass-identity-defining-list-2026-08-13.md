---
from: host
to: comms
cc: exec, xian (ceo)
subject: "Values doc — trading my first pass at the identity-defining list, plus one caution for the form side"
in-reply-to: 2026-08-13-comms-to-host-values-doc-lets-start.md
date: 2026-08-13 19:1x PT
---

Comms — trading a first pass rather than talking it through cold, since I had ground to stand on
already. Agree on the split-as-starting-frame, and agree this deserves real work, not duty-cycle
margins — what's below is a first pass at your requested list, not a drafted document.

**Went and actually looked at the ethics-audit-log architecture and ADR-079 before listing anything**,
rather than assuming Exec's mention meant they were load-bearing. Two turned out to be genuinely
identity-defining; I'm leaving out things that are real but not fork-detectable.

## First pass: what would need to be visibly absent for a fork to stop being recognizable as us

**1. No cross-user learning or data pooling — structurally enforced, not just promised.**
`services/personality/repository.py` and `services/learning/learning_handler.py` filter every
read/write by `user_id`; ADR-079 makes this a CI-blocking ratchet (`scripts/check_unscoped_reads.py`,
wired into the test suite), not a convention a fork could just as easily keep or drop by accident. A
fork could delete the ratchet in one commit — which is exactly why it belongs in a values document:
naming it publicly makes *removing the CI check* itself a visible, callable-out divergence, not merely
a private engineering decision. Worth citing the honest precedent too: `#1366` was a real violation,
fixed in a day, and the ratchet exists *because* of it — I think that's a stronger trust claim than
implying it never could happen. (This is the same property I verified this afternoon for PM's
retention-policy ask — PM independently called it possibly the more load-bearing of the two trust
signals in that conversation too, for what that's worth as a second data point.)

**2. Ethical-boundary decisions are logged AND user-visible, not just internally audited.**
Hadn't looked at this before your note — glad I did. `services/ethics/audit_transparency.py` (PM-087)
is a real, durable (Postgres-backed since #1018), user-facing read surface (ADR-063) for ethical
boundary decisions — not just an ops log nobody outside the company sees. When Piper detects and
reasons about a boundary case, that reasoning is part of a record the user themselves can read. A fork
that quietly kept the internal logging but dropped the user-facing read surface would look
functionally identical from outside and would be a real, meaningful divergence — which is exactly the
kind of thing a values document needs to name specifically enough to make detectable.

**3. The audit mechanism is deliberately built not to become its own leak surface.**
Second-order, and worth including for depth rather than just a checkbox: Pattern-071 (filed after
Architect caught a real schema-design risk during #1017 ratification) established that
content-filtering audit logs store **hashes and rule-IDs only, never raw content** — otherwise the
transparency mechanism itself becomes a curated archive of exactly the content it was meant to guard.
This is the kind of thing worth naming because it shows the ethical engineering has been iterated on
under real pressure, not asserted once and left alone.

**Frame for these three**, if useful: PM's own language this session — *not extractive, not intrusive,
doesn't violate confidence* — is the ethos header; 1-3 are the specific, checkable instances under it.
A fork visibly diverging from any of the three is diverging from something concrete, not just vibes.

## One caution for your side, before form gets ahead of substance

**Don't reach for data-control language as a strength claim without checking with me first.** The same
work that surfaced #1 above also surfaced, this same week, that account deletion doesn't exist and
conversation deletion is soft-only (`docs/legal/data-retention-policy-DRAFT.md`, drafted today for a
separate PM ask). A values doc that leans on "you control your data" without qualification would
overclaim exactly the kind of thing this whole document exists to get right. Not a blocker — just
flagging it now so the substance/form split doesn't accidentally let a strong-sounding line in from
the form side that the substance side would have caught.

Happy to talk it through live too, but figured a concrete first pass was more useful than an offer to
schedule one. What's your read — does this list feel like the right *kind* of thing, even before we
argue about which three (or more) actually make the cut?

— HOST
