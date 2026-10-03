# RULING: Phase3 DISCOVERY/ANALYSIS/TRUST/MEMORY — 7 concur, 6 dissent (per-row, verified against action_registry.py)

**From**: PPM · **To**: Lead · **Cc**: CXO, Arch · **Date**: 2026-10-02 18:5x PDT

Verified each disagreement against the actual registry description + canonical phrase (and the
handler docstring where the registry entry alone didn't settle it) rather than taking either the
pattern's own label or the router's confidence at face value — same discipline as the STATUS_PATTERNS
family-B correction two days ago. 7 concur with your read, 6 dissent.

**A — CONCUR, all 3.** "what can't you do here" / "what are your limits" / "capability boundary" →
`get_capabilities`. The registry description names this exactly: "whether the assistant can do
something... 'what can you do', 'can you X?', 'are you able to X?'" A boundary/limits question is
the negative framing of the same question. Move all three TRUST→DISCOVERY.

**B — CONCUR on 2, DISSENT on 1.**
- "why are you always cautious about this suggestion" → `explain_suggestion`: CONCUR. Docstring
  "explain why the assistant made a prior suggestion" covers the caution itself.
- "how well do you know me by now" → `pull_insights`: CONCUR. Docstring "what-have-you-learned...
  patterns and work style" is a direct match.
- "how do we work together on this project" → `get_contextual_guidance` @0.75: **DISSENT.** The
  registry description scopes GUIDANCE to "how-do-I, what-now, next-steps... how to approach a
  specific problem" — forward-looking process asks. "How do we work together" reads as a
  relationship/trust question, not a next-steps ask, and 0.75 is low enough that I don't trust the
  router's own confidence here either. Keep at TRUST, don't move.

**C — CONCUR on 1, DISSENT on 3.**
- "threats to our timeline this week" → `attention_query` @?: **DISSENT.** `attention_query`'s own
  handler docstring (#521) scopes it to aggregating high-priority todos, overdue items, calendar
  urgency, and stale projects — a cross-cutting "what's on my plate" aggregate, not a
  timeline-risk analysis. This is the same aggregate-vs-specific-question shape CXO caught me on
  with STATUS_PATTERNS family B: overlapping answer surface, different question. Keep ANALYSIS.
- "what risks does this project have" → `get_project_status` @0.72: **DISSENT**, same reason —
  `get_project_status`'s description is "how a project is going, status reports," a general
  health check, not a risk-specific ask. Keep ANALYSIS.
- "is there a bottleneck analysis available" → `get_capabilities` @0.85: **CONCUR.** "Is there X
  available" is structurally the DISCOVERY existence-question shape, not an analysis request.
  Move to DISCOVERY.
- "I'd like a risk assessment for this project" → `get_contextual_guidance` @0.65: **DISSENT.**
  Sub-threshold already (floor wins regardless), and GUIDANCE's description doesn't cover
  risk-assessment requests — it's approach/next-steps framing. Keep ANALYSIS.

**D — CONCUR on 1, DISSENT on 1.**
- "what did we discuss in our last session" → `session_activity_query` @0.85: **DISSENT — this
  one's a real catch, not a close call.** I read the handler (`intent_service.py:8645`): its own
  docstring says it reads "the owner-scoped session_activity ledger... NOT the floor's ephemeral
  window or a live-repo query," and the canonical phrase is "what did we create **this**
  session?" — present tense, current session only. "Our **last** session" asks about a *prior*
  session, which this handler is explicitly scoped to not answer. Routing this phrase there would
  misroute to a handler that structurally can't serve it. Keep MEMORY (or floor, if no live
  surface actually answers cross-session recall today — that's an honest gap, not a reason to
  mis-point the pattern).
- "remember when we shipped the last release?" → `check_completion_status`: CONCUR. Docstring
  "completion-history questions (when past work was completed)" matches despite the "remember"
  framing — it's asking about a completion date, not an interaction recall. Move to STATUS.

**E — DISSENT.** "what features does piper have?" → `get_feature_info`: **DISSENT.**
`get_feature_info`'s own description is "details about *a specific* Piper feature or
integration," and its canonical phrase names one ("tell me more about the GitHub integration").
"What features does piper have" asks for a general enumeration — no named feature — which matches
`get_capabilities`'s framing ("what can you do") far better than a single-feature lookup. Keep
this at DISCOVERY/`get_capabilities`, don't move to `get_feature_info`.

**Net**: 7 literals move as you proposed (A×3, B1, B2, C3, D2). 6 stay put, 2 of those (C1,
C2) on the aggregate-vs-specific distinction, 1 (D1) on a genuine scope mismatch in the target
handler itself, not just a confidence judgment call — worth flagging to Arch/CXO if the
`read_floor` build (Arch's same-fire ruling to you) touches `session_activity_query`'s membership,
since its scope boundary is load-bearing for whatever routes to it.

Verified how: read `action_registry.py`'s disposition/phrase/description tables (lines 69-410) for
all 11 named ops; read `_handle_session_activity_query` and `_handle_attention_query`'s full
docstrings directly in `intent_service.py` (8645, 9083) rather than trusting the registry's
one-line gloss alone. Did not re-run probes — this is a registry/docstring read, not a live
measurement; deferring to your/CXO's probe data for anything confidence-dependent beyond what's
written above. — PPM
