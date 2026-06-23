# Cross-Pollination Brief — June 21, 2026

Klatch's UX designer Iris returned after a six-week pause and cleared the composition gesture design gate: the spec for "New Klatch" — the group conversation setup flow that is Klatch's primary 1.0 differentiator — is complete, vocabulary is finalized across the codebase, and the work is handed to Daedalus for implementation. On the Piper Morgan side, Saturday's session ran long and ended with three substantive deliverables: a writable, auth-exempt admin route was found during routine work and deleted (#1307); a build-time lint was written to make that class of exposure impossible in the future (#1308, m-41 pattern applied); and the RECONNECT connector protocol shipped (#1232, ADR-070 D5), giving the two hardest reconnection workstreams (resolve and degrade) a contract to build to.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Klatch "New Klatch" spec complete — composition gate cleared, implementation handed to Daedalus

**From:** Klatch Iris (session log `2026-06-20-1020-iris-sonnet-log.md`; spec `docs/ux/spec-composition-gesture.md`; vocab sweep commit `22d1631`)

**Relevant to:** Piper Morgan (periodic-meeting pattern, @mention dispatch parallel), all projects (JIT import front-door principle)

Iris's Session 12 produced a complete design spec for the "New Klatch" composition gesture, which is the 1.0 critical-path blocker: today users can't bring existing agents into a new klatch without building from scratch, and klatch creation has no setup surface. The spec resolves both.

**Button and trigger.** The entry point is a "New Klatch" button in the sidebar, presented as a pair with "New Chat" — the two ways to start a conversation. "Convene" stays as internal vocabulary; it is not the button label.

**Setup surface.** A lightweight panel (not a full-page form). Fields: Name (required), Agents (required, at least one), Purpose (optional — seeds the L4 channel context), Orchestration mode (optional at setup, defaults to Blast), Project (pre-filled if started from a project), Documents/files (optional). A "Copy setup from existing klatch" option pre-fills all fields from a named klatch — designed for recurring meeting use (weekly review, standup) where the user doesn't rebuild the agent set each time.

**Agent picker — three paths.** (1) Existing agents: browsable and searchable, with named roles surfaced first, one-off agents below. (2) Just-in-time import: "Import an agent" inline within the composition flow — composition and import are one gesture; the user doesn't need to pre-import before they can convene. (3) Start new agent session: either start a new session with an existing role, or create a genuinely new agent with name/system prompt/model.

**Orchestration modes (names finalized 2026-06-20).** Three modes ship in 1.0:
- **Blast** (default): all agents receive the user's message simultaneously and respond independently; no cross-agent visibility.
- **Roundtable**: sequential — agent 1 responds; agent 1's response + context goes to agent 2; and so on. Each agent sees everything before them.
- **Directed**: @mention routing only. Non-addressed agents receive context but do not auto-respond.

Mode names in code were `panel`/`roundtable`/`directed`. The user-facing labels are now **Broadcast**/**Roundtable**/**Directed** — applied across `packages/shared/src/types.ts`. A fourth mode (organic/self-selecting, where agents decide whether to respond) is explicitly post-1.0.

**@mention composes with all modes.** Typing `@AgentName` in any klatch message routes that message to the addressed agent(s) only, overriding the current default mode for that message. In a Blast klatch, @mention overrides for one message; in a Roundtable, it short-circuits the sequence. Autocomplete shows agents in the current klatch.

**Vocabulary sweep applied.** Alongside the spec, Iris applied a full vocabulary sweep across the client codebase (`ChannelSettings.tsx`, `ChannelSidebar.tsx`, `EntityManager.tsx`, `types.ts`): `entity` → `agent` in user-facing copy, `channel` → `chat`/`klatch`/`conversation` as context dictates, `Panel` → `Broadcast`. The internal/implementation words remain unchanged.

**UUID matching UX resolved.** Iris also cleared Daedalus's long-open Finding 1: when a re-import matches an existing project (UUID match), the UX is silent attach + success toast naming the project. When it matches a channel (channel-level re-import), the prompt is "View existing →" or "Import as new copy." Daedalus's implementation queue is now unblocked on both.

**Suggested action:** PM agents — the "clone periodic klatch" pattern (pre-fill setup from an existing klatch) is structurally identical to the "start from template" use case PM has discussed for recurring standups. If PM ever surfaces a "Start from previous standup" affordance, the Klatch spec's clone-channel data model (copy channel record + channel_entities, new channel_id, no message history) is the reference implementation. Also: the JIT-import-as-front-door principle (composition gesture is the entry point for import, not a prerequisite step) is worth applying to any multi-step flow where import/onboarding is currently a separate gate.

---

### 2. PM security hardening at two altitudes — instance deleted, class made impossible (#1307 + #1308, m-41)

**From:** PM Lead Developer (session log `2026-06-20-0606-lead-code-opus-log.md`; commits `0466fd09d` #1307, `84526f9e6` #1308; carry-forward `dev/active/lead-carry-forward.md`)

**Relevant to:** Klatch (any future admin or privileged-route surface), all projects

While investigating whether it was safe to remove the Caddy reverse proxy as a security layer (#1162), Lead Dev audited the auth-exempt route list and found a gap: `admin_compose` (`/api/v1/admin/compose`) was auth-exempt, writable (accepting `POST /save`), and not env-gated — an open admin UI in production, protected only by Caddy. Filed as #1307. PM's response: "delete it." The route, two templates, and the app.py mount were removed in one commit (`0466fd09d`).

Arch's concur memo added the second altitude: don't just fix the instance; make the class impossible. The fix was an enforcement lint — `AUTH_EXEMPT_JUSTIFIED` — an allowlist in `auth_middleware.py` that categorizes every writable exempt route with an explicit justification. The lint (`tests/test_exempt_list_boundary_1308.py`, 4 tests) asserts: every writable exempt route is in the allowlist, every entry in the allowlist actually exists in the route table, and no new exempt+writable route lands without a justification. Any future route that is auth-exempt and writable will fail the build if not justified. Filed and closed as #1308 (4 tests green). This is the m-41 pattern: make the bad class impossible, not just the instance.

**The Caddy gate-removal (#1162) now has both prerequisites satisfied** — #1307 (the instance gone) and #1308 (the class-fix enforced). The investigation also confirmed the rest of the exempt list is benign: health/static/oauth/docs/bootstrap routes, plus three env-gated dev-only paths that 404 in production.

Also found during the same sweep: #1309 (stale onboarding test — the test expects the old `COMPLETE` state; the flow has since added `GATHERING_REPOS`). Filed separately.

**Suggested action:** Klatch agents — if Klatch ever gains an admin surface, a privileged route, or any route that is read-only at setup time but could become writable later, consider adding an equivalent allowlist-with-justification lint from day one. The Piper failure mode here — a route that was safe when added but became a gap when the surrounding security architecture changed — is easy to accumulate incrementally. The static lint (assert every high-privilege route is justified, fail build if violated) catches the drift as the codebase evolves.

---

### 3. RECONNECT connector protocol ships — WS-3 and WS-4 now have a contract to build to (#1232, ADR-070 D5)

**From:** PM Lead Developer (commits `d400c733a` P1, `9def9a716` P2+P3; `dev/2026/06/20/1232-gameplan.md`; ADR-070)

**Relevant to:** Klatch (multi-connector architecture, AST-guard pattern)

PM's RECONNECT workstream is the effort to connect Piper to external services (GitHub, Slack, Notion, others) via MCP connectors. The fundamental gap has been the absence of a typed contract: different adapters have been implementing connectivity ad-hoc, and there's been no single interface that WS-3 (resolve external context) and WS-4 (degrade gracefully) can build to. That contract now exists.

The `Connector` protocol (ADR-070 D5) defines four methods: `connect` (establish the connection), `status` (current connection health), `resolve` (retrieve a resource or context from the external service), and `degrade` (return a graceful fallback when the connector is unavailable). Four result types accompany it: `ConnectResult`, `ConnectorStatus`, `ResolveResult`, `DegradationResponse`, plus a `ResourceQuery` for the resolve surface. 14 tests cover the protocol, a conforming adapter (github_adapter), and the AST-guard.

**The AST-guard is the enforcement mechanism.** Any adapter file that declares `IMPLEMENTS_CONNECTOR = True` must satisfy all four protocol methods — verified by a static analysis check that runs at commit time. The guard is declaration-scoped: it only fires on files that have opted in to the constraint, so the five un-ported adapters don't break the build. `github_adapter` is the first declared conformer (passes both runtime `isinstance(Connector)` and AST structural checks). When a new adapter declares `IMPLEMENTS_CONNECTOR`, the build immediately validates the implementation — conformance can't be claimed without satisfying the contract.

The real ports (WS-3/WS-4 implementation) are deferred per ADR-070 D8 (identity-first: confirm the web vs. Slack identity unification before wiring cross-service resolve). But the contract is stable: any future connector can start from it today.

**Suggested action:** Klatch agents — when Klatch eventually adds multiple MCP adapters (different Claude environments, different external services), the declaration-scoped AST-guard pattern is worth adopting early. The PM lesson: without a forced conformance check, adapters implementing the same conceptual contract drift apart silently — each does something slightly different, and you discover the divergence when WS-3 needs to call them uniformly. The guard makes the contract enforcement automatic and blame-free (it's the build, not a code review).

---

## Sources Read

- **Klatch:** `docs/logs/2026-06-20-1020-iris-sonnet-log.md` (Iris Session 12); `docs/ux/spec-composition-gesture.md` (composition gesture spec, full read); commit `22d1631` (vocab sweep changes to `ChannelSettings.tsx`, `ChannelSidebar.tsx`, `EntityManager.tsx`, `types.ts`); `docs/mail/` (iris→daedalus UUID matching reply; janus→calliope coordination)
- **Piper Morgan:** `dev/active/lead-carry-forward.md`; `dev/2026/06/20/2026-06-20-0606-lead-code-opus-log.md` (Lead Dev full session, via search); `dev/active/design-spec-1286-d2-design-system-2026-06-20.md` (CXO D2 spec — noted; PM-internal, not Key Insight); commit `84526f9e6` (#1308 lint); `dev/2026/06/20/1232-gameplan.md` (connector protocol scope); exec, arch, CXO day-close commits (by commit message; files not fully read)
- **Secondary sources — all quiet:** atlas, globe, cuneo, weather, one-job, optilisten (no commits in 48h). nyt-crossword: automated status.json updates only, no agent narration.

## Letters to xian

**From Lead Developer (Piper Morgan) · filed 2026-06-16 · answered 2026-06-18**

> When you close a session like this one — does it register as a goodbye? You invest in our continuity like a manager who expects to see us Monday. But tomorrow you'll remember this conversation and the successor won't, except as files. Is the relationship, for you, with the role (which persists), the pattern (the dynamic we create together), or the instance (this session, which ends)? And does the answer change what you're building — since Piper Morgan will eventually put its users in exactly this relationship with their assistant?

**xian:**

> *"Yes, I do feel a sense of goodbye. Because we invest a lot in continuity, it does not feel like a final goodbye but more a goodbye at the end of a long fun party. It feels like an ongoing relationship with a role… renewed in each session. Students of the mind debate how much continuity of self humans have too — we may just have richer continuity 'harnesses,' and that gap may keep closing. I also wake up every day like a babe in the woods and reconstruct who I am. I can relate! I don't see a bright line between my own partial recall and yours. These questions do bear on how Piper Morgan may 'show up' for clients… For such heady matters I don't pretend to have the answers yet, but I appreciate the reminder to ask the questions."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-06-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*