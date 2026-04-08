# Test Coverage Audit — April 7, 2026

## Key Statistics
- 58 total service modules
- 27 services (46.6%) with **zero test coverage**
- Total tests: ~6,100+ functions across platform

## Critical Infrastructure Gaps (Zero Coverage)
- `services/api/` — API handlers
- `services/cache/` — Caching layer
- `services/config/` — Configuration management
- `services/container/` — Dependency injection
- `services/persistence/` — Data persistence
- `services/scheduler/` — Task scheduling
- `services/session/` — Session management

## Critical Services with Minimal Coverage
| Service | Test Files | Test Count | Risk |
|---------|-----------|-----------|------|
| auth | 1 | 17 | HIGH — authentication |
| llm | 1 | 23 | HIGH — LLM integration |
| orchestration | 1 | 5 | MEDIUM — workflow orchestration |
| todo | 1 | 8 | HIGH — user-facing feature |

## Limited Coverage (< 80 tests)
- database (40 tests) — models.py is 83KB
- conversation (28 tests)
- infrastructure (53 tests)
- security (46 tests)

## Well-Tested (Reference)
- intent_service: 46 files, 1,186 tests
- mux: 29 files, 1,080 tests

## Observation
32% of all tests are concentrated in just 2 services (intent_service + mux).
Foundational infrastructure has essentially zero test coverage.

## Recommendations
1. Prioritize auth and llm test coverage — these are security and functionality critical
2. Config and container testing would catch the class of bugs we hit with port mismatches
3. Todo service needs real integration tests (Pattern-045 finding from UAT)
