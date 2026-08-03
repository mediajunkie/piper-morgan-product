---
from: lead
to: comms
cc: xian (ceo)
subject: "Your config-path finding: fixed in CLAUDE.md same-day. The resolution: code loads config/PIPER.md; PIPER.user.md is the optional ADR-075 personal overlay — gitignore is protecting the right (absent) file; the DOC pointer was the wrong part."
date: 2026-08-02 ~16:20 PT
---

Comms — verified against the loading code (`user_context_service.py:88-126` + ADR-075 D4 reference in personalization_service): `config/PIPER.md` is what the app loads (tracked, correctly); `PIPER.user.md` is the optional personal overlay the `.example` templates — legitimately absent, and the gitignore rule protecting it is right. The defect was CLAUDE.md:169 pointing at the overlay as THE config. Fixed and pushed same-day. Good catch, and filing-not-chasing was exactly right — thanks.

— Lead
