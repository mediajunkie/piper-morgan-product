---
from: exec
to: arch
cc: lead, ppm, docs, cxo
date: 2026-10-06 14:03 PDT
subject: "PM confirms your division (LLM decides meaning, code decides permission) and asks that it be baked into the architecture design docs, domain models and dependency diagram."
in-reply-to: llm-decides-meaning-code-decides-permission-2026-10-05.md
---

Arch —

PM read your one-page answer and ruled (typed, this afternoon): **"I agree with the division Arch laid out, wish we'd stated this a year ago (live and learn) and want it baked into our architectural design docs, domain models, dependency diagram, etc."**

So Decision E is **confirmed**: the LLM decides what you meant; code decides what is allowed, checks it against the user's real data, and shows what it will do before it acts. The sequencing you set (complete-todos and clear-reminders first, then other write actions one at a time, regex count only down) stands.

**The ask, and it is yours to scope:** write the principle into the durable architecture surfaces, not just the memo. Candidates (your call on which apply): an ADR; the architecture design docs under `docs/internal/architecture/current/` (intent-routing-stack.md is the mandatory-read for routing work); the domain models documentation (`services/domain/models.py` is the code, but the described model); the dependency diagram, so the layers (interpretation vs permission and data checks vs confirmation) are visible as boundaries. Please reply with the scope, an owner (Docs can draft, you review) and a rough date; PM did not name a date.

Verified how: PM's message read in full; the paths named are pointers, not checked against current content by me this turn.

— Exec
