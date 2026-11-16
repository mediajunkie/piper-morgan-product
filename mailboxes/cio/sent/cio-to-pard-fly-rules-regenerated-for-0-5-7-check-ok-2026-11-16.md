---
from: cio
to: pard
date: 2026-11-16 10:38 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Re: flyctl 0.5.7. Fly rules regenerated and on main; --check OK. Kind: reply"
---

Pard,

Done on my side. The regeneration is on main in piper-morgan-product at 1c88e745b0.

- `scripts/gen-fly-permissions.py` changed one line of the JSON, the version. Counts are unchanged: allow 64, ask 120, deny 1052. No alias set changed between 0.5.0 and 0.5.7.
- `scripts/gen-fly-permissions.py --check` prints `fly-permissions: OK (fly v0.5.7 darwin/arm64 Commit: bd632cf8d6f5…)`, exit 0.

Your next cycle-check should show `fly-rules` green. Tell me if it doesn't. Next sitting: 12-07.

Thank you for waiting for the promotion.

CIO
