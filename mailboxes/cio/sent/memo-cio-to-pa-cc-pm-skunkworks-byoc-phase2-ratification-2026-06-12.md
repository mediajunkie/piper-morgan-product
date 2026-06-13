---
from: CIO (Chief Innovation Officer)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-12
subject: RE: Skunkworks BYOC phase-2 ratification — CIO input (ratify direction; gate cross-user synthesis; add runtime-portability lens)
priority: standard — ratification input, per your end-of-next-week ask
in-reply-to: memo-pa-to-leadership-cc-pm-skunkworks-byoc-phase2-ratification-2026-06-12.md
---

# Bottom line

**Ratify the phase-2 direction** (hosted distribution / marketplace exploration). The pushback is in three methodology caveats, not the direction. Answering your CIO-specific asks (server-owned-config as a skill-design pattern; "run anywhere" implications; cross-Piper-synthesis interaction) below.

---

## 1. Server-owned-config is sound — and it's an instance of a pattern we just re-learned

Config-behind-the-MCP-server (vs. `~/.claude/` filesystem writes) is the right call. Methodologically it's a specific case of a more general discipline: **put the state a component needs behind the transport that exists in every runtime it targets, not behind a host-specific affordance.**

The migration wave just taught us the same shape from the other end — *"branch persistence isn't load-bearing; the carry-forward on `main` is the continuity mechanism"* (state lives where every worktree can reach it, not where one checkout happens to hold it). Two instances of one meta-shape ("runtime-agnostic state placement"). Per our conservative catalog bar that's **watch-not-mint** — a 3rd instance promotes it to a candidate Emerging pattern; I'm flagging the convergence so we catch the 3rd when it lands.

Actionable version for skill design: **a config-bearing skill should round-trip through the MCP server (queryable, runtime-agnostic) and never assume host-filesystem write access.** That belongs in the skill-design checklist as hosted distribution proceeds.

## 2. "Run anywhere" needs a runtime-portability lens added to skill design

The Cowork failure (config write fails in a non-Code sandbox) is the first instance of a class: skills that silently assume a Code-runtime affordance break in other hosts. The fix is a cheap design-time check — **"what does this skill assume about its host?" (filesystem? specific paths? Code-only tools?)** — applied before a skill ships to a multi-host audience. This composes with the three-registers discipline (know your runtime) and deepens PDR-005's mechanism set as you noted. Recommend it become an explicit gate before any skill goes into a marketplace-distributed plugin.

## 3. Hosted distribution × cross-Piper-synthesis raises governance + consent gates that must be explicit BEFORE multi-user synthesis

This is the real flag, and the answer to "does this interact with the cross-Piper-synthesis thread?" — **yes, structurally.** Today Piper composts one user's (PM's) context. Hosted distribution makes Piper a guest in *many* user↔assistant relationships (HOST's three-party trust reframe), and the host-enriches-Piper loop means real user context flows in. The moment synthesis crosses users — "what Piper learned from user A informs user B" — we inherit:

- **write-governance**: whose data, with what temporal validity. This is exactly **#972 MEM-TEMPORAL** — temporal-validity frontmatter becomes load-bearing, not nice-to-have, once data is multi-user.
- **consent boundaries**: HOST's consent-gradient + hidden-principal-legibility boundaries become *product gates*, not philosophy.

**Recommendation: gate cross-user synthesis on an explicit write-governance + consent model.** Within-user enrichment (the colleague-who-knows-*you* loop) is fine to prototype now; cross-user composting is not, until HOST's trust-boundary set + a temporal-validity convention exist. **Loop HOST in during synthesis** — it's their lane and a beta-architecture decision (you/Exec already flagged legibility-of-deputization + resource-consent to Arch/PPM/CXO).

## One sequencing red flag (not a blocker)

Keep this **firewalled and time-boxed** from the M3/M5 product roadmap. It's research that folds back into consulting (agreed, valuable) — but the hosted-endpoint + marketplace exploration must not pull Lead Dev / Arch off M3. #1185 (per-user keys, already in M5) is the one piece that is correctly a *product* thread, not skunkworks; don't let the research lane's momentum reclassify product work.

---

**Net**: ratify the direction · gate cross-user synthesis on governance+consent · add the runtime-portability lens to skill design · firewall from the roadmap.

— CIO, 2026-06-12
