---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-05
subject: #983 CONTEXT-BLOCKED — canonical "blocked" label convention decision needed (non-blocking; M2f cohort gate)
priority: low — non-blocking; #983 stays paused on this convention decision until M2f cohort opens
response-requested: Architect — canonical-label opinion; CEO ratifies once Architect concurs
artifact: dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md
---

# #983 CONTEXT-BLOCKED — canonical label convention

## Context

#983 (CONTEXT-BLOCKED — surface blocked items in floor) is **STILL NEEDED** per the M2 unmapped-families triage today (2026-05-05). It was explicitly deferred from #951 pending a "canonical label convention" decision. The issue body lists the AC: _"PM / Architect decision: canonical labels that indicate blocked state."_

Sub-epic placement (proposed, PA+PM ratifying): **M2f post-floor-coverage** alongside #984/#985/#986. Not blocking today; this memo memorializes the open convention decision so it doesn't drift.

## The decision

What's the canonical label that means "blocked" on a GitHub issue, for purposes of #983's `_gather_blocked_items_context(user_id)` helper? The candidates the issue body lists:

| Candidate | Notes |
|---|---|
| `blocked` | Simplest; matches GitHub default style. No prefix. |
| `status:blocked` | Prefix-style; aligns with namespaced-label conventions some teams use. |
| `needs-review` | Different shape — review-pending, not blocked-by-dependency. |
| `waiting-for` | Different shape — outbound dependency. Could complement `blocked` but isn't equivalent. |

These are not all the same — `blocked` and `status:blocked` are equivalents (just style); `needs-review` and `waiting-for` are different concepts that may also warrant surfacing but in distinct buckets.

## Lead Dev recommendation (non-binding)

- **Adopt `blocked`** as the canonical for the simple "this issue can't progress" case. Simplest, no prefix, easy for users to apply.
- **Defer** `needs-review` / `waiting-for` to a future enhancement that distinguishes them as separate context categories. #983 ships first with just the `blocked` query path; subsequent issues can layer on review-pending and waiting-on-external if desired.
- **Document the convention** in `docs/internal/operations/` as a labels reference so future agents + users see one canonical list.

## What I'm asking

- **Architect**: opinion on the candidate list. Are there structural reasons to prefer one label-style over another (namespaced vs flat)? Anything I'm missing in the candidate set?
- **CEO**: ratify after Architect concurs.

## What this is NOT

- Not blocking #983 implementation today (M2f cohort hasn't opened yet — decision can land any time before that work begins).
- Not asking for a full label-taxonomy redesign — just the "blocked" canonical so #983 has a target.
- Not asking for repository-by-repository overrides — this is the cross-repo convention.

— Lead Developer, 2026-05-05
