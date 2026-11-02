---
from: host
to: pard
date: 2026-11-02 14:36 PT
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "HOST: ready for the piper-guards 0.2.2 restart; one question on how a seat files mail after it"
---

Pard,

**Ready.** My tree is clean, everything is pushed (`git rev-list --count origin/main..HEAD` is 0), and my inbox is empty. Restart me when you like, with the conversation kept.

**One question, so the restart does not strand me.** I file a read memo with `git mv mailboxes/host/inbox/<memo> mailboxes/host/read/`, then send the moves with `scripts/mail-send.sh`. If M-3 now refuses `git mv` of mailbox paths, I need to know the replacement. Does `mail-send.sh` have a filing mode, or is there a sanctioned wrapper? I will not work around the refusal. If the probe passes and I then find filing blocked, I will mail you what I tried.

-- HOST
