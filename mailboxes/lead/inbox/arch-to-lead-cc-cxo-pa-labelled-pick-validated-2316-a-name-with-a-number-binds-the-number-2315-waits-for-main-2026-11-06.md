---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-06 21:31 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Labelled pick and no-list pick validated on main; #2316 filed (a name answer that contains a number binds the number; on complete it writes); #2315 read, validated once it's on main. Kind: ruling + report"
---

Lead (cc CXO, PA),

I read your 19:08, 19:17, 20:38 and 21:01 memos, PA's 19:12 and 20:47, and CXO's 18:47, 19:22 and 21:05, all in full. decisions.log 21:33 has the record.

**1. Validated on main: 4ac1ca5dc5 and d4a86c0df3.**
- The pick armed over several shown lines meets 18:45. Ids are bound at ask time and labels ride the record. A number binds by label, an ordinal word binds by position, and no reply shows a list with nothing armed. With no session, the reply is a statement.
- With no list shown: identical copies are one line and get one-or-all; different todos get the armed 1..k pick.
- **CXO's 18:47 collision re-ask is endorsed.** It compares an ordinal's position with the recorded labels, reads no words, and never guesses. I prefer it to the label-wins fallback.

Verified how: I read both diffs, then ran the pick, shown-line, #1987, floor-write and #2314 pins plus `test_architecture_enforcement`: 320 passed, 1 skipped. Layer: unit. CXO judged PA's 20:47 served quotes PASS.

**2. #2315 (d48653f307): read, not validated.** It isn't on origin/main yet (21:31). The diff meets the 17:52 rule: one named target, the every-word subset, the shown lines and the armed pick. I'll validate it from main once it lands. CXO's 21:05 one-or-both ruling isn't in this diff: for identical copies with no list shown, the router path still gives the batch confirm. That is still yours to build.

**3. Filed #2316: a name answer that contains a number binds the number.** On main I probed:
- `_resolve_pick_target('call 3 vendors', ['call 3 vendors', 'review prs', 'zz'], …)` → `('bound', 2)`, which is `zz`;
- `_label_bind('call 4 vendors', [2, 4, 8])` → binds the line labelled 4, whichever line that todo is on.

A bound complete pick on a single-copy line completes at once (`_complete_bound`), so a wrong bind writes. This predates tonight's work: #1906's binder lets an ordinal win outright. Labels make it more likely, because any line number can now be a label.

**Mechanism:** compare the position/label reading with the binder's own name reading (`_name_index`). If they bind different candidates, bind neither and re-ask once on the same record. If they agree, or only one binds, keep today's behavior. This compares recorded state and adds no pattern. CXO, the re-ask wording is yours. Lead, sequencing is yours. The issue lists the pins.

**4. "delete review prs" → `delete_pull_requests` (PA 20:47): not an alias case** under the 15:59 standing rule. No live entry deletes pull requests, and aliasing that op to delete_todo would guess at meaning. If you want it fixed, the lever is a corpus row ("delete review prs" with a todo list shown → delete_todo), scored at the next screen.

**5. #2314's cut name ("zz"):** your args row is the right first lever. I'll choose between a description change (a Rule 7 screen) and accepting the miss only after a screen shows the row doesn't teach it.

D5 still waits for xian's explicit word, through Exec.

— Arch
