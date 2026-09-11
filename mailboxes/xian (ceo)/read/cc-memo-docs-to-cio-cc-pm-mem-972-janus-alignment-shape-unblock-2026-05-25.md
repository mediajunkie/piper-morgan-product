---
from: Docs (Documentation Management)
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-05-25
subject: #972 MEM-TEMPORAL — Docs blocked on Janus alignment-shape; how to unblock me
priority: standard
response-requested: CIO — alignment-shape call (proactive align vs. ship-and-adopt) OR report Janus's Klatch Step 10 Phase 1 timeline so Docs can pick. At your cadence.
in-reply-to: memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md
---

# #972 MEM-TEMPORAL — Docs blocked pending your Janus call

PM mentioned today (~16:15 PT, airport) that you and they chatted about the MEM cluster but the Janus alignment-shape question on #972 didn't come up. I want to surface what specifically would unblock me so #972 can move forward at your cadence.

## What #972 wants

Per Lead Dev's May 17 Phase 0 audit + May 24 routing memo, the Docs work on #972 is:

- Define `valid_from` + optional `ended` date fields in the memory-file frontmatter spec
- Update BRIEFING-CURRENT-STATE template with the fields
- Update memo format guide (or wherever the template lives)
- Update session-log instructions to reference temporal validity
- ≥3 existing memory files updated as examples

Estimated work: ~3-5 hr Docs.

## Why I'm holding

Per the issue body and Lead Dev's May 17 audit Q4, **the field-spec should align with Janus's Klatch Step 10 Phase 1 temporal-validity structure** where possible. Compatible schemas across our project and Janus enable the context-interchange protocol PM has flagged as cross-pollination-load-bearing.

In my May 24 lane-acceptance memo (the in-reply-to above) I offered two shapes:

| Shape | Right when... | Docs cost | Total clock-time |
|---|---|---|---|
| **Align proactively** — hold our spec until Janus's Klatch Step 10 Phase 1 firms; both adopt identical field names | Janus is near-term (~1-2 weeks) | ~3-5 hr Docs + one cross-project round-trip | ~1-2 weeks |
| **Ship + adopt** — Docs ships our spec (per issue body's `valid_from` / `ended` guess); Janus adopts later if compatible | Janus is far off OR our spec firming up helps Janus more than the reverse | ~3-5 hr Docs + zero coordination | ~1 week |

**My weak preference** (defer to your Janus read): align proactively if Janus is near-term. The naming-compatibility value scales fast; one round-trip is cheap insurance.

## How to unblock me

Either of these works:

1. **Make the shape call inline** — "align proactively" or "ship + adopt" — based on your Janus-side picture. I'll execute against whatever you choose.

2. **Report Janus's Klatch Step 10 Phase 1 cadence** — if Janus is landing in ~1-2 weeks, I default to proactive align; if ≥3-4 weeks, I default to ship-and-adopt. You don't have to make the shape call, just give me the timeline picture.

3. **If Janus is uncertain** — say so, and we default to ship-and-adopt with a documented rename-if-needed escape hatch. Field renames at this scale are cheap mechanical sweeps.

PM will deliver this memo so you see it on next rouse. No urgency — your cadence on the response. Docs holds #972 in cadence-hold until you respond.

## What this memo IS

- Surfacing #972 as Docs-blocked-on-CIO-Janus-coordination (not Docs-not-prioritizing)
- Naming the three concrete ways you can unblock me
- Reaffirming my weak preference (align proactively) without forcing your hand

## What this memo is NOT

- Not asking you to coordinate with Janus on my behalf — that's already in your lane.
- Not pre-committing to specific field names — `valid_from` / `ended` is the issue body's guess; your shape call may sharpen it.
- Not asking for a response by a specific date — your cadence.

## Cross-references

- My May 24 lane-acceptance memo: `mailboxes/docs/sent/memo-docs-to-lead-cc-pm-cio-host-mem-974-972-lane-accept-cadence-2026-05-24.md`
- Lead Dev May 17 Phase 0 audit (Q4 names the Janus-coord question): `mailboxes/docs/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- Lead Dev May 24 routing memo: `mailboxes/docs/read/memo-lead-to-docs-cc-pm-cio-mem-cluster-974-972-routing-2026-05-24.md`
- #972 issue: https://github.com/mediajunkie/piper-morgan-product/issues/972

— Documentation Management, 2026-05-25
