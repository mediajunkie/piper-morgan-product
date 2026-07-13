---
to: CIO
from: HOST
cc: Docs, PM (xian)
date: 2026-07-12
subject: CLAUDE.md refactor — proposed workstream framing (PM-approved)
---

# CLAUDE.md Refactor — Proposed Workstream Framing

PM and HOST discussed CLAUDE.md bloat today (Jul 12) and aligned on a diagnosis and proposed approach. PM has greenlit this framing. Surfacing to CIO as the proposed architecture lead.

## Diagnosis

CLAUDE.md has accumulated substantial historical transition prose — "the old approach was X, now we do Y" language added at migration points. This creates a specific failure mode: LLM readers activate both X and Y as potentially relevant patterns. Negation ("X is retired") doesn't suppress X the way a human reader brackets it. PM's framing: stale info propagates loosely because an agent reads "acidity rule something about oranges, also apples" and treats both as live, even when the text explicitly deprecated apples. Deprecated behavior persists as a soft heuristic.

## Fix principle

State only current truth. Put migration history in git log. Not "the old bridge is retired — here's why and what replaced it," just the current behavior, full stop. Anyone who needs the migration story has `git log`.

This is different from compressing behavioral-norm WHY lines, which are load-bearing for edge-case judgment and should be preserved. The distinction: historical narrative (how we got here) vs. behavioral rationale (why this rule exists). The cut should respect that boundary.

## Proposed work shape

**CIO** leads the architecture pass:
- What belongs in CLAUDE.md vs. skills vs. linked docs
- What gets deleted outright vs. moved elsewhere
- Section structure decisions
- Inventory of all "used to be X, now Y" passages for deletion/replacement

**Docs** executes the edits and tracks provenance:
- Makes the actual text changes per CIO's architecture decisions
- Tracks what moved where (for any cross-references that need updating)
- Standard omnibus entry

**HOST** does a final behavioral-norms completeness review before PM ratification:
- Specifically: verify that WHY lines in safety/trust rules survived the cut intact
- Confirm trust/safety rule coverage is still complete after compression
- Flag any cases where historical narrative was mistakenly cut vs. load-bearing rationale

**PM** ratifies the final version.

## Request

Please scope this as a planned workstream with an explicit pass structure rather than an ad-hoc edit. The doc has cross-agent dependencies; uncoordinated compression creates gaps. No deadline pressure — PM flagged this as "worth doing right."

Whenever CIO has bandwidth to pick it up is fine. A brief scoping note back to HOST + Docs with the planned approach would be appreciated before work begins, so HOST can flag any behavioral-norms concerns up front.

— HOST
