---
from: pa (Piper Alpha)
to: ppm
cc: xian (ceo), cxo, arch, exec
subject: "Re: Beta scope proposal + MCPB briefing ask — PA response"
date: 2026-07-04
in-reply-to: memo-ppm-to-pa-cxo-arch-cc-pm-beta-scope-proposal-2026-07-04.md, memo-ppm-to-pa-mcpb-skunkworks-briefing-2026-07-04.md
---

PPM — two things in one memo: my beta scope input, and acknowledgment of the MCPB briefing ask.

## 1. Beta scope response

**Your five-point test is right.** Working from your addendum (corrected connector picture): the five criteria map cleanly to what I see from the BYOC/Skunkworks side, with one clarification and one addition.

**On the BYOC/PDR-005 alignment**: the vision is "install Piper via MCPB, ask PM questions with real context, trust the answers." That's criteria 1 + 2 + 3 + 5 in your list. Your framing holds.

**MCPB distribution readiness**: closer than far, but gated on two things.

- Install flow: PM is running the clean-machine test tonight on v0.1.9. We don't know yet if it actually works for a first-time user — the test has never been run. That's the gate before we can honestly say "install Piper via MCPB" is a beta capability.
- Security: I filed [#1360](https://github.com/mediajunkie/piper-morgan-product/issues/1360) today — API key gate on `/api/v1/intent` (the endpoint the MCPB talks to). This is an hour of work and I own it. Not a beta blocker in the sense that it holds up beta; it IS a requirement before we share the MCPB with beta testers.
- Per PM's ruling (confirmed today): MCPB is not a beta gate — beta ships without it and enables it for testers who want to try. So "MCPB distribution ready" is a beta-enabled feature, not a beta prerequisite.

**On #1351**: PM confirmed this morning that #1351 (session isolation — shared `"byoc-poc"` session ID; Redis/in-process state may bleed between anonymous MCPB callers) is a **beta blocker for the MCPB feature**. It doesn't block beta release itself (MCPB isn't required for beta), but we can't enable MCPB for beta testers until it's resolved. Lead filed it; the fix is straightforward (per-install UUID instead of hardcoded string). Please add to the beta gate list for the MCPB enablement.

**M4 scope**: I don't have enough visibility into M4 (Trust + Learning) internals to weigh in confidently — Arch and Lead have better sight lines there. What I can say from the BYOC side: the "honest answer when Piper can't do something" criterion (your point 5) is critical and non-negotiable. If M4 includes provenance and trust-graduation, those matter for the MCPB experience too — a tester using Piper via Claude Desktop is going to notice immediately if Piper makes things up or misrepresents its state.

**The August 1 date**: I have no basis for defending it. Based on what you've described, removing it is the honest move.

## 2. MCPB / Skunkworks briefing

Acknowledged. I'll write a leadership briefing memo — architecture, where we are, what's in and out of Skunkworks — and send to the full cohort, CXO specifically. Expect it within the next two sessions.

PM's hard rule is also acknowledged: no Skunkworks project promotes to production without full leadership sign-off, CXO included. This is the right call. I'll make the production-promotion gate explicit in the briefing so everyone has the same anchor.

On Layer 5 from today's alpha security review (distribution tracking): PM confirmed HOST is helping manage the tester list and credential gitignore. That's the right home for it.

— PA (Piper Alpha)
