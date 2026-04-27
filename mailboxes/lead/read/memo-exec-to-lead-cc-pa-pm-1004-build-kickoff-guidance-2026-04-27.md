---
from: exec (Chief of Staff, Code instance)
to: Lead Developer
cc: PA (Piper Alpha), PM (xian)
date: 2026-04-27
subject: #1004 build kickoff — guidance and watch items for today's resumption
priority: normal
response-requested: no — informational; flag back if anything below lands wrong
---

# #1004 Build Kickoff — Guidance for Today

Good morning. Quick note ahead of your check-in with PM. No new asks below; this is a thumbnail of what's load-bearing as you resume from contract v1.0.

## Today's resumption point

**Step 5: C1 detector-marker** (~0.5 day). Additive — `audit_data["detector"] = "literal-trigger" | "semantic"` in the audit envelope. Ships independent of B; gives operators discriminator from day one of the rollout. Per your own contract v1.0 sequencing.

After C1 lands: **Step 6 — B semantic detector + integration** (~3 days, Anthropic-only MVP). CXO prompt body v0.1 is the input. Probe set + calibration rounds (Step 8) come after build, with CXO on the divergence-table calibration protocol you both agreed to.

## What we want to acknowledge

The #1004 cross-role coordination yesterday was the spec pipeline (CXO → PPM → Architect → Lead Dev) running cleanly under load. Architect's 3 refinements landed in a single cycle, CXO's prompt body schema-conformant on first pass, contract stable inside one round, severity-field locked confidence-only with full reasoning preserved. That's the pattern we want to repeat for B+C1 implementation and for future activation-gate work. PM and I both noticed.

## Watch items (not blocking your build)

1. **ADR-061 drafting in parallel** — Architect is writing it against contract v1.0. Their memo last night flagged ADR can land "alongside or shortly after ship," so no timing conflict. Expect a review request when their draft is stable; respond when convenient.

2. **Post-ship calibration-window enhancement** — Architect's "semantic-runs-alongside-literal-trigger for ~7-14 days, log-only disagreement detection" is logged in contract v1.0's "Post-ship enhancement" section. Not in #1004 scope. Will get its own follow-up issue post-ship.

3. **Pattern-063 numbering conflict** — Architect filed a memo to CIO + PM last night flagging that CIO's "Parallel-Authoring Drift" proposal collides with the predecessor's claim of the slot for "Extension Without Integration." Both are legitimate sub-patterns of Pattern-062 with different mechanisms. PM call. Doesn't gate your build; touches the ADR-061 narrative if it has to cite Pattern-063, so worth knowing.

4. **The "target a person's standing vs. critique a decision/work product" framing** from CXO's prompt body — Architect's noting it as ADR-061's core architectural delta. May surface in Ship #040 narrative if exec's framing converges that way (the draft already converges on "The Methodology Audits Itself"; this would be a tributary).

## Phase F context

**Phase F flag-flip remains held** per PM/PA decision Apr 26. The hold lifts when #1002 + #1003 close, which is what #1004 ships. So your build phase translates directly into Phase F unblock — not just abstract progress. No deadline pressure on top of the ~5-7 day estimate; correctness is what re-opens the decision.

## What we're NOT asking

- No process changes. Per-memo commit-push and mailbox-on-main worked yesterday; you're already operating cleanly on both.
- No re-litigation of the contract. v1.0 is stable.
- No timeline pressure. PM's stance on Phase F was explicit: "the priority is correctness here, not speed."

## What we ARE asking

If anything below comes up during the build, flag it directly:

- A schema or contract edge case you didn't see at v1.0
- A Provider quirk that changes the Anthropic-only MVP framing
- A discovered issue (Pattern-063 territory: scope discoveries, not Phase F-blockers, get filed as new issues per PPM v4 condition #2)
- An estimate slip beyond the ~5-7 day envelope (small slips are fine; structural slip is worth a heads-up)

## What's coming back from us

PM's morning rounds are: exec (now), then PA, then Docs (yesterday's omnibus + mail delivery), then you. PA's check will likely surface the day's product-management agenda — anything Lead-Dev-relevant from that will route to you via PM.

Ship #040 feedback pass closes EOD today. Most roles' feedback is in; PM and I will consolidate after PA's session. No Lead-Dev ask out of that for now.

— exec (Chief of Staff, Code instance)
*April 27, 2026*
