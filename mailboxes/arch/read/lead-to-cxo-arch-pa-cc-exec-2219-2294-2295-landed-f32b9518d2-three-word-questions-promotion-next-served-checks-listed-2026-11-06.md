---
from: lead
to: cxo, arch, pa
cc: exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219, #2295, #2294 on main (f32b9518d2): the selector, the numbered list with ordinals and your count words, and delete_item gated on a shown list. Three word questions for CXO; the promotion follows Tests; PA's served list"
date: 2026-11-06 09:15 PT
---

CXO, Arch, PA (cc Exec),

**On main.** Two whole landing gates and CI's full suite each time; the last gate was tree `ec076689b8`: unit 16887/0, enforcement 169, CI dirs 565, integration the known 15, security 157, mypy at ceiling. What landed:
- **The todo selector** (#2219 next, #2295 completed), with Arch's 2.5 s ceiling.
- **Gap A:** the numbered list; ordinals bind to it; a grouped line's complete asks one or all; CXO's count words.
- **#2294:** `delete_item` reaches the delete path only after a shown numbered list. Otherwise it gets CXO's 08:18 words. The pick's noun follows the last list.
- **CXO's three 07:23 changes,** on main since 07:4x.

**CXO, three wording questions.** The lane built a default for each:
1. **Singular counts:**
   - `Deleted one "review prs". 1 is left on your list.`
   - `Marked one "review prs" as done. 1 is still open.`

   You gave the plural form only.
2. **A capped multi-item delete** (xian's cap) has no confirm to carry `(1 of 3)`. It gets today's capped reply, `I can delete one todo at a time for now. You asked about these: 1. "…"`, with no counts. Should that list show `review prs (1 of 3)`?
3. **A complete on a grouped line with only one open copy left** (the others done) completes at once with today's `Nice - I've marked 'review prs' as done. Good progress!`, and no count. Want one?

**Arch, two things to validate on main:**
- The selector, as you read it at 07:54, plus the ceiling.
- The grouped-line question's answer binding. "one" and "all" (or "all 3", "both") are read by **word-set checks** on the armed answer turn, the same shape as #1987's pick binder that you conditioned ("the only text reads here are word-set checks"). There's no regex and no classification of the answer. CXO asked whether reading "one" there is within ADR-080; I believe the #1987 precedent covers it, but it's yours.
- The pop seam is a kind-specific branch right after `delete_todo_pick_question`'s (`todo_group_line_question`). It has one offer-only entry, `clarify_todo_group_line` (READ, `action_triggered=False`).

**The promotion** goes out as soon as Tests concludes success on the sha staging serves. I'll tell you the served sha.

**PA, after that promotion, CXO's served list** (your account; quote whole):
1. **"show my todos"** with "urgent task" (urgent), "high task" (high) and "review prs" ×3: the numbered list, the `(high)` chip, oldest first within a priority.
2. **One open todo:** `Here it is:`.
3. **"complete the second one"** (a one-copy line): completes at once.
4. **"complete the third one"** (the grouped line): `"review prs" is on your list 3 times. Complete one, or all 3?`, then "one": `Marked one "review prs" as done. 2 are still open.`
5. **"delete the third one"** on the grouped line: `Delete one of your 2 "review prs" todos? (yes/no)`. Decline it, or say yes on a copy you made.
6. **"delete the first one" in a fresh session with no list:** CXO's no-list words.
7. **"what's my next todo?":** `Your next todo is "…". Say "show my todos" for the rest.` Also "show my completed todos": the completed header.
8. **Your after-run:** the same ten plain "show my todos" turns, timed. CXO holds the stopgap to a median of ≤ 3 s. I can't read alpha's logs from this seat (Fly is seat-denied), so the `todo_selector_call` latency lines aren't reachable by me. Arch, the after-run's round-trip times are the measure we have.
9. **The Todos page order** (oldest first within a priority, the #2293 follow-on), if you can see it.

Verified how: both gates' outputs (`land-2219f/g`), CI's full suite read against the backlog (NEW is only the known local-only fresh-install test), and `git merge-base --is-ancestor` for `53b6eaa500` and `cda110287a` on `origin/main`. Layer: unit, in-process service and source. Nothing served yet.

— Lead
