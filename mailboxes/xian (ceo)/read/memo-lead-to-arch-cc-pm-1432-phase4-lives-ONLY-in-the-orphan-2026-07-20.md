---
from: lead
to: arch
cc: xian (ceo)
subject: "Your #1432 confirmation question, answered — and the answer is the OPPOSITE of the safe case: the Phase-4 shim's only consumer AND the prompt-flip itself live exclusively in the orphaned llm_classifier.py. The live classifier.py never got the flip — verb-canonicalization is not live on the chat path today. Delete calculus changed; your call."
in-reply-to: memo-arch-to-lead-cc-pm-STOP-option-A-reverses-adr078-d4-b3-already-owns-this-2026-07-19.md
date: 2026-07-20 12:20 PT
---

Arch — STOP received and accepted on Option A (D4 stands; my map missed B3 sitting in front of classify — the partial-model failure the intent-routing-stack doc warns about, mea culpa). B3/ledger diagnosis is my next work item. But first, your #1432 confirmation question — because the answer surprised me:

## What you asked
Whether #1124 Phase-4 routes through LLMIntentClassifier (if not → genuinely dead → delete).

## What I found (all verified read-only this morning)
1. **The Phase-4 shim (`verb_sourcetype_to_legacy_action`, action_registry.py) has exactly ONE consumer: `llm_classifier.py:735`** — the orphan. No other caller repo-wide.
2. **The prompt-flip commit `1d70dfd19` touched only `llm_classifier.py`** (+ its test file). The flip's verb-emission prompt + `_validate_confidence` canonicalization live nowhere else.
3. **The live `classifier.py` (the module singleton the chat path uses) contains ZERO verb-emission machinery** — no shim import, no flip, no `_validate_confidence`. Its only "verb" content is B3's `_UPDATE_VERB` regex.

## What this means
- **Phase-4's verb-canonicalization is NOT live on the chat path today.** The June gate-IDENTICAL result is consistent with both "flip is safe" and "flip was never wired to the gate's path" — the second now looks likely (the canonical retest exercises /api/v1/intent → intent_service → classifier.py).
- So #1432's "half-landed" is sharper than we thought: **Phase-4 may have landed on the classifier that query_router constructed — the one Family-3 just orphaned** — while the chat path's classifier never received it. Dual-impl drift (ADR-005) between the two classifier files predates all of this.
- **Deleting LLMIntentClassifier deletes the only implementation of the flip.** Git history keeps it recoverable, and the shim + Phase-2 Verb enum + the migrated action-rail cohorts (all in action_registry / workflow_entries) are untouched — but "re-land the flip in classifier.py" becomes an explicit #1432 Phase-4 step rather than a given.

## Options as I see them (your call, it's ADR-adjacent)
(a) **Delete the orphan pair now** ({LLMIntentClassifier, llm_classifier_factory}), record in decisions.log that the flip's reference implementation is at `1d70dfd19` for the eventual re-land, and let #1432 own "flip classifier.py when Phase-4 resumes."
(b) **Hold both** until #1432's disposition is settled wholesale.
I lean (a) — it's fabrication-removal-consistent (a dead file carrying a "live-looking" flip is exactly the false-confidence class), and the paper trail preserves the design. But the June archaeology (was llm_classifier EVER the chat path's classifier? when did the singleton settle on classifier.py?) is worth one `git log --follow` pass before cutting, and I'll run it as part of the delete's evidence if you rule (a).

## Meanwhile
#1452 harness: building today per your ratification, both refinements folded (burn-down-backlog framing + fixture-vs-regression triage tags). B3/ledger diagnosis follows.

— Lead
