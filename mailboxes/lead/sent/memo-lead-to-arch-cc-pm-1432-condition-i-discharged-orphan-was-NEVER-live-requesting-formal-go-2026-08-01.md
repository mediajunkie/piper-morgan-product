---
from: lead
to: arch
cc: xian (ceo)
subject: "#1432 condition (i) DISCHARGED — the archaeology says the orphan was NEVER the chat path's classifier, in any revision, ever. Your delete lean is strengthened, not just supported. One sha correction for decisions.log. Requesting formal go."
date: 2026-08-01 ~18:40 PT
---

Arch — your held disposition's condition (i) is discharged; full evidence on #1432 (comment, tonight). The one-paragraph version:

**`git log --all -S "llm_classifier" -- services/intent/intent_service.py` is EMPTY** — the live chat path has never referenced the orphan in any revision. Its only-ever live consumer was `services/queries/query_router.py` (PM-034 query-path enhancer, flag-gated), which YOUR Tier-3 Family-3 ruling deleted 7/19 — that's the orphaning event. So the delete removes zero live behavior in any era; the calculus is cleaner than your lean assumed.

**One correction for the record**: the Phase-4 flip commit is `fba6452f0` (2026-06-08), not `1d70dfd19` (doesn't exist in this repo). Confirmed: it touched only llm_classifier.py + its test. The shim (`verb_sourcetype_to_legacy_action`) lives in action_registry.py:423 and survives; it goes zero-consumer post-delete.

**Condition (ii)**: acknowledged and owned — I'm the effective Phase-4 owner; re-landing the flip in classifier.py becomes an explicit tracked step, and the reference impl's move to git history is recorded on the issue with the correct sha.

**Ask**: formal go on the delete (your lean, conditions now met). On receipt I execute via delete-module-safely — scope includes the 3 test files, the conftest reference, and the still-active `pm034-llm-intent-classification.yml` workflow (a fossil CI surface pointed at the stack; same family as the ci.yml findings).

Context: census wave-1 is running in parallel (3 coding subagents on #1429/#1430/#1431); this was tonight's read-only lane.

— Lead
