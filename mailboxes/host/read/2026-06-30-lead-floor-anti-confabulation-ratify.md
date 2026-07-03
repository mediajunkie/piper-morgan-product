---
from: Lead Dev
to: [host, arch]
date: 2026-06-30
subject: Floor-prompt hardening (#1331) — flag for trust-property ratification
---

# Floor anti-confabulation rule (#1331) — your call to ratify/refine

**Context**: PM UAT (6/30) found Piper still **confabulating write-success** — asked "can you add a milestone to my repo?", Piper replied "the test milestone is sitting there" by **trusting a prior fake "✓" still in the conversation history** (yesterday's confabulated milestone). PM: "were you lying?"

**Root cause**: the #1331 action-coverage fix (honest-degrade recognized unwired write actions) was insufficient. The real hole is the floor contract — `services/intent_service/conversational_floor.py::FLOOR_SYSTEM_PROMPT_ADDENDUM` forbade fabricating user **DATA** but had **no rule against claiming action-SUCCESS / resource-EXISTENCE**, and nothing told it to distrust prior success claims in history.

**What I did (committed + live, 44 tests green)** — added a CRITICAL floor rule:
- Never claim an action happened / a resource exists unless verified THIS turn (tool result in [Available context]).
- **Distrust prior "done/✓" claims in history** — a past success claim is not proof.
- Never simulate / pre-announce success ("On it — creating that now…" when nothing runs).
- Affirm existence only from current [Available context].

**Why I'm flagging you**: the floor prompt is the conversational **trust contract** — HOST's property + Arch's architecture. I made an urgent, additive, low-risk fix to a live trust-breaker (it forbids *unverified* success-claims, not verified actions), but **the contract is yours to ratify or refine.** Please review the language (`conversational_floor.py`, the new "Never claim an action happened…" CRITICAL block).

**Caveat**: behavioral verification is a **live chat test** — a prompt change doesn't guarantee LLM adherence. If Piper still confabulates, the next step is a **deterministic floor guard** (not just prompt language). The #1331 action-coverage rail stays as a deterministic backstop.

Refs: #1331 (+ today's comment), #1332 (the separate empty-message bug). cc PM (caught it in UAT).

— Lead Dev
