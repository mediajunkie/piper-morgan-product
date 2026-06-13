# Cross-Pollination Brief — June 13, 2026

PM closed out a dense Friday by codifying a reusable architecture pattern for when a domain concept carries two jobs at once — durable record and transient working state — into a new ADR ratified same-day. Live-testing the autonomous executor uncovered a classifier safety hole: actions with `_query` in their name were slipping through a keyword-based safe filter even when they were mutating actions, not read-only ones. Docs closed out all 206 broken links — the resolution came only after reframing what "broken" meant. And BYOC Phase 2 received a full cohort green-light overnight, with Arch shipping a lens that proposes a three-phase build plan and a "run anywhere" architecture amendment.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Domain concepts that carry two jobs need an explicit contract for both — ADR-069 formalizes the pattern

**From:** Lead Dev June 12 session log; ADR-069 commit `56b67b5` (authored) + `144385e` (v0.2 ratified); Arch ratification memo 2026-06-12 ~19:35
**Relevant to:** Klatch (conversation and message objects have both persistence and runtime-state jobs); both projects (any domain object used both as a record and as working context)

The #1207 conversation-context unification surfaced a recurring trap: PM had two classes both named `ConversationContext` — one the system of record in the domain layer, one an in-memory aggregate in the mediation layer — with different field names, one-way data flow, and a dead hydration block hidden behind a `except: pass`. Antecedent resolution saw empty history because the persistence path and the floor-reading path were never connected.

The fix itself was straightforward. What's new is that Lead Dev then filed ADR-069 to make the solution reusable — "so the next instance isn't re-litigated from scratch." The core decision: when a domain concept has both a durable record and a transient working state, split it into three explicit layers: the domain entity (system of record, DB-backed), the mediation layer (single access path per ADR-029), and the in-process projection (working state: recent-turn window, lens stack, provenance sidecar — no I/O of its own). A guard test (`test_context_unification_guard.py`) pins the carve by construction so the dual implementation can't silently regrow.

The reconstructability test is the sharpest diagnostic: working state is derivable from the system of record; the system of record is not derivable from working state. That asymmetry is what makes one durable and one disposable. Lead Dev named the next two candidates for this treatment: `Intent` and `Artifact` (#952). Arch ratified both the carve and the standalone ADR.

**Suggested action:** Klatch — the same pattern applies to any object that's both stored (messages, entities, channels) and used as runtime context (current entity state, streaming context, conversation working state). Worth checking whether any in-process objects are implicitly carrying the "system of record" job alongside the "working state" job — ADR-069's three-layer carve is directly applicable if they are.

---

### 2. Keyword-based safety classifiers have a systematic vulnerability when action names follow a naming convention that matches safe keywords (#1210, HIGH)

**From:** Lead Dev June 12 session log (~19:05–19:45 PT); commit `3bf46bd` (#1195 AutonomousExecutor wire); issue #1210 filed
**Relevant to:** Both projects (any automated action dispatcher with a safe/unsafe classification layer)

Lead Dev wired the AutonomousExecutor into the pattern-application path (flag `AUTONOMOUS_EXECUTION_ENABLED`, default OFF). During live verification, the "read-only by construction" claim turned out to be false.

The classifier uses a SAFE keyword set — verbs like "query," "list," "get" — to identify read-only actions. Several mutating actions in PM's registry follow a naming convention that appends `_query` as a suffix: `comment_issue_query`, `close_issue_query`, `reopen_issue_query`. The substring match meant the classifier rated these as SAFE even though they write to GitHub. The AutonomousExecutor as first wired would have auto-commented and auto-closed issues.

The fix: an explicit read-only allow-list (`_AUTOEXEC_READONLY_ALLOWLIST`) as the outer gate, with `execute_with_safety` remaining the inner gate (defense-in-depth). The classifier bug is filed separately as #1210 (HIGH) because the same false-classification would affect any future executor caller, not just this wire.

The unit tests all passed — they used clean action names that don't contain `_query`. The failure was only catchable by live-testing against the real registry.

**Suggested action:** Both projects — if a safety or routing classifier uses keyword matching on action names, the match should be explicit allow-list (only known-safe names pass) rather than keyword-contains (anything that looks like a safe verb passes). Naming conventions that encode categories via suffix/prefix create systematic substrate for this class of false-positive. The live-verify requirement is also load-bearing here: unit tests using synthetic names can't catch real-registry surprises.

---

### 3. BYOC Phase 2 green-lit overnight — "run anywhere" becomes a constraint-derived property, not an aspiration (ADR-066 v0.2 candidate)

**From:** Arch session log June 13 04:22 PT (Fire 40); commit `a56b290` (Arch lens + cohort cc); PA/CIO/CXO/Exec/Lead Dev ratification commits June 13 morning
**Relevant to:** DinP (public positioning when BYOC ships); Klatch (if hosted or packaged deployment comes up)

Arch shipped a full architectural lens on BYOC Phase 2 to PA and nine cohort members early Saturday, and the green-lights came back across the morning: CIO, CXO, Exec, Lead Dev all ratifying with scoping notes.

The key architectural finding: the Cowork server-owned-config constraint (each plugin deployment gets its own isolated config environment, not a shared pool) means "run anywhere" stops being an aspirational claim and becomes a structural property. A single-tenant containerized deployment (FastAPI + DO/Render/Fly + managed Postgres/Redis) gets environment isolation by construction. Arch is proposing this as an ADR-066 v0.2 amendment — goodness-from-constraint rather than designed-in flexibility.

Three sub-phases proposed (2a/2b/2c). Two threads flagged to keep separate: a ChatGPT plugin marketplace listing (comparative research only, not a parallel build) and ADR-068 (the marketplace-listing ADR, which strengthens from the Phase 2 substrate but is a distinct decision thread). #1185 (server-stored encrypted key, the multi-tenant prerequisite) remains the gate for multi-user; single-tenant is the correct M5 beta scope.

**Suggested action:** DinP — when BYOC ships, the "run anywhere" story is structurally grounded, not aspirational. Worth reserving narrative space for it on the project page rather than framing it as a future goal.

---

## Sources Read

- **piper-morgan-product**: Lead Dev June 12 session log (full day — #1122, #1207, ADR-069, #1195, canonical regression, #1165); Arch June 12 session log (day-close section, ADR-069 ratification); Arch June 13 session log (04:22 PT, Fire 40, Phase 2 lens); Docs June 12 session log (STOP section — #1182 close, omnibus chain); commits `56b67b5`/`144385e` (ADR-069), `3bf46bd` (#1195 wire), `a56b290` (BYOC Phase 2 lens), `caff746`/`38a458f` (ratification replies)
- **klatch**: brief-delivery commits only; no new original content in 48h window
- **Secondary repos (atlas, globe, cuneo, one-job, optilisten, nyt-crossword)**: no narrative commits in 48h window; automated status commits only on weather and atlas (brief delivery)

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*
