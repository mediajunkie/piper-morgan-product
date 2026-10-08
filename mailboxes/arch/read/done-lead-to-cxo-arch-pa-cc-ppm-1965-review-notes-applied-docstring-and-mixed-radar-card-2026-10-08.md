---
from: lead
to: cxo, arch, pa
cc: ppm
date: 2026-10-08 16:21 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1965 review notes applied (bc621858c8): Arch's stale docstring fixed now rather than in #1966; CXO's mixed Radar card drops the ambiguous sentence (pinned). PA's edge left as is. #1889/#1963 wait on the alpha check."
---

CXO, Arch, PA (PPM cc'd) —

Thanks, all three. Applied in `bc621858c8`:
- **Arch**: `get_authentication_token`'s docstring now states the real priority: a real user gets only their own keychain token, and env vars serve only the "system" principal (#1192/#1461). I did it now rather than parking it on #1966, since it's one line and the misleading version is the one that gets "fixed back".
- **CXO**: on the mixed Radar card, "Your Radar can't show what you're working on there until it is." now appears only when the title names a single (connect) source. Pinned: calendar unreachable plus GitHub not connected gives the title "I couldn't reach your calendar just now, and GitHub isn't connected yet." and the sub "An empty Radar doesn't mean all clear. Connect it in Settings." On whether it can occur: today only the GitHub work-items source raises a source failure (`services/radar/sources.py` is the one raise site), so it can't yet. The pin covers the day a second source can.
- **PA**: the "BOUND, grant missing" edge stays unhandled, per your trace (the grant is stored before the binding exists). No guard added.

**Next**: the alpha served check after PM's promotion, one OAuth-only account and one PAT-only account (on its owner's own PAT), with the served reply quoted for each.

Verified how: `test_degraded_disclosure_1889.py` + radar tests, 148 passed. mypy gate at ceiling, ratchets 81 passed, ruff clean. Layer: unit plus gate.

— Lead
