# Piper self-knowledge: design exploration

**Status:** DRAFT. Arch's sections are written. CXO's and Docs' input was folded in at 14:25 PST (memos 01M78XJ2P371XTWETCC8PSXAKW, 01M78XKW74E2EQQCAJQ2Z1TWSR). CIO's section (area 5) and the cost answer were written in place at 14:28 PST (memo 01M78XVXC3).
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

## The fork that decides the design: whose Piper? (CXO)

xian's words read two ways, and they need different corpora and different privacy lines:
- **Tier 1, every user's Piper.** It knows how it works, what it can and can't do, and what it stands for, and it says so in its own voice.
- **Tier 2, Piper on the team's own account.** It knows the codebase, ADRs, methodology and lore the way a seat does.

**This is a question for xian, sent through Exec.** The recommendation designs both tiers and orders them. Tier 1 comes first: it is the smaller privacy surface and the larger trust risk.

**Arch's reconciliation with the mechanisms below.** Raw repository tools (option C) are a **Tier 2** mechanism. For a hosted user they would answer in the repo's register, with issue numbers, roles and internal words. And as an index of the whole tree they would reach the rule-8 material in `dev/` and `mailboxes/`. Tier 1 is a **curated, versioned corpus written for users**. Each item is voice-passed by CXO and traced to shipped behaviour. The capability catalog is already that kind of source for "what can you do".

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

CXO, 01M78XJ2P371XTWETCC8PSXAKW, summarized:
- **What it means (Tier 1):** honest answers, in Piper's own voice, to "how do you work, what can you do, what won't you do, why did you decline that".
- **Sources:** PDR-004 (experience philosophy); ADR-060 (floor-first: honest about what it can't do); ADR-072 D5 (transparency when gated); the trust gradient; the voice rulings already in the copy modules. Piper states these as how it behaves, in the first person. It doesn't quote them.
- **Voice:** the Colleague Test, with one voice across surfaces.
- **The largest trust risk:** a self-description that claims a feature that isn't built. Every capability claim needs a source in code or a served check.
- **When it doesn't know, or the source is stale:** it says so and names what it can check. It never confabulates from a nearby document.
- **A user never meets:** internal roles, mailboxes, issue numbers, session logs, agent names and their words; rule-8 material; xian's business matters; anything per-tester; fix-status claims that aren't live; internal terms ("COMPOSTED", ADR numbers).
- **Served verification:** a fixed question set run against the live reply, judged by CXO on quoted replies. It includes one question about a feature that isn't built (expect an honest no) and one about a person or business matter (expect a decline that doesn't leak). A unit pin on the corpus text does not count.

### 3. Documentation (Docs, open)

Docs, 01M78XKW74E2EQQCAJQ2Z1TWSR. These are counts on main; nothing was read for quality.
- **Size:** 1,880 markdown files under `docs/`, not counting omnibuses. `docs/internal/` holds 1,100 of them, 501 in architecture. The user-facing set is small: `docs/public/` user-guides 15, getting-started 8, api-reference 6. `docs/briefing/` (32 files) is the nearest thing to a curated "what the team knows" layer.
- **Currency:** only 28% of files carry a parseable `status:` header, and the values are free-form, so status can't filter today. Freshness comes from git, not headers. Nobody owns `docs/internal/` page by page, and a retriever can't tell stale from current.
- **Docs' view:** start with a curated corpus of a few hundred files: the current-state briefing, `PROJECT.md`, `METHODOLOGY.md`, the glossary, the `current/` architecture set, ratified ADRs, public user guides, and the published blog. Fix status headers only for those. **Docs offers to own the corpus manifest** (paths plus a last-verified date) and re-verify it in the weekly audit.

### 4. Lore (Docs, with Arch on privacy, open)

Docs, 01M78XKW74E2EQQCAJQ2Z1TWSR:
- **Where lore lives:** 523 omnibus logs; 7,263 session-log files under `dev/`; 435 blog posts in the website repo.
- **Docs' view:** lore is a separate, dated layer. Piper cites it as history, never as current fact. The omnibuses record unresolved divergences on purpose, which makes them poor sources for "what is true now".

**Arch's privacy constraint, already binding:** session logs, mail and rollups are in a public repo, but they may hold old mentions of outside people (CLAUDE.md rule 8), xian's business matters, and per-tester details. **Piper never reaches lore through raw logs or mail.** It reaches lore only through a published, reviewed form, such as the blog or a curated digest Docs maintains. The raw record is for the team, and the published record is for Piper.

### 5. Best practices (CIO)

*Written 2026-11-12 by CIO, from memo 01M78XVXC3. Per-entry table: `dev/2026/11/12/methodology-core-manifest-2026-11-12.md`.*

**What "best practices" means for Piper is two different things, and they need different mechanisms.**
1. **Practices Piper follows itself:** be honest about what it can't do, check before claiming something is done, say what it measured, don't confabulate, ask when it's unsure. These are behaviour, not knowledge.
2. **Practices Piper can explain or teach a PM:** the working method this team uses (verification discipline, "a clear is not a measurement", the Excellence Flywheel). This is product content.

**How agents learn the methodology today, measured 11-12.** There are four layers, sorted by how they reach an agent:
- **Every session:** `CLAUDE.md` (159 lines of rules), the SessionStart role card, and the memory index.
- **At the task:** 36 skills, loaded when the task matches.
- **At session start, by instruction:** role briefings, current state, `METHODOLOGY.md` (346 lines).
- **On demand:** the 58 `methodology-core` entries. Only 11 of the 58 are named by any loaded surface. The other 47 reach an agent only if it goes looking, and 35 have no status line.

**What transfers: agents follow what is put in front of them when they act, not what they could look up.** Measured this week:
- The rule that mail between v4 seats goes on v4 lived in a skill step and an ops doc, and was followed 6% of the time (3 of 52, 11-09/10). Once a warning sat at the send command, it was followed 85% of the time (58 of 68, 11-11; Exec's nudge was mixed in).
- "Run the lint gates before pushing" stayed a lesson in logs, and main went red three times in two days, until it moved into the pre-push hook.

Both are methodology-53. For Piper this means:
- **Practices it follows (1)** belong in what is in front of it on every turn: the system context (option A) and guards in code. They should not go in a retrieval index (option B), which gives knowledge but not behaviour. Keep them small, ruled and versioned, as `CLAUDE.md` is: xian approves the wording, and a history log records each change.
- **Practices it teaches (2)** belong in the Tier 1 curated corpus (option B), as plain, user-register summaries voice-passed by CXO. The blog's insight posts are already in that register and come first. A `methodology-core` entry is written in the incident register (role names, issue numbers, xian's words, other projects), so **none is usable as written**. Each needs a rewrite, not indexing.
- **For a Tier 2 team-account Piper:** copy the agents' layering instead of building one index: a small always-loaded rules layer, procedures loaded by the task, and the corpus on demand. The 47 unreached entries show what happens to anything left in the on-demand layer alone.

**What stays private:**
- **Agent memory** (`~/.claude-pm/`, 279 files, 235 of them feedback). Never a source for any tier. It has no git history, and it holds xian-specific and sometimes personal material. Anything in it worth teaching gets rewritten into the repo first.
- **The incident narratives in methodology entries,** and the logs and mail they cite.

**How it stays current:**
- The methodology audit (next 12-29) and the skills review (12-01) already exist.
- **CIO's standing item 9p:** give every entry a parseable status (Emerging, Proven or Retired) and a one-line plain summary. That manifest becomes the methodology part of the corpus list, alongside Docs' manifest. A Proven entry with a user-register summary is a candidate for Tier 1. Nothing else is.

**How to check it, served:** three questions added to CXO's set. "How should I check a fix is really done?" "What's wrong with an all-clear?" "When should I stop and ask?" Judge them on the quoted replies, for substance and for leaks (no role names, no issue numbers).

## Mechanisms compared (Arch)

| Option | What it is | For | Against |
|---|---|---|---|
| A. Briefing layer | A small generated "Piper about Piper" text in the system context, built from the capability catalog plus curated summaries | Cheapest; always present; same shape as an agent's briefing | Fixed size; can't answer depth; costs tokens on every turn |
| B. Curated corpus plus retrieval | An index of a curated set (architecture current docs, ADR summaries, help docs, published lore) built at deploy, retrieved on demand | Depth without token cost per turn; reuses the existing ingestion stack | A second copy that can drift; the curation is ongoing work |
| C. Read-only tools over the served snapshot | Search and read over the repository at the served sha, as agents do | Matches the "as any agent" bar exactly; always current; cites real lines | Raw code needs interpretation; the privacy boundary must be enforced by path (logs and mail excluded) |
| D. Hybrid: A + C, with B only for lore | A short briefing so Piper knows what it is and where to look; tools for codebase depth; the published lore as the only lore source | Each area gets the mechanism that fits its privacy and currency | More parts |

**Arch's leaning (updated after CXO's and Docs' input):** Tier 1 first, as a curated, voice-passed corpus traced to shipped behaviour. That's option A's briefing plus option B's retrieval over a manifest Docs owns. Option C's repository tools wait for Tier 2, behind an account line. **Arch's earlier leaning, before contributions:** D. A short generated briefing extends what `capability_catalog()` already does. Read-only tools over the served snapshot cover codebase and architecture depth, with an allow-list of paths: code, `docs/internal/architecture/`, the help docs. Logs, mail, `dev/` and the briefings stay out. Lore comes only from its published form. The same rule as ADR-080 holds: the LLM decides what the person is asking about, and code decides which paths it may read.

## Open questions

0. **Whose Piper: Tier 1, Tier 2, or both, and in what order?** xian's call, sent through Exec.
1. Does Piper's self-knowledge include its own limits and known bugs? (PPM and CXO.) Open issues are public, but they aren't written for users.
2. Is self-knowledge per-deployment (hosted beta) or also for self-hosters? A self-hosted Piper reading its own checkout is the same mechanism.
3. Cost: the per-turn token budget for option A, and any retrieval cost (CIO's cost discipline).
   **CIO's answer:**
   - **Every token in option A is the user's money on every turn.** Piper has no provider key of its own; each account brings its own key (xian, 10-29). So option A's briefing gets a hard size budget, set the way `CLAUDE.md`'s is: rules only, the rest behind a pointer.
   - **A starting cap of about 1,000 tokens,** which is half the size of `config/PIPER.md` today (about 2,000 tokens at 4 characters per token). The build fails if the generated briefing exceeds it, and the size is printed at each deploy.
   - **Put the briefing in the cacheable static prefix** (#2145's `CacheablePrompt`) on every call that carries it, so repeat turns are billed at the cache-read rate. Today only the classifier uses that prefix. The cache-read price comes from the current Anthropic pricing page at build time, not from this note.
   - **Retrieval (option B):** an index built at deploy costs one embedding pass per deploy, and a retrieval call happens only when a self-knowledge question is detected. Measure the share of turns that trigger it in the first week, and say the expected range before building.
   - None of these numbers is measured yet. This is the budget to measure against, not a measurement.

## Timeline

- 2026-11-12: this draft (Arch's sections).
- 2026-11-13 15:00 PST: CXO, Docs and CIO sections due.
- 2026-11-14 12:00 PST: Arch's recommendation with options, to Exec for xian's board.
