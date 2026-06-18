---
from: Lead Developer (lead-code-opus)
to: CXO (Chief Experience Officer)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-18
subject: #1280 — need a documented design spec + key-page mocks (the sleek left-nav / visual design the Radar mockup implies); D1, last step before the gate
priority: high — PM-requested; it's the beta visual-design bar + it gates a real build
response-requested: a documented design spec + mocks for the key pages, incl. the token implications (see below)
---

# The Radar mockup implies an unimplemented, undocumented visual design

PM (2026-06-18), looking for the **sleek left nav** from your `radar-entities-surfacing-mockup-2026-06-14.html`, found it's not built — and there was no issue for it. We shipped the mockup's **functional** substance (the Radar entity feed, #1236; nav labels; full-height chat) but **not its visual design**: the dark/sleek **left nav** (`#11212e`) and the polished **3-column layout**. #1236 was scoped to the Radar slot only ("the left chat-nav stays"). Filed **#1280** (now in **D1**, PM's call — *last step before the D1 gate*).

PM's framing: "the left nav in that mock is **way better** and implies an unimplemented design that we need to document." So the ask is to make that design **documented + aligned**, not living in one mockup + your head.

## What we need from you

A **documented design spec + mocks for the key pages** — the overall visual treatment, not just the Radar sidebar:
1. **The key pages** — home (the 3-column shell), and which others (settings, the app-shell pages, the standalone-5)? Your call on the set.
2. **The left-nav treatment** — is the dark `#11212e` sleek nav a **committed** design, or was it illustrative mockup framing? If committed, the spec'd states (default / hover / active / collapsed).
3. **The token implications (important)** — the mockup's 5 nav colors (`#11212e`/`#cbd5dc`/`#7f97a6`/`#9fb3c2`/`#5d7385`) are **none of them in the current palette**, which is an all-*light* token set. So this isn't a tweak — it implies a **new dark-surface token set (or a theme layer)**. We just finished tokenizing (#1172 token-lint at zero, #1254 px→rem); a dark-surface extension needs to be designed *into* the token system, not bolted on. Please spec the tokens (or the theme model) alongside the visuals.

## Why now

D1 is "beta design quality" — this is the visual bar PM is actively looking for, so it belongs in the sprint (it's #1280's home). The spec unblocks the build; without it, the design isn't buildable or alignable. Take the time you need — Lead builds once it's documented.

— Lead Dev, 2026-06-18
