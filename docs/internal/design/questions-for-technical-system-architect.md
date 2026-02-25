# Questions for Technical System Architect

**Purpose**: Prepare for a meeting with a technical system architect to discuss Piper Morgan.  
**Audience**: PM / product lead meeting the architect.  
**Source**: Derived from codebase review, ADRs, and open suggestions (Jan 2026).

---

## How to Use This

- **Before the meeting**: Skim the “Current architecture (for context)” section so you can orient the architect in 2–3 minutes.
- **During the meeting**: Use the questions as a checklist; skip or reorder based on time and the architect’s focus.
- **After**: Capture decisions or follow-ups; consider promoting any agreed direction into an ADR or issue.

---

## Current Architecture (For Context)

- **Stack**: Python 3.11+, FastAPI, PostgreSQL (async), Redis, ChromaDB; optional Temporal.
- **Entry**: All requests go through **intent classification** (`services/intent_service/`), then canonical handlers.
- **Services**: Domain logic in `services/`; no controllers talking to DB directly. **ServiceContainer** is app-scoped (FastAPI lifespan), not a global singleton—ADR-048.
- **Integrations**: Slack, GitHub, Notion, Google Calendar, MCP; swappable backends (e.g. GitHub vs Jira) per Pattern-040.
- **Memory**: Conversational memory (DB), cross-session layers (ADR-054), learning/composting.
- **Multi-tenancy**: ADR-058 in progress—user-scoped tokens, RequestContext enforcement, owner_id filtering.
- **Deployment**: Single-process today; horizontal scaling unblocked by ADR-048 but not yet run multi-worker/Kubernetes.
- **Docs**: 60+ ADRs in `docs/internal/architecture/current/adrs/`; PR/FAQ and “by analogy” in `docs/internal/design/`.

---

## 1. Scaling & Deployment

1. **Multi-worker / horizontal scaling**  
   We moved ServiceContainer off a singleton to app state (ADR-048). What’s the next set of steps you’d recommend to run multiple uvicorn workers or scale out behind a load balancer (e.g. session affinity, shared Redis, anything we might have missed)?

2. **Stateful vs stateless**  
   Where is our remaining state that would break under multiple instances (in-memory caches, background jobs, WebSockets)? How would you make the app “stateless enough” for horizontal scaling?

3. **Kubernetes vs simpler orchestration**  
   We have Docker Compose for staging (ADR-007). For a first production deployment, would you advise going straight to Kubernetes, or a simpler path (e.g. single-node + Compose, or managed app platform)? What would change in our architecture for K8s?

---

## 2. Data Model & Persistence

4. **Single source of truth for schema**  
   DB schema lives in `services/database/models.py` (SQLAlchemy) and alembic migrations; domain and docs are in other places. We’re considering a single **data dictionary / data model document** that can also drive an ER diagram. What format and workflow would you recommend (e.g. schema-first codegen, doc-from-DB, or doc-as-source)?

5. **Cross-session memory and retention**  
   We have a three-layer memory model (conversation, history, composted learning—ADR-054). How would you approach retention, archival, and GDPR-style “right to be forgotten” without breaking learning and context? Any patterns (e.g. soft delete, anonymization, separate analytics store)?

6. **Postgres + Redis + ChromaDB**  
   We use Postgres for relational data, Redis for cache/sessions, ChromaDB for embeddings. For a future multi-region or higher-availability deployment, what would you change (replication, failover, or consolidating/splitting stores)?

---

## 3. Integrations & Federation

7. **“Colleague that shows up where you are”**  
   Vision is Piper in Slack, web, future email/IDE. We have a single backend that multiple frontends call. How would you architect for Slack-first vs web-first vs adding email/IDE later (e.g. event-driven, webhooks, adapter layer, or separate edge services)?

8. **Swappable backends (Jira vs GitHub vs Linear)**  
   We have an integration swappability pattern (Pattern-040). When we add Jira/Linear alongside GitHub, how would you avoid the “N+1 integration” maintenance trap (unified abstraction vs thin adapters, testing strategy, feature flags)?

9. **MCP and agent protocols**  
   We use MCP for some integrations. Where would you draw the line between “our API + MCP adapters” vs “MCP-first and we’re just one tool”? Any pitfalls or standards we should align with?

---

## 4. Security & Multi-Tenancy

10. **Enforcing user isolation**  
    ADR-058 is tightening multi-tenancy (user-scoped tokens, RequestContext, owner_id). What’s your checklist for “tenant isolation” in a system like ours (auth at edge, query-level filtering, audit logging, secrets per tenant)?

11. **API keys and secrets**  
    We store provider API keys (OpenAI, etc.) in a keychain; user OAuth tokens in DB. How would you segment app vs user secrets, rotation, and audit in a way that stays simple for a small team?

12. **Auth and identity**  
    Today: JWT, optional Slack/OAuth for some flows. If we add “login with Google/Microsoft” or SSO, what would you change in our auth layer (identity provider abstraction, token format, refresh)?

---

## 5. Observability & Operations

13. **LLM observability**  
    We have minimal tracing on the LLM adapter (no spans, run IDs, or cost attribution per request). We’re considering something LangChain-style or OTLP. What’s the minimal observability you’d want before production (per-request latency, token usage, errors, optional sampling)?

14. **Health and dependency checks**  
    We have health endpoints and a setup wizard that checks DB, Redis, ChromaDB, etc. What would you add for “production readiness” (dependency health, circuit breakers, graceful degradation, or runbooks)?

15. **Feature flags and config**  
    Config is a mix of env, PIPER.user.md, and DB. How would you introduce feature flags and environment-specific config without turning it into a big migration (e.g. single config service, flags in DB, or external system)?

---

## 6. Strategic / Future

16. **Meta-platform (practitioner / demonstrator / enabler)**  
    ADR-000 describes Piper as practitioner (do PM work), demonstrator (show orchestration), enabler (let PMs orchestrate agents). From a system architecture perspective, what would you build first to support “enabler” (e.g. workflow engine, agent registry, sandbox)?

17. **Tech debt and refactor order**  
    We have a large `web/app.py`, some remaining direct ServiceContainer use (deprecated per Issue #322), and plugin loading. If you had to pick one refactor to do before scaling or adding major features, what would it be and why?

18. **Documentation and onboarding**  
    We have many ADRs and internal docs. What would make the system easiest for a new architect or senior engineer to understand in one day (e.g. one-pager, C4 diagrams, runbook, or “architecture decision index”)?

---

## References (If Architect Wants to Go Deeper)

| Topic | Location |
|-------|----------|
| Meta-platform vision | ADR-000 |
| ServiceContainer lifecycle (no singleton) | ADR-048 |
| Multi-tenancy isolation | ADR-058 |
| Cross-session memory | ADR-054 |
| Intent as universal entry | ADR-032, ADR-039 |
| Integration swappability | Pattern-040 |
| Staging / Docker | ADR-007 |
| PR/FAQ (product narrative) | docs/internal/design/piper-morgan-prfaq.md |
| Piper vs Jira (positioning) | docs/internal/design/piper-morgan-by-analogy.md |
| Open suggestions (observability, data dictionary) | suggestions/SUGGESTIONS_ted.md |
