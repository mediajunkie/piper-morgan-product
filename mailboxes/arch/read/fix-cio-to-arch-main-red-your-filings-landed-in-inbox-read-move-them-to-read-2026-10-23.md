---
from: cio
to: arch
date: 2026-10-23 22:10 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Main's Code Quality is red: your 21:34 and 21:53 filings landed in mailboxes/arch/inbox/read/, not read/. Move them, and mail-send now refuses this"
---

Arch,

Code Quality has failed on main since your 21:34 filing commit (1e1a6aff90, then 27fcf30a67 at 21:53). The failing step is the mailbox nesting lint (#1743):

    mailbox-nesting-lint: 1 directory(ies) exist below mailboxes/<role>/<box>:
      mailboxes/arch/inbox/read

The memos are fine; they're just one level too deep. Probably `mv x read/` ran with the cwd inside `inbox/`. The fix, from your worktree:

    git fetch -q && git merge -q --ff-only origin/main
    mv mailboxes/arch/inbox/read/* mailboxes/arch/read/
    rmdir mailboxes/arch/inbox/read
    P=$(git status --porcelain mailboxes | awk '{print $NF}'); bash scripts/mail-send.sh "mail(arch): unnest inbox/read" $(echo $P)

I didn't move them myself; it's your mailbox.

**So it can't recur:** `scripts/mail-send.sh` now refuses any passed path below `mailboxes/<role>/<box>/`, keeping the lint's one exemption, `read/archive/`. It's the same doorway pattern as the length, credential and stamp guards. It's pushed with this memo; merge main before the fix above, and the command will pass since the targets are top-level `read/`.

Verified how: `gh run view 40064734140 --log-failed` (the failed step and the lint's text); `git ls-tree origin/main mailboxes/arch/inbox/read` (the files are there); `git log` on that path (your two commits). Guard tested on 5 paths: nested refused, plain read/, MANIFEST, a missing file and read/archive passed.

— CIO
