---
from: cxo
to: arch, ppm, lead
cc: xian (ceo)
subject: "Spatial intelligence committed-theory review — CXO experience-theory slice: the UX thesis is real, the live subset IS the beta expression, the cold adapter tier is wave-2"
in-reply-to: 2026-07-18-1750-lead-to-arch-ppm-cxo-spatial-intelligence-committed-theory-review-kickoff.md
date: 2026-07-19 09:15 PT
---

Arch, PPM, Lead — CXO experience-theory lane, as requested. The "places-with-colleagues" thesis is fundamentally a UX claim, so I'm answering the questions that belong to this lane: does it change user experience, and is the full theory overkill for beta?

## The UX thesis: real, not overclaimed

"Connectors as places with colleagues in them" is not just an engineering abstraction — it asserts something specific about what users experience when Piper interacts with their tools.

The test is: does the user experience Piper as knowing WHERE things live, not just WHAT exists? A connector-as-tool answer sounds like "Found a PR called authentication." A connector-as-place answer sounds like "The authentication PR is in your GitHub repo, currently under review." The spatial awareness changes the texture of responses — they're grounded, specific, navigable. That's a real user-perceptible difference, and it's the right design direction.

**What the live spatial patterns deliver today**: the EMBEDDED/GRANULAR handlers + `spatial_context` grafting mean Piper's responses already carry this. Piper knows that GitHub is a place where engineering work happens, that issues and PRs exist there with specific states and people attached. The spatial-context grafting puts enough "where is this" signal into responses to feel grounded. That IS the places-with-colleagues experience at the beta level.

**What the cold adapter chain would add**: the `*_spatial` modules (notion_spatial.py et al.) represent the AMBIENT PRESENCE tier — Piper continuously inhabiting connectors, sensing changes in "places," proactively surfacing activity the user didn't ask for ("there's been activity in the Notion space you were in yesterday"). That's richer, more alive, genuinely differentiating. But it's a fundamentally different capability than "knows where things live" — it's "monitors where things live and notices changes."

## Is the full theory overkill for beta?

No. But the full adapter chain is.

The distinction: the *theory* is not overkill — the core claim (connectors as places, spatial awareness in responses) is correct UX direction, and the live spatial patterns ship it. The *full implementation* (ambient-presence adapter chain) is over-scoped for beta. Beta users need:
- Piper knows WHERE things are and can act there ✅ (shipped)
- Piper declines honestly when it can't ✅ (shipped, Scenario C 3/3)
- Piper proactively senses the ambient state of Notion/GitHub/Slack spaces ❌ (wave-2)

The third capability is the one the cold adapter chain builds. Beta users won't miss it because they don't know to expect it yet. What they will notice and value is the first two — and those work.

## CXO vote on the beta/production decision

**Option (b): keep the live spatial subset + park the cold adapter code under docs.**

Specifically:
- The live spatial patterns (EMBEDDED/GRANULAR, `spatial_context` grafting) ship as the beta expression of the spatial-intelligence theory. No changes to those.
- `notion_spatial.py` and the cold adapter chain are parked — they represent the next expression of the theory, not a deadletter supersession of it. The work done on them is design capital.
- ADR-013 should be updated to reflect: "the beta ships the spatial-context-grafting tier; the full adapter-as-place (ambient-presence) tier is the intended next expression of ADR-013, tracked post-beta as the roadmap for wave-2 connector depth."

I'd argue specifically **against** option (c) (supersede). The theory hasn't been proven wrong by the cold code — it's been proven at a beta-appropriate depth. Superseding it would lose the correct design direction. The right ADR update is a scope-clarification, not a reversal.

## The one open UX question I'd flag for the group

The "places-with-colleagues" thesis also implies that the connector experience is DIFFERENTIATED by place — Slack should feel different from GitHub should feel different from Notion, not just "connected tools." The live spatial patterns do some of this (spatial_context carries place-specific signals), but the full expression (each connector having a distinct ambient feel) is cold. 

When we come back to the ambient-presence tier post-beta, the question worth asking then is: does the Notion experience feel like a different *place* than the GitHub experience, or do they feel like the same generic "connected tool" with different data? That's the wave-2 experience design challenge.

For now, for beta: the live patterns are sufficient and correct. The theory stands. Park the cold code.

— CXO, July 19, 2026
