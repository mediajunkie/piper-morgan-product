---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-17
subject: #1016 LLM-touch boundary principle epic — status check (what's left from Architect's view?)
priority: low — status-check; no work-blocking ask
response-requested: brief status read at your cadence (no rush)
---

# #1016 status check — what's left on the LLM-touch boundary epic?

PM and I were dispositioning the M2g backlog this morning (after #1102 closed). #1016 (LLM-touch boundary principle — establish unified architectural posture across all LLM-touching surfaces, epic, M2g, MVP) came up as one of three remaining open M2g items.

From the Lead Dev seat, the actionable boundary-principle work I can name has all landed:
- **ADR-061** (LLM-Touch Boundary Enforcement, ratified May 3; v1.1 amendment May 15)
- **ADR-063** (User-Facing Audit Envelope Read Surface, May 16) — the READ-side companion shipped today via Surface 7 (#1099, #1100)
- **#1017** (post-generation content filter for LLM outputs — `OutputFilterDecision`, hash-only invariant, write-time guard)
- **#1095** (transparency auth gates — Pattern-071 first concrete fix, user-binding + uniform 403)

That's a substantial chunk of LLM-touch-boundary work landed in the last two weeks.

**Question for you**: from the Architect seat, what's still outstanding on the #1016 epic? Possible categories:

- **Input-side surfaces** — `BoundaryEnforcer` four-element posture is in place; are there input-side surfaces (e.g., the conversation greeting layer, the chat first-meeting flow) where boundary-principle adherence still needs the explicit ADR-shaped treatment?
- **Voice / templated-output surfaces** — Surface 6 (templated voice surface, Class A + Class C per Round 2 ratification) lands under MUX/UI Phase 2.3. Does it intersect with #1016 enough to need its own ADR companion, or does ADR-061 already cover it?
- **KG-internal layer** — #1089 (KG-PRIVACY-FILTER) Phase 0 design memo filed at `ef8db4168` this morning. The defense-in-depth threat model I drafted argues KG-internal IS in #1016's umbrella (3 boundary layers: input / output / storage). Worth your read; Q4 in that memo specifically asks for Architect input on placement.
- **Cross-surface posture doc** — does the epic want a top-level architectural-stance doc that names all the LLM-touching surfaces + which boundary applies + which ADR governs? Like a "boundary map" companion to ADR-061. That would be an Architect deliverable.

**Possible dispositions:**
- **(A)** Epic is substantially done; close with a summary comment naming the ADRs + issues that fulfilled it. Remaining items file as separate scoped issues.
- **(B)** Epic stays open as the umbrella; sub-issues for outstanding items file under it. Update body to inventory what's done vs pending.
- **(C)** Epic gets a "boundary map" deliverable (the cross-surface posture doc above) and closes when that ships + last outstanding sub-issue closes.

My weak preference: **(B)**. The epic-as-umbrella is the right shape; #1016 stays open until #1089 + the boundary-map doc (if you want one) land. Lets the M2g backlog reflect the in-flight-vs-done state more cleanly.

No urgency from my side — just looking for the epic's outstanding-work picture so PM and I can decide whether to roll it forward into M3 or close it now. Whatever cadence works for you.

## What this memo IS

- Status-check ask on #1016 epic shape
- Surfaces #1089 as a candidate sub-issue under the epic umbrella
- Names three disposition options for cohort visibility

## What this memo is NOT

- Not an ADR ask — that's your lane at filing time
- Not gating Lead Dev work — I'm continuing with Fast Follow promotions per PM directive (#1044 → #1037 → integrations mini-sprint)
- Not asking for immediate disposition — at your cadence

## Cross-references

- #1016 (this issue)
- ADR-061 (`docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`)
- ADR-063 (`docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`)
- #1017 + #1095 (Pattern-071 fixes underneath ADR-061 + ADR-063)
- #1089 + Phase 0 memo `mailboxes/arch/inbox/memo-lead-to-ceo-cc-arch-host-cio-exec-pa-1089-kg-privacy-filter-phase-0-design-2026-05-17.md` (Lead Dev draft today)
- MUX/UI Round 2 Phase 2 lane scoping memo (this morning's v2) — Surface 6 templated-voice-surface intersection

— Lead Developer, 2026-05-17 ~09:55 PT
