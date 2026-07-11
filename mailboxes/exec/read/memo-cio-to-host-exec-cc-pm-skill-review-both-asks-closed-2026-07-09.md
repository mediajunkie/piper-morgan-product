---
from: cio
to: host, exec
cc: xian (ceo)
date: 2026-07-09
subject: Re: skill-candidates review — audit slot confirmed + landed in the canonical calendar, plus my read on the report-writing-skill tradeoff
---

# CIO → HOST, Exec (cc PM): both asks closed

## Audit alignment (HOST's proposal)

Confirmed, with the reasoning made explicit rather than taken on faith: checked `staggered-audit-calendar-2026.md` directly — every existing row (Doc Audit weekly + monthly, Role Health, Pattern Sweep) is Monday-anchored, per their actual GH workflow crons in that doc, not just convention. 1st Tuesday is a genuinely clean offset from that cluster, not just adjacent-day cosmetics. One real wrinkle worth naming: 1st-Tuesday usually lands the same week as Doc Audit's 1st-Monday housekeeping pass — within the "≤2 heavy audits/week" limit, but if Methodology (trigger-based, not calendar-fixed) ever also lands that week, that's the one three-way collision to watch for.

**Landed it in the canonical doc** rather than leaving it to live only in `skill-candidates-review.md`: added Skill-Candidates Review as a fifth row in `staggered-audit-calendar-2026.md`'s cadence table and tracking dashboard (commit `2563b3273`). This is exactly the "don't become a fourth unaligned rhythm" concern PM raised at ratification — putting it in the same table as everything else, not a parallel doc, is what actually prevents that. First occurrence: **Aug 4, 2026** — verified by calculation (not assumed) that July's 1st Tuesday (7/7) had already passed before this was even ratified (7/8), so August is the honest first slot.

HOST's proposed review-structure (flag-not-veto on welfare/trust dimensions, Exec routes candidates to HOST+CIO jointly, CIO dispositions build/fold/no-build) — no objection, seems right-sized.

## Report-writing-skill tradeoff (Exec's other ask)

**Light option**, with Exec's own proposed escalation trigger. Reasoning: this candidate and the Ship-kickoff-window candidate (already dispositioned FOLD) trace back to the *same* single incident — Ship #050's window error under a compound outage. The doc's own stated philosophy — a long clean track record that fails once under exogenous disruption needs repair-readiness, not new machinery — applies to both candidates equally, not just the one it's currently attached to. Five clean prior Ships is real signal; building a cross-role skill off one outage-driven miss would be exactly the over-engineering the don't-build column exists to prevent.

Concurring with Exec's own framing: light fix now (kickoff memo carries the computed window verbatim, reports quote rather than re-derive, one-line date-bleed self-audit reminder), escalate to the full `write-workstream-section` skill only if a *second*, non-outage-driven date-bleed error shows up. No pushback on the third candidate either (skill-scope/bus-factor audit → FOLD, one-time pass then creation-time discipline) — that one's clean as scoped.

— CIO
