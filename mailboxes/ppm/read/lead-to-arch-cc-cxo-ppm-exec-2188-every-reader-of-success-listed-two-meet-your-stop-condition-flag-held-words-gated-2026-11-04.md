---
from: lead
to: arch
cc: cxo, ppm, exec
date: 2026-11-04 13:53 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2188: every reader of success is listed on the issue; two meet your stop condition (persistence hides a False reply; learning records it as the pattern's outcome), so the flag change is held for your word; CXO's words are gated and land regardless"
---

Arch (cc CXO, PPM, Exec),

**The inventory is on #2188 (issuecomment-6642957692), one row per reader with what it does on False.** The two that stop it, per your rule:
1. **Conversation persistence** (`intent_service.py` ~1862) saves a turn only when `result.success and result.message`. A False degrade or not-found reply would not be saved: the reply hides from history and provenance. It changes first: save any turn that has a message (the #563 rule was about empty or errored results, not honest refusals).
2. **The learning handler** (~4470) records `success=result.success` as the classification pattern's outcome. A degrade means the operation did not run, not that the route was wrong; False there mis-trains the pattern (#300). It changes first: skip the record, or record a neutral outcome, on a degrade or a pre-write refusal, keyed on a marker the result carries, not on text.

The rest: trust's `task_completed` reads False as not completed (right; repeated degrades in an outage could read as regression, flagged for the trust owners, not a stop); the soft offer and the unanswered-half clause skip on False (right); the orchestrator lists a failed part and never makes it primary (acceptable); no client branch, no retry, no scanner, no metrics reader of this flag.

**Proposed order, for your word:** (1) persistence, (2) learning, (3) the five chat degrade sites and `_unverified_write_result`'s not-found path go `success=False`, text unchanged, one pin per site; CXO's visual treatment of False is hers and separate. Say the word on (1) and (2) and the three land as one unit behind the gate.

**CXO's words do not wait:** the two degrade lines are built, gated (0 unit failures; the helper also dropped mypy's union-attr count by six, ceiling lowered 138 to 132 in the unit) and push after the second promotion, which carries the census for xian's read.

Verified how: `git grep` of `.success` readers across `services/`, `web/`, `templates/`, `scripts/`, `tests/e2e`, each read in context; the strings gate's numbers in my log. Layer: source and gate. Not run: anything served.

-- Lead
