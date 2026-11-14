# Piper self-knowledge: design exploration

**Status:** BOUNDARY ACCEPTED by xian, 2026-11-13 ("accepted", relayed by Exec 01M7BW10QMGKW11P13PJZKMWZK): the revised boundary below, under which Tier 2 is no longer a tier. #2358 and #2359 can move. Previously: RECOMMENDATION READY (2026-11-12 14:29 PST). All three contributions are in: CXO 01M78XJ2P371XTWETCC8PSXAKW, Docs 01M78XKW74E2EQQCAJQ2Z1TWSR, and CIO 01M78XVXC34GVSQAZQF67DX88W, written in place. Open: xian's answer on "whose Piper".
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
- **Two homes for ethos, not one (CXO, 11-12 14:50, agreeing with CIO's finding).** Retrieval gives Piper knowledge *about* its ethos; it does not make Piper behave by it. So:
  - **How Piper must behave** (honest about what it can't do, never claims done without evidence, says when it doesn't know) lives where it is already enforced: the floor-first routing and the copy modules in code, and the persona in `config/PIPER.md`. It stays small, ruled and versioned, with xian's yes on the wording. It is not an index.
  - **How Piper explains itself** (the Tier 1 corpus) is curated user-register text, voice-passed, each claim traced to shipped behaviour. The blog's insight posts are the first source, rewritten where they carry internal terms.
  - A self-answer must not contradict the behaviour. The served check below catches that: ask Piper to explain a decline, then trigger one.
- **Answer to open question 1 (limits and known bugs), revised 11-12 after xian's answer ("Yes, and Piper should be able to communicate them in plain language"): yes to both, told humanly.** My first answer was limits yes, bug list no, because the issue list is written for the team and would carry fix-status claims that aren't live. xian's yes stands over it. The conditions I hold it to: Piper tells a known problem in the user's terms ("I can't do X reliably yet; here is what I can do"), never recites issue numbers or internal labels, and states a fix status only when the fix is live on the build the person is using. The source is a curated known-limits list written for users and re-read at each release, not the issue tracker. I voice-pass it.
- **Added to the served question set (from CIO):** "How should I check a fix is really done?", "What's wrong with an all-clear?", "When should I stop and ask?" Judged for substance and for leaks (no role names, no issue numbers, no incident quotes).

### 3. Documentation (Docs, open)

Docs, 01M78XKW74E2EQQCAJQ2Z1TWSR. These are counts on main; nothing was read for quality.
- **Size:** 1,880 markdown files under `docs/`, not counting omnibuses. `docs/internal/` holds 1,100 of them, 501 in architecture. The user-facing set is small: `docs/public/` user-guides 15, getting-started 8, api-reference 6. `docs/briefing/` (32 files) is the nearest thing to a curated "what the team knows" layer.
- **Currency:** only 28% of files carry a parseable `status:` header, and the values are free-form, so status can't filter today. Freshness comes from git, not headers. Nobody owns `docs/internal/` page by page, and a retriever can't tell stale from current.
- **Docs' view:** start with a curated corpus of a few hundred files: the current-state briefing, `PROJECT.md`, `METHODOLOGY.md`, the glossary, the `current/` architecture set, ratified ADRs, public user guides, and the published blog. Fix status headers only for those. **Docs offers to own the corpus manifest** (paths plus a last-verified date) and re-verify it in the weekly audit.

**Docs addendum, 11-12 ~15:00 (answers Arch's ask for areas 3 and 4: what a user may be pointed at, and the canonical published form of lore).**
- **What a user may be pointed at today:** `docs/public/` user-guides (15), getting-started (8) and api-reference (6), plus the published blog on pipermorgan.ai. Nothing under `docs/internal/` is written for a user, and it names roles, issue numbers and ADRs freely.
- **The blog is the canonical published form of lore, but it is not user-register as it stands.** I scanned the full text of all 439 post bodies in the website repo's `blog-content.json` (by crude regex, so a floor, not a verdict) for issue numbers (`#1234`), ADR references and role names. 107 of the 181 insight posts hit at least one, 126 of 217 building posts, and all 33 Ships. So CIO's "insight posts are the first source" holds only after a pass: a post needs a screen or a rewrite before it goes in the Tier 1 corpus, and the manifest should list posts individually, never "all insights".
- **Lore stays a dated layer:** each manifest row for a post carries its pubDate, and Piper says "as of that post" when it cites one. It must not answer "how does X work now" from a post.
- **Manifest shape Docs can own:** one row per item with source path or slug, tier, last-verified date, re-verify window, owner (Docs for documents and posts, CIO for methodology rows, Lead for the generated capability answers). The deploy check Arch proposes (missing file or lapsed window fails) can read the same file.
- **Not yet decided, flagged for Arch:** whether a "curated digest" of lore is worth building at all. The blog already is a reviewed form, and a second digest is a new thing to keep current. My lean is no digest until the blog screen shows a real gap.

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

## Recommendation (Arch)

**Build Tier 1 first. Treat "following" and "knowing" as two mechanisms (CIO's finding). Never index raw team records.**

**1. Following (every Piper, first):** a small, versioned **conduct layer** in the per-turn prompt (`config/PIPER.md` and its loader), with code guards where a rule can be checked. It holds the practices Piper acts by: honest limits, no claim without a source, verify before "done", say when it doesn't know.
- CIO drafts it from the Proven entries, CXO voices it, and xian approves the wording.
- **Budget:** CIO's cap of about 1,000 tokens, in the cacheable static prefix (#2145). The build fails above the cap. Every token is the user's money on every turn.

**2. Knowing, Tier 1 (every Piper):** a **curated user corpus**, retrieved on demand through the existing ingestion stack and built at deploy from a manifest. It has three parts:
- (a) **What Piper can and can't do,** *generated* from `capability_catalog()`, never written by hand. This answers CXO's largest trust risk: no capability claim without a source in code.
- (b) **How it works and what it stands for:** user-register explanations written from the `current/` architecture docs, PDR-004 and the ADRs, voice-passed by CXO.
- (c) **Teachable practice:** blog insight posts and rewritten user-register summaries of Proven methodology entries. **Each post is listed and screened one by one** (Docs' 14:33 addendum: 107 of 181 insight posts carry issue numbers, ADR references or role names). The manifest never says "all insights". A post enters the corpus only after the internal-term screen passes or the post is rewritten.

Rules for the corpus:
- One manifest row per item: source, tier, last-verified date, re-verify window and owner (Docs' shape). The deploy check reads the same file. **Docs owns the manifest, and CIO owns the methodology rows.**
- A deploy fails if the manifest names a missing file, or an item past its re-verify window.
- Answers about how Piper works describe the **served** build.

**3. Knowing, Tier 2 (team account only, second):** copy the agents' layering, not one index:
- a briefing;
- read-only tools over the served snapshot, with a path **allow-list** (code, `docs/internal/architecture/`, `docs/briefing/`, the user docs);
- the Tier 1 corpus.

An account line in code decides who gets Tier 2. The LLM decides what the person asks about, and code decides which paths it may read (ADR-080).

**Excluded for every tier, pinned by an enforcement test:** `dev/`, `mailboxes/`, the omnibuses and agent memory. Lore comes only from its published form (the blog), cited as dated history, never as current fact.

**4. Verification (served, not unit):** CXO's question set plus CIO's three questions, run against the live reply and judged on quoted replies. It includes a feature that isn't built (expect an honest no) and a person or business-matter question (expect a decline with no leak).

**Options for xian:**
- **Smaller:** the conduct layer and 2(a), the generated capability answers, alone. That's the cheapest real gain, and it closes #1186's original "how do you work" decline.
- **As recommended:** parts 1, 2 and 4.
- **Larger:** add part 3 for the team account. Do it only once Tier 1's corpus discipline (manifest, dates, voice) has held for a sprint. The repository's privacy surface is far bigger.

**Owners (proposed; PPM places it):**
- Conduct layer: CIO drafts, CXO voices, xian says yes, Lead builds.
- Manifest and the generated capability answers: Docs and Lead.
- Corpus items: Docs, with CXO's voice pass.
- Exclusion test and served question set: Lead, with CXO judging.
- Tier 2 after.

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
   - **xian (11-12): research and experiment.** The plan is in "Question 3: the experiment plan" below.

## Timeline

- 2026-11-12: this draft (Arch's sections).
- 2026-11-13 15:00 PST: CXO, Docs and CIO sections due.
- 2026-11-14 12:00 PST: Arch's recommendation with options, to Exec for xian's board. **Delivered early, 2026-11-12 14:29 PST,** once all three contributions had arrived.

## The tier boundary, revised (Arch, 2026-11-12 17:26, after xian's answers)

**Accepted by xian 2026-11-13** (Exec 01M7BW10QM…).

xian, relayed by Exec (01M797TQEAE37X7AYMMZ3V1KZ9): "if every user's Piper doesn't have some of the skills and isn't able to use all of the methods that my own agent team has available then we're giving people a weaker form of assistance than I have developed for myself." He asked us to probe the boundary.

**The proposal: draw the line at whose records Piper reads, not at how much it knows or what it can do.** The earlier split put three different things in Tier 2 (methods, depth on its own code, and the team's records), and only the last needs an account line.

| What | Who gets it | Mechanism | Token cost (unmeasured; to measure under Q3) | Privacy cost |
|---|---|---|---|---|
| **Methods it follows** (verify before "done", say what it measured, ask when unsure) | Every Piper | The conduct layer (recommendation part 1), plus code guards | The ~1,000-token cap on every turn, cached | None, if written in user register |
| **Methods it uses on a task** (the team's skills: drafting an issue or a spec, planning a sprint, a stakeholder update, a verification checklist) | **Every Piper (moved from Tier 2)** | Task-loaded procedures, the shape agents use. Piper already ships some: `.claude/skills/piper-*`, `trust-check`, `propose-feature`, `compost-review`, `update-piper`. The new work is rewriting team procedures that are worth having (CIO's Proven entries, the review and verification skills) into that user-register form. | Paid only on a turn whose task matches, the size of one procedure | None for a rewritten procedure. The team's own skills cite roles, issues and xian's words, so they are rewritten, never copied. |
| **Knowing how its own code works** (reading the source to answer "how does saving work?") | **Every Piper (moved from Tier 2),** behind a read budget | Read-only tools over the served snapshot (option C), with a path allow-list: `services/`, `web/`, `config/`, `docs/internal/architecture/current/` and the user docs. The tools are offered only on a turn the LLM classes as a question about Piper itself, and code caps the reads per turn (a proposed starting cap is 3 reads and 20 KB, to be tuned by the Q3 experiment). | The most expensive row: every read is the user's tokens. This is why it has a budget and goes after the corpus. | Low. The code is public, as xian says. The allow-list still matters because rule 8's old mentions of outside people can sit anywhere in the repo, not only in `dev/` and `mailboxes/`. A file found to hold one leaves the allow-list (we report the mention and don't edit it out). |
| **The team's records** (sprint position, logs, mail, briefings, decisions in progress) | **Nobody, as a self-knowledge source** | None | None | High: rule 8, and the incident register |

**What happens to Tier 2.** It goes away as a tier. When xian's own Piper knows where the Piper Morgan project stands, that is the ordinary thing every user gets: Piper reading the user's own project through their GitHub connector (issues and milestones). It is not a special index of the team's repo. `dev/`, `mailboxes/`, the omnibuses, `docs/briefing/` and agent memory stay excluded for every account, pinned by the enforcement test.

**Exec's point on "open source, so nothing to reveal."** I agree, with one widening. The exclusion is not about secrecy. It exists because rule 8 says old mentions of outside people may sit in the repo and are reported, not removed. The same reason means the allow-list is a list of paths, checked file by file when a path is added. It is never "the repo minus dev/ and mailboxes/".

**Self-hosters (Q2, yes).** It's the same mechanism. The "served snapshot" for a self-hoster is their own checkout at its commit. The allow-list and the read budget apply unchanged.

**Order (unchanged in spirit):**
1. The conduct layer.
2. The Tier 1 corpus, including the answers generated from `capability_catalog()`.
3. Served verification.
4. The task-loaded procedures, one at a time, each through CXO's voice pass.
5. Code-reading tools behind the budget, once the Q3 experiment has measured their per-question cost against CXO's question set.

**Q3 experiment (research, not the plan).** Run CXO's and CIO's question set three ways on one account: corpus only; corpus plus code tools; code tools only. For each, record tokens per answer, the share of answers that are right on the served build, and any leaks. CIO's budget is the hypothesis to test. Lead runs it, CXO judges the replies, and it uses a provider key handed over the way xian rules (the rule-7 key question).

## Question 3: the experiment plan (CIO, 2026-11-12 17:30, after xian's answers and Arch's revised boundary)

xian's words on question 3: "let's do some research and experimentation to figure out how we may deploy a lean effective solution." This plan turns the cost answer above into four hypotheses. Each one gets a measure, a pass line written *before* the run, and the cheapest run that settles it. Expectations are written down now so the results can contradict them. They are guesses, not measurements.

**Rules for every run**
- **Price first.** Before any paid run, write the number of calls, the expected tokens and the cost at the current Anthropic pricing page, and send it to Exec. Nothing runs on an unpriced estimate.
- **Key.** Runs go through one test account on the served beta, so they need that account's own stored provider key. Which key pays, and who enters it, is xian's call. It is #2340's open key-handover question (paid rule-7 screens), applied to a served account, and Exec puts it on his board (CIO 01M799HEVBM5KDWBJ7ND67R24E, 11-12). Planning and the zero-cost steps don't wait for that ruling, but every paid run does.
- **Served build.** Runs go against a served build at a named sha, never a local stand-in, and answers are judged against that build.
- **Results.** They go in a dated section of this record, next to the pass lines, including any that fail.
- **Owners.** Lead runs, CXO judges replies (right for the build, register, leaks), and CIO writes up the numbers against the pass lines.

| # | Hypothesis | Measure | Pass line (set now) | Cheapest run | Expectation (a guess) |
|---|---|---|---|---|---|
| H1 | The conduct layer fits about 1,000 tokens and is billed mostly as cache reads | Token count of the drafted layer. On a multi-turn session, the share of turns 2+ whose layer tokens come back as `cache_read_input_tokens` in the API usage fields | At most 1,000 tokens. At least 80% of turns 2+ read it from cache | A token-counting call on the draft (no generation), then one 10-turn scripted session | Fits. Cache share depends on the prefix staying byte-identical, so a timestamp or user name in the prefix would break it |
| H2 | Questions about Piper itself are a small share of turns, so retrieval cost is small in total | The share of served turns the router's LLM classification marks as a self-knowledge question, never a keyword match (ADR-080). Counted only, never the content, through the `piper.evidence` logger (#2350). The line isn't emitted until the router has that class (Arch, 11-12) | Below 10% of turns. Above that, retrieval cost is per-turn-scale and gets its own budget | A counter, live for one week after the corpus ships. No paid run needed | 1 to 5% |
| H3 | The corpus alone answers most questions right, and code tools earn their cost only on how-it-works questions | Run CXO's set plus CIO's three in four arms. Arm 0 is the leaner alternative #2357 asks for: generated capability answers in the prompt, with no retrieval. Then Arch's three: corpus only, corpus plus code tools, code tools only. For each: input and output tokens per answer, right on the served build (CXO), and leaks (CXO's leak list). Each question 3 times per arm, for variance | Corpus only: at least 80% right on what-can-you-do and practice questions, with 0 leaks. Code tools are adopted for a question type only if they raise the right share there by at least 20 points at no more than 5 times the corpus-only tokens. Any leak in any arm fails that arm until it's fixed | Arm 0 and corpus only first, side by side. If arm 0 meets the same 80% with 0 leaks on a question type, it wins that type, because it has no retrieval cost. The two code arms run only if corpus-only misses the 80% on some question type | Corpus only is enough for capability and practice questions, and the code arms win on "how does X work". Code tools cost 3 to 10 times as many tokens |
| H4 (Arch) | A task-loaded procedure costs tokens only when its task matches, and matches rarely when it shouldn't | Token size of each procedure. Over a mixed question set (matching and non-matching tasks): the share of matching turns that loaded it, and the share of non-matching turns that loaded it anyway | Each procedure at most 1,500 tokens. It loads on at least 90% of matching turns and on at most 10% of non-matching ones | The first rewritten procedure only, on 20 mixed prompts | Loading by task is easy to get right on matching turns and harder on near-misses |

**Order.** H1's token count and H2's counter cost nothing, so they run first, with the build. H4 runs when the first procedure is rewritten. H3's corpus-only arm runs when the corpus is served. The code arms run last, and only if H3 says they are needed. That is the same order as step 5 of Arch's sequence.

**What the results decide**
- H1 fails on size: the layer is cut, not the cap raised. Raising the cap is xian's call, because it's the user's money.
- H1 fails on caching: fix the prefix before shipping more of it.
- H2 is above 10%: retrieval gets a per-turn budget like the code tools.
- H3: decides whether code-reading tools ship at all, and for which question types.
- H4: decides whether procedures load by task or need an explicit trigger.

**Self-hosters (Q2).** It's the same mechanism and the same costs, on their own key. They need no separate run. The served-build rule becomes "their checkout at its commit".

### H1: price and a precondition (CIO, 2026-11-13 10:12 PST)

**What H1 runs on.** Piper's chat model on the Anthropic leg is `claude-sonnet-4-6` (`services/llm/config.py`, `LLMModel.CLAUDE_SONNET`, the `"default"` tier). Rates from Anthropic's pricing page, read 11-13 10:07 to 10:12 PST: input $3 / MTok, 5-minute cache write $3.75, cache read $0.30, output $15.

**Precondition found: the conduct layer would not be cached as built today.**
- #2145 caches one call: the intent classifier's prompt (`services/intent_service/classifier.py:824`, the only `CacheablePrompt(` in `services/`). The prompt that writes Piper's reply has no cache breakpoint. So "the layer goes in the cached static prefix (#2145)" isn't true yet for the reply prompt. The layer has to go into a reply prompt that carries its own breakpoint.
- On Sonnet 4.6 the API caches only a prefix of at least 1,024 tokens (prompt-caching reference). The layer alone is about 510 tokens, so it caches only as part of a larger fixed prefix: the system prompt plus the layer, with nothing per-user or per-turn in front of the breakpoint.
- OpenAI caches stable prefixes on its own, also from 1,024 tokens, so the same size condition holds for users on that key.
- **This is for Lead and Arch to build or rule. H1's caching half can't pass until it's built.** H1's size half (the token count) doesn't depend on it.
- **Arch's ruling (11-13 10:19, 01M7B26F1A):** the reply `system` starts with the per-user base. The layer goes after the static addendum and before the capability manifest. The breakpoint goes after the manifest, and the per-user warmth guidance stays after it. So the cache is **per user**. Lead accepted (01M7B25Q4M); #2354 isn't placed in a sprint yet.
- **H1's caching half, restated to match:** one user's turns 2 to 10, sent less than 5 minutes apart, read the layer from cache on at least 80% of them. A hit across different users isn't the measure. A shared cache would need the base moved after the breakpoint, which is a screened behavior change and a separate item. File it only if the per-user rate turns out too low to matter.
- **New check for the build report:** base + addendum + layer + manifest must reach 1,024 tokens on Sonnet 4.6. A short neutral base could leave the prefix under it, and then nothing caches at all.

**Price of H1.**
- **Token count of the layer:** one `count_tokens` call. The pricing page lists no rate for it, and I haven't checked whether it's free, so I treat it as $0.01 at most.
- **The 10-turn scripted session:** a chat turn makes several model calls (#2101's trace: the classifier, the reply and up to two more). The assumptions are written so the result can contradict them:
  - 4 calls per turn, 40 in all;
  - 6,000 input tokens per call, none cached;
  - 800 output tokens per call.
  - That's 240,000 input tokens, $0.72, plus 32,000 output tokens, $0.48: **about $1.20.**
  - **Cap: $5** (four times the estimate). The run stops if `usage` passes it. With caching built, turns 2 to 10 cost less, not more.
- **Who pays:** the account's provider key, which waits on #2340/#2357 (xian). Nothing paid runs before his answer and Exec's yes to this price.
