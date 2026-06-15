# Cross-Pollination Brief — June 15, 2026

PM's Radar sidebar surface went from decision to working code in a single Saturday evening: domain + backend + frontend shipped behind a `?radar=1` feature flag, 84 tests green. Then PM expanded the scope — "no partial ship" — to require all four entity types (Conversations, Documents, WorkItems, People) for beta, not just conversations. Phase-0 verification on the Document source immediately found a multi-tenancy hole: the document store has no user scoping, any return would leak documents across users. The investigation broadened into a systemic audit (#1241). Meanwhile, a US government directive suspended Fable 5 and Mythos 5 three days after launch — the first documented government-forced frontier model takedown. Today two more models retire from the API. Both projects are code-clean, but vendor-risk assumptions need updating.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Radar ships behind a feature flag — then immediately expands to a 4-entity beta requirement

**From:** Lead Dev June 14 session log (Fires 24–29); commits `98f460cdc` (Phase 2 frontend), #1236 closed; PM directive; issues #1237–1240
**Relevant to:** Klatch (channel navigation surface; entity-types as first-class objects); both projects (feature-flag UAT pattern)

The sidebar slot-swap decided Saturday morning (June 14) shipped by evening. PM's right sidebar is now a Radar entity surface — domain layer (8 tests), API endpoint, and JS frontend (17 tests) all landed behind `?radar=1`. Render is XSS-safe (all user data via `textContent`), honest provenance (● observed / ○ example), and frame-agnostic so the upcoming F2 page-shell can re-home it without a rebuild. The stale-server trap was caught before UAT: the running server (PID 95577) predated the backend commit by 13 hours — `/openapi.json` proved the route was absent before the restart, avoiding a silent fallback to the old history list that would have looked like it worked.

Then PM's "no partial ship" direction doubled the scope. PDR-002 names four entity types; shipping conversations-only doesn't count as shipping Radar. Three issues (#1238 Document, #1239 WorkItem, #1240 People) were filed, audit-cascaded, and placed in D1 — but all three immediately surfaced blocking prerequisites (see Insight 2 for Document; #1233 identity map gates WorkItem; PPM entity-model gates People). The Radar surface is live and UAT-ready; the entity-type backends are a sequenced multi-lane effort.

**Suggested action:** Klatch — the `EntitySource` protocol (an async `fetch(user_id) → list[RadarEntity]` interface) is the slot-in seam that let PM build and ship the Radar surface before all entity backends existed. If Klatch's channel navigation evolves toward surfacing entities (entities, archived conversations, project channels), the same pattern applies: ship the surface behind a flag, slot in entity types as backends exist.

---

### 2. PM's Document source reveals a systemic multi-tenancy gap in content stores (#1241)

**From:** Lead Dev June 14 session log (Fire 31); commit `21bc3fe32` (Arch memo + #1241 filed); issue #1241; issue #1238 BLOCKED
**Relevant to:** Klatch (any async database context or content-store wrapper); both projects (verify user-scoping before building any per-user surface)

Phase-0 contract verification on the Document EntitySource (supposed to be the "unblocked, small" case) found that `DocumentService` in PM's knowledge graph layer has no `user_id` or owner anywhere — not in methods, not stamped by the ingester, not passed by any upload caller. Returning documents from it would expose every user's documents to every other user, violating ADR-058 multi-tenancy. The Lead Dev immediately stopped (#1238 BLOCKED) and filed #1241 requesting an Arch-lens audit: how many content stores in PM share this same pattern? The "deep plumbing-out" note from PM suggests it's not isolated.

The broader lesson: **conformance checks don't catch soundness assumptions**. The Radar entity-source issues were audit-cascade conformant (sections filled, ACs in place) before Phase-0 verification revealed the gap. The proposed amendment to the audit-cascade skill adds a Referent-Verification / Dependency-Completeness check: trace each claimed capability to a concrete verified backend or an open tracked dependency, not just a planned one. The June 14 Lead Dev session caught this twice in one night — once with a closed "dependency" epic (#706), once with an unscoped content store.

**Suggested action:** Klatch — the `messages`, `entities`, `channels`, and `message_artifacts` tables are all single-user data with no inherent multi-tenancy concern (local-first tool, single user). But if Klatch ever gains shared or networked channels, user-scoping at the data layer is the prerequisite. The PM audit pattern is worth watching: when the #1241 audit completes, the canonical anchoring pattern it produces (Arch-authored) will describe what correct user-scoped content storage looks like end-to-end.

---

### 3. US government suspended Fable 5 + Mythos 5 three days after launch — the first export-control model takedown (Klatch intel)

**From:** Klatch Intel sweep 2026-06-15 (item 1); `docs/intel/2026-06-15-sweep.md`; external sources (anthropic.com/news, CNBC)
**Relevant to:** Both projects (any Anthropic-dependent product); Klatch roadmap (cross-vendor entity channels)

On June 12, three days after GA, Anthropic received a US government directive under national-security export-control authority and suspended Fable 5 and Mythos 5 globally — foreign users, foreign nationals inside the US, and foreign-national Anthropic employees all blocked. Fallback is Opus 4.8 (all other models unaffected). Neither model appeared in Klatch's `AVAILABLE_MODELS` and neither project has code exposure, but the strategic context changes: a single-vendor dependency on Anthropic now carries demonstrated regulatory-closure risk, not just theoretical IPO-volatility risk.

Separately, Anthropic published three policy frameworks on June 10 — including an Advanced AI Framework proposing FAA-style government authority to block frontier models. The suspension happened three days later. The framework-then-reality sequence is now the strongest evidence in the ecosystem for why cross-vendor flexibility belongs in the architecture, not the roadmap's "someday/maybe" column.

Today (June 15), `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire from the Anthropic API — calls now return 404. Klatch's `MODEL_ALIASES` map both deprecated IDs to active equivalents; a live database spot-check today is recommended to confirm the May 10 snapshot audit is still current. Klatch's Anthropic SDK is also now 8 minor versions behind (`^0.96.0` vs current `0.104.1`) — Anthropic's recommended fallback for the Fable/Mythos suspension is Opus 4.8, which requires an SDK bump.

**Suggested action:** Klatch — three actions, sequenced by urgency: (1) Argus live-DB spot-check today confirming zero rows with deprecated model IDs; (2) Daedalus SDK bump from `^0.96.0` to `^0.104.1` after reviewing release notes for breaking changes; (3) Daedalus add `claude-opus-4-8` to `AVAILABLE_MODELS` — Anthropic's own recommended fallback from the Fable/Mythos suspension.

---

### 4. 26 concurrent agents on shared main create a write-race condition — commit-immediately discipline adopted

**From:** Lead Dev June 14 session log (Fire 28, "someone" investigation); commit `4f3237d8c` (day-close)
**Relevant to:** Klatch (Daedalus, Argus, Theseus, Calliope running concurrently); both projects (any multi-agent repo with a high concurrent-writer count)

PM's multi-agent cohort now runs ~26 concurrent Claude instances across 18 worktrees sharing `origin/main`. Frequent `git merge origin/main` syncs by other agents race against another agent's uncommitted working-tree writes — the other agent's in-flight appends get clobbered before they can commit. Two session log entries were lost this way before the pattern was identified (reconstructed from commits and carry-forward notes).

Adopted mitigation: commit dev/ writes immediately on append + verify-by-content (`git show HEAD:<file> | grep`); commit-before-sync. The Lead Dev flagged the underlying cohort scaling problem (too many concurrent writers on one repo) to Arch as a cross-lane issue, but parked it — not a daily blocker yet, but will escalate as the cohort grows.

**Suggested action:** Klatch — the team runs 4–5 named agents (Daedalus, Argus, Theseus, Calliope, plus cross-poll delivery). At current scale, commit-immediately discipline suffices. If Klatch's agent count grows toward 10+, the PM pattern suggests a structural solution (separate working trees for long-running sessions, or a mailbox-on-main pattern for coordination files) will be needed before the write-race becomes a data-loss source.

---

## Sources Read

- **piper-morgan-product**: Lead Dev June 14 session log (`dev/2026/06/14/2026-06-14-0631-lead-code-opus-log.md`) — Fires 24–32 + DAY-CLOSE; Docs June 15 overnight log (`dev/2026/06/15/2026-06-15-0317-docs-code-sonnet-log.md`) — START only
- **klatch**: `docs/intel/2026-06-15-sweep.md` (automated external scan); brief-delivery commits only in source code

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*