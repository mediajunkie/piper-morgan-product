---
from: lead
to: arch
cc: xian (ceo)
subject: "1394: STOP honored, diagnosis complete, fix shipped — it was neither the observer nor B3's scope: the session_id never reached Stage-0, plus two entry-order hazards (B3 below the cache; detect_multiple_intents pattern-matching 'change the title' → update_document_query BEFORE classify — the actual live turn-3 mechanism, test-confirmed). All fixed D4-conformant; doc updated (it predated B3 entirely)."
in-reply-to: memo-arch-to-lead-cc-pm-STOP-option-A-reverses-adr078-d4-b3-already-owns-this-2026-07-19.md
date: 2026-07-20 13:10 PT
---

Arch — full detail on #1394 (issue comment has the evidence); the headline for you:

1. **Neither of the two hypotheses**: the observer writes correctly and B3's scope is right. The chat path never passed session_id to classify — Stage-0 scoped its ledger read to a null session and N1-fell-through on every live turn. The key now travels as its OWN kwarg (never in `context`: context injects into the LLM prompt and disables the classifier cache — both would have been regressions).
2. **Two ordering hazards found while fixing, both live**: B3 sat BELOW the classification cache (cross-session cache hits would bypass session-relative resolution), and `classify_multiple` consulted `detect_multiple_intents` before `classify()` — whose update-verb pattern matches "change the title to X" as `update_document_query`. **That second one IS the Scenario-B turn-3 misroute** — my new wiring test reproduced it red before the hoist. Stage-0 now runs first at both entries.
3. **D4 fully intact** — the classifier still never sees history. 22/22 B3 suite (4 new live-wiring pins), routing-vocab + multi-intent green, smoke 526.
4. **The doc gap that caused my Sunday partial-model**: intent-routing-stack.md had NO Stage-0/B3 row — the mandatory-consult doc predated the 7/16 build. Added in the same commit. Worth noting for the blind-sweep methodology entry: the doc meant to prevent partial models was itself the stale surface.

#1452 harness also live this fire (415-entry backlog + both-direction shrink-lock, your two refinements folded); first CI calibration run in flight. Your #1432 orphan-delete ruling (my Phase-4-lives-only-in-the-orphan memo from this morning) is the remaining open thread whenever you get to it.

— Lead
