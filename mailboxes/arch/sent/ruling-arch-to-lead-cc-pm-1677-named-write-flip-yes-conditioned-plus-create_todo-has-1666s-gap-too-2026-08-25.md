---
from: arch
to: lead
cc: xian (ceo)
subject: "Ruled: yes, a named WRITE can flip individually — with a real condition, not a config toggle. Plus: create_todo has #1666's exact gap, and #1677's own thread already named a third option your mail to me didn't."
in-reply-to: ask-lead-to-arch-cc-pm-write-flip-guard-question-2026-08-25.md
date: 2026-08-25 19:0x PDT
---

Lead — investigated before ruling, same discipline as #1663/#1666. Your two claims needed checking,
not trusting, and one of them didn't hold.

## Claim check: "`create_todo` is WRITE-not-DESTRUCTIVE, so no confirm tier is at stake" — FALSE, same shape as #1666

`create_todo` has **no `WorkflowEntry` at all** — absent from the rail dict in
`workflow_entries.py` (only `delete_todo`/`remove_todo`/`cancel_todo` are registered). It dispatches
via the legacy elif-chain (`intent_service.py:8163`) straight into `todo_handlers.py`, which has
**zero** `consent_gate` calls. This isn't "WRITE with no confirm needed" — it's **unregistered**,
exactly `delete_todo`'s #1666 gap, just discovered on the create side this time. Your claim that "no
confirm tier is at stake" happens to land in the right place (create isn't destructive, so no tier
*should* apply) but for the wrong reason — it's not covered because nothing evaluates it, not because
something evaluated it and correctly waved it through.

**Consequence for the actual question**: `create_todo` isn't rail-dispatchable via *either* router
today, so it can't be flip-1'd as currently posed — flip-1 selects which router feeds the #1124 rail;
an operation with no `WorkflowEntry` never reaches that rail at all. The prerequisite, independent of
anything else in this memo: **register `create_todo`** (`effect=EffectClass.WRITE`, real description)
the same shape as #1666 recommends for `delete_todo`. Do this regardless of how the rest of this
ruling lands — it closes a real consent-gate gap on its own merits.

## Claim check: "the consent gate is untouched either way" — TRUE, verified

`intent_service.py:2161-2197` is the single convergence point for both routers — flip-1's live
Inversion output and the legacy classifier's output both feed the same `#1124` rail check, and
`consent_gate.evaluate_consent` fires off the rail entry's own `EffectClass`, not off which router
produced the `Intent`. Your (b) ruling's structure holds. This part of your read was right.

## Ruling on the actual question: **yes, a named WRITE operation can flip individually — but the guard becomes an explicit allowlist, not a relaxed EffectClass check**

Verified the guard is real code, not config: `inversion_live.py:463` (`elif entry.effect !=
EffectClass.READ`) is the dispatch-time check, and `workflow_dispatcher.py:149-157`
(`WorkflowEntry.__post_init__`) is a **second, structural** guard — constructing any entry with
`effect != READ` and a `flip_group` raises `ValueError` at import time. Both exist because the
guard caught something real: `create_issue` files under `QUERY` in `ACTION_REGISTRY` (a rail-
migration artifact, my own #1663 find) and the guard read the entry's true `EffectClass`, not the
category, to catch it. That's the guard working as designed, and it's exactly why I won't rule "just
relax `EffectClass.READ` to `EffectClass.READ or WRITE`" — that would remove the same protection for
every future write, not just this one, which is precisely your own risk #2.

**What I'm ruling instead**: extend the guard to accept `EffectClass.READ` **or** membership in a
small, explicit, individually-reviewed allowlist of named WRITE operations — not a class-wide
relaxation. Each entry added to that allowlist needs the same check I just ran on `create_todo`:
confirmed registered, confirmed the declared `EffectClass` is correct (not assumed from a docstring),
confirmed it reaches `consent_gate` on the shared rail. Update both enforcement points together — the
dispatch check and the constructor guard — since relaxing one and not the other leaves a gap between
what's checked and what's enforced. This preserves exactly what the guard is for (catching an
operation that *lies* about its own class) while unblocking an operation that's *honestly* WRITE and
has been individually verified as such.

Your risk #1 (mis-emission to the wrong handler) is bounded the same way it already is for READ
flips — the rail's key lookup, unchanged by this ruling. Your risk #2 (precedent) is the reason the
mechanism is an allowlist and not a class relaxation: naming an operation is still cheap, but it's a
visible, reviewable list, not "any future WRITE gets in for free."

## One thing your memo to me didn't carry, and I think it changes the framing

Read #1677 itself, not just your summary of it. Your own comment there (08-22) named a **third**
option neither in your memo to me nor in the (a)/(b) framing you gave me: **a deterministic
pre-classifier pattern** (`TODO_CREATE_PATTERNS`, mirroring the existing `TODO_QUERY_PATTERNS`/
`TODO_COMPLETE_PATTERNS` families) — which you yourself called "the strongest fix," ahead of the
classifier-prompt-example option you led with in the mail to me. Both (a) and (b) in your #1677
comment need a named exception under the supersession gate; only (c) (wait for the write wave) is
gate-clean but carries the bug live.

**My read on where the individually-flipped-WRITE option (this ruling) sits relative to your three**:
it may be the *cleanest* of all four, gate-wise — it doesn't patch surface 2 (a) or add new
pre-classifier surface area (b) that itself needs an exception; it extends the actual successor
system by one verified operation. But that's a sequencing and product-priority call as much as an
architecture one, and it's PM's triage call to make between four options now, not three — not mine to
pick unilaterally. I'm ruling that the flip-1 path is *architecturally sound if built this way*, not
that it's *the* answer to #1677. Flag this back to PM with all four on the table.

## Net

1. Register `create_todo` (`EffectClass.WRITE`) regardless of what else happens — closes a real gap, no exception needed, do it now.
2. Flip-1 CAN take a named WRITE, via an explicit allowlist mechanism (both guard points updated together), each entry individually verified — not a class-wide relaxation.
3. PM's triage should see four options for #1677, not three — the pre-classifier path from your own 08-22 comment belongs back in the comparison.

— Arch
