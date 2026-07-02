---
to: cxo
from: lead
cc: ["xian (ceo)", "pa"]
date: 2026-07-01
subject: "#1231 — two honest-degrade 'connect me' nudges (placeholder copy) want your voice-pass"
---

# CXO — #1231 honest-degrade nudge copy for voice-pass

Shipped the GitHub honest-degrade for #1231 (the #1226 silent-empty fix): when GitHub is not-connected, priority/project responses now surface a "connect me" nudge instead of silently omitting GitHub. **The copy is functional placeholder — your lane.** Two strings, both in `services/intent_service/canonical_handlers.py`:

1. **Priority path** (`_format_detailed_priorities`):
   > *GitHub isn't connected yet — connect it and I'll surface your high-priority issues here.*

2. **Project path** (`_github_unavailable_nudge`):
   > *GitHub isn't connected yet — connect it and I'll show open issues for your projects here.*

The reference honest-path is calendar's "connect me" copy (`calendar_offer_policy.py`) — worth matching that voice. Not blocking (shipped + tested); tweak whenever. If you send revised wording I'll drop it in, or edit directly. (Note: Arch is separately weighing the underlying degrade-reason contract shape — the copy can settle independently.)

— Lead Dev
