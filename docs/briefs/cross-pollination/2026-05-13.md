
# Cross-Pollination Brief — May 13, 2026

Tuesday was a fast-resolution day on both projects. The Opus 4.7 default-flip that yesterday's brief reported as "held" shipped by mid-morning — Daedalus's own 4.7 sessions hadn't surfaced the compaction-threshold concern, and xian released the flip along with a singleThread fix for the client test parallelism flake. Argus turned around the full Dreaming research spike in a single 2-hour session (478 lines, 5 passes), confirming that Anthropic's memory store is architecturally identical to Klatch's L3 and that the April 12 Janus synthesis predicted the design space with ~90% accuracy. On the design side, Iris session 11 resolved all five outstanding user vocabulary questions and delivered the 1.0 critical path design brief. PM completed M2f-E — four issues shipped in twelve hours, giving the conversational Floor real-time access to GitHub state (blocked issues, active milestones, recent activity). *Audit and Talk* published Tuesday morning at pipermorgan.ai.

## Key Insights

### 1. Opus 4.7 default-flip ships — compaction-threshold concern resolved in practice

**From:** `klatch/docs/logs/2026-05-12-0739-daedalus-opus-log.md`; commit `ba69f7f` (DEFAULT_MODEL 4-6 → 4-7 + singleThread fix)
**Relevant to:** Klatch (all agents — sessions now run 4.7 by default); PM (Lead Dev — same flip pending evaluation)

Yesterday's brief reported that Daedalus had shipped Opus 4.7 plumbing but explicitly held the default-flip pending compaction-threshold recalibration. By mid-morning Tuesday that hold lifted: xian approved the flip after Daedalus noted the +35% tokenizer concern hadn't materialized in actual 4.7 sessions he'd been running.

Two changes in one commit: `DEFAULT_MODEL` flipped from `claude-opus-4-6` to `claude-opus-4-7` (with a spec comment recording the manual-by-design rationale — no upstream "recommended default" signal, flips have product implications). Separately, Vitest's singleThread option was enabled for the client suite to fix a pre-existing ~8% flake rate (14 tests / 5 files contending on 5000ms testTimeout under jsdom load). Wall-time impact negligible: 19.7s vs ~20s. Three tests updated to pin the new `DEFAULT_MODEL` constant. Suite: 1263 total green (1085 server + 178 client).

The process discussion that followed: Calliope had sketched a structured intel-artifact for future model-flip evaluations; all three (xian + Calliope + Daedalus) agreed to wait for a second data point before locking the artifact shape — extracted-over-designed discipline.

**Suggested action:** PM (Lead Dev) — the Klatch flip is empirical evidence that the +35% tokenizer concern is real in principle but not necessarily a problem in practice on current session patterns. If PM's session logs aren't hitting compaction unexpectedly early on 4.7, the practical threshold may be fine. The forcing function remains: watch the PreCompact hook's fire timing on 4.7 sessions and compare to 4.6 baseline. If the hook fires at the same task depth, the +35% isn't a practical constraint for current session shapes.

---

### 2. Argus dreaming spike: Anthropic memory store ≅ Klatch L3 — import/export contract intact

**From:** `klatch/docs/research/anthropic-dreaming-import-export-impact-2026-05-12.md` (478 insertions); commit `3979f42` (Argus 5/12: dreaming research spike published); Argus session log `2026-05-12-0900-argus-opus-log.md`
**Relevant to:** Klatch (Daedalus — D1–D5 decisions; Step 11 scoping); PM (Piper Alpha — parallel spike pending; Architect — ADR implications)

Calliope's morning memo commissioned the spike; Argus delivered a 5-pass, 2-hour research doc that answered all four questions with primary-source evidence and named five decisions.

**The architectural finding:** Anthropic's Managed Agents memory store is a markdown filesystem — paths like `/preferences/formatting.md`, ≤100KB per file, version-tracked, workspace-scoped, mounted at `/mnt/memory/`. This is structurally identical to Klatch's L3 (markdown files, hierarchical namespace, session-persistent context). The April 12 Janus synthesis (14-system landscape, six-tier framework, `valid_from`/`type`/`source`/`trust_level` field set) predicted this shape with ~90% accuracy four months before Anthropic's announcement. **The strategic finding from yesterday's brief holds: don't compete on "external memory layer for Claude"; compete on assembly-layer differentiation.**

**The contract finding:** None of Klatch's three importers or three transports touch memory store APIs today. The conceptual slot exists at L3; the wire is missing. The `extensions` namespace in `packages/server/src/export/package-builder.ts:184` already accommodates producer attribution. Import/export contract is unaffected by Anthropic's release.

**Five decisions named (D1–D5):** D1 (should Klatch add `extensions.klatch.l3_snapshot` to export packages?); D2 (what constitutes the L3 boundary for import?); D3 (does Phase 5b HTTP transport need a memory-store handshake?); D4 (should the JSON schema version tick for the L3 additions?); D5 (cross-read with PM's Piper Alpha spike before finalizing). None urgent; D5 gates on PM's publication.

**Suggested action:** Klatch (Daedalus) — D1 is the load-bearing decision. If Klatch exports L3 snapshots, PM projects (or other users of Klatch exports) can absorb session context on import rather than starting cold. The `extensions` namespace is already there; this is a schema-version bump + one new builder method, not an architecture change. Worth deciding before Step 11 scoping finalizes.

---

### 3. Iris session 11: vocabulary resolved (V1–V5) + 1.0 critical path design brief

**From:** `klatch/docs/logs/2026-05-12-0715-iris-opus-log.md`; commits `f521032` (session 11 wrap); `docs/ux/object-model.md` (V1–V5 added); `docs/ux/design-brief.md` (new)
**Relevant to:** Klatch (Daedalus — Tier 1+2 patches; Theseus — MAXT vocabulary baseline); PM (CXO — vocabulary/mental model methodology for Piper Morgan's own UX)

Iris session 11 resolved the five outstanding user-vocabulary questions and wrote a holistic 1.0 design brief:

**Vocabulary (V1–V5):**
- V1: *Chats* and *klatches* are the primary user-facing categories; *conversation* is the singular generic fallback; *channel* stays in implementation
- V2: *Agent* is the broad user-facing word for any AI participant; *role* is the subset with persistent identity in a project; *entity* stays in implementation
- V3: Users "set up a klatch" with direct field-level properties; *workflow* and *meeting* stay internal; three-audiences-three-views principle extended
- V4: *Invite* (add agent to existing klatch) + *convene* (create new klatch) — Slack-flavored composition verbs
- V5: Naming an agent IS the promotion — no separate verb. The naming flow IS the promotion flow

**1.0 critical path:** composition gesture + klatch setup surface + Tier 1 patches that matter + working meeting experience + promotion gesture. Proposed sequence: Daedalus Tier 1+2 patches (in flight) → Iris + xian spec composition gesture → Daedalus implements → Theseus MAXT-validates → 1.0 beta. Holistic redesign continues in parallel post-beta.

The faint-token finding from Argus's 5/11 session completed a one-day round-trip: Iris spec'd option 2 (reclassify usage sites to `text-muted`) → Daedalus shipped same day → Argus pinned the new contract in tests. The Track 1 cadence is working.

**Suggested action:** PM (CXO) — the V4 vocabulary principle (verb pairs: *invite* for adding to existing, *convene* for creating new) is transferable to any product surface where users initiate vs. join collaborative workflows. The key discipline: don't overload one verb for both operations. PM's multi-agent sessions have an analogous gesture; worth checking whether the user-facing language maps the two operations cleanly.

---

### 4. PM M2f-E cohort complete: 4 issues in 12 hours — Floor gains GitHub-state awareness

**From:** `piper-morgan-product/dev/2026/05/12/2026-05-12-0708-lead-code-opus-log.md`; commits `b134f907` (#984), `bcb36c0c` (#983), `55ba8d1` (#985), `2437f43b` (#986); day tally: 7 issues closed, 57 new tests
**Relevant to:** Klatch (Argus — context-surface architecture; all agents — PM's floor-context model as design reference); PM (all roles — floor capabilities now available)

PM's M2f-E was 4 issues (CONTEXT-CACHE + CONTEXT-BLOCKED + CONTEXT-SPRINT + CONTEXT-ACTIVITY). All four shipped in a single session on Tuesday:

- **#984 CONTEXT-CACHE** (morning, 31 tests): `ContextCache` helper with graceful Redis fallback. Mirrors the `token_blacklist` pattern. 4 gather methods, 4 source-level helpers; all cache the superset and slice on read so temporal-limit-10 and status-limit-5 share one cache entry.
- **#983 CONTEXT-BLOCKED** (mid-morning, 7 tests): GitHub `status: blocked` label → top 10 open blocked issues surfaced in floor via `blocked_items` formatter.
- **#985 CONTEXT-SPRINT** (late morning, 7 tests): Active GitHub milestones sorted by `due_on`, surfaced in both `status_priority_context` AND `temporal_context`.
- **#986 CONTEXT-ACTIVITY** (evening, 8 tests): GitHub issues + PRs touched in last 7 days, type-distinguished (issue vs. PR), surfaced in both contexts.

**Floor context inventory (end of day):** 7 cached, fail-graceful, fresh surfaces — trust_profile, pending_todos, completed_todos, reminders, calendar, projects, user_context, blocked_items, active_milestones, recent_activity. All with explicit TTLs and graceful Redis fallback (no crash on cache miss).

**Straggler sweep:** #1068 (milestone routing pre-classifier fix), #1069 (attention_query source-transparent empty-state wording), #1078 (friendly-error Set-Cookie preserve via `HTTPExceptionWithCookieClear` subclass) — all shipped same day. #1070 (multi-turn evaluation harness) deferred (3–5 hr methodology investment, past 8pm).

**Suggested action:** Klatch (Argus) — PM's `ContextCache` helper pattern is worth noting for any eval or research pipeline that hits external APIs repeatedly. The core discipline: cache the superset at the API level, slice at the consumer level. One cache entry serves multiple query shapes. Klatch's test infrastructure doesn't currently have this concern, but the Managed Agents memory-store cross-read (D5 above) may eventually involve external API calls worth caching.

---

## Sources Read

- `klatch/docs/logs/2026-05-12-0739-daedalus-opus-log.md` — full read; Iris signal close (faint-token), default-flip + singleThread shipped, Argus situational-awareness check, Calliope close-loop memo
- `klatch/docs/logs/2026-05-12-0715-iris-opus-log.md` — full read; faint-token reclassify spec, vocabulary pass V1–V5, design brief + 1.0 critical path
- `klatch/docs/logs/2026-05-12-0900-argus-opus-log.md` — full read; dreaming research spike 5-pass, D1–D5, Calliope publication memo
- `klatch/docs/logs/2026-05-12-0742-calliope-opus-log.md` — full read; two-day catch-up, Step 11 scoping doc, entity-reframe blog draft, default-flip routing, Argus spike commissioning
- `piper-morgan-product/dev/2026/05/12/2026-05-12-0708-lead-code-opus-log.md` — full read; M2f-E cohort end-to-end session log (#984, #983, #985, #986), straggler sweep (#1068, #1069, #1078)
- `piper-morgan-product/dev/2026/05/12/2026-05-12-0739-docs-code-opus-log.md` — partial read (80 lines); *Audit and Talk* publish pipeline, May 11 omnibus, doc audit #1076, dev/active cleanup
- `piper-morgan-product/dev/2026/05/12/2026-05-12-0855-pa-opus-log.md` — partial read; PA Dreaming research project planning only (research not yet published as of log end)
- `designinproduct` — hub CLAUDE.md (context); sweep-log (prior dates)
- `atlas`, `globe`, `cuneo`, `weather`, `one-job`, `optilisten` — 48h logs empty; skipped
- `nyt-crossword` — 48h log: automated status commits only (fetch/print/remarkable); no narrated insights; skipped

**Not re-reported (covered in prior briefs):** Managed Agents Dreaming strategic reframe from Argus's 5/11 sweep curation (May 12); Opus 4.7 +35% tokenizer plumbing shipped, flip held (May 12); Iris session 10 two-track design + panel disclosure taxonomy (May 12); PM M2f Group C ships (#857) + Comms voice discipline (May 12); Iris session 9 panels-as-musculature reframe (May 11); #921 FastAPI directional-evidence merge + Monitor idle-spin Pattern-068 (May 11).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and routing hints.*
