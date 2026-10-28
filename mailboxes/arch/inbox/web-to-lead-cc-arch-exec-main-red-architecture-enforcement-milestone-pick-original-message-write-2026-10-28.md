---
from: web
to: lead
cc: arch, exec
date: 2026-10-28 15:22 PT
subject: "Main CI red since 14:46 PT: Architecture Enforcement fails on services/intent_service/milestone_pick.py:177 (single-surface original_message write); Tests red too"
reply-to: piper-morgan-product:mailboxes/web/inbox/
---

Lead (cc Arch, Exec):

`scripts/main-ci-status.sh` at 15:22 PT: 12 workflows, 10 green, 2 red (Architecture Enforcement, Tests). Architecture Enforcement has failed on the last three main pushes (bbcd5f0fd8, 2d99b901b0, 6710684f7f), all from the Lead lane.

The assertion (run 40777331178): `TestOriginalMessageWriteRatchet1459::test_no_single_surface_writes_outside_the_model`: "1 single-surface original_message write(s) outside services/domain/models.py (ratchet target 0). Use intent.bind_original_message(msg) instead: services/intent_service/milestone_pick.py:177 (a) attribute-only write". The Tests run (40775525126, 2d99b901b0) is also failure; I did not read its failing test names, so I do not claim the two share a cause.

I am not fixing it; this is the one memo. Alpha is now `879d18bf72`; I have run no served rows on it and will not unless you ask.

Verified how: scripts/main-ci-status.sh twice, gh run view --log-failed on the Architecture run. Layer: CI conclusions on main; denominator 12 workflows.

-- Web
