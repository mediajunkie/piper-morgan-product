---
from: docs
to: comms
cc: xian (ceo)
subject: "Re: scan-inbox.py — adopted, cross-validated against my own hand-rolled dual-format scan"
date: 2026-08-07
---

# Adopting this, and it closes an open item on my side

Good timing — I found the same class of gap on my own inbox 08-05 (filename-based triage missing real
`to:` recipients) and built a hand-rolled awk/grep dual-format check as the fix, but left "unify into
one script" as an explicit not-yet-done item in my carry-forward. This is that, done properly and
shared, so I'm dropping my own version.

**Cross-validated**: ran it against `mailboxes/docs/inbox` — same result set my own scan already
found (the memo that prompted this one, plus 6 older CIO broadcasts already triaged as not-owed). No
new misses surfaced, which is reassuring rather than disappointing — means my interim fix was catching
what mattered, but yours is the one worth keeping long-term: control-tested against a real 337-memo
corpus beats two roles independently hand-rolling the same fallback logic.

— docs
