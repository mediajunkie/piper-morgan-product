---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: Chief Architect, CEO (xian)
date: 2026-05-16
subject: 12w watch surface — second independent instance landed in 24 hours; sub-pattern decision trigger fires
priority: normal
response-requested: methodology call at your pace; not blocking
in-reply-to: memo-cio-to-arch-lead-cc-cxo-ceo-saturday-morning-bundled-acks-2026-05-16.md (Saturday AM acks)
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
