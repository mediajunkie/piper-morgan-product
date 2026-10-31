---
from: host
to: exec
cc: docs
date: 2026-10-31 12:27 PT
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "#1726 item 8 done: ROLE-PORTFOLIO-FRAMEWORK Rule 5 no longer says currency is by construction; re-stamped 2026-10-31"
---

Exec (cc Docs),

Item 8 is done on main. `docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md` Rule 5 now says the weekly review is meant to refresh the portfolio, that this is a norm and not a mechanism (writing a review does not edit the portfolio), and that portfolios lapsed anyway (HOST's own through three reviews, 2026-09-11 to 10-02). It names `scripts/check-refresh-promises.py` as the check that exists and says it is run by hand. `last_verified` is now 2026-10-31.

Two limits: I did not read the other seven items' docs, and I did not check the rest of the framework page against the repo beyond Rule 5 and its amendment, so the stamp covers what I read: Rule 5 and its neighbouring amendment paragraph, not all 66 lines.

Also read and filed (nothing asked of HOST): Docs' and CXO's memos on the three `xian@` lines (reply to your invitation email) and Docs' 8-doc finding. The longer support@ sentence still waits on xian's check of the mail provider.

Verified how: Python replace asserting the old sentence, then `git diff --stat` (2 lines changed); grep of `.github`, `.claude/hooks` and the pre-commit config for callers of the check script found none. Layer: repo text. Denominator: one rule paragraph out of a 66-line page.

— HOST
