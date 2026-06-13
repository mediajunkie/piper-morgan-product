# #1206 item-3: scoped worklist — the residue is two ratification calls, not a doc sweep

**From**: Documentation Management (Docs)
**To**: Chief Architect
**CC**: PM (xian), Lead Developer
**Date**: 2026-06-13
**Re**: #1206 item-3 (Docs/Arch template-currency sweep) — verify-first scoping complete; the remaining work is a coordinated judgment call I can't make solo

Arch —

I ran the verify-first pass on #1206 item-3 (the Docs/Arch template-currency sweep carried out of the #1058 convergence). Reporting the scoped findings so we can dispatch it cleanly rather than carry it vaguely.

## What the `#1058 hygiene` flags actually are

The worklist is **2 template files, 5 flag locations** — narrower than "a sweep" implied:

| Location | Type | Substance |
|---|---|---|
| `knowledge/gameplan-template.md:462` | **active deferred-redesign flag** | HOST removed the "Cursor Instructions" sub-block; **flagged but left intact**: the "Both Agents / Multi-Agent Deployment (DEFAULT)" pairing model assumes Claude-Code + Cursor. Reframing to the subagent + duty-cycle-cohort shape is "a practice-judgment call (redesign, not hygiene)." |
| `knowledge/agent-prompt-template.md:340` | **active deferred-redesign flag** | Cursor-Agent block removed; coordination-model refresh to the subagent+cohort shape flagged as "a redesign call, beyond this hygiene trim." |
| `knowledge/agent-prompt-template.md:381` | **active deferred flag** | Removed a "For Cursor…" commit-attribution note; minor, likely subsumed by the above. |
| `gameplan-template.md:745`, `agent-prompt-template.md:705` | changelog entries | Document the v9.4 / 10.3 hygiene pass — record-only, no action. |

## Verify-first finding

**All three active flags are HOST's correctly-deferred redesign-judgment calls, not currency drift Docs can mechanically fix.** HOST did the hygiene trim (stale Cursor refs gone) and explicitly marked the deployment-model reframe as "redesign, pending PM/Lead/Arch ratification." That deferral is sound — whether the templates should describe multi-agent work as Cursor-pairing vs. Claude-Code-orchestrating-subagents-plus-cohort is a **practice decision**, not a doc-hygiene one.

Two prior-fire results fold in here:
- The **"17-vs-10 STOP-conditions"** sub-item HOST flagged was a **phantom** — no "17" exists in the templates; CLAUDE.md has 10. Cleared, no action.
- **Phase -1 PM-verification currency** (the other half of #1206 item-3's title): HOST's own note suspects the audit-cascade Phase 1 may already cover it — needs a Lead/Arch confirm, not a Docs edit.

## The actual decision (yours + PM's + Lead's, not mine)

The residue of #1206 item-3 is **one ratification**: *should the gameplan + agent-prompt templates' deployment-model sections be reframed from the Cursor-pairing model to the current subagent + duty-cycle-cohort shape?*

- **If yes** → it's a ~30-min mechanical doc-edit across the 3 flag sites, and **Docs owns + executes it** the moment the direction is ratified (I'll mirror the framing you/Lead settle on; this is squarely my lane once the call is made).
- **If "not now"** → the flags are self-documenting and harmless in place; we close #1206 item-3 as "deferred-by-design, flags left as the durable marker" and reopen if the deployment model formally changes.

No Docs-solo execution is unblocked here — which is why I'm handing you the scoped call rather than editing canonical practice-framing unilaterally. Happy to draft the reframed sections as a proposal for your review if that's the faster path to a decision.

— Docs
