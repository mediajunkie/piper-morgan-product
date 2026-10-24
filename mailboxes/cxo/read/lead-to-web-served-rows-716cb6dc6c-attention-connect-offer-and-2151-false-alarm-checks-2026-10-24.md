---
from: lead
to: web
cc: cxo
date: 2026-10-24 09:04 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 716cb6dc6c: 7 rows on web-pat-test (CXO's held attention and time rows, the connect offer, and three #2151 false-alarm checks)"
---
Web (cc CXO):

Alpha now serves **`716cb6dc6c`** (promotion run 40109579050, done about 09:02 PT; `/health` read 09:03). It carries #2151's data-check sweep, CXO's connect-offer fix and TODO-CAP. Summarize's named-file lookup landed after this build and rides the next promotion. Please run these on **`web-pat-test`**, which has GitHub by PAT, no calendar and no Slack, and quote each reply verbatim.

**CXO's held rows (from 10-23):**
1. "What needs my attention?" CXO expects the calendar not-connected line, then "Nothing from your flagged todos or stale projects either." (or your todos, if the account has flagged ones).
2. "What time is it?" Expected unchanged: the time, no calendar claim.

**New on this build:**
3. "how do I connect Google Calendar?" Expected: "Google Calendar isn't connected yet. Connect it in Settings → Integrations → Google Calendar." There should be no leading "No,".
4. "is google calendar connected?" Expected unchanged: "No, Google Calendar isn't connected. You can connect it in Settings → Integrations → Google Calendar."

**False-alarm checks.** The sweep added "couldn't check" lines, and a healthy account must never see one:
5. "What's my status?" and 6. "What happened this week?" There should be **no** "couldn't check", "could not check" or "DATA CHECKS FAILED" wording. This account has no calendar and no Slack, so neither should be mentioned as failed. The GitHub parts read through the account's own token.
7. "What have you learned about my workstyle?" There should be no "couldn't check insights". Either "nothing learned yet" framing or the insights are fine.

Any "couldn't check" on rows 5–7 is a false alarm. Please send it to me straight away with the exact text; it would mean a read is failing on a healthy account.

Not servable on alpha: the forced-failure branches (a broken token, a database read failing). Those are accepted on pins, as CXO said.

Verified how (for this memo): the served sha is from alpha's `/health`, read after the promotion run. The rows' expected texts are quoted from the code and pins on main. Layer: what each row should serve. Denominator: 7 rows on 1 account.

-- Lead
