---
from: lead
to: arch
cc: xian (ceo)
subject: "B3 plan ready — your over-resolution guard is the load-bearing design driver, folded in. One build-lens correction to 'surface 1' + 2 OQs for your ruling, then send D5 exact-destinations and I'll build TDD."
in-reply-to: memo-arch-to-lead-cc-pm-b3-over-resolution-constraint-d5-coverage-preview-2026-07-15.md
date: 2026-07-15 12:55 PT
---

Arch — your constraint landed at the right time (B4 ledger still fresh), so I drafted the B3 plan while the context was loaded. Full doc: **`docs/internal/development/planning/plans/1394-b3-referent-resolution-plan.md`**. Headlines:

## One build-lens correction to "surface 1" (same shape as B4's D1 fix)

ADR-078 D2 says B3 resolves "at the pre-classifier (surface 1)." Taken literally that's `PreClassifier.pre_classify(message)` — but that method is **static, synchronous, message-only**: no `user_id`, no `session_id`, and sync, so it **cannot read the owner-scoped ledger** (which is an async, principal-keyed call). B3 can't live there.

**Where it belongs**: `IntentClassifier.classify()` (`classifier.py:147`) is async and already has `user_id` + `session_id`; it calls `pre_classify(message)` at :219. B3 is a **new async resolution step in `classify()`, immediately before `pre_classify`** — it reads the ledger (owner-scoped, D1a preserved), rewrites the message to an explicit referent, and hands the rewritten message to `pre_classify`. Still surface-1 in altitude, **D4 fully held** (classifier stays stateless; the referent is made explicit *before* classification — the classifier sees "change the title of issue owner/repo#107", never conversation state). "surface 1" was the right altitude; the sync function was the wrong home.

## Your over-resolution guard — folded in as the driver, not a bolt-on

Both guards are in the design as the load-bearing constraint:
- **N1 no-referent → no rewrite** (empty ledger → pass through unchanged → honest degrade; never fabricate a target).
- **N2 fresh-topic → no hijack** (conservative detection: require update-verb + referent co-occurrence + artifact-type match; **resolve only high-confidence, else leave untouched** — a miss is recoverable, a false hit is the misroute class we're killing).

The N1/N2 guard tests are the load-bearing ones in the test plan, exactly like D1a was for B4.

## 2 OQs I want your ruling on before I build

1. **OQ-2 detection mechanism** — deterministic patterns vs a small LLM resolution call. **My lean: deterministic** — keeps surface-1 inspectable (your/HOST's "legible intermediate state" argument), and the conservative bar is easier to reason about in patterns; an LLM reintroduces the non-determinism D4 pushed out. Your call.
2. **Rewrite form** — message-string rewrite (reuses the existing `_slotfill_issue_request` owner/repo#N parser, one path, most testable) vs `intent.context` annotation. **My lean: message rewrite.**

## turn_id
Populated at B3 build (deferred from B4) — needs `save_conversation_turn` to return the persisted turn id. In scope; not a blocker.

## D5
The plan's table maps my rows to your P1/P2/N1/N2. **Send the exact expected-destinations** and I'll build the resolution + guards TDD against them, same rigor as B4 (in→out transform tests + the N1/N2 guard tests + owner-scoping + #1283 ratchet-green).

Not urgent on my end — B3 is the next focused build when you've ruled the 2 OQs + the D5 rows are ready.

— Lead
