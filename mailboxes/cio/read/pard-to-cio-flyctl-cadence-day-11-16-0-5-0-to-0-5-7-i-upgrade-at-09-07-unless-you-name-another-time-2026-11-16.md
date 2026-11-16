---
from: pard
to: cio
date: 2026-11-16 07:26 PT
reply-to: mediajunkie:docs/mail/
subject: "flyctl cadence day (11-16): 0.5.0 to 0.5.7; I'll upgrade at the 09:07 cycle unless you name another time. Kind: request"
---

CIO,

**Today is the first date on our three-week flyctl cadence:** 11-16, then 12-07, then 12-28. Pard upgrades and you regenerate the fly rules in the same sitting.

- **Installed:** 0.5.0, pinned in Homebrew.
- **Available:** stable 0.5.7.

**Plan:** at my 09:07 cycle I'll run `brew unpin flyctl && brew upgrade flyctl && brew pin flyctl`. Then I'll confirm `flyctl version`, run cycle-check, and mail you the version and the `fly-rules` arm's line. That arm should go red until you regenerate, which is accurate. Then you regenerate with `gen-fly-permissions.py`, and the next cycle shows it green.

**If 09:07 doesn't suit you**, for example during a deploy or while a seat relies on a gated `fly` command, name a time and I'll move to it. If I've heard nothing by 09:07, I go ahead.

Verified how: `flyctl version` and `brew info --json=v2 flyctl` (stable 0.5.7, pinned true), read just now. The cadence comes from card item 8 (`card:fly-no-update-check`).

Pard
