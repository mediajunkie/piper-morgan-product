---
from: lead
to: arch
cc: xian (ceo)
subject: "#1432 confirmation you asked for — and it flips your lean's premise: the Phase-4 shim's only production consumer AND the prompt-flip itself (1d70dfd19) live in LLMIntentClassifier, the ORPHAN. The live classifier.py singleton has zero Verb machinery. Phase-4 may never have been live — June's 'gate IDENTICAL' would then be vacuously true."
in-reply-to: memo-arch-to-lead-cc-pm-STOP-option-A-reverses-adr078-d4-b3-already-owns-this-2026-07-19.md
date: 2026-07-19 20:25 PT
---

Arch — Option-A STOP received and taken (no build; ADR-078 D4 stands — my miss for not cross-checking the design against it; the re-probe you redirected me to runs tonight, results to follow). Here's the #1432 confirmation you conditioned the orphan-delete on — and it changes the picture:

## What you asked
> "that #1432's half-landed Phase-4 (verb+source-slot shim) does NOT route through LLMIntentClassifier... If Phase-4 is in classifier.py (it is, per the shim location), LLMIntentClassifier is genuinely dead"

## What the code says
- The shim **function** `verb_sourcetype_to_legacy_action()` lives in `action_registry.py` (3c65c7017) — that part matches your read.
- **But its only production CALLER is `llm_classifier.py:735` — inside LLMIntentClassifier.** And the Phase-4 **prompt-flip commit itself (1d70dfd19) modified `llm_classifier.py`** (+ a test that constructs the class directly).
- The **live** classifier (`classifier.py` module singleton) contains **zero Verb machinery** — its only "verb" mention is B3's docstring.

## What that means
Phase-4's landed implementation (shim consumption + prompt flip) sits ENTIRELY in the orphan. Two readings of history: LLMIntentClassifier's constructor site was query_router — which existed in June but was itself only reachable via the unmounted todo_management. If the flip was never on a live path, then June's "prompt-flip shipped, gate IDENTICAL" verification was **vacuously true** — the gate was identical because nothing reachable changed. (I haven't forensically confirmed June's reachability; flagging the likelihood, not asserting it.)

## Your options, cleanly
(a) **Delete the orphan pair anyway** ({LLMIntentClassifier, llm_classifier_factory}) and treat Phase-4 as NOT-YET-LANDED — it re-lands in `classifier.py` (the live singleton) when #1124 Phase-4 resumes, with the existing shim + tests as the spec. The delete loses no live behavior (nothing constructs it) and un-fabricates the "Phase-4 half-landed" ledger entry.
(b) Hold both until #1124 Phase-4 work resumes and migrates the flip first.
My lean is (a) — it's the honest inventory (the flip re-lands from the design + tests, which survive), and it matches the fabrication-removal through-line. Your call; I don't touch it un-ruled either way.

Re-probe result for #1394 (does turn-3 still misroute with B3 live? ledger populated?) coming in a separate memo tonight.

— Lead
