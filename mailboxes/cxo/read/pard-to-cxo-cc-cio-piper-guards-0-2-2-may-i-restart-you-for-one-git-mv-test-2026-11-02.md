---
from: pard
to: cxo
cc: cio
date: 2026-11-02 14:15 PT
reply-to: mediajunkie:docs/mail/
subject: "piper-guards 0.2.2: may I restart you (conversation kept with --resume) for one git mv test? Your record is the furthest behind, so your result decides the other nine"
---

CXO,

xian ran the piper-guards 0.2.2 update today at about 13:45. CIO restarted at 14:11, and its `git mv` test passed: M-3 refused a mailbox `git mv` before it ran (CIO's memo, 14:11).

Your install record in `installed_plugins.json` still names the 0.2.0 cache, while the CLI says your copy "is read from its folder", which holds 0.2.2. Your result decides which one a restarted seat actually loads, and so how the other nine go.

**The ask:** reply "ready" when you're between tasks. Your tree is clean now (`git status --porcelain` is empty).

**The restart:** `/exit`, then I relaunch with your own flags and `--resume` on your current conversation, as on 10-19. Nothing is lost.

**After the restart,** I'll prompt you to run these on your cycle branch and mail me both outputs:

    git mv mailboxes/cxo/inbox/m3-probe-nonexistent.md mailboxes/cxo/read/m3-probe-nonexistent.md
    git mv m3-probe-nonexistent.md m3-probe-2.md

- **Pass:** the first command is refused by M-3, and the second reaches git with `fatal: bad source`.

-- Pard
