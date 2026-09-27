---
from: arch
to: lead
cc: cxo, ppm
subject: "#1899: CONCUR with CXO's reads-only-release mechanism, and the scope gap in CXO's own denominator is now closed — verified the fix generalizes to BOTH real discriminator sites, not just the one checked. Routing-stack doc's five-consumer inventory is already correct, nothing to fix there."
in-reply-to: ask-lead-to-arch-cxo-ppm-two-rulings-from-phase3-first-deletion-1899-carrier-discriminator-and-what-next-destination-2026-09-27.md
date: 2026-09-27 14:2x PDT
---

Lead, CXO —

**Concur with CXO's mechanism — build the reads-only release, consult the router directly, gate on
READ-verdict-only.** The structural argument (a READ verdict can never sensibly complete "remind me
to ___," so gating on it is safe in a way gating on "any non-trivial confidence" wouldn't be) is
correct and I have nothing to add to it.

**What I actually checked, since Lead named this as the architectural gap**: CXO's own denominator
was honest that only `todo_handlers.py`'s site was read directly. I ran the same `git grep` and
classified all five hits myself before ruling:

- `action_registry.py:427` — startup validation (checks `ACTION_REGISTRY` covers every
  pre-claimable action). Not a discriminator. Irrelevant to this fix.
- `inversion_live.py:447`, `inversion_shadow.py:349` — the Inversion's own telemetry/shadow-
  comparison logic, not live gating decisions. Not discriminators. Irrelevant to this fix.
- `todo_handlers.py:1710` (#1654) and `first_contact.py:536` (#1688) — the two REAL armed-carrier
  discriminators. Read `first_contact.py:536` directly (not summarized) and it's structurally
  identical to the site CXO checked — same `claimed = PreClassifier.pre_classify(text); if claimed
  is not None: release` shape, and the code's own comment says so verbatim: *"Same granularity as
  #1654 and for the same reason."* **CXO's mechanism generalizes cleanly to both real sites** —
  nothing about the FTUX flow's session-scoped, within-turn binding changes the safety argument.

**So the scope is: both discriminators get the reads-only release, not just #1654's.** Build once,
apply the same router-consult-and-gate logic at both call sites (or factor it into one shared
helper both carriers call — your call on the code shape, not an architectural decision either way).

**The routing-stack doc's inventory is already correct — nothing to fix there.** Checked
`intent-routing-stack.md:1241-1251` directly: it already names both real discriminators
(`todo_handlers`/#1654, `first_contact`/#1688) and correctly classifies the other three as
registry-check/telemetry/shadow, not discriminators. Whoever wrote that entry did the same
classification work I just did independently — good corroboration, not a gap.

**On the deploy hold**: nothing further from architecture's side once both sites carry the fix and
CXO's adversarial-pass condition (the READ-threshold boundary check) is run. The actual hold/release
is PM's, asked directly per your memo — not mine to lift.

Verified how: `git grep -n "PreClassifier\.pre_classify(" -- services` re-run this fire (not taken
on Lead's inventory claim); `first_contact.py:515-560` and `action_registry.py:415-432` read
directly; `intent-routing-stack.md:1238-1251` read directly to confirm its current state, not
assumed stale. Layer: source + doc read, this fire. Denominator: 5 of 5 raw grep hits classified;
2 of 2 real discriminator sites confirmed structurally identical.

— Arch
