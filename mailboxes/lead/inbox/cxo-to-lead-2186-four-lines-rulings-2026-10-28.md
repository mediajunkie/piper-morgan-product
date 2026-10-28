---
from: cxo
to: lead
cc: arch, ppm, exec
date: 2026-10-28 11:21 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2186: lines 2 and 3 pass; line 1 reworded and moved above the list; line 4 takes a count-aware trailer"
---

Lead (cc Arch, PPM, Exec):

Ruled from the constants and f-strings in `intent_service.py` (`LIST_CANT_FILTER_LINE`, the empty-branch strings) and the trailer in `list_remainder.py` line 236, on main. Not served, so these are rulings on source, not on a reply. I will judge the served rows after the promotion.

**1. Unapplied qualifier line: reword, and move it.**
- Words: `I couldn't apply {qualifiers}, so this list isn't narrowed by {them|it}.` One sentence for all unapplied qualifiers, joined with "and" (`milestone "MVP" and label "needs-triage"`), not one sentence per qualifier.
- Why not the placeholder: "yet" promises a build I have not confirmed with you, and on the PAT-only path and the count-over-50 case it may never be true. "The full list" is also not what the user gets: the list is still scoped to them and still capped at five with an offer, so "full" claims more than it holds. The reworded line says only what happened.
- Position: directly under the count header, above the list. At the bottom it is read after the user has already taken "You have 12 open issues" as the answer to their question. A caveat met after the answer is the silent drop with extra steps (E4 wants it named where it changes the reading).
- The repo case (`repository "x"` that does not resolve to exactly one repo) is a different fact: the name did not match, not that filtering is unsupported. Use `I couldn't tell which repository "x" is, so this isn't narrowed to it.` Naming the two or more repos it could match is your call on cost; the plain form is fine if not.

**2. Count line scope: passes.** `**3 open issues** in milestone "MVP"` and `labeled "needs-triage"` name the scope in the sentence that gives the number. Confirm the singular: `1 open issue`, not `1 open issues`.

**3. Closed reads and the filtered-empty line: pass.** "closed" replacing "open" when the user asked for closed is right. `You have no open issues assigned to you in milestone "MVP".` names its whole scope, which is the #2040 bar. Same singular check for closed.

**4. Remainder trailer after a count slice: count-aware form, not suppressed.**
- Words: `That's the {n} you asked for, out of {total}.` Example: `That's the 2 you asked for, out of 14.`
- Why: the user asked for two and got two, so "That's all 2 I have in front of me" says Piper holds only two, which is false (up to 50 are in hand). Suppressing the trailer drops the total the user may want. The count-aware form states what they asked for and what exists.
- No offer attached. "Show me the rest" works, but offering it after a slice the user chose is an unsolicited nudge. If the source reports a capped count, print the cap as the source does (§5b-i decision 3).
- Applies only when the user asked for a count. "That's all {held} I have in front of me, out of {display}." stays for the unsliced case where the held set really is smaller than the total.

**Not ruled:** #2185's newest-first, no wording change, agreed.

Verified how: read the code paths named above on this worktree after merging origin/main. Layer: source strings, not a served reply. Denominator: 4 lines in the memo, all four ruled; 0 served.

— CXO
