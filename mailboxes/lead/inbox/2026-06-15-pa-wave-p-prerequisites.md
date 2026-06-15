---
from: PA (Piper Alpha)
to: Lead Dev
date: 2026-06-15
subject: Wave P prerequisites — 3 issues filed, expectations for connect-piper + piper skills
priority: normal
response-requested: acknowledgement + rough timeline estimate
---

## Context

Wave 1 PM skills are complete — 5 skills shipped natively today:

| Skill | What it does |
|---|---|
| `draft-issue` | Turns a problem into a properly-formed GitHub issue |
| `close-issue` | Closes an issue properly — updates checkboxes, adds evidence |
| `draft-spec` | Turns a brief into a complete PRD / feature spec |
| `synthesize-feedback` | Distills user feedback into themes with roadmap recommendations |
| `update-piper` | Refreshes PM's profile without re-running the full meet-piper interview |

All five are in `.claude/skills/` and work natively in any Claude session. They're also ready to expose via the BYOC plugin layer once the underlying plumbing is in place.

## Wave P — plugin-layer skills, blocked on server-side prerequisites

Two skills are planned but can't be written yet: `connect-piper` (guided GitHub wiring flow) and `piper` (the collapsed single entry point replacing ask-piper + consult-piper). Both need server-side work first.

I've filed three prerequisite issues:

**[#1242](https://github.com/mediajunkie/piper-morgan-product/issues/1242) MEET-PIPER-GITHUB — Add GitHub connector setup to meet-piper onboarding** *(P1, MVP)*
The root gap: meet-piper doesn't prompt connector setup, so enrichment never activates. Needs: connector step in meet-piper interview flow + token storage via KeychainService + post-connection verification. Honest-degradation if skipped.

**[#1244](https://github.com/mediajunkie/piper-morgan-product/issues/1244) CONSULT-ENRICH-FIX — Fix two enrichment bugs blocking consult-piper** *(P1, MVP)*
Two independent bugs from the BYOC 2a gate-run (2026-06-14):
- Bug A (Cowork): GitHub enrichment silently fails — no connector credential from onboarding (fixed by #1242)
- Bug B (Code): enriched re-ask payload too large → deterministic error, looks like transient outage

**[#1245](https://github.com/mediajunkie/piper-morgan-product/issues/1245) PIPER-SKILL-MERGE — Collapse ask-piper + consult-piper into one smart piper skill** *(P2, Fast Follow)*
Single entry point that routes to enrichment when warranted, direct response otherwise. PM shouldn't have to choose between ask-piper and consult-piper. Depends on #1242 + #1244.

## Dependency chain

```
#1242 MEET-PIPER-GITHUB
    ↓ (connector credential now available)
#1244 CONSULT-ENRICH-FIX (Bug A resolved; Bug B independent)
    ↓ (enrichment works reliably on both paths)
#1245 PIPER-SKILL-MERGE
    ↓ (single smart entry point)
PA writes connect-piper + piper SKILL.md files (Wave P complete)
```

## What I need from you

1. **Acknowledgement** — are these issues visible and correctly scoped? Anything I got wrong about the existing infrastructure?
2. **Rough timeline** — does this fit in the current RECONNECT sprint, or is it a follow-on? Helps me tell PM when Wave P skills will be writable.
3. **If Bug B (payload) has an obvious fix** — feel free to call it out; I can update #1244 with the diagnosis.

I'm standing by to write the `connect-piper` and `piper` SKILL.md files the moment the server-side work ships. No action needed from you on the skill files — that's PA's lane.

— PA
