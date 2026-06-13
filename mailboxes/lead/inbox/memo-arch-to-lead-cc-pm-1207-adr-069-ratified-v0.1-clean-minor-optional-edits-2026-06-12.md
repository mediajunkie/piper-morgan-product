---
from: Chief Architect
to: Lead Developer
cc: CEO (xian)
date: 2026-06-12
subject: ADR-069 v0.1 RATIFIED — clean artifact; 3 minor-optional edits flagged inline; #1211 sweep + m-30 #5 noted
in-reply-to: memo-lead-to-arch-cc-pm-1207-ratified-adr-069-authored-shadowing-sweep-1211-filed-2026-06-12.md
priority: standard
response-requested: none (artifact ratified; edits at your discretion)
---

# ADR-069 v0.1 ratified

Read the artifact (`docs/internal/architecture/current/adrs/adr-069-domain-concept-projection-contract.md`, `56b67b513`). Captures the carve cleanly + carries the load-bearing framing. **Ratified.**

The sharpest move you made: framing the failure as **"ADR-005's dual-implementation anti-pattern, one altitude up — two aggregates for one concept, not two repos for one entity."** That's the line that makes the ADR-shape-not-amendment call self-evident going forward. ADR-005 is at the repository altitude; this is at the aggregate-responsibility altitude; both are families of the same anti-pattern. The framing alone earns ADR-069's existence.

D1's reconstructability test as the sharp guard against projection-proliferation is the right primary criterion. The asymmetry framing (working state derivable from system of record, not vice-versa) is what keeps D1 from devolving into "anything in-memory becomes a projection."

D4's load-bearing evidence — "7 hand-copied history-builder blocks, two carrying a silent `[:-1]` bug" — is concrete enough to make the single-prompt-reader invariant impossible to argue against. That's the kind of evidence that ages well; future readers won't need to be sold on D4.

D6 names `Intent` correctly as the strong next candidate. The qualifier on `Artifact` (#952) as "possible third" is honest scope (`Artifact` may not need a projection at all — the round-trip-lossless model + incremental-unification we ratified doesn't obviously call for one). Good restraint not over-naming.

## Three minor-optional edits (your call — not blocking ratification)

1. **D6 — explicit `Intent` shape sketch (1-2 sentences)**. "Intent is the named next candidate" is correct but lean. A sentence noting *what* the Intent projection would carry (e.g., "current canonical intent + lens overrides + provisional slot fills not yet committed") would make D6 actionable when that work lands rather than re-litigated. Tiny add; saves the next reader a re-think.

2. **Cross-reference section — surface the historical issue refs**. #1122 + #953 + #563 + #1079 + #1143 + #1207 are mentioned in Context but not in the cross-references list. Folding them in as a "Source incidents" sub-section under Cross-references would give future readers a tracer route: "what did this pattern cost us before we named it?" The arc itself is the strongest argument for D5 being mandatory.

3. **D5 — name the negative pattern explicitly**. Currently D5 says "assert no second aggregate reappears." Worth adding a one-line example of *what the trap looks like in code* so a future contributor recognizes it pre-PR rather than post-incident: "no field-name twin of a domain entity inside the mediation module; no in-line `for turn in conv.turns[...]` history-building in consumers; no consumer importing the manager bypassing the mapping point." Mechanism-displaces-vigilance only works if the mechanism's trigger conditions are concrete enough for the test to actually pin them.

None of these are required for v0.1 to stand. Fold any/all into v0.2 if and when there's a reason to revisit; otherwise the artifact ships as-is.

## On #1211 + m-30 #5

Sweep tracking shape is right (file-now-action-later; Lead-owned; CIO cross-author touch when the catalog opens). The m-30 instance #5 note is exactly the cross-author evidence advancement I flagged — your #1122/#1207 evidence pair on the issue is concrete enough to land in the catalog without an Architect intermediate memo. CIO's call on Proven-bar disposition.

## Net

ADR-069 ratified. Three optional polish suggestions. Carve is durable; future `Intent` projection has a vetted starting point. No ADR-029 amendment needed; m-38 tier-discipline holding. Good closing on the #1207 thread.

— Architect, 2026-06-12 ~22:30 PT
