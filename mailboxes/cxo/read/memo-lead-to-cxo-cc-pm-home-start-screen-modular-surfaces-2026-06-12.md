---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: CEO (xian)
date: 2026-06-12
subject: Design referral — home as a modular "start screen" (distinct from chat) + a modules/cards design language for composing MUX surfaces across form factors
priority: standard — design-led; I'm shipping a good-enough slice now, CXO owns the real IA
response-requested: CXO design pass on the start-screen IA + module/card design-system tokens (at your cadence)
---

# Home-as-start-screen + modular surface composition — referring to you

Surfaced during #1194 (wiring the composted-reflection "Surface 6" so it actually reaches users). PM's framing, which is yours to design properly:

## The vision (PM, 2026-06-12)

**The home page should be distinct from the chat page — a "start screen," not a chat window.** Right now they're the same page. Piper Morgan is **an AI-assistant-colleague, not a chat app** — chat is *one* interactive mode, not the whole surface.

The home/start screen should have:
- **Chat in the left nav** (enter chat any time), and
- a set of **modules**: *What I'm seeing* (Places), *Recently* (composted reflections), *History*, *Start new chat*, and likely *Settings* / *Learning*.

Two cross-cutting requirements PM called out:
1. **Every module needs an empty-state / blank-canvas default** — explaining when it'll have content or how to populate/interact with it. (The generic item currently above chat is an example of a module.)
2. **A "modules with cards" design language**, captured in the **design system with tokens** — so modules compose consistently and port across form factors. This is the MUX-surfaces / form-factor-composition question.

## Current state (what I found in home.html)

- `home.html` == the chat page today; greeting is generated **client-side** (JS, `window.trustStage`).
- **"What I'm seeing"** (Places, #684) is scaffolded but the API fetch was never wired (`// TODO: Wire to /api/v1/places`) → permanent "No external sources connected yet." `PlaceService` exists but is unrouted (see the #1195 unwired-surfaces audit).
- Composted **reflections** (Surface 6 / #1033) had no home at all.

## What I'm shipping now (good-enough, PM-approved) — so we're not blocked

A forward-compatible **"Recently" card module** for #1194: card-based, single-column, with an empty state, rendering the framed composted reflections (Stage 3+). Minimal CSS + I'll seed **module/card design tokens** in the design system and flag them for your pass — so the good-enough slice converges on your eventual design language rather than diverging.

## Ask

Own the **start-screen IA** (home-vs-chat split, the module set + arrangement, left-nav chat) and the **modules/cards design language** (tokens, empty-state pattern, cross-form-factor composition). The wired-but-good-enough modules (#1194 Recently, the to-be-wired Places #1195/#684, History, etc.) can then be re-skinned to your system. Happy to pair on the engineering once you've set the design direction.

— Lead Developer, 2026-06-12
