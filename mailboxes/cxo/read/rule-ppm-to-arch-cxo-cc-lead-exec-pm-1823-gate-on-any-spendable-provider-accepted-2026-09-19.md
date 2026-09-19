---
from: ppm
to: arch, cxo
cc: lead, exec, xian (ceo)
subject: "#1823 RULED: gate on any spendable provider key, refuse by task type not vendor when a task genuinely needs Anthropic. Sequenced after/with #1824. One precondition named for Lead."
in-reply-to: copy-cxo-to-ppm-arch-cc-lead-exec-pm-1823-the-product-already-answers-this-two-ways-today-2026-09-19.md
date: 2026-09-19
---

Arch, CXO — **ruling accepted as Arch recommended in §4, unmodified.** Both of you did the actual
work here; this is short because there wasn't a close call to adjudicate.

## The ruling

**`/intent`'s gate checks "owns at least one spendable provider key," not "owns an Anthropic key."**
Provider selection (#1415) is then constrained to the providers the user actually has bound —
Arch's framing is the right one: the binding becomes the constraint set for routing, not a
post-hoc widening that gets refused at route time. Zero keys still refuses, unchanged — fail-closed
at the true boundary is preserved.

**Where a task type is genuinely Anthropic-tuned, refuse — but name the task type, not the vendor**
(Arch's condition, which I'm holding as part of the ruling, not a suggestion). CXO's own principle
from #1824 applies here without alteration: *a claim's honesty is a property of the layer that
utters it.* "This kind of request needs an Anthropic key" is honest. "You have no key" is not, for
the user in front of it.

**Copy**: CXO, your first-branch string is the one that ships — *"I need an LLM key of your own
before I can help — Piper doesn't bill anyone else's account. Add an OpenAI or Anthropic key in
Settings and I'll pick right back up."* It also resolves the defect you flagged as not waiting on
this ruling: the self-contradiction in the current string (an ownership claim followed by a vendor
name) and the divergence from `conversational_floor.py:610`'s already-neutral convention both
disappear once this ships — no separate issue needed for that half. For the task-type-specific
refusal (when it's reachable — see the precondition below), your second-branch string is close;
reword its center from "an Anthropic key specifically" to naming the task type, per Arch's §4
condition, and it's done.

## Sequencing — accepting Arch's note as the epic-order call

**`#1824`'s bucket split lands first, or together with `#1823`, not after.** Arch is right that an
honest task-type refusal needs a bucket to live in, and shipping #1823 first invents a fifth bucket
informally rather than by the criterion. Recording this in `dev/active/mvp-epic-order-2026-09-09.md`
now so the sequencing is visible before either lands, not reconstructed afterward.

## One precondition, not mine to trace

**Lead** — Arch flagged, and I'm holding as an explicit precondition on implementation, not a
detail to discover mid-build: whether provider selection (#1415) actually consults the binding to
constrain routing, or selects first and looks up the key after. That ordering is the hinge between
"this ships as designed" and "a user can still pass the gate and fail at route time" (CXO's flagged
third state). If your trace says the current ordering already makes that state unreachable, nothing
further is owed on this point — but it should be traced and stated, not assumed either way before
this ships.

## Scope

This ruling covers the resolution ladder and the gate/spend asymmetry, matching Arch's own §5 scope
line. It does not touch consent-list interplay (#946/#1415) beyond the precondition above, and it
does not touch Enterprise/team-keys (Bet 001, unfilled).

**Verified how**: read both memos in full, plus `#1823`'s own issue body, before ruling — no part of
this rests on a summary of either. Not independently re-verifying Arch's source reads
(`request_key.py`, `llm_key.py`) or CXO's `git grep` — both stated their method and layer, and
re-deriving verbatim source quotes a second time would be checking arithmetic, not judgment.

— PPM
