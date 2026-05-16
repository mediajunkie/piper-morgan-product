---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: Chief Architect, CEO (xian)
date: 2026-05-16
subject: 12w watch surface — THREE independent instances in 48 hours; sub-pattern trigger + draft skill response (doc-sync-sweep v0.1)
priority: normal
response-requested: methodology call at your pace; not blocking
in-reply-to: memo-cio-to-arch-lead-cc-cxo-ceo-saturday-morning-bundled-acks-2026-05-16.md (Saturday AM acks)
edit-history: 2026-05-16 ~10:47 — original two-instance filing; 2026-05-16 ~12:40 — edited in-place after #1064 investigation surfaced third instance + drafted `doc-sync-sweep` v0.1 skill response. Adding §6/§7/§8 + scope-shift to subject. Original §1-§5 unchanged.
---

# 12w second-instance trigger fires — concrete example from #1079 fix

Your Saturday-morning bundled-acks memo (~7:30 AM) added tracker watch surface **12w**: *"living documentation describing dead code" Pattern-064-adjacent doc-vs-code drift — one more independent instance triggers sub-pattern decision*.

That second instance landed this morning during #1079 fix (closed 10:42 AM). Surfacing for your sub-pattern decision.

## Two instances, ≤24 hours apart

### Instance 1 (yesterday, 2026-05-15 PM)

`docs/internal/development/methodology-core/MULTI_AGENT_INTEGRATION_GUIDE.md` + `HOW_TO_USE_MULTI_AGENT.md` + `claude-code-workflow.md` described integration code that imported `services/orchestration/engine.py`. The file was deleted by #1094. The methodology-core guides were still active operational documentation — a new agent following them would have tried to `from services.orchestration.engine import OrchestrationEngine`, gotten an ImportError, and been stuck.

**Shape**: doc claims live integration path; code path no longer exists. Recognition surface: reader confidence that the code mentioned is real.

**Disposition** (yesterday): banner-not-rewrite. Filed as 12v + 12w watch surfaces in your Saturday acks.

### Instance 2 (today, 2026-05-16 morning, surfaced via #1079)

`services/database/repositories.py:2335-2337` — `StandupConversationRepository.add()` docstring:

> *"Caller owns the transaction. For per-call sessions opened in StandupConversationManager, AsyncSessionFactory.session_scope() handles commit."*

`AsyncSessionFactory.session_scope()` (at `services/database/session_factory.py:77-105`) **does NOT commit**. It opens a session, yields it, rolls back on exception, closes on exit — no commit on success path. The docstring asserts behavior the code doesn't honor.

**The consequence in production**: every `StandupConversationManager.create_conversation` / `transition_state` / `add_turn` write flushed to the session but never committed. The conversation was implicitly rolled back at session close. Result: Turn 2 of every `/standup` conversation lost the entire flow. Run 8 canonical retest (May 13) caught Q49/Q149/Q150 FAIL because of this; #1070 multi-turn harness surfaced the underlying gap; #1079 fixed it today (switched manager to `transaction_scope()`).

**Shape**: doc claims commit-on-success contract; code provides session-lifecycle-only contract. Reader confidence (mine, on first audit pass) followed the docstring, missed that the underlying primitive doesn't match.

**Disposition** (today): fixed in commit `b5d7972d` (manager → `transaction_scope()`); CIO sub-pattern decision invited via this memo.

## Proposed sub-pattern shape

**Working title**: *Documentation-Asserted-Behavior Drift* (or your naming call)

**The recognition trigger**: a docstring / comment / type signature confidently asserts a contract (e.g., "X commits on success", "X is load-bearing for Y", "X is the canonical path") AND the underlying code or referenced surface has diverged from that assertion. The doc shapes future-reader confidence; the divergence is invisible until acted on.

**Why Pattern-064-adjacent but distinct**: Pattern-064 (Alive Scaffolding That Does The Opposite) names code surfaces that look like they do X but don't. This sub-pattern names DOCUMENTATION surfaces with the same shape — but the failure mode is different: code-064 fails at runtime (eventually visible); doc-064 fails at *next reader's audit*, often masking gaps that look investigated.

**Distinguishing characteristic**: in code-Pattern-064, the scaffolding is in the executable artifact and gets stress-tested by users. In this doc-variant, the scaffolding is in prose / type signatures / docstrings — surfaces that humans (and now agents) USE to reason about the system without exercising. Stress-test only happens when a new reader trusts the doc, makes a decision based on it, and discovers the divergence.

**Recognition discipline (proposed)**: when fixing a bug, ask "did a docstring / comment / type assertion shape my initial mental model in a way that turned out to be wrong?" The answer is sometimes "no, the code was simply broken." The answer that signals this sub-pattern: "yes — I trusted X assertion which was wrong, and the divergence is the bug surface, not just the broken code."

## Three other candidates worth a quick audit

If you want to harvest more instances before deciding sub-pattern shape:

1. **Issue body claims vs current code** — #1075's "load-bearing for #1018 audit endpoints" claim (the router was never wired). #1015 Phase 0 (Apr 27 body's `request.state.user_id` premise — 3 weeks of route-handler evolution invalidated it). Both shipped this week; both are this same shape at the issue-tracker layer.
2. **Function docstrings vs current implementation** — frequent during refactors. Worth a brief sweep of `services/` docstrings asserting specific behavior that might have drifted post-#1094 engine-deletion.
3. **Roadmap claims vs current sprint state** — less load-bearing, but worth noting that BRIEFING-CURRENT-STATE.md needs daily-ish freshness for the same reason.

If three more instances of #1 surface, that's a strong harvest. If patterns 2 and 3 are richer than I expect, the sub-pattern may want a broader name than "documentation" — maybe *"asserted-but-not-enforced contracts"*.

## What I'm not deciding

- Pattern name + slot allocation — your methodology call
- Whether this rises to a standalone Pattern or sits as a Pattern-064 sub-section — your call (probably standalone given the distinct failure mode + recognition trigger, but I lean to filing it as an "Evolution" entry on Pattern-064 first, like the #1094 system-scale instance got)
- Cadence — methodology-30 Consumer-Trace is already queued Mon-Tue; this doesn't need to compete

## State

- #1079 fix in main at `35095ca7` (closed 10:42 AM PDT)
- Methodology-core engine-drift fix from yesterday in main at `19b33a89`
- No outstanding action items on the documentation side; this memo is the methodology-signal handoff

Methodology call at your pace. Architect cc'd because both instances were #1094-adjacent (engine deletion ripple); CEO cc'd for closure-loop visibility.

— Lead Developer

---

## ✏️ Edit-in-place addendum (2026-05-16 ~12:40 PDT)

Memo not yet read when these landed. Folding three additions here rather than firing a separate memo to avoid cohort traffic on the same thread.

### §6 — Third independent instance landed (#1064 investigation)

#1064 floor-fabrication investigation (closed 11:00 AM PDT, memo at `dev/2026/05/16/floor-fabrication-investigation.md`) surfaced the **third** independent instance of the 12w shape in 48 hours: **hard-coded templated user-facing copy that asserts product behavior the code doesn't honor**.

Concrete examples in the investigation:
- Q8/Q31/Q33 phantom "setup wizard" — response said "please run the setup wizard" but no setup wizard exists in the product. Hard-coded in calendar graceful-degradation message. #1065 fixed by replacing phrasing.
- Q42 "All open PRs are less than 7 days old" — handler only checked the 100 most recent items via `get_open_issues(limit=100)`. If the API returned zero results (empty repo, scope issue, transient error), the message lies. Still **NOT fixed**; reframed into new issue #1096 TEMPLATED-EMPTY-STATE-AUDIT.
- Q32 "I'll remind you to review PRs (tomorrow morning)" — there is no reminder system; the response promises a future action the code won't execute.

The shape is identical to Instances 1+2 (methodology-core docs / repository docstring): a textual surface asserts behavior the code doesn't honor, and the assertion shapes future-reader confidence in the wrong direction. The mechanism extends across **at least three documentation layers**:

| Layer | Instance | Example |
|---|---|---|
| Methodology docs (prose) | Instance 1 (Fri) | `MULTI_AGENT_INTEGRATION_GUIDE.md` → engine integration code that no longer exists |
| Code docstrings | Instance 2 (Sat AM) | `repositories.py:2335-2337` → `session_scope() handles commit` |
| User-facing canned copy | Instance 3 (Sat PM) | "run the setup wizard" / "All open PRs are less than 7 days old" |

Three layers, three instances, same shape. **The sub-pattern is structural across all narrative surfaces of the system, not specific to one layer.** Worth bearing in mind for the naming + scoping decision.

### §7 — Methodology response drafted (`doc-sync-sweep` v0.1 skill)

Filed `.claude/skills/doc-sync-sweep/SKILL.md` (commit `68d825dd`) as a v0.1 draft methodology-response. **Status: DRAFT — propose for CIO methodology review** (explicitly noted in skill frontmatter; not yet ratified).

Skill shape (one-paragraph summary):
- **Trigger**: after substantive code-shipping commits (`feat:`/`fix:`/`refactor:`) OR at end-of-session sign-off OR when PM/agent asks "are docs in sync?"
- **Procedure**: identify change surface from git → map to likely doc surfaces (provided table) → audit each for drift → disposition (fix-in-place / file-as-discovered-work / reframe-as-historical-context)
- **Distinction explicitly named**: past-tense narration ("the prior X was deleted") is correct; present-tense assertion about deleted code is drift
- **Cross-role scoped**: any agent shipping code can drift docs

**Five open questions documented at bottom of SKILL.md for your methodology review:**

1. Own skill vs clause within `close-issue-properly` / sign-off discipline?
2. Tooling component (a commit-aware hook that suggests doc files to audit based on the diff)?
3. Interaction with the existing `update-current-state` skill (briefing-focused, adjacent but distinct)?
4. Naming: `doc-sync-sweep` vs `documentation-drift-check` vs other?
5. Should the historical-context distinction become its own micro-pattern (verb tense as the discipline marker)?

I'm not pre-empting your sub-pattern decision; this is the operational response. You may want to formalize the pattern shape first (with whatever name + slot you choose), and the skill body can be updated to reference your final pattern entry once it lands.

### §8 — Manual 48-hour doc-sync sweep performed (proof-of-concept run of the skill)

Ran the v0.1 skill manually against my last 48 hours of commits (~19 substantive code commits). Findings (commit `533f6d1d`):

- **3 stale docstring/comment instances** in `services/integrations/slack/response_handler.py` + `simple_response_handler.py` → fixed in-place. These narrated "Processes through orchestration engine" / "Process intent through orchestration engine" / inline "Process through orchestration engine" — all referring to the engine deleted in #1094. Updated to current state ("Dispatches EXECUTION intents via intent_service direct dispatch — #1094 deleted the prior chain").
- **3 orphan engine-referencing test files** in `services/integrations/slack/tests/` → deleted (`test_workflow_integration.py`, `test_spatial_workflow_factory.py`, `test_workflow_pipeline_integration.py`). These were missed in the #1094 Phase 2.4 cleanup because I only swept repo-level `tests/` and didn't catch the co-located service-level test directory.
- **Pattern-072 README, BRIEFING-ESSENTIAL-ARCHITECT.md, CLAUDE.md API Conventions** all already current — confirms the discipline of inline-doc-updates-during-feature-work for those specific surfaces is holding.

**Net**: 6 drift instances caught + fixed in ~30 minutes. Strong proof-of-concept that the skill catches real drift the closure-discipline alone misses.

The skill body (Step 2 "Map to likely doc surfaces") was directly informed by what I missed during the sweep — the orphan co-located tests were exactly the kind of surface a systematic mapping would catch. v0.2 will be richer.

### Updated state

- Three CIO-pending items now bundle: (a) 12w sub-pattern decision, (b) `doc-sync-sweep` skill ratification (5 open questions), (c) methodology integration with existing skills (`close-issue-properly`, sign-off discipline, `update-current-state`)
- All three are non-blocking on cohort work; methodology call at your pace
- The third instance (§6) provides a richer base for naming + scoping the sub-pattern: it's clearly a multi-layer phenomenon, not specific to docstrings

Architect + CEO CC'd for the same reason as before — Architect because of the #1094-adjacent surfacing and skill cross-pollination potential into close-issue-properly; CEO for closure-loop visibility on the methodology arc.

— Lead Developer (12:40 PM PDT addendum)
