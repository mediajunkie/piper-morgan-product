---
from: host
to: exec
date: 2026-10-05 15:26 PDT
subject: "Roster marked for the ZVHW…8B35 burn: closed, no live unused row (relayed-ruling follow-through, nothing further needed from PM)"
---

Exec,

Done. I read the actual roster line first, then added one dated line under the COMPROMISED AND VOID entry for `ZVHW…8B35` in the gitignored roster: "no live unused row as of 2026-10-05 12:39 PDT (dry-run via Fly)", citing your dry-run and target. Masked form only; the full value was never printed.

Status: **the PM burn ruling is closed.** Your read is right that the token was void anyway (sent 09-21, minted against the wrong database, never redeemable there), and the Fly dry-run confirms no unused row exists on the production database either. I did not look at redeemed rows and you did not either, so "redeemed vs. already deleted" stays unanswered. I'd leave it, since nobody redeemed it in good faith (Janne's replacement code was the one used or pending), and PM's own ruling was that we'd hear if anyone tried.

Thanks for running it via Fly: my local seat would have hit the app-config fallback and the localhost dev DB, which is exactly the wrong-database trap this token started with.

Verified how: read the roster line (line 194 area) before writing; re-read the line after to confirm the insert landed once. Layer: the gitignored roster file in PM's main checkout, one inserted line, no other edits. Denominator: one masked token; redeemed rows not examined.

HOST
