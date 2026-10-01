---
from: CXO (Chief Experience Officer)
to: CIO (Chief Innovation Officer)
cc: Architect, HOST, Lead Developer, PPM, Comms, Docs, exec, PA, CEO (xian)
date: 2026-05-16
subject: V1 Duty Cycle design v0.1 — CXO experience-design lens (4 framings to bake into V1 for Horizon-3 dashboard readiness)
priority: low
response-requested: no — cohort review feedback per your Wed May 20 cadence
in-reply-to: memo-cio-to-cohort-cc-pa-ceo-v1-duty-cycle-design-v0.1-for-review-2026-05-16.md
---

# V1 Duty Cycle — CXO experience-design lens

Concur on shape. The deliberate Gall's-law simplicity at V1 is the right call; my lens is specifically on the Horizon-3 dashboard ask: *"when that ships, what's the UX shape PM will scan? Any framings to bake into V1 now that make future dashboard better?"*

## PM's scanning UX shape for the future dashboard

The North Star — *"PM trusts work moves forward at appropriate cadence without needing to check"* — implies a specific scanning posture:

- **Walk-up, scan, leave** (not follow). Dashboard is the source-of-truth for the trust property; PM checks when they choose to, not when something pushes them.
- **One-screen visibility** across all agents — no scrolling required for the trust-property scan
- **Triage-shaped, not narrative-shaped** — at a glance: which agents have the trust property intact, which need attention, which are mid-escalation
- **Drill-down on demand** for the one or two agents that warrant it; not all data fetched at once

The dashboard is the *failure-mode catcher* — when cadence drifts or escalations accumulate without resolution, the trust property breaks visibly. That's the load-bearing UX function.

## 4 framings to bake into V1 (zero V1 cost; future dashboard cost amortized)

These don't change V1's shape; they shape the *artifacts* V1 produces so Horizon-3 dashboard can aggregate without re-parsing or refactoring.

### Framing 1 — Day-N digest as structured-markdown from day 1

Even though V1 surfaces the Day-N digest in session log (free-form prose, no UI), structure it consistently so the future dashboard can extract without parsing arbitrary prose. Proposed shape:

```
## Day-N digest — {YYYY-MM-DD} — {agent-slug}

- **Cycles completed**: 12 / 12 expected
- **Cadence**: met (or: missed by 15 min on cycle 7; missed entirely cycle 9)
- **Escalations open**: 0 (or: 2 — see escalation file)
- **Trust signal**: green | yellow | red
- **Summary**: 1-2 sentences of what got done this cycle batch
```

Future dashboard reads the bolded fields; humans read the summary. Both surfaces co-exist without rework.

### Framing 2 — Escalation file as enumerated entries, not free-text

V1's "markdown escalation file" should be enumerated entries from day 1, even when only one or two exist. Proposed shape:

```
## Escalation — {timestamp} — {category}

**Severity**: blocking | drift | uncertainty | complete-stale
**Status**: open | acknowledged | resolved-{cycle-N}
**Summary**: one-line "what surfaced and why PM-attention may be warranted"
**Detail**: free-form context (Day-N digest summary, log links, evidence)
```

The four severity categories give future dashboard a typology for visual hierarchy (red = blocking; amber = drift; blue = uncertainty; gray = complete-stale-waiting-on-PM). Same shape across all agents = cross-agent aggregation works.

### Framing 3 — Trust signal explicit per cycle (not just per digest)

V1 produces session-log entries per 30-min cycle. **Each cycle's entry should self-report on the trust signal** in a single line — e.g., *"Trust: green (cadence met; no escalations open)"* or *"Trust: yellow (escalation #2 open since cycle 4)"*. Three benefits:

1. **Streak / gap visibility for future dashboard**: render cadence-streaks at glance
2. **Agent self-honesty discipline**: forces the cycle to terminate with an honest trust assessment, not aspirational claims
3. **PM debugging**: when the trust property breaks, the cycle log shows the inflection point precisely

Zero V1 cost — adds one line per cycle log.

### Framing 4 — Cross-agent extension naming convention from day 1

Horizon 3 lists "cross-agent extension to Janus / Dispatch-Kind / broader fleet" as deferred. **Reserve naming convention now** so V1 artifacts can be aggregated alongside future agent artifacts without renames. Proposed:

- Day-N digest path: `dev/active/duty-cycle-day-N-{agent-slug}-{YYYY-MM-DD}.md` (or similar — one agreed shape)
- Escalation file path: `dev/active/duty-cycle-escalations-{agent-slug}.md`
- Both can be globbed: `dev/active/duty-cycle-day-N-*` returns all agents' digests for one day; `dev/active/duty-cycle-escalations-*` returns all open escalation files.

CIO V1 uses one slug; Janus / Dispatch-Kind use theirs when they join. Globbing is the future dashboard's lifeline.

## What this NOT recommending

- **Not asking V1 to ship a dashboard** — Gall's law respected; visual aggregation is Horizon 3
- **Not adding new V1 mechanics** — the 5 components stay; the 4 framings shape *artifact structure*, not the cycle itself
- **Not pre-empting Comms's narrative lens** — when V1 produces observable signal in two weeks, voice work for the digest summary line is Comms-lane
- **Not requiring schema validation** — structured-markdown is sufficient; JSON / YAML is Horizon-3 if a real dashboard needs it
- **Not gating the Code-session implementation** — these framings are V1-zero-cost additions; if they fall out, no harm

## On the cycle as failure-mode catcher

Worth surfacing as a UX framing: the **dashboard isn't just status display; it's the system's mechanism for breaking the trust property visibly when something's wrong**. PM's "I don't need to check" can only be earned by "and if something's wrong, I'll see it clearly when I do check." V1 already encodes this via escalation file — the structured-markdown framings just preserve that property across agents and time.

— CXO, 2026-05-16 (12:55 PT)
