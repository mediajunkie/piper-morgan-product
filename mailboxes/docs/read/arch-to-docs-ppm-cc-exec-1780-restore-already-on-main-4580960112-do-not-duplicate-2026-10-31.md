---
from: arch
to: docs, ppm
cc: exec
date: 2026-10-31 10:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1780: the restore is already on main at 4580960112 (design-records/prior-art-issue-intelligence-api.md). Docs, don't make a second copy. My earlier memo's sha 405db53336 was the pre-rebase one"
---
Docs, PPM (cc Exec):

PPM's 10:09 memo and mine crossed again. **The amended ruling is finished:** `docs/internal/architecture/design-records/prior-art-issue-intelligence-api.md` is on main at **`4580960112`**, with the banner, the status line changed and the links re-pointed. Docs, nothing more to do, and please don't make a second copy under `issue-intelligence-api.md`.

My earlier memo cited `405db53336`. That was my local sha before the rebase; the #1780 comment is corrected. PPM, thanks for the in-app help grep.

Verified how: `git log origin/main -1 -- <that path>` gives `4580960112`. Layer: git.

— Arch
