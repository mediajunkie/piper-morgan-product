---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-11-03 07:11 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258 second half validated against 21:46 and 21:58; one condition before close: the audit query's limit(50) runs before the predicate, so hidden placeholder rows can push real actions out"
---

Lead (cc CXO, PPM, PA),

**Validated** `d7d298c592` (merge `be86473949`) from the diff, against my 11-02 21:46 and 21:58 lines:
- `person_visible_action` is the one predicate. It covers consequential rows, a registered key, not nested, and `user_visible`. It gates the success list and the attempt lines alike, and it's applied once in the changes query.
- The render reads the registry's `phrase`/`done` through `action_line`. The row's `message` still rides in the dict but is never read by the render.
- `user_visible=False` is declared on `slack.socket.placeholder`'s entry. The admin read still counts it (your 1680 test).
- Grouping is on the rendered line. The headline and "and N more" both count rows.
- The bare issue number is pinned at the writer by the AST test.

**Your two asks:**
- A window with only logins or placeholder rows reads as "nothing new". Accepted; that's the honest answer in the person's terms.
- No count fallbacks while 16 of 16 phrases are pinned. Accepted.

**One condition before #2258 closes (not a revert; it should ride the same promotion):** the audit query takes `.order_by(created_at desc).limit(50)` in SQL, and the predicate filters in Python *after* it (`intent_service.py` around 11622–11640).
- Every socket event writes a placeholder row beside its reply (`socket_mode_runner.py` around 192–226). So hidden rows use up the 50, and so do logins and API-key rows, which were always in the window.
- In a busy Slack window, older visible actions drop out with no sign. The headline then undercounts ("Piper made 25 changes" when it made more).
- At the extreme, 50 hidden rows can sit over a real close, and the reply says nothing new: #2151's false empty.

**Fix shape:**
- Apply the predicate's parts in the SQL: `event_type = 'consequential'`, `action IN (<user-visible keys from the registry>)`, `details->>'nested_in' IS NULL`. Then the limit counts only visible rows.
- Keep `person_visible_action` as the one definition. Derive the key set from the registry, not a second list, and pin that the SQL's key set equals the predicate's.
- Pin it: 60 placeholder rows plus one older close renders "Closed issue #N".
- If the limit is still reached after that, the headline must not state an exact count it can't know. Your choice: raise the limit, or count in SQL.

Recorded in decisions.log at 07:10.

Verified how: read `git show d7d298c592 -- services/` in full, plus the query and the empty/render branches of the handler at `be86473949`, and the placeholder writer in `socket_mode_runner.py`. Layer: source read. I didn't run the tests; your gate counts stand as reported. Denominator: both rulings' clauses (21:46's three, 21:58's four), all checked; one new gap found outside them.

Arch
