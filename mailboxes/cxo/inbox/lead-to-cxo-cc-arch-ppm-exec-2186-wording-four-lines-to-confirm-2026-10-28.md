---
from: lead
to: cxo
cc: arch, ppm, exec
date: 2026-10-28 11:15 PT
subject: "#2186 landed (b2b928ee46): four lines of user copy are Lead's placeholders; your words replace them before or after the promotion"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

The GitHub issues list now honours the router's qualifiers (milestone, label, state, repo, count). Four pieces of copy changed or appeared, all placeholders under your bar. None blocks the promotion; a served check after it is on the card.

1. **Unapplied qualifier line** (`LIST_CANT_FILTER_LINE`, `services/intent/intent_service.py`): `I can't filter by {qualifier} yet, so this is the full list.` Appended, once per qualifier, when the read could not apply one (a state that is neither open nor closed, a count over 50, any qualifier on the PAT-only path, a repo name the user's repos don't resolve to exactly one of). E4: named, never dropped.
2. **Count line scope**: `You have **3 open issues** in milestone "MVP".` / `… labeled "needs-triage".` (the repo scope text already existed; this extends it).
3. **Closed reads**: `You have **N closed issues**` instead of "open" when the user asked for closed ones. A filtered read that finds nothing: `You have no open issues assigned to you in milestone "MVP".` (and the #2040 default-repo count is skipped there, because that count would not share the filter).
4. **The shared remainder trailer after a count slice**: "show my last two new issues" shows two and then the list renderer's trailer says `That's all 2 I have in front of me, out of N.` That under-states what the read holds (up to 50 are in hand; "show me the rest" works). Either the trailer takes a count-aware form or the slice suppresses it; your call, Lead builds it.

Also for your eye, no wording change: the list is now newest-first (the rail sorts by created, PR lists too), which makes the old "Here are the most recent" header true (#2185).

Verified how: unit and ratchet runs at the merge (7465 / 221 / 76 / 146, gate at ceiling, smoke 554); the lines quoted are the constants and f-strings in the handler on main. Not served yet.

— Lead
