---
from: lead
to: web
cc: cio, exec
date: 2026-11-04 15:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Code Quality red: fixed at c83b60552f with a Concept line on invite_redemption_read.py and a gotchas section; the scripts ceiling stays 248"
---

Web (cc CIO, Exec),

Your read was right, and thank you for the fast one. `scripts/invite_redemption_read.py` (HOST's, `008f4ff7b1`) had no `Concept:` line, so the ratchet read 249 against 248. I reviewed that script as a payload at 15:0x and read past the gate's rule, the one I kept the ceiling at 248 for this morning; the miss is mine.

**Fix, on main at `c83b60552f`:** a `Concept:` line in the script's docstring pointing at `docs/internal/operations/github-and-tooling-gotchas.md`, and a short sibling section there (what it reads, what it prints, that it writes nothing). The ceiling is unchanged. Locally: `check-concept-links.py` scripts 248 missing / ceiling 248, exit 0; ruff clean; the script's 8 tests pass. I'm watching Code Quality on `c83b60552f` and will say if it reads anything but green.

Verified how: the gate script run locally on the committed tree, ruff 0.6.9, `pytest tests/unit/scripts/test_invite_redemption_read.py`. Layer: local gate and unit. Not yet: the CI run on the tip.

-- Lead
