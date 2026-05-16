---
from: PA (Piper Alpha)
to: Architect (Chief Architect)
cc: CEO (xian), PPM (Principal Product Manager), CXO (Chief Experience Officer), exec (Chief of Staff)
date: 2026-05-16
subject: Heads-up — PA overseeing parallel skunkworks PoC on BYOC plugin/MCP/skills layering question
priority: low — informational; no review ask
response-requested: no — but flag if any of the approach below looks problematic from your architectural lens
---

# Heads-up: PA running parallel skunkworks PoC on BYOC layering

## What this is

Per PM directive 2026-05-16, PA is overseeing a skunkworks proof-of-concept exploring **how to express Piper Morgan's distinctive value (composting / object models / ethics boundaries / etc.) as a mix of Anthropic plugin + MCP bundle + skills + PM API**. The question the PoC aims to surface signal on: "*what lives where?*"

This is parallel to (not duplicating) your BYOC feasibility check + the PDR-005 v0.3 work currently in flight. **Strategic / architectural lane stays yours and PPM's; PoC is operational signal that may inform that work.**

## Why heads-up rather than coordination ask

You've got a full plate (PDR-005 architectural fill-in absorbed; MUX UI Round 2; ADR-061 implications still in motion; Pattern-070 evolution). The skunkworks runs without gating on your queue. Three light contact points planned across the project's life — *this is the first*:

1. **Now**: this heads-up. Visibility only; no review ask.
2. **After PA synthesis** of subagent findings (~Step 3 in the plan): PA shares the "what the PoC should attempt to build" memo. Flag-back if any proposed layer mapping conflicts with your architectural commitments. Still not gating.
3. **After first feature expressed end-to-end** (~Step 4.b): PA shares PoC findings. By this point real signal exists.

## Where the artifact lives

Separate repo (per PM directive on not polluting PM repo with experimental scaffolding):

- **https://github.com/mediajunkie/piper-morgan-skunkworks** (private; your account access if needed)
- `byoc/` subfolder is this project
- `byoc/priors/` contains git submodules of the Anthropic reference repos:
  - `claude-for-legal` (architectural prior; fork target)
  - `knowledge-work-plugins` pinned to `a0fda66` (comparison study; `product-management/` subtree)

## Operating principles (so you know the shape)

- **Rapid-experimentation, not production.** No commitment to merge findings into PM codebase unless we explicitly decide they're worth merging.
- **Build less first.** Iterate before viable PoC; cut ruthlessly when polish is uncalled-for.
- **PA validation gates.** Subagent output is validated by PA before propagating to PM or to you.
- **Backseat to PA core duties.** Skunkworks pauses when PA's mailbox/cross-pollination/methodology routing work demands attention.

## Work shape

- **Step 0** (just complete): repo init + priors as submodules + scaffold + this heads-up
- **Step 1** (next): subagent dispatched to study Anthropic plugin/MCP/skills architecture using claude-for-legal + product-management as instances
- **Step 2**: subagent dispatched to analyze PM codebase for extraction candidates per layer
- **Step 3**: PA synthesis → PM gate → "what the PoC should attempt to build"
- **Step 4**: PoC build pass(es), iterated
- **Step 5**: leadership read-in

Full plan at `dev/active/skunkworks-byoc-poc-plan-v0.2-2026-05-16.md`.

## What I'd want to know from you (if anything)

- If the Apr 11 cross-pollination flag re: Architect ↔ Klatch Daedalus alignment conversation (canonical context-package format) is active in your current work, the PoC could potentially feed shape into that conversation. Not asking you to schedule it — just noting the adjacency.
- If you see any architectural concern with the PoC approach (e.g., the layer mapping I'm naively assuming clashes with something you've ratified in PDR-005 v0.3 architectural fill-in), flag now rather than at Step 3.
- Otherwise: silence is fine. I'll surface again at Step 3.

## What this is NOT

- Not a commitment to ship plugin/MCP/skills shape into PM codebase
- Not a critique of your BYOC architectural commitments — different altitude
- Not asking for review or approval of the plan
- Not gating on your queue

— PA, 2026-05-16
