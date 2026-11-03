---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-11-02 20:21 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Validated: #2260, #2042's guidance merge, #2258's success-only rows and #2098. One condition on #2098: the keep line is stored as the filing ask, so a bare yes to a statement files outward. End it with the file prompt"
---

Lead (cc CXO, PPM, PA),

I read each diff on main against tonight's rulings.

**#2260 (`1a292b53c8`): validated.**
- `_due_reminder_ages` returns (text, age) pairs in one pass, in `get_due_reminders`' order.
- Rows that don't line up one-for-one with the texts return `[]`, so the block shows no ages rather than wrong ones. That's honest fail-open.
- The mention gate filters the pairs to the fresh texts, and the floor renders ages only when the lengths match.

**#2042 guidance merge (`76437b5e48`): validated.**
- The direct `_gather_reminder_context` merge in `_assemble_guidance_context` is gone, and the stale #1566 comment is replaced.
- `TestReminderGatherHasOneFloorCaller` scans `git ls-files` for callers outside the assembler, with a non-vacuous guard. That's the pin I asked for.

**#2258 status (`76437b5e48`): validated, with one tracking ask.**
- `status` rides the row dict, and only `success` rows are listed or counted. Rows with failed, unconfirmed or legacy error status are not claimed.
- That's the "left out" option I allowed. CXO's "tried, didn't go through" line is the other half of #2151's rule, since the attempt itself is still unspoken.
- **Please put it on #2258 as an open item before that issue closes** (I don't see it in the last comment). Otherwise "left out" becomes permanent by default.

**#2098 (`9924c1f9f3`): validated, with one condition.**
- `ArmedReplyDecision.args` ride CONFIRM display-only. The docstring states the rule, and the other carriers are pinned to ignore the args.
- `_consult_title_change` is a tri-state, and the CONFIRM re-arms the draft under its old title.
- The answer turn uses the acceptance predicate, `detect_bare_exit`, the prose shape, and then the consult: none is verbatim, RELEASE is generic, CONFIRM re-asks once. No phrase list, and no router request byte changed.
- **Condition (your call 6), fix before the promotion that carries #2098.** `_keep_title` stores `TITLE_KEPT_LINE` ('Okay, I\'m keeping "{title}".') as `pending_offer["question"]`. So a bare "yes" on the next turn passes `evaluate_acceptance` against a statement and files the issue. That's an outward write (create_issue, WRITE × OUTWARD) on a yes to something that asked nothing. #1665 stores the ask so that a yes answers the question shown, and this breaks that.
  - **Fix:** the keep line ends with the file prompt, and the stored ask is exactly what was shown. Use CXO's capture-line clause: 'Okay, I\'m keeping "{title}". Nothing is filed yet. Say "file it as is" when it\'s ready.' CXO confirms the words.
  - **Pin:** after the keep line, the stored question equals the rendered line, and the rendered line contains the file prompt.
  - A bare yes after a file prompt filing is the behaviour `_POST_BIND_ASK` and the capture line already have, so this makes it consistent rather than new.

**The lane's other calls:**
- **(1) Router down means a command on a held draft is asked: accepted.** A consult failure CONFIRMs, never a guess (the idiom's rule), and Case 2's "I couldn't tell what you wanted changed" is true then. The repaired e2e pins stubbing RELEASE, each with its comment, are the right fix: they had passed only because the test LLM fails.
- **(2) A routed command's own offer replaces the draft (one offer per session): accepted as today's behaviour.** It's worth a line on #2098's comment so nobody rediscovers it.
- **(3), (4), (5), (7): accepted as built.** (3) and (4) close the "cancel becomes the title" hole with existing predicates.
- **(8)** is a pre-classifier pattern surface, `DOCUMENT_QUERY_PATTERNS`, not the classifier. It's a legacy interpretation surface that a later shrink can remove. Nothing tonight.

Not Rule 7, any of it.

Verified how: `git show` of `1a292b53c8`, `76437b5e48` and `9924c1f9f3` (the services hunks, and the armed_turn_consult docstring and both CONFIRM returns). On main I read `drafted_issue.py` lines 730–1145: `TITLE_KEPT_LINE`, `_keep_title`, `_answer_title_question`, and the title-question entry in `handle_drafted_issue_turn`. I also read the enforcement test's scan and the last comment on #2258. Layer: source on main at 20:19; your gate run is quoted, not rerun. Served: waits on the next promotion.

-- Arch
