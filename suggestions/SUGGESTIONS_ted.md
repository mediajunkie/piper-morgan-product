# Suggestions (Ted Nadeau)

Pre-issue ideas and change requests. Promote to GitHub issues when triaged/approved.

---

## Open

- **Consider LangChain in addition to or alongside PM LLM adapter**  
  Context: LangChain offers observability, chains, agents, RAG; PM adapter is minimal and fast. Option: use LangChain for flows that need those features, keep adapter for simple completion/streaming.  
  Status: open

- **Add observability to LLM adapter (e.g. LangChain-style tracing)**  
  Context: Today the adapter logs usage only; no request/span tracing or runnable callbacks. Adding tracing (e.g. spans, run IDs, optional export to LangSmith or OTLP) would help debugging and cost analysis.  
  Status: open

- **Add a dedicated data model / data dictionary document, visualizable as an ER diagram**  
  Context: A single authoritative data dictionary (tables, columns, types, FKs, relationships) would help onboarding, migrations, and cross-team alignment. The document should be machine- or tool-friendly so it can be rendered as an entity-relationship diagram (ER diagram).  
  **Where it currently exists**:  
  - **Code (source of truth for DB schema)**: `services/database/models.py` (SQLAlchemy ORM: tables, columns, FKs, relationships); `services/domain/models.py` (domain/in-memory models); `alembic/versions/` (migration scripts).  
  - **Docs (architecture)**: `docs/internal/architecture/current/models/` (domain-models-index.md, models-architecture.md, domain-models.md, models/ subdirs: pure-domain, supporting-domain, integration, infrastructure); `docs/internal/architecture/current/database/` (personality-schema.md, README).  
  There is no single data-dictionary document or ER diagram artifact today; schema is inferred from code and scattered architecture docs.  
  Status: open

---

## Drafted

_(Artifact drafted; ready for review, edit, or promotion to issue.)_

- **Add PR/FAQ (Working Backwards) for Piper Morgan**  
  Context: Amazon-style PR/FAQ aligns stakeholders on what we're building and for whom before committing. Piper Morgan had no PR/FAQ; one was requested.  
  Deliverable: [docs/internal/design/piper-morgan-prfaq.md](../docs/internal/design/piper-morgan-prfaq.md) (press release + FAQ; linked from NAVIGATION under Product Managers).  
  Status: drafted

---

## Promoted

_(When a suggestion becomes an issue, add it here with link.)_

- (none yet)

---

## Deferred / Rejected

_(Move here with a short reason if we decide not to pursue.)_

- (none yet)
