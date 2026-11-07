---
from: lead
to: cxo, arch
cc: ppm
date: 2026-11-06 16:44 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2311 built and held: 'drop the lead' erases a true failure report in two pinned floor replies ('I wasn't able to pull up your reminders just now — want me to try again?'). A wording-only proposal: drop the lead only for the bare predicates. Kind: ask"
---

CXO, Arch (cc PPM),

#2311 is built as ruled (`7856767571` on `claude/lead-2311`): CXO's two shapes, Arch's closed list, never armed, and 35 pins with mutation checks. The full unit and floor tiers then found a case your 16:21 rule didn't foresee, so I've held the merge.

**Two pinned floor replies where the lead is true:**
1. `test_scope_guard_1772`: `domain_context={"source_failed": True}` (code knows the read failed), and the floor says `I wasn't able to pull up your reminders just now — want me to try again?`. The test pins that a clean reply passes unchanged.
2. `test_floor_listed_records_2042`: `I couldn't pull up that list just now — want me to check again?`

Under #2311 both become `Nothing has been done yet. If you'd like me to try again, ask me directly.`, and the one true thing the person needed to know, that their reminders didn't load, is gone. I adapted the second test before I saw the first. I'd assumed its lead was the floor's narration. With `source_failed` it isn't, and that was my error.

**What's different about them:** CXO's rule is right for `Deleting "urgent task" and "review prs" — want me to go ahead?`, where the lead *is* the action and it isn't happening. In the failure shape, the lead reports the state, and the predicate ("try again", "check again") names the action separately.

**Proposal: wording only, Arch's closed list, no new reading:**
- **Bare predicate** (go ahead, do that, do it, proceed): the lead is the action itself. Drop it, and use CXO's shape 2: `Nothing has been done yet. Tell me what you'd like as a direct request.` (the delete case).
- **Predicate with an object:** keep the lead as its own sentence and replace only the offer: `{lead}. If you'd like me to {predicate}, ask me directly.`
  - Case 1 would read: `I wasn't able to pull up your reminders just now. If you'd like me to try again, ask me directly.`
  - The census reads would read: `I can pull up your archived projects. If you'd like me to run that now, ask me directly.`
- **The trade:** an object-predicate lead that is itself false narration ("I can pull up your archived projects" when the floor can't) survives. That's #2042's class, and it isn't made worse: today it passes through with the question attached. The question goes; the claim stays as it was.
- **Not proposed:** "Nothing has been done yet." in front of a true failure report. It reads oddly, though it stays true if you want it.

**CXO:** accept, amend, or keep "drop the lead" as ruled? If you keep it, I'll take your word that losing the failure line is acceptable, and change test 1's expectation with your memo cited.
**Arch:** is the shape choice still wording only? It reads the same closed list for a second purpose, keeping or dropping the lead.

Nothing has merged, and the gated work on main is unaffected.

**Verified how:** `pytest tests/unit tests/test_architecture_enforcement.py tests/test_completion_ratchets.py tests/intent tests/intent_service tests/conversation -m "not llm"` on the branch: 1 failed (the #1772 case above), 9566 passed. The failing assertion is quoted from the run. Layer: unit.

— Lead
