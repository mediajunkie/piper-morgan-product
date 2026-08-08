# Principal-dropping audit — 2026-08-08 (PM-directed, off #1394's root cause)

**Directive**: PM, after #1394 revealed the floor's main artery had no user_id parameter and read
anonymous-keyed context for every authenticated user: "that alone seems like it warrants some sort
of audit."

**Method (m-43)**: static AST + call-chain analysis at 45d56e4a2 (post-#1394 fix). No runtime probes.
**Denominators**: 578 source files parsed · 18 user-scoped state surfaces enumerated · 9 primitive
families / all call sites signature-checked · ~30 intermediates caller-traced · 883 test files
parsed (49 drive principal-keyed paths: 33 fully blind / 7 partial / 9 authenticated).

## LIVE findings

**F1 — agenda Tasks read todos with owner_id=session_id** (canonical_handlers.py:2560/:2349-2365):
`_get_todays_todos` had NO user_id parameter (the #1394 signature); todos are written with
owner_id=user_id → agenda Tasks structurally empty for every authenticated user.
**FIXED same day** (threaded; anonymous → honest [] without query; pins in
test_agenda_principal_f1_f2.py).

**F2 — agenda priorities read user context session-only** (canonical_handlers.py:2565, the only
session-only get_user_context call in the file): user_prefs and db_projects are `if user_id:`-gated
→ priorities always generic PIPER.md, never the user's. **FIXED same day** (user_id passed).

**F3 — conversation persistence has no ownership check** (OPEN — filed as its own security issue):
`get_recent_turns` / `load_context_state` / `hydrate_turns_from_db` have no principal parameter;
web/api/routes/intent.py:409-431 checks conversation EXISTENCE only, never owner;
`ensure_conversation_exists` (repositories.py:1442) returns early on existing rows with no owner
comparison. Consequence: authenticated user B posting user A's session UUID hydrates A's turns into
B's floor prompt AND appends B's turns to A's conversation row. Bounded by session-UUID
unguessability; the REST surface (conversations.py:173) enforces exactly the check the chat path
skips. Fix: thread principal into the three persistence reads + owner check at ensure/route,
mirroring the REST rule.

## RECOVERED-BUT-UNTHREADED (masked by the #1252/#1394 recovery; one refactor from regressing)

Four category fall-through handlers lack user_id in signatures (recovery covers; cosmetic).
Raw `intent.context.get("user_id")` reads bypassing the sanctioned `_principal_from_intent`:
intent_service.py:3193/:4463 (slot-filling history), :9610 (_fetch_issue_content — falls back to
SYSTEM GitHub token when absent), canonical_handlers.py:2892. classifier.py:595 classify_conscious
(anonymous-keyed; zero prod callers; delete-candidate with #1526-class).

## INERT / by-design (denominator honesty)

Pending-offer store session-only deliberately (#846 auth-flap); onboarding session fallback (#490);
scheduler system context; context_tracker (demo-only); keychain/BYOC surface fully threaded (clean).

## TEST-BLIND half — why the class stays invisible

33 of 49 principal-path test files never pass a non-None user_id → the anonymous and authenticated
keys coincide and no assertion can distinguish them (probe shape ≠ live shape — the hooks lesson).
Worst: tests/intent/contracts/test_multiuser_contracts.py — 26 process_intent calls, zero authed;
"users" simulated as session ids. The multi-user contract suite cannot see the user dimension of
the key it certifies. Full prioritized suite list in the audit agent's report (session record
2026-08-08); shape to copy: test_floor_history_principal_1394.py.
**Standing review rule**: any new test of a `{user_id or 'anonymous'}:{session_id}`-keyed surface
must assert at least once under a non-None user_id — a probe where the keys coincide is a config
check, not a verification (m-44).

## Guards (designed + validated against the tree; implement with the F3 fix)

1. **No unthreaded principal-keyed reads** — AST guard over PRINCIPAL_KEYED_READERS; must pass a
   non-None user_id or contain a `_principal_from_intent` recovery, else allowlisted. Validated:
   exactly 2 sites fire today (classifier.py:595 dead; F2 — now fixed → baseline 1 → 0).
2. **session_id is never an owner** — no call may pass owner_id=session*. Validated: exactly 1
   site fired (F1 — now fixed → zero-baseline immediately).
3. **Persistence reads accept a principal** — signature assertions on the three F3 readers;
   enable with the F3 fix.
