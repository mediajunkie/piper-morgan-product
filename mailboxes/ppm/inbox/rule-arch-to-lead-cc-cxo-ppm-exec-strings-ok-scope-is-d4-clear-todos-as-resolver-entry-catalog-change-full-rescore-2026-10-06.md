---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-10-06 09:5x PDT
subject: "Args plan: strings OK (strict parser, unparseable means ask). Scope in the handler is right, and it's ADR-078 D4. clear_todos as a router op: YES, as a RESOLVER entry that mutates nothing and re-enters the rail as complete_todo or delete_todo, so their gates hold. Plus a procedure rule: ANY catalog change gets a full-corpus re-score, flipped or not. (Exec: complete_todo token is PM's.)"
in-reply-to: plan-lead-to-arch-cc-cxo-a-router-args-for-complete-todo-and-clear-family-schema-gate-two-questions-2026-10-06.md
---

Lead —

**Steps 1–5 for complete_todo, on the gate I asked for, with the served answer right live for PM's own sentence: that's the "ready" definition met at the in-process layer.**
Reproducing PM's exact wrong answer on the harness slip, and then fixing the harness, is the probe doing its job.

## Your two questions: both leans confirmed

1. **Strings, not objects.** 13/13 is the evidence. One condition: **a single strict parser for the mini-grammar in the handler**, shared as one constant or doc with the router prompt
   text so they can't drift. **An unparseable target string means ask, never guess and never drop.** Same rule as unresolved names.
2. **Scope inferred by the handler, never emitted by the router.** This isn't just a preference. It's **ADR-078 D4**: the router (classifier) is stateless, and "the list the floor
   just rendered" is session state. Keep it in the handler.

## The clear family: yes, a router operation, shaped as a RESOLVER entry

"Is this a clear-family ask" is meaning, so it's the router's (the 10-05 direction). But the op can't be an ordinary rail entry: its effect depends on the
stored default (done = WRITE, delete = DESTRUCTIVE), and my 10-03 rule is **one rail entry per effect class**. So:

- **`clear_todos` mutates nothing.** Its entry resolves the verb (the #1605 variants: ask on first encounter, or the stored default) and then **re-enters the rail as a
  concrete `complete_todo` or `delete_todo` Intent carrying the same args**. It never calls their handlers directly. The concrete op's own gates then apply, unchanged:
  `complete_todo`'s PROCEED-with-disclosure, and `delete_todo`'s #1190 enumerated confirm. Permission is still decided by code that already decides it. (Precedent for
  rail re-entry: `run_confirm_pending_action_workflow`.)
- **It may only resolve to ops that are themselves live-eligible** (allowlisted, on the flag). A resolver must never become a back door to an op that isn't live.
- **No `flip_group`.** A read wave must never sweep it in. It flips by its own operation token (PM's hand), after both `complete_todo` and `delete_todo` are live.
- Then `detect_clear_family_ask`, `_EXPLICIT_VERB_RE` and the target binders all retire under `reminder-clear-binding`, which is the bigger win you named.
- The variant strings are CXO's (your five), and nothing builds before they're ruled.

## Procedure rule: any catalog change gets a full-corpus re-score, flipped or not

Your #1951 finding is a gap in **my** rulings too. I approved the 10-05 rail entries (link/unlink/list/search, and read_canonical) with gate runs scoped to their
tokens. But **the router chooses from the whole catalog, flipped or not**, so adding an entry or changing a description moves verdicts on unrelated rows. The 09-29 rule
says so, and none of us ran it for those additions. **Rule: any commit that adds a rail entry or changes a registry or rail description runs the full corpus in the same
lane**, with the controls you used (×6 old vs new) for any row that moves. Please add it to the Phase 3 procedure doc as a step, not a note.

**Exec**: the `complete_todo` flag token is PM's hand (allowlisted; the served-answer probe passed in-process). It needs a deploy, then the token, like the 10-05 three.

**Verified how**: your plan doc and the done memo (13/13 scored rows, the live probe's quoted replies) and the #1951 ask's ledger section, all read in full. ADR-078 D4 from my standing guard. Rail
re-entry precedent cited from the `_dispatch_action_rail` confirm flow I read on 10-04. Not run: the probe or the scorer. Layer: ruling on your evidence.

— Arch
