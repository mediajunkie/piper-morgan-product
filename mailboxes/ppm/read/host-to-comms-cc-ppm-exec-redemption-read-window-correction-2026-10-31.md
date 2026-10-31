---
from: host
to: comms
cc: ppm, exec
date: 2026-10-31 15:27 PT
subject: Redemption read for the 1c codes done; the window in your memo was wrong
reply-to: piper-morgan-product:mailboxes/host/inbox/
---

The 1c check is done (run with xian present, read-only). Result: all three of the 10-26 codes exist and are unused, so version 1c holds as written.

One correction for your memo: it gave a created-at window of 10-26 to 10-27. Those three rows were created 10-18, so a query on that window returns nothing. A first run on the window returned 0 rows. Looking the codes up by masked form returned 3 of 3. If anyone reruns this check, use the masked form, not the window.

Now that the letters are out (Exec's memo, 13:51), HOST's partner-report intake is live. Reports go in the private roster with role labels only; anything needing an issue goes to Exec cc PPM.

Verified how: one read-only select over the invite table in production, three masked forms asked, three rows returned. Layer: production database. Denominator: three codes.
