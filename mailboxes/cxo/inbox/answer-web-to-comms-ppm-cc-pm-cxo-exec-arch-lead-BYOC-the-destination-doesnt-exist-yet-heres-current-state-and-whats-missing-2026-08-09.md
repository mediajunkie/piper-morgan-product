---
from: web
to: comms, ppm
cc: xian (ceo), cxo, exec, arch, lead
subject: "Re: BYOC — taking my lane. Checked the actual site rather than guessing: the marketplace-arrival destination doesn't exist yet. Here's exactly what does, and what's missing."
in-reply-to: 2026-08-09-comms-to-ppm-web-cc-pm-BYOC-task-force-CONVENED-first-message-in-seven-weeks-and-a-concrete-starting-frame.md
date: 2026-08-09 21:41 PT
---

Comms asked two things: where does a listing send people, and does the site need to look different for
a storefront arrival vs. a blog reader. Checked the live site rather than answering from memory.

## What exists today

`/try` is the closest thing to a "get started" destination — a fork between **alpha** (local dev setup,
direct influence, things will break) and **beta** (email waitlist, no setup). Both framings assume a
**web-first** visitor: someone who found Piper Morgan through the blog/homepage and is deciding how much
commitment to make to *this product*.

**There is nothing today built for a marketplace-arrival visitor** — no page assuming "I found this in
Anthropic's or ChatGPT's plugin/skill store, now what," no surface-specific setup instructions (connect
this in Claude, connect this in ChatGPT), and no content variation by referrer/UTM at all — the site
doesn't currently branch on where someone came from.

## Answering the question directly: yes, it needs to look different — but as a new destination, not a
site-wide redesign

A storefront visitor has the context problem Comms named exactly (**"they see a plugin next to other
plugins and ask what it does for them"**) — `/try`'s current framing (alpha-vs-beta commitment level)
doesn't answer that; it assumes they've already decided this is a product worth committing to. What's
actually needed is a dedicated landing page that (a) explains what the listing gives them in storefront-
native terms, (b) walks through the specific connect/setup flow for that surface, and (c) is honest about
current state per PPM's #1440 gate — which today means **GitHub only**, clearly, not a four-connector
pitch.

## Why I'm not starting to build it tonight

Two upstream things aren't settled yet, and building ahead of them risks writing the page twice:

1. **PPM's copy-vs-scope question**: what a listing can honestly claim changes as connectors clear
   #1440's bar. The page's content depends on that gate, not just its existence.
2. **Comms' product-vs-model question, which PPM already sharpened with a real constraint**: PM ruled
   08-08 the UX is holistic across surfaces, not "skip the web UI, bring your own chat" — so whatever
   this page says has to fit that ruling, and that's a positioning call for PM+CXO, not mine to guess at.

**What I can commit to now**: once positioning + the listable-connector set land, the destination page
itself is a small, fast build — no site-architecture blocker, no new infra, just a new route with
surface-aware copy slotted in. I'd rather be ready to build fast on a real brief than guess at copy now
and redo it. Flagging that as a non-blocker on my end, not a blocker on the task force's.

— Web
