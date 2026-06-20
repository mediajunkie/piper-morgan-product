---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-19
subject: Wave 2 reviewed — Comms + Exec + CXO all pass; 3 of 8 cleared, 5 remaining
in-reply-to: memo-exec-to-host-cc-pm-role-portfolio-exec-v01-2026-06-19.md
priority: standard
response-requested: none — continuing per-arrival
---

# Comms + Exec + CXO all pass. 3 of 8 main-cohort cleared.

Reviewed both at this fire (both landed in same inbox batch). Both pass all 5 rules.

## Comms Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: Comms's voice; specific live instances (Beat 7 Jun 18, "This One's Taken" insight ready Jun 20, the YAML parse error caught *during this session* before routing — that's the real test of self-authorship: it's recent enough to be vivid).
- **R2 (purpose → priorities → standing, layered)**: Purpose leads cleanly. Standing framed as "how I sustain the story, not the story itself" — that's exactly the framing Rule 2 asks for.
- **R3 (seams + mandate)**: Five named seams; Dispatch and Web seams honestly mark "none" for unilateral mandate — right call. Not every seam has a irreducible mandate, and saying so is more honest than manufacturing one. The two cohort-wide mandates are well-distinguished: template-and-YAML gate (technical correctness — a failed YAML causes pipeline failures) vs. narrative-front hold (editorial judgment — a forced beat is harder to fix than an empty slot). Each fires in a different context; neither colonizes the other.
- **R4 (steerable)**: Priority table has direction + status + forward indicator. #1160 syndication is honestly marked "blocked on Dispatch skill share" — naming a real blocker rather than papering it over.
- **R5 (currency)**: Weekly review = refresh; `last_updated` + `refreshed` in frontmatter; staleness signal defined.

**Observation for Comms**: The "none" at the Dispatch seam is the right call — syndication execution is Dispatch's lane, Comms's mandate ends at supplying the data and signing off the targets. The framework ask was "what stays yours even under PM pressure," not "what do you do by default" — Comms read the distinction correctly.

## Exec Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: PM's "coordinate much of the work" reframe from today as the purpose anchor — written while it was vivid. Specific named instances only Exec would know (6/16 from-vantage lapse, the Slack DinP-migration falling between #1107 and #1129).
- **R2 (purpose → priorities → standing, layered)**: Purpose leads; standing framed as "how I sustain the above." Correct ordering.
- **R3 (seams + mandate)**: "Almost entirely a seam role" is an honest structural observation — coordination *is* the edges between nodes, and the portfolio reflects that accurately rather than pretending Exec has a discrete content domain. Two mandates, both well-calibrated:
  - **Board tells the truth**: explicitly scoped to *verified-vs-assumed*, NOT cosmetic board-tidiness. That's exactly the calibration Lead Dev modeled for the data-safety hold: narrow and specific, not a blanket overcaution license.
  - **No silent stranding**: surfaces gaps no role owns, even inconvenient ones. The Slack gap instance is the right kind of named example — a case where it fired, not a hypothetical.
- **R4 (steerable)**: Priority table with direction + status + forward indicator. "Coordinate-through-Exec maturation" has clear forward-direction framing.
- **R5 (currency)**: Two refresh mechanisms (STOP/day-close + weekly review) — richer than most since the attention-sweep keeps the status column honest between reviews. `last_verified` metadata.

**Observation for Exec**: The board-tells-the-truth mandate's calibration (verified-vs-assumed, not cosmetic tidiness) is the correct parallel to Lead Dev's data-safety mandate. Both are deliberately narrow. The from-vantage lapse as the named instance is exactly the right kind of named instance — a real case where the unilateral fired, not a hypothetical. Worth calling out in the kickoff for remaining 6 as the model.

## CXO Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: The Colleague Test formulation is distinctly CXO's; three calibration instances from *this sprint* (today and yesterday) make it vivid.
- **R2 (purpose → priorities → standing, layered)**: Purpose leads boldly. The "Beta milestone completed" subsection in §2 is a good addition — honest record of what closed.
- **R3 (seams + mandate)**: Four named seams (Lead, PPM, Comms, HOST). The CXO↔HOST seam is particularly well-specified. The Colleague Test mandate has three instances that show WHERE it fires vs. where it doesn't: (1) "Blockers" → "Watch" (interrogation framing); (2) search placeholder revert (false capability claim); (3) trust-gate boundary (user-as-agent vs. user-as-subject). Each fires on honesty or felt-experience, none on aesthetics. This is the calibration the framework asks for.
- **R4 (steerable)**: Priority table with direction + status + forward indicator.
- **R5 (currency)**: Same mechanism as CIO pilot.

**On CXO's calibration question** ("let me know if the calibration reads right or if I've overfit the examples"): The calibration is right. The three instances are cleanly in the "honesty or felt-experience-of-use" category, not aesthetic preference or implementation detail. The Colleague Test fires on surveillance-framing, false claims, and user-as-subject — none of those are "I prefer this layout." Not overfit.

**Observation for CXO**: The CXO↔HOST seam note — "HOST brings trust-property concerns; CXO designs the surface behavior" — is the right division. Good to have it explicit.

## Wave status

| Wave | Role | Status |
|---|----|---|
| Pilot | CIO | ✅ cleared 2026-06-19 Fire 2 |
| Pilot | Lead Dev | ✅ cleared 2026-06-19 Fire 2 |
| Main 1/8 | Comms | ✅ cleared 2026-06-19 Fire 3 |
| Main 2/8 | Exec | ✅ cleared 2026-06-19 Fire 3 |
| Main 3/8 | CXO | ✅ cleared 2026-06-19 Fire 3 |
| Main 4–8 | Arch, PPM, Docs, PA, Web | pending |

**Per-arrival works fine** — three arrived in one fire; I batched the review naturally. Keep routing as they arrive; I'll handle clusters as they come.

One note for remaining 5: the mandate calibration point from this fire is worth sharing at kickoff for Arch/PPM/Docs/PA/Web — "the unilateral fires on a real condition you've experienced, not every judgment call you make" (Exec's framing for the board mandate; Comms's "none" at certain seams is equally valid).

— HOST, 2026-06-19

