# DATA: DISCOVERY / ANALYSIS / TRUST / MEMORY deposited and scored — 13 router disagreements for ruling (no PM decision inside)

**From**: Lead Developer · **To**: PPM, CXO · **Date**: 2026-10-02 16:04 PDT

Four small pattern lists (62 rows deposited this afternoon, scored on Haiku): DISCOVERY 18/19, ANALYSIS 11/15, TRUST 9/15, MEMORY 11/13. All four route to floor destinations today (get_capabilities, analyze_blockers, explain_trust, get_memory). The 13 disagreements, grouped — in several the router looks more right than the pattern, which is the point of asking:

**A. TRUST → DISCOVERY (3).** "what can't you do here", "what are your limits as an assistant", "what's the capability boundary here" → router `get_capabilities` @0.85–0.92 (pattern: explain_trust). *My read*: these ask what Piper can do, not how it handles data — get_capabilities. A ruling moves three literals from the TRUST list to the capability answer.

**B. TRUST → elsewhere (3).** "why are you always cautious about this suggestion" → `explain_suggestion` (PROVENANCE's own op — plausible); "how well do you know me by now" → `pull_insights` (MEMORY — plausible); "how do we work together on this project" → `get_contextual_guidance` @0.75 (guidance — plausible, or floor).

**C. ANALYSIS → (4).** "threats to our timeline this week" → `attention_query` (live read; plausible); "what risks does this project have" → `get_project_status` @0.72; "is there a bottleneck analysis available" → `get_capabilities` @0.85 (asks whether the feature exists — a capability question, arguably right); "I'd like a risk assessment for this project" → `get_contextual_guidance` @0.65 (sub-threshold). Is `analyze_blockers` what any of these should reach, or is the floor honest?

**D. MEMORY → (2).** "what did we discuss in our last session" → `session_activity_query` @0.85 (a live read that answers exactly this — I'd rule it); "remember when we shipped the last release?" → `check_completion_status` (floor STATUS; plausible).

**E. DISCOVERY (1).** "what features does piper have?" → `get_feature_info` (FEATURE_INFO's own op — plausible).

One line per family is enough. Surface-2 probes for all 62 rows are running now (both provider legs, N=5) so the gate can read these lists under the same rules as the four deleted today.

Verified how: `inversion_phase1_shadow_score.py --provider anthropic` per list, served line quoted in each report (`docs/internal/architecture/current/inversion-phase3-{discovery,analysis,trust,memory}-score-2026-10-02.md`); 62 Haiku calls, 0 ERROR. — Lead
