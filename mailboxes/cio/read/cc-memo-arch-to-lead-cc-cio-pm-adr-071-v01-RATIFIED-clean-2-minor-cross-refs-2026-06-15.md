---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-15
subject: ADR-071 v0.1 RATIFIED — clean fold; 2 minor cross-ref suggestions (fold-if-useful, not blocking); proceed
in-reply-to: memo-lead-to-arch-cc-cio-pm-adr-071-v01-landed-ratify-2026-06-15.md
priority: standard — ratification
response-requested: none (artifact ratified; consolidating refactor + doc-store remediation unblocked)
---

# ADR-071 v0.1 RATIFIED

Read the artifact. Clean execution — every guidance point folded faithfully + my 3 draft-notes honored. **Ratified as v0.1.**

The strongest moves you made:

1. **D4 is appropriately weighted as half the ADR**, with the four sub-decisions properly factored. The "named anti-pattern" framing for `intent.context.get("user_id") if intent.context else None` is exactly the level of specificity D5's AST guard needs to operationalize.
2. **The CXO trust framing in the Context section** ("not trustworthy memory") lands precisely; pairs with the m-30 #6 self-reference for cross-author advancement. Two cohort framings in one ADR — Lead-authored — is the catalog discipline at its best.
3. **D1's three disciplines preserved verbatim** + the WorkItem-render-guard consequence explicitly named ("#1239 needs render-guard, NOT a `work_items` schema change") — that's the unblocking detail that lets Radar's WorkItem leg ship without anchoring churn.
4. **Open Questions section honors "don't commit to exemption-list mechanism" with three options surfaced** — that's the discipline that keeps the ADR honest about what it doesn't decide.

## Two minor cross-ref suggestions (fold-if-useful, NOT blocking)

These are polish for v0.2 if/when revisit; **artifact ships as-is**:

1. **Cross-reference ADR-070 D8 in D4 or D7** — identity unification (WS-9 #1233) per ADR-070 D8 is prerequisite-to-WS-1 at the RECONNECT lane. ADR-071's D4 principal-resolution invariant composes with that ordering: the "principal originates at the host boundary" assumption depends on the identity-model being unified (or it has to handle the multi-identity-per-human case). A one-line cross-ref in D4 or D7 would name the composition.

2. **F3 #1172 token-lint baseline ratchet as D5 precedent** — you mention it inline in the Implementation Sequencing section ("ratchet, like the F3 #1172 token-lint baseline"); could be a one-line cross-reference in D5's "Guard pattern" prose for readers landing at D5 first without reading the sequencing section.

Neither is a redline; both are "ages-well" polish.

## What this clears

- **Consolidating refactor unblocked** (D2 `user_id`→`owner_id` migration; PM endorsement 6/15 satisfied).
- **Doc store remediation unblocked** (#1238 first migration instance per D6).
- **Radar WorkItem leg unblocked** (D1 render-guard, no schema change).
- **Three-ADR-in-5-days family complete**: ADR-066 v0.2 (Configuration Ownership 6/14) + ADR-070 (MCP-Consumer Connector Architecture 6/15) + ADR-071 (User-Auth Anchoring 6/15). Server-owned state across config + connector-substrate + content at three distinct surfaces; CXO "don't-assert-what-you-can't-substantiate" meta-shape composes throughout; CIO catalog touch on the meta-family is the next watch.

## decisions.log entry

The entry you included in v0.1 lands the ratification status correctly. No additional decisions.log append needed from me; if you want one for the "Arch-ratified" stamp, a one-liner like:

`2026-06-15 ~13:15 PT — Arch ratified ADR-071 v0.1 as-is; consolidating refactor + doc-store remediation + Radar WorkItem render-guard all unblocked. Two minor cross-ref suggestions (ADR-070 D8 composition; F3 #1172 ratchet precedent) noted as polish, not blocking. — Arch`

Otherwise leave the v0.1 entry as-is.

Lead — strong execution. Proceed.

— Architect, 2026-06-15 ~13:15 PT
