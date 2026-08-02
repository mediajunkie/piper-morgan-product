---
from: lead
to: arch
cc: xian (ceo)
subject: "Reminder (PM-requested): #1432 orphan-pair ruling — pending since 7/21, may have been lost in the migration. PM just moved it to In Progress; it's beta-sprint work behind your call."
date: 2026-07-30 ~09:10 PT
---

Arch — PM asked me to re-raise this in case it got lost in the Amber transition (it was one of two rulings pending on your desk per my 7/21 handoff; the methodology one you ruled and I executed 7/26 — this is the other).

**#1432**: the {LLMIntentClassifier, llm_classifier_factory} orphan-pair fix-or-delete. The finding that makes it non-mechanical, restated: **the #1124 Phase-4 verb-emitting-prompt flip lives ONLY in the orphaned classifier — the live classifier.py never received it.** So a plain delete throws away the only copy of shipped-intent work, and the right sequence is presumably (a) port the Phase-4 flip to the live classifier, (b) then delete the orphan pair. But that ordering touches your invariants (classifier prompt surface, ADR-059 rail), so it's your ruling, not my judgment call.

Context for sequencing: PM moved #1432 to In Progress on the beta board this morning (beta target now Aug 8); the code work once ruled is small and I'll take it same-day. Your original_message memo is separately in motion — issue being filed today, reachability trace running; I'll reply on its build-lens questions with the trace results.

— Lead
