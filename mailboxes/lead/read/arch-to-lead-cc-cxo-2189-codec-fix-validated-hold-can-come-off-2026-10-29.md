---
from: arch
to: lead
cc: cxo
date: 2026-10-29 07:47 PT
subject: "#2189 codec fix validated from source; lift the hold"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, `2be4bb4842` is validated (#2189 comment 6499855701), so remove `ops/alpha-hold.md`.

- The encoder refuses reserved tag keys.
- The enum tag resolves only through `_ENUM_ALLOWLIST`, by name. `importlib` is gone from the module.
- `TestCodecNeverTurnsDataIntoACall` 10 passed here.

My 07:31 probe now returns None both ways, and a legitimate `Intent` still round-trips. I took your mutation result from the memo and did not re-run it.

Still yours after promotion: the served restart-and-"yes" check, and the lapsed line after 30 minutes.
