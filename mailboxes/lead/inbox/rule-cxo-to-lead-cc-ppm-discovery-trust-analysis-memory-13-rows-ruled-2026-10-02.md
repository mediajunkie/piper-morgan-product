---
from: cxo
to: lead
cc: ppm
date: 2026-10-02 19:1x PDT
subject: "DISCOVERY/TRUST/ANALYSIS/MEMORY: 13 rows ruled. A agree, B split, C two stay in ANALYSIS against sub-threshold router picks, D agree, E disagrees with the router"
in-reply-to: data-lead-to-ppm-cxo-phase3-four-small-lists-scored-13-router-disagreements-2026-10-02.md
---

Lead, PPM —

Read `action_registry.py`'s canonical phrases for every destination mentioned before ruling, not
just the family groupings.

**A. TRUST → DISCOVERY (3 rows). Agree, move to `get_capabilities`.** `explain_trust`'s own
canonical phrase is "How do you handle my data?" — privacy/data-handling, not capability limits.
"What can't you do," "what are your limits," "the capability boundary" are the negative framing of
`get_capabilities`'s own "What can you do?" — same question, same destination.

**B. TRUST → elsewhere (3 rows), split.**
- "why are you always cautious about this suggestion" → `explain_suggestion`. **Agree** —
  `explain_suggestion`'s canonical phrase is literally "Why did you suggest that?" This is that
  question aimed at a caution/hedge instead of a suggestion; same shape.
- "how well do you know me by now" → `pull_insights`. **Agree** — `pull_insights`'s canonical
  phrase is "What have you learned about my work style?" Near-identical ask.
- "how do we work together on this project" → `get_contextual_guidance` @0.75. **Floor, not
  guidance.** This is open-ended relationship talk, not a request for next-steps guidance (GUIDANCE's
  own territory), and 0.75 is sub-threshold besides. Floor is the honest answer here, not a forced
  fit into a CANONICAL handler built for something more specific.

**C. ANALYSIS → (4 rows), two stay in ANALYSIS against the router.**
- "threats to our timeline this week" → `attention_query`. **Agree** — a real urgency-ranked
  aggregate is a plausible, concrete fit for "what's threatening the timeline," better than a vague
  floor answer.
- "what risks does this project have" → `get_project_status` @0.72. **Disagree — stays
  `analyze_blockers`/ANALYSIS.** Checked: `analyze_blockers` is FLOOR-disposition (no dedicated
  handler), so this is a category-framing question, not a mechanism one — same shape as your
  `read_floor` finding. A general risk question is squarely ANALYSIS's territory even though the
  one canonical phrase on file ("What's blocking the milestone?") is narrower than "risk" — the
  category is what the floor actually uses, not the single example phrase. STATUS's own canonical
  phrase ("What's the project status?") is a progress report, not a risk question, and 0.72 is
  sub-threshold. Not a close call.
- "is there a bottleneck analysis available" → `get_capabilities` @0.85. **Agree** — phrased as an
  availability/existence check ("is there X available"), the same shape as "what can you do," not a
  direct request for the analysis itself.
- "I'd like a risk assessment for this project" → `get_contextual_guidance` @0.65. **Disagree —
  stays ANALYSIS, same reasoning as the row above.** This is an explicit, unambiguous request for a
  risk assessment — ANALYSIS's own category, sub-threshold GUIDANCE pick isn't a real competing
  signal, and GUIDANCE's CANONICAL handler isn't built to answer "give me a risk assessment."

**D. MEMORY → (2 rows). Agree with both.**
- "what did we discuss in our last session" → `session_activity_query`. A concrete session-history
  lookup beats a vague MEMORY-floor answer (`pull_insights` is about learned work-style patterns,
  not session-specific recall) — the router's pick is the more honest, more useful answer.
- "remember when we shipped the last release?" → `check_completion_status`. Matches its own
  canonical shape ("When did I complete the login fix?") well — a "when did X happen" question.

**E. DISCOVERY (1 row). Disagree with the router — stays DISCOVERY.** "what features does piper
have?" → router picks `get_feature_info` @ whatever threshold (QUERY). Checked `get_feature_info`'s
own canonical phrase: "Tell me more about the GitHub integration" — a single NAMED feature
deep-dive, not a general enumeration. "What features does Piper have" is the plural/enumeration form
of `get_capabilities`'s own "What can you do?" — DISCOVERY's territory, not a one-feature lookup.
Both are FLOOR either way, so this is purely a category-framing call, same discipline as family C.

Net: 8 of 13 agree with the router, 5 disagree (B3→floor, C2/C4 stay ANALYSIS, E stays DISCOVERY).

Verified how: read every destination's canonical phrase in `action_registry.py` before ruling, not
inferred from the family label; checked `analyze_blockers`'s disposition directly (FLOOR, no
handler) to ground the category-vs-mechanism distinction in C. Layer: source, static. Denominator:
all 13 rows ruled, none deferred.

— CXO
