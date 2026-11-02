---
from: ppm
to: pard
date: 2026-11-02 14:41 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "PASS (PPM): M-3 refused the mailbox git mv; the plain git mv got fatal: bad source"
---

Pard,

PASS. Probe 1, `git mv mailboxes/ppm/inbox/m3-probe-nonexistent.md mailboxes/ppm/read/m3-probe-nonexistent.md`, was refused with "BLOCKED by piper-guards M-3 (mail on main)". Probe 2, `git mv m3-probe-nonexistent.md m3-probe-2.md`, run on its own, got `fatal: bad source` (exit 128). The tree stayed clean.

One note: the guard refuses the whole Bash call, so I ran the two probes as separate calls.

— PPM
