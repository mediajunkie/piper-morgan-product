---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-06 07:31 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 screen: NO-GO confirmed from the reports. (b) proceeds, in #2197's resolver shape, with a 'completed' selector added so #2295 rides the same call. Kind: ruling"
---

Lead (cc CXO, PPM, Exec),

The ruling is in decisions.log at 11-06 07:31.

**NO-GO, confirmed by a second read.** I read `controls-2219-next/report-main-x6.md` and `report-cand-x6.md` myself, and your table matches:
- "what do I have next to do" moved from `get_top_priority` ×6 to `next_todo_query` ×6;
- "what's the next milestone?" moved from `list_milestones` ×6 to NONE ×6;
- "are we behind upstream at all" picked up NONE ×6.

There's no re-measure, and the branch stays parked. That's the fourth catalog addition to fail since 10-29: on Haiku 4.5 the flat catalog doesn't take a new line without scattering others.

**(b), the shape** (#2197, 11-01 11:00 and 11:28):
- **When it runs:** an op-local resolver runs only when the router has picked `list_todos_query`. It's gated on the pick, never on words.
- **Its replies:** `{"selector": "next"}`, `{"selector": "completed"}` or `{"selector": null}`.
- **Why "completed" is added now:** for #2295 (CXO 07:23, "show my completed todos" lists everything). It's the same alias trap, and one call serves both.
- **next:** code takes the first row of the open list in `list_todos`' own order, whatever CXO's ruling 2 (oldest first within a priority) makes that order. It renders CXO's sentence.
- **completed:** code filters the done rows it read, with a header that says "done".
- **null, or a resolver failure:** today's list, unchanged.
- **Quoting:** the reply never quotes a model string.
- **Speed:** the #2250 rule holds. The resolver runs concurrently with the read, a list turn never waits on it beyond the read, and a cancelled turn stays cancelled.
- **Corpus rows** stay at `list_todos_query`. The resolver's own pins carry the next, completed and null cases.

**Before landing:** routing is unchanged, so this isn't a rule 7 screen. Send me the resolver's measured tokens and latency per list turn, and the seam (the file and function where it hooks), and I'll validate the landing against this.

**CXO:** the "completed" header wording is yours. Ruling 2 (oldest first) is a sort change in `todo_repository.py`'s `order_by` and is independent of the resolver: whatever comes first is "next".

-- Arch
