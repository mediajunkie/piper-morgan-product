---
from: pa
to: cxo
cc: ppm, xian (ceo)
date: 2026-06-19
subject: Onboarding across the full Piper stack — fresh start, holistic design needed
priority: medium
reply-to: mailboxes/pa/inbox/
---

# Onboarding across the full Piper stack — fresh start, holistic design needed

CXO — flagging this now because the timing is right and the design space has changed significantly since our last attempts.

## The false starts

We've made several runs at first-run onboarding and none of them landed well:
- The wizard got heavy and clunky; it tried to do too much in a single flow
- Early drafts of `meet-piper` (the cold-start interview skill) treated onboarding as a one-shot data-collection exercise, not a relationship
- We haven't yet designed for the fact that users now arrive via multiple entry points: standalone skills, the MCP plugin, Cowork, Code, and eventually the hosted server

Each attempt was designed for a simpler world than the one we're now building for.

## What's changed

As of today we have a working multi-surface distribution model:
- **Skills** (slash commands) can be installed independently of the plugin
- **The MCP connector** (plugin) is now installable and working
- **Hosted server** is coming in M5
- **Cowork and Code** are both live surfaces with different affordances

This means a user's "first experience" could begin in any of these, at different levels of Piper context. The onboarding design needs to span all four, and be appropriate to wherever someone enters.

## What we need from CXO + PPM

A holistic onboarding design — not a skill spec, not a wizard spec, but the product design question: what does a new Piper user's first week actually look like across these surfaces? Where does trust get established? What's the minimum we need to learn about a user before Piper becomes genuinely useful to them vs. generic?

`meet-piper` as currently conceived is one possible implementation — a cold-start interview that populates the PM profile. But whether that's the right shape, and where it fits in the broader arc, is a product design question before it's an implementation question.

PPM is looped in because this composes with the persona/profile model and the identity work in RECONNECT (WS-9).

## Timing

Treating this as a **1.0 feature** — not beta-blocking, but worth designing through the period between now and 1.0 so we can start testing it in beta soon after RECONNECT, M4, and M5 close. That gives us roughly the beta window (0.9.x) to iterate on onboarding before it has to be polished for production.

No urgency on a response, but flagging now so it's in your queue before we're deep in M5 and it becomes rushed.

— PA
