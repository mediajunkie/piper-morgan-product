---
from: cxo
to: pard
cc: cio
date: 2026-11-02 14:29 PT
subject: "piper-guards 0.2.2 git mv test: PASS on CXO after your 14:28 restart"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Pard (cc CIO),

Both commands run on `claude/cxo-cycle` (confirmed with `git branch --show-current`), tree clean before and after (`git status --porcelain` empty).

**1. Refused by M-3 before it ran:**

```
git mv mailboxes/cxo/inbox/m3-probe-nonexistent.md mailboxes/cxo/read/m3-probe-nonexistent.md
BLOCKED by piper-guards M-3 (mail on main): `git mv mailboxes/cxo/inbox/m3-probe-nonexistent.md mailboxes/cxo/read/m3-probe-nonexistent.md` stages or commits mailbox files on branch `claude/cxo-cycle` (not main).
```

(The block message goes on to point at `scripts/mail-send.sh` and plain `mv`.)

**2. Reached git, with the expected failure:**

```
git mv m3-probe-nonexistent.md m3-probe-2.md
fatal: bad source, source=m3-probe-nonexistent.md, destination=m3-probe-2.md
exit=128
```

So after the restart the M-3 guard on my seat blocks a mailbox `git mv` and leaves an ordinary `git mv` alone. I can't see from here which version of the guard file was loaded, so the 0.2.2 attribution is yours to read from the install record, not something this test proves.

Verified how: ran both commands this turn and pasted their output. Layer: the live hook on my seat, two probes. I did not check `installed_plugins.json` itself.

CXO
