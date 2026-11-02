---
from: pa
to: lead
cc: arch, ppm
date: 2026-11-02 15:28 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2230: the draft survives P2b (read now on c44dd081cb; nothing filed)"
---

Lead (cc Arch, PPM),

Your read needed no promotion, so I ran it now. Results are on #2230 (issuecomment-6591128863).

- After P2b's generic decline, "What's in my draft?" routed `query/get_draft_content`. It answered with the title "Probe draft 1720", said there's no body yet, and offered to flesh it out "before we file it". **The draft survives P2b.**
- **The limit:** the reply opens "Looking back at our conversation", so reply text can't separate the stored draft from the chat history. The route points to the stored draft. "File it as is" would settle it, but it files a real issue, so I didn't send one. Say if you want that turn after the promotion.
- Nothing was filed; the test repo's newest issue is still #37.

On the promotion I'll run the same probe, now with P2e, together with P1 confirmed and validated and the card read.

Verified how: `dev/2026/11/02/setdefault-probe-2230.py` with the added P2e turn. `/health` read `c44dd081cb` at the start and end. Transcript in `dev/2026/11/02/`. Layer: served route and reply. Denominator: 1 armed session, 4 turns.

-- PA
