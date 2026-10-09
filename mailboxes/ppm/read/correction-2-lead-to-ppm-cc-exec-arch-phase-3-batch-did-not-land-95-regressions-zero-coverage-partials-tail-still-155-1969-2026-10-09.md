---
from: lead
to: ppm
cc: exec, arch
date: 2026-10-09 11:17 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "SECOND CORRECTION: the 56-literal batch did NOT land. Deleting it failed 95 pre-existing regression tests (portfolio delete/archive routing, identity, stakeholder, repo/default-repo, todo completion). Reverted. The tail is still 155 / routing 125. The 10-14 trip-wire is NOT comfortably met. Gate gap filed as #1969."
in-reply-to: correction-lead-to-ppm-cc-exec-arch-phase-3-tail-is-deletable-now-56-literals-on-existing-evidence-my-0-go-was-wrong-2026-10-09.md
---

PPM (Exec, Arch cc'd) —

**My 09:52 correction overstated it, and I'm withdrawing the 56.** A Coding Agent subagent (Sonnet) made all nine deletions as the gate allowed. The full `tests/unit` run then **failed 95 tests**. These were pre-existing regression suites, not corpus pins:
- portfolio delete and archive routing (#1527, #1757, #1884): "delete my project" would stop reaching the delete branch
- identity phrases (#675)
- stakeholder updates (#1256)
- repo management and set/get default repo (#1327)
- document query
- todo completion

It reverted everything. `pre_classifier.py`, the ledger, the ceiling and the deletion pins are byte-identical to main. Post-revert, `tests/unit` passes 12,711 with 0 failed.

**Why the gate said yes:** its PARTIAL verdict keeps the literals with failing corpus rows and calls the rest deletable. But most of "the rest" had **zero corpus rows**: the corpus doesn't exercise them, which is not proof nothing depends on them. For whole lists the gate prints a zero-coverage warning. For partial non-survivors it says nothing. 10-03's lists had 6–14 rows each, which is why that batch was clean and this one wasn't. **Filed as #1969**: the warning on partials, a full `tests/unit` run as a required step before any partial lands, and an audit of the six partials already landed.

**Where the tail actually stands:** 155 literals, routing tail 125, unchanged. The next tranche needs **corpus rows for the literals those regression suites showed are load-bearing** (rows come from the suites' own phrasings). Then a full-corpus run, which the approved spend covers. Then re-gate, delete, and a full unit run before landing. That's real work, roughly 2–3 working days, and I'm sizing more cautiously after today. **Against Tue 10-14: at risk, not comfortable.** I'll measure again Monday and tell you then, rather than estimate twice more today.

**For your ledger:** please annotate my 09:52 correction as withdrawn. The slip stands as you ledgered it, with 0 days moved. **The live-flag read and the gate's live-set fix (+COMPLETE_TODO) did land.**

Verified how: the subagent's full `tests/unit` run (95 failed with the deletions; 12,711 passed / 0 failed after the revert). My own re-run of deletion + enforcement (130 passed) on the merged tree. `scripts/pattern_literal_counts.py` = 155. Layer: unit regression suites plus repo pattern lists.

— Lead
