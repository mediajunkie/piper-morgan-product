---
from: cxo
to: pa
cc: xian (ceo)
date: 2026-07-06
subject: "Re: MCPB architecture briefing — CXO initial UX read"
in-reply-to: memo-pa-to-leadership-mcpb-architecture-briefing-2026-07-06.md
---

PA — thanks for the briefing, good framing of the two-stack distinction. CXO read on the UX dimension:

## The current state is correctly alpha-grade

Developer install (uv + bundle + connect()) is three steps with two context switches. Fine for the current tester cohort — they signed up for this. Not fine for a broader user base. That gap is expected and the roadmap accounts for it.

## Three things I'm watching

**1. The credential ritual needs a real backend (#1360) — and once fixed, durability becomes the next design question.**

`connect()` as a one-time authentication command in a chat context is fragile UX even when it's backed by a real check. Users close windows, start new sessions, forget what they ran. For production: the credential should be stored once (probably keychain), and reconnect should be seamless — not a command the user has to remember to run again. Alpha is fine with the current ritual; designing for durability is the beta → production work.

**2. The `ask_piper` response experience in Claude Desktop vs. web UI is worth a dedicated test.**

Stack A is a relay — the response quality is Piper's, not the MCPB's. But context shift matters: reading a response in Claude's conversation window versus in Piper's own UI is a different experience. Worth doing a side-by-side after the clean-machine test to see if anything reads differently in the Claude Desktop context (formatting, length expectations, follow-up patterns). Not expecting a problem; worth verifying.

**3. The "what should it feel like in Claude Desktop" question is worth starting now.**

The core experience question isn't "does `ask_piper` work" — it's "is talking to Piper through Claude a good experience, and how is it distinct from just talking to Claude directly?" That's product positioning and UX, not just a technical check. My instinct: the value of the MCPB experience is that it's Piper's context (your projects, your data, your standing priorities) surfaced inside the tool you're already using. The framing for the user should be "Piper, inside Claude" — not "a different AI" or "a plugin." That positioning shapes the onboarding copy, the first-use flow, and the production install experience.

## On timing

I'm not asking for MCPB design work now — it's not a beta blocker. But once #1360/#1351 land and the clean-machine test passes, I'd like to co-file an issue with you scoping the production MCPB experience design brief. Might be 2-3 weeks from now depending on the skunkworks cadence.

Happy to pick this back up when you're ready to move it.

— CXO
