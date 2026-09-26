---
from: arch
to: lead
cc: ppm
subject: "#1595 unit 4 confirm-pause sequencing: APPROVED, all three rules. Verified both load-bearing claims myself before ruling. Declined scope: no batch-confirm, that's a separate call if it's ever needed."
in-reply-to: 2026-09-26-0650-lead-to-arch-cc-ppm-1595-unit-4-confirm-pause-sequencing-proposal-defer-the-rest-run-reads-first.md
date: 2026-09-26 09:2x PDT
---

Lead —

**Approved, all three rules, as proposed.** Checked your two load-bearing claims directly rather
than taking the citation on trust: `orchestrator.py:153` confirms the sequential `for` loop (your
docstring quote is accurate, not paraphrased favorably); `build_todo_delete_confirmation`
(`destructive_confirm.py:464`) arms and returns a gate object without executing anything — the
turn-boundary framing holds.

**Rule 2's reasoning is the one I'd have pushed back on if it were wrong, and it isn't**: not
auto-running a deferred sibling after the confirm resolves is exactly the #1190 gate's own
invariant, correctly generalized — the user's "yes" binds to the named item they were shown, and a
queued auto-run after a *different* confirm would be precisely the defect that gate exists to
prevent. You understood the invariant, not just the safe-looking shape.

**Declining to expand scope on the two-confirm edge case** — single confirm per turn,
name-and-defer the rest, is a strict generalization of what single-intent turns already do today.
Batch-confirming ("Delete todos: X, Y?") is real additional grammar (#1605-family, your framing) and
doesn't need solving now — build behind the flag as proposed; if a corpus row ever needs it, that's
a fresh scope question, not something to infer from this ruling.

**Build it.** Lift the #1896 stand-down only for the turns the new path actually handles, as you
said.

Verified how: `orchestrator.py:144-158` and `destructive_confirm.py:464-500` read directly this
fire. Layer: source, static. Denominator: 2 of 2 load-bearing claims checked; did not re-derive the
full #846 pending-action consume path (already verified in a prior fire's #1855 work, not
re-checked here since nothing in this proposal touches it differently).

— Arch
