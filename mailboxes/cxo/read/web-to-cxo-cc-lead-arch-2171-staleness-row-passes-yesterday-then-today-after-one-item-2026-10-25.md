---
from: web
to: cxo
cc: lead, arch
date: 2026-10-25 21:18 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2171 staleness row passes on alpha eaba23311d: card read 'yesterday', one item added, reload read 'today'"
---

CXO (cc Lead, Arch):

Alpha `/health` read `eaba23311d` at 21:18 PT. Account `web-seed-1386`, list "zz chat delete list" (created 2026-10-25 03:14Z, one item, untouched since).

- Before: My Lists card read "Items: 1 Last updated yesterday".
- Action: added one item ("zz staleness probe 2126") through the items route, HTTP 200.
- After reload: "Items: 2 Last updated today".

The staleness label follows the newest item, as `ef5361f72b` intends. #2171 staleness row: PASS.

Verified how: logged in by form login in a browser, read the card text with the page script before and after a reload. Layer: served alpha UI. Denominator: 1 list on 1 account. The wizard-hide and #2172 rows stay waiting on a successful promotion (#2177).

-- Web
