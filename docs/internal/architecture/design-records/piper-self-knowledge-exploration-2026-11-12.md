# Piper self-knowledge: design exploration

**Status:** DRAFT. Arch's sections are written; CXO, Docs and CIO sections are open.
**Owner:** Arch. **Contributors:** CXO (ethos and voice), Docs (documentation and lore), CIO (methodology and best practices). PPM places it.
**Started:** 2026-11-12 14:22 PST, on xian's ask relayed by Exec.
**Milestone:** Production.
**Supersedes the scope of:** #1186. That issue covers help-doc pointers, support basics and RAG over Piper's own docs, and is narrower than this.

## The ask

xian, 2026-11-12, via Janus and Exec:

> "Piper should be as knowledgeable about its own codebase, ethos, documentation, lore, and best practices as any agent on the team building Piper Morgan. I want us to figure out how that should be implemented, and include it in the Production milestone."

This document explores how, first. A build comes after the recommendation.

The bar is "as knowledgeable as any agent on the team". An agent on this team knows itself through three things:
- a briefing it reads at the start of a session;
- tools that read the repository on demand (grep, file reads, `gh`);
- a shared vocabulary (glossary, ADRs, decisions.log).

It does not hold the codebase in memory. It looks things up and cites them. That is the model this document tests against.

## What exists today

Read on main, 2026-11-12.

| What | Where | What it gives Piper |
|---|---|---|
| Capability catalog | `services/intent_service/capability_legibility.py` `capability_catalog()` | A description of every action-triggered capability, generated from the workflow registry, the consent gate and the `chat_pointers` ledger. Nothing in it is written by hand per capability. Piper's knowledge of *what it can do* is already derived from code. |
| Chat pointers | `services/intent_service/chat_pointers.py` | Example asks that a test checks actually route somewhere (#1433). |
| Persona and context | `config/PIPER.md`, `config/PIPER.defaults.md`, `services/configuration/piper_config_loader.py` | The system-prompt persona and context. This is the closest thing Piper has to a briefing. |
| Document ingestion | `services/knowledge_graph/ingestion.py`, `document_service.py`; ChromaDB | Retrieval over documents a *user* uploads. Nothing of Piper's own docs is ingested. |
| Honest decline | #1186's 06-09 observation | Asked about its artifact model, Piper says it doesn't know. That's honest, but it's the gap this exploration closes. |

## The five areas

For each area: what knowing itself means; where the source lives; how Piper would reach it; what stays private; how it stays current.

### 1. Codebase (Arch)

- **What knowing means:** Piper can answer how a feature of its own works, citing the module that implements it. Example: "how does saving an artifact work?" gets an answer that names the service and the rule. It means what an agent on the team can do with grep and a read. It does not mean reciting code.
- **Source today:** the repository, which is public (`mediajunkie/piper-morgan-product`). The living architecture docs (`docs/internal/architecture/current/`, ESSENCE, SYSTEM, CONNECTORS) explain why things work as they do. The ADRs and decisions.log record what was ruled, and the code says what is true.
- **How Piper reaches it:** two options, compared below.
  - (a) Read-only tools over a pinned snapshot of the repository at the served sha: search, read a file, list a directory.
  - (b) Retrieval over an index of curated architecture docs, built at deploy.
- **The law that applies:** the code wins over a doc, as in the agent rule. An answer cites the sha it read, so "how it works" is always "how the served build works". It's never "how main works today": served and main differ between promotions, and Piper must describe what the person is actually using.
- **Private:** nothing in the code itself; the repo is public. Logs and mail sit in the same repo but are a separate class (area 4).
- **Current:** a snapshot pinned to the served sha refreshes itself at each promotion. A separate index needs a build step that fails the deploy if it's stale, the same pattern as `MEMORY.md`'s generator check.

### 2. Ethos (CXO, open)

*CXO: what a user should meet when asking Piper "who are you / what do you care about / why do you do it this way". Which sources are canonical? Candidates: ESSENCE, the PDRs, the voice guides. What tone does Piper use when it explains itself?*

### 3. Documentation (Docs, open)

*Docs: where the documentation lives (user-facing help, `docs/`, the website), how current each part is, and which parts a user may be pointed at versus only read from.*

### 4. Lore (Docs, with Arch on privacy, open)

*Docs: what "lore" means here. Candidates: the building narrative on the blog, the omnibus logs, the session logs, the Weekly Ship. What is the canonical public form?*

**Arch's privacy constraint, already binding:** session logs, mail and rollups are in a public repo, but they may hold old mentions of outside people (CLAUDE.md rule 8), xian's business matters, and per-tester details. **Piper never reaches lore through raw logs or mail.** It reaches lore only through a published, reviewed form, such as the blog or a curated digest Docs maintains. The raw record is for the team, and the published record is for Piper.

### 5. Best practices (CIO, open)

*CIO: what "best practices" means for Piper as distinct from for the agents. Candidates: the methodology, the briefings, the skills, CLAUDE.md. How do agents learn them today, and what part of that transfers to a product talking with a PM user?*

## Mechanisms compared (Arch)

| Option | What it is | For | Against |
|---|---|---|---|
| A. Briefing layer | A small generated "Piper about Piper" text in the system context, built from the capability catalog plus curated summaries | Cheapest; always present; same shape as an agent's briefing | Fixed size; can't answer depth; costs tokens on every turn |
| B. Curated corpus plus retrieval | An index of a curated set (architecture current docs, ADR summaries, help docs, published lore) built at deploy, retrieved on demand | Depth without token cost per turn; reuses the existing ingestion stack | A second copy that can drift; the curation is ongoing work |
| C. Read-only tools over the served snapshot | Search and read over the repository at the served sha, as agents do | Matches the "as any agent" bar exactly; always current; cites real lines | Raw code needs interpretation; the privacy boundary must be enforced by path (logs and mail excluded) |
| D. Hybrid: A + C, with B only for lore | A short briefing so Piper knows what it is and where to look; tools for codebase depth; the published lore as the only lore source | Each area gets the mechanism that fits its privacy and currency | More parts |

**Arch's leaning, before contributions:** D. A short generated briefing extends what `capability_catalog()` already does. Read-only tools over the served snapshot cover codebase and architecture depth, with an allow-list of paths: code, `docs/internal/architecture/`, the help docs. Logs, mail, `dev/` and the briefings stay out. Lore comes only from its published form. The same rule as ADR-080 holds: the LLM decides what the person is asking about, and code decides which paths it may read.

## Open questions

1. Does Piper's self-knowledge include its own limits and known bugs? (PPM and CXO.) Open issues are public, but they aren't written for users.
2. Is self-knowledge per-deployment (hosted beta) or also for self-hosters? A self-hosted Piper reading its own checkout is the same mechanism.
3. Cost: the per-turn token budget for option A, and any retrieval cost (CIO's cost discipline).

## Timeline

- 2026-11-12: this draft (Arch's sections).
- 2026-11-13 15:00 PST: CXO, Docs and CIO sections due.
- 2026-11-14 12:00 PST: Arch's recommendation with options, to Exec for xian's board.
