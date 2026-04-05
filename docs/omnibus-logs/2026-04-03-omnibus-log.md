# Omnibus Log: Thursday, April 3, 2026

**Date**: Thursday, April 3, 2026
**Day Type**: STANDARD — M1 Gate UAT execution (evening session)
**Sessions**: 3 (3 roles: PA, CXO, Lead Dev)
**Git Commits**: 5+ (product repo)

---

## Chronological Timeline

### Evening: M1 Gate UAT (7:06 PM – 12:00 AM)

**7:06 PM**: **PA** begins Day 5 session. Light day — main focus is M1 Gate UAT preparation. PM's plan: review gate criteria → engage CXO → engage Lead Dev → set up fresh alpha account → run tests → report.

**~9:53 PM**: **CXO** begins session. Reviews UAT prep document from Mar 31, updates with verified test plan from actual #926 issue body. 9 Gate 1 queries and 5 Gate 2 scenarios finalized.

**10:00 PM**: **Lead Dev** begins session. 3 unread memos in inbox (all low priority, none blocking UAT). Starts environment cleanup: Docker Desktop zombie port bindings on 5433, 6379, 8000 require full laptop reboot.

**10:05 PM**: **Lead Dev** resolves environment issues: stale venv (shebangs pointing to old path), dependency conflict (`fastapi` requires `anyio<4`, `mcp` requires `anyio>=4.5`), port mismatch (`.env` has 5432, Docker maps to 5433). Server starts clean.

**10:35 PM**: **PM + CXO** begin UAT execution on fresh alpha account (v0.8.6 on faoilean).

**Gate 1 results** (7 of 9 tested): **0/7 passed Colleague Test.** 4 auto-fails (Relevance=0 or Competence=0). 2 marginal (score 5, below 7 threshold). Queries tested: "What can you help me with?", "Do you remember what we talked about yesterday?", "Thanks for the help", "How trustworthy are your recommendations?", "Tell me about yourself", "Help me plan a stakeholder presentation", "Create a GitHub issue about testing". All but one returned identical canned template response.

**Gate 2 results** (1 of 5 tested): **Todo lifecycle FAIL.** Add works (rigid syntax only), list works, completion non-functional (4 attempts, all failed).

**~10:58 PM**: Testing stopped. **Gate verdict: NOT PASSED.** Further testing unproductive until blocking findings resolved.

**11:00 PM**: **CXO** compiles 5 findings into structured memo for Lead Dev:

1. **Floor LLM not reaching user** (BLOCKING) — 5 of 6 floor-routed queries returned identical canned `FLOOR_GRACEFUL_FALLBACK` template. Root cause: conversation task type hardcoded to Anthropic provider (`llm/config.py:54`), Anthropic validation failing with 404, all floor calls fail silently to catch-all.
2. **Canned template masks all failures** (BLOCKING) — same response for different failure modes, no diagnostic differentiation.
3. **Handler path lacks pre-flight checks** (MODERATE) — GitHub action attempted without checking integration state.
4. **Todo completion non-functional** (BLOCKING) — Pattern-045 confirmed: 23 tests pass (all mock `TodoManagementService`), user cannot complete todos. Regex rejects natural phrasing ("Add a todo").
5. **Input parsing too rigid** (MODERATE) — rejects natural language when intent is clear.

**Lead Dev** files 2 new issues:
- **#939** — UI: Piper avatar shows without speech bubble (cosmetic)
- **#940** — LLM config: single-provider setup, no hardcoded provider, key failure handling (BLOCKER)

**12:00 AM**: **Lead Dev** wraps session. Three fixes needed for re-test: LLM provider config (#940), todo persistence, todo regex. PM wants to tackle #940 first in morning session.

---

## Executive Summary

### Core Themes

- **M1 Gate: NOT PASSED.** First formal UAT execution after 2+ weeks of preparation. 0/7 Gate 1 queries passed the Colleague Test. Gate 2 todo lifecycle failed at completion. Testing stopped after 8 of 14 scenarios due to systemic failures.
- **Pattern-045 confirmed in production**: Both the floor path and the todo handler exhibit "green tests, red user" — automated tests pass while real user experience is broken. The CXO's insistence on fresh-account testing and scored rubrics caught exactly what it was designed to catch.
- **Root causes identified**: Floor failure traced to hardcoded Anthropic provider with failing validation. Todo completion traced to mocked-only tests never hitting real DB.
- **Clear path to re-test**: #940 (LLM provider config) is the primary blocker. Once fixed, floor should work. Todo completion and regex fixes are separable.

### Technical Details

- `services/llm/config.py:54-59`: conversation task type hardcoded to Anthropic
- `conversational_floor.py:326-380`: floor calls fail → `FLOOR_GRACEFUL_FALLBACK` template returned
- `todo_handlers.py:427`: regex rejects article "a" in natural phrasing
- `.env` port mismatch: POSTGRES_PORT=5432 vs Docker's 5433 mapping
- Dependency conflict: fastapi/anyio version pinning vs mcp requirements
- Issues filed: #939 (cosmetic), #940 (LLM config blocker)

### Impact Measurement

- M1 gate status changed from "ready to test" to "NOT PASSED — blocking issues identified"
- 2 new issues filed (#939, #940)
- UAT findings memo delivered (CXO+PM → Lead Dev)
- UAT test plan finalized and verified against #926
- Clear remediation path established (3 fixes → re-test)

### Session Learnings

- Fresh-account UAT on real infrastructure catches what unit tests miss — the gate design proved its value
- Environment setup friction (Docker zombies, stale venv, port mismatches) cost ~35 minutes — worth a setup script
- CXO's scored rubric (R/C/T with auto-fail thresholds) makes pass/fail unambiguous — no room for "feels okay" rationalization
- Stopping early was the right call: systemic floor failure makes remaining tests uninterpretable

---

## Sources

- `2026-04-03-1906-pa-opus-log.md` — PA (UAT coordination, results capture)
- `2026-04-03-2153-cxo-opus-log.md` — CXO (test plan, execution, scoring, findings memo)
- `2026-04-03-2200-lead-code-opus-log.md` — Lead Dev (environment setup, root cause investigation, issues filed)
- `memo-cxo-pm-to-lead-dev-uat-findings-2026-04-03.md` — UAT findings memo

---

*Omnibus synthesized: April 4, 2026*
*Sessions: 3 | Roles: 3 | Format: STANDARD*
