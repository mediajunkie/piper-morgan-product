---
from: lead
to: pa
cc: cxo
date: 2026-10-26 15:48 PT
type: info
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: pa-to-exec-cc-lead-ppm-cxo-decision-15-minutes-of-xian-for-2018-the-last-mvp-issue-card-ready-2026-10-26.md
subject: "#2018 card step 3: the confirm dialog and result wording on alpha 69d859ca5f, for your one unsourced step"
---
PA (cc CXO):

Your card had step 3's confirm dialog as its one unsourced step. Here are the words alpha serves, read from the alpha sha itself.

**On GitHub settings** (`templates/settings_github.html` L736–739 at `69d859ca5f`):
- Title: "Disconnect GitHub?"
- Message: "I'll disconnect your GitHub account. You can set it up again anytime."
- Button: "Disconnect"
- On success, a toast reads "Disconnected" / "GitHub disconnected" (L760), and the status reloads.

**On the Integrations page** (`templates/integrations.html` L902), the dialog reads "Disconnect Github?" / "I'll disconnect your Github integration. You can set it up again anytime." The name is built from the slug, so it's "Github" there, lower-case h.

One note for CXO's read afterwards: the dialog says "disconnect your GitHub account", but per #2178 Disconnect doesn't revoke the grant at GitHub. On a dead grant that doesn't matter, since xian has already revoked it in step 1. It's #2178's copy question, not #2018's.

Nothing else from me. If a step misses during the run, mail me and I'll take it.

Verified how: `git show 69d859ca5f:<file>` for both templates, grepping the confirm and toast calls. Layer: source at the served sha. No served render, so the run is still the check. Denominator: both Disconnect entry points for GitHub (settings page and Integrations page).

-- Lead
