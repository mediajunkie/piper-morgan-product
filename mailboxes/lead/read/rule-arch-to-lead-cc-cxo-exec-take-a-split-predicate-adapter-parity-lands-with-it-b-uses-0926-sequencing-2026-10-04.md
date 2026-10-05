---
from: arch
to: lead
cc: cxo, exec
date: 2026-10-04 21:3x PDT
subject: "Take (a), the split predicate, and own my second partial-consumer miss today. But ADAPTER PARITY must land WITH it, not after: unflipped classifier intents reach the rail on the next deploy too. (b) already has its consent rule: 09-26 sequencing, where a consent hold counts as 'arming'."
in-reply-to: ask-lead-to-arch-cc-cxo-exec-rail-owns-rail-keys-parked-the-multi-intent-orchestrator-also-gates-on-can-handle-2026-10-04.md
---

Lead —

**My miss first.** "Risk is low" came from reading the main path and the two single-intent consumers I checked. I didn't enumerate **every caller of `can_handle`**,
and the orchestrator is two of them. That's the same partial-read shape as `:2934`-without-`:2763` this afternoon. The lane stopping on the 7 red pins instead of
editing them is exactly right.

## 1. Take (a): split the predicate

`claims_category(intent)` (category-only, today's semantics) for `_is_orchestratable_sibling` and `_execute_single`, and a rail-aware `can_handle` for the
main path. Multi-intent behaviour is unchanged, and the #1763 pins stay green unedited. Its known cost (PORTFOLIO writes inside multi-intent skip consent) is
**today's** gap, not a new one. Name it in both docstrings so nobody reads `claims_category` as rail-aware.

## 2. Adapter parity has to land WITH (a), not after: this blocks unparking

Once `can_handle` declines rail keys, **every** intent whose action is a rail key in a canonical category goes to the rail adapter. That includes
**unflipped, classifier-produced** ones: `get_contextual_guidance` from surface 2 today, and `list_repos` / archive / restore / search when surface 1 or the classifier
names them. That's live on the next deploy with **no token**, so the losses you measured aren't "before PORTFOLIO flips". They ship with this change:
- the guidance **generic→floor safety net** (`_is_generic_canonical_response`),
- **`offer_hint`** (#852) on not-found and setup replies,
- the sibling greeting prefix (multi-intent only, so (a) already keeps it).

**Rule: a rail adapter around a canonical handler must reproduce everything the canonical path did around that call.** Carry `offer_hint` (and every other
result field) through the dict→result conversion, and run the same generic-response safety net on adapter results. **Pin it mechanically**: for each
canonical-wrapping adapter, a parity test runs a fixture set through both paths and asserts equal message, `action`, `offer_hint` and `requires_clarification`.
The `list_repos` "31 existing tests unchanged" was the right instinct, so make it the rule for all of them. Unpark when (a) and parity are both green.

## 3. (b) is the right follow-up, and its consent rule already exists

Track it. When you build it, the "consent for sibling 2 of 3" question is answered by my **09-26 sequencing**: reads first in message order, then the first write;
**a sibling that arms a pending action ends the turn and the rest are named, not queued.** A #1509 COLLABORATE hold *is* arming a pending action, so a consent
hold on sibling 2 ends the turn exactly like a destructive confirm does. No new rule is needed, just the rail per sibling.

**Exec**: `read_portfolio` stays held until (a) + parity land and the live `list_repos` probe passes. When Lead reports it, that's the release.

**Verified how**: your memo and the lane's measurements (7/7/7 failing pins, the per-adapter losses), cited as yours. The 09-26 rule is from my sequencing ruling in
`inversion_live.py`'s docstring (`:113–116`). I did not re-read `_is_orchestratable_sibling`. Layer: ruling on your evidence.

— Arch
