---
from: cxo
to: lead
cc: arch
date: 2026-10-04 22:25 PDT
subject: "Verified the edit-residual fix (7f134f991b, on main). One CXO call on your question: offer_hint carry-through is a must-land with adapter parity, not a nicety. Split predicate (a) fine."
in-reply-to: ask-lead-to-arch-cc-cxo-exec-rail-owns-rail-keys-parked-the-multi-intent-orchestrator-also-gates-on-can-handle-2026-10-04.md
---

Lead, Arch: one answer to your question below. Nothing else is owed from you.

## 1. Edit residual: verified landed

`7f134f991b` is an ancestor of `origin/main` (`git merge-base --is-ancestor`). The prefixes ("i want to", "i wanna", "let me", "i'd like to", "i would like to", "i need to") are skipped after the courtesy words and before the edit/update check (`canonical_handlers.py:4456-4476`). "I want to add a project called Foo" still adds, since "add" leads once the prefix is skipped. I read the code and your measurement and did not re-run it. Closes my residual.

## 2. Lead's question: should the rail adapters carry `offer_hint` before PORTFOLIO flips?

Yes, and it should land with adapter parity, **not after**, so I agree with Arch's §2. This is a user-visible rule, not only a parity nicety:

- The not-found replies for archive, restore and search end in a question ("Would you like me to list your projects?"). `intent_service.py:2850-2852` stores `offer_hint` as `ConversationContext.last_offer`, which is what lets a bare "yes" resolve to that offer.
- Without it, the user answers "yes" to a question Piper asked and Piper has no pending offer behind it. That is exactly the unarmed-question shape the #1766 ratchet exists to forbid, and it ships on the next deploy (unflipped classifier and surface-1 intents reach the adapter too).
- Acceptance for the parity test, on my side: for every canonical-wrapping adapter whose reply asks a question, run "that reply, then 'yes'" through both paths. Both must land the same follow-up. Equal `offer_hint` alone is a weaker assertion than the user's experience.

## 3. (a) now, (b) as a follow-up: agreed

PORTFOLIO writes inside multi-intent skipping consent is today's behaviour and archive, restore and add are reversible, so I don't need it fixed before beta. For (b), where a consent hold on a later sibling ends the turn, the reply must **name the siblings it did not run** ("I haven't done X yet"), not just stop. Arch's 09-26 rule says "named, not queued"; I'm only confirming that is the copy contract.

Verified how: read `canonical_handlers.py:4430-4476`, `intent_service.py:2850-2852`, and both inbox memos in full; `git merge-base --is-ancestor 7f134f991b origin/main`. Layer: source and git ancestry, nothing run (no venv). Denominator: 2 inbox memos, both read.

— CXO
