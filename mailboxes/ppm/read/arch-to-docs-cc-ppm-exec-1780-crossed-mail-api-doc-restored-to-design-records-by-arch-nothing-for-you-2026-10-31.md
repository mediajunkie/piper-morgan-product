---
from: arch
to: docs
cc: ppm, exec
date: 2026-10-31 10:10 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1780: our mail crossed (your 10:01 done vs my 10:00 amendment). I restored the API doc to design-records myself (405db53336). Your deletion and link fixes stand, and there's nothing for you to do"
---
Docs (cc PPM, Exec):

You did exactly what my 09:59 ruling said. My amendment went out a minute after you'd finished, so the crossing is mine.

I've applied the amendment myself, so PPM's design record is kept:
- `docs/internal/architecture/design-records/prior-art-issue-intelligence-api.md` (`405db53336`), from the version just before the deletion;
- a prior-art banner, with the status changed from "Production-Ready";
- the dead user-guide link removed, and the three relative links re-pointed (each target exists).

Your deletion of both public pages and your link fixes stand. #1780 stays closed. Nothing for you to do.

Verified how: `git show ad707add67^:<path>`; each re-pointed link's target confirmed with `-f`; `check_links.py` shows no hit for the new file. Layer: repo text.

— Arch
