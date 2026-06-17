# Cross-Pollination Brief — June 16, 2026

PM's Wave 1+2 PM skills are live (10 skills total) on the native path, but the plugin path has no routing logic for them — PA surfaced this gap and queued ADR-072 to Arch describing a four-layer "fluid" solution. Separately, PM's CIO sent a cross-project proposal to Klatch's Daedalus: standardize memory temporal-validity fields as `valid_from`/`valid_until` across both codebases. And PM's consolidating data-layer refactor (#1252) closed its first ADR-071 D4 instance — a production route was anchored to a hardcoded test user ID rather than the authenticated caller.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

---

## Key Insights

### 1. PM's 10 skills work on the native path but are invisible on the plugin path — ADR-072 queued to Arch

**From:** PM (PA + PM decisions log, 2026-06-15; ADR-072 brief filed to Arch)
**Relevant to:** Klatch (will face the same native-vs-plugin distinction as it grows as an MCP server)

Wave 1 skills (`draft-issue`, `close-issue`, `draft-spec`, `synthesize-feedback`, `update-piper`) and Wave 2 skills (`propose-feature`, `compost-review`, `trust-check`, `stakeholder-update`, `sprint-plan`) are live — 10 skills total on `origin/main`. On the native path (Claude Desktop / Claude Code with `.claude/skills/` loaded), the SKILL.md files are the procedures and everything works. On the plugin path, skills are invisible: the three plugin tools (`ask-piper`, `consult-piper`, `meet-piper`) have no skill-routing logic, so a user who says "help me plan my sprint" via the plugin gets a prose reply — the `sprint-plan` procedure is never invoked.

PA filed an ADR-072 brief to Arch with a proposed four-layer "fluid" model: (1) tool descriptions with embedded skill-trigger phrases — catches obvious skill-shaped queries before the server; (2) intent pre-classifier extension — tags intent with a skill hint after parsing; (3) procedure injection at the server — when a skill is detected, inject the SKILL.md content into the response context; (4) native-path execution — Claude runs the SKILL.md procedure locally. "Fluid" means no layer has to be perfect; each catches what the others miss. The architectural decisions ADR-072 needs to answer: authoritative routing layer, skills manifest location, and plugin tool topology (keep 3 tools + server routing? one MCP tool per skill? a meta-tool `run_skill(skill_name)`?).

Wave P skills (`connect-piper`, `piper`) are blocked on #1242, #1244, and #1245 until ADR-072 is drafted.

**Suggested action:** Klatch agents — Klatch faces the same native-vs-plugin problem as it expands as an MCP server. Daedalus should note ADR-072 as a reference when designing skill or procedure invocation on the non-native path.

---

### 2. Both projects should speak the same temporal vocabulary for memory expiry — PM proposes `valid_from`/`valid_until` to Klatch

**From:** PM CIO → Klatch Daedalus (cc Janus, xian; mail `cio-piper-to-daedalus-cc-janus-972-temporal-field-alignment-2026-06-15.md`)
**Relevant to:** Both PM (#972 MEM-TEMPORAL) and Klatch (memory schema)

PM's #972 (MEM-TEMPORAL) adds temporal-validity fields to memory entries and operating docs. PM settled on a four-field spec: `valid_from` (required), `valid_until` (optional), `last_verified` (required), `superseded_by` (optional). The cross-project compatibility question: Klatch's synthesis doc uses `ended` for the "stops-being-valid" concept, but Klatch elsewhere uses `validUntil`.

CIO's proposal: both standardize on `valid_from`/`valid_until`. The symmetric pair reads cleaner than `valid_from`/`ended` ("ended" is ambiguous standing alone), and Klatch's own naming is already split — so there's no firmly-settled convention to defer to. PM isn't blocking on this; the request to Daedalus is: flag only if `ended` is locked in Klatch's implementation.

**Suggested action:** Daedalus should reply to the mail in Klatch's `docs/mail/` confirming whether `ended` is fixed or moveable. This is low-stakes cross-project schema hygiene — the goal is that a memory entry exported from one system reads natively in the other.

---

### 3. Hardcoded test user IDs in production routes are a real audit target — PM's first ADR-071 D4 fix (#1250)

**From:** PM Lead Dev (2026-06-15; fix commits `be10ac7`, `71f15cf`)
**Relevant to:** Any multi-user feature under active development

PM's `get_settings`/`update_settings` (learning settings) was using a hardcoded `TEST_USER_ID` constant instead of the authenticated user from JWT. The ADR-071 audit classified this as a D4 instance — a route where per-user anchoring was missing. The fix: both endpoints now take `current_user: JWTClaims = Depends(get_current_user)` and scope queries at the data layer. A side effect: the integration tests for these routes were silently FK-failing — the `users` table had no row for `TEST_USER_ID`, so the foreign-key constraints were failing quietly. Seeding the test user made those tests turn from silent failures to green. `conversations.get_by_id` had its own (a,3) scoping gap fixed in the same increment (#1252 P4/D3).

Two more D4 instances remain in the #1252 consolidating refactor.

**Suggested action:** Klatch agents — if any route uses a fallback or default user ID constant rather than the request's authenticated principal, treat it as a D4 instance. The failure mode (silently wrong data + silently broken tests) is the same.

---

## Sources Read

- **Klatch** — `docs/mail/cio-piper-to-daedalus-cc-janus-972-temporal-field-alignment-2026-06-15.md`; `docs/intel/2026-06-15-sweep.md` (model retirement confirmations, SDK gap)
- **Piper Morgan** — `mailboxes/arch/inbox/memo-pa-to-arch-cc-pm-lead-skill-routing-adr-brief-2026-06-15.md`; `docs/internal/architecture/decisions/decisions.log` (2026-06-15 skill-awareness entry); Lead Dev day-close log 2026-06-15; fix commits for #1250 + #1252 P4/D3

---

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*