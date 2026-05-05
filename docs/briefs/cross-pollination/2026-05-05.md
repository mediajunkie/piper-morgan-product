
# Cross-Pollination Brief — May 5, 2026

PM's Monday session extended the M2e sprint with four issues shipped end-to-end (#1027, #1042, #1039, #1040) plus two multi-phase Phase 1 milestones (#869 tabs, #1052 persistence), totalling the fifth multi-issue day in two weeks. Audit-cascade caught a blocking persistence gap in #900 before any implementation code ran — the same stop-and-file pattern as #1018→#1035 one week earlier, now repeating as a confirmed operating discipline. A morning scan also revealed that 12 M2d issues shipped Sunday had never had their GitHub state-transition run; all retroactively corrected with a formal UAT tracker (#1047) filed for the deferred browser-smoke items. Ship #041 workstream reviews landed from all 7 leadership roles; publish target is May 6.

## Key Insights

### 1. M2e INTENT-COVERAGE arc ships: RepoResolver + milestones/releases + labels/branches in one day

**From:** PM `dev/2026/05/04/2026-05-04-0637-lead-code-opus-log.md` (commits `2d577225`/#1042, `dc467511`/#1039, `b90b6488`/#1040, `69813e4c`/#1027)
**Relevant to:** Klatch Daedalus/Argus (intent routing expansion methodology; repo-resolution decision-tree pattern)

Four issues shipped in sequence:

**#1027** — `LLMModel.CLAUDE_OPUS` repointed from a Sonnet fallback comment to `"claude-opus-4-7"`. Filed Apr 29 with "wait until Opus 4 ships"; Opus 4 had already shipped before that date. PM caught the stale premise during morning triage; resolved in under 15 minutes. The pattern: issues filed with conditional-on-event language sometimes don't get triaged after the event fires. A periodic "issues with conditional language" sweep would catch these.

**#1042** — New `services/integrations/github/repo_resolver.py` (220 LOC) implementing a 4-level resolution cascade: explicit `owner`/`repo` args → project-linked repo → user `default_repo` preference → `PIPER_DEFAULT_REPO` env var → raise `UnresolvedRepoError`. Removed hardcoded `piper-morgan-product`/`mediajunkie` literals from 14 files, including two USER-FACING chat-message templates that were surfacing PM's GitHub username directly to users. 33 new tests; 64 existing tests clean.

**#1039** — `list_milestones_via_mcp` + `list_releases_via_mcp` wrappers; pre-classifier adds 12 patterns; handlers sort milestones by due_on, releases by published_at with "Current version" headline for latest non-prerelease. State-filter and prerelease-filter patterns deliberately withheld per PM Q3/Q4 — filed as #1051 (post-MVP, same "precedent as #1037 for #1031 topic tabs" deferral pattern). 65 new tests, 1525 regressions clean.

**#1040** — `list_labels_via_mcp` + `list_branches_via_mcp`; pre-classifier adds 12 patterns with deliberate negative-test exclusions (`label this as urgent`, `branch out from this approach`); handler sorts branches default-first and bundles `default_branch` from a `get_repository_info` call. 63 new tests, 1588 regressions clean.

**Suggested action:** Klatch Daedalus — the #1042 RepoResolver decision-tree is a useful pattern for any capability that needs to resolve an implicit target at runtime. The 4-level cascade (explicit → user-preference → env-var → error) separates "what the user said" from "what we infer" cleanly. Also: the negative-test patterns in #1040's pre-classifier (explicitly testing that `label this as urgent` does NOT route to `list_labels_query`) are worth adding to AAXT coverage for any Klatch capability that shares vocabulary with conversational English phrases.

---

### 2. Audit-cascade catches StandupConversation persistence gap before #900 implementation — second instance of the #1018→#1035 pattern

**From:** PM `dev/2026/05/04/2026-05-04-0637-lead-code-opus-log.md` (commits `4129fd5`/#1052 feat, `e54a8c1f` merge)
**Relevant to:** Klatch (audit-cascade as pre-implementation gate; persistence design at gameplan-phase)

#900 gameplan refresh triggered a Phase 0 spike on `StandupConversation`. Finding: persistence was a module-level singleton dict at `services/conversation/conversation_handler.py:42-43` — lost on restart. Surfacing-then-resume (Phase 4 of #900) requires durability; the gameplan as written could not work.

PM disposition: **file #1052 as pre-work** (same as the #1018→#1035 precedent from May 2). Phase 1 (data layer) ships tonight; Phase 2 (manager rewrite + 7 consumer callsites) queued for tomorrow before #900 resumes.

**#1052 Phase 1 delivered same evening:** `StandupConversationDB` SQLAlchemy model with `postgresql.JSONB().with_variant(JSON, "sqlite")` for unit-test compat (mirrors the #1035 lesson learned); `StandupConversationRepository` with `add`/`get_by_id`/`get_by_session_id`/`get_active_for_user`/`update`/`delete`/`count_for_user`; Alembic migration with strategic indexes on `(user_id, state)` + `session_id`; 22 tests covering CRUD + query shape + user-scoping + nested-field round-trip. All pass.

Lead Dev's note: *"The audit-cascade discipline catching the StandupConversation persistence question before any code got written for #900 is exactly the value of running the refresh — same lesson as #1018 → #1035 a week ago."*

**Suggested action:** Klatch — this pattern has now recurred twice in a week, which validates it. Before any Klatch gameplan execution that depends on data being "available" or "resumable" across sessions, an explicit Phase 0 question: *"where does this data persist? Module-level? Repository? DB?"* The question takes 15 minutes to answer; discovering the gap during implementation costs a day. The pattern could be formalized as a one-line gameplan template addition.

---

### 3. Systemic close-issue-properly failure in M2d sprint: 12 issues retroactively corrected; #1047 M2D-UAT filed

**From:** PM `dev/2026/05/04/2026-05-04-0637-lead-code-opus-log.md` (issue cleanup pass 8:11–9:00 AM; commits via close-issue-properly skill)
**Relevant to:** Klatch (fast sprint → deferred closure hygiene; explicit UAT tracker pattern)

The Sunday M2d sprint shipped 8 issues end-to-end with implementation-evidence comments but without running the GitHub state-transition or updating description checkboxes. PM caught this Monday morning. Full remediation: 8 OPEN issues properly closed (description checkboxes updated first, then state-transition), 4 already-CLOSED issues with unchecked-box drift annotated. Lead Dev's root-cause note: *"description-checkbox-update step is where most closure failures happen."*

**The recurring caveat category:** Most deferred checkboxes were "no manual browser smoke" across the UI issues (#704, #714, #1030-#1033, #1035). Automated tests covered code paths; no end-to-end click-through ran during the sprint. These consolidated into **#1047 M2D-UAT** (P3): a single-pass UAT report targeting one agent in one sitting, producing a `dev/YYYY/MM/DD/m2d-uat-report.md`. Defects (if any) get separate issues with repro steps. Also filed: **#1048** (stage-visual design for Insight Journal page — P4 CXO/PPM design conversation, not a verification gap).

**Suggested action:** Klatch — if any multi-issue sprint completes, add a next-morning hygiene check: `git log --oneline --since="24 hours ago" | grep merge` to list what merged, then verify GitHub state matches. Fast sprints reliably produce the implementation-evidence-without-state-transition pattern; the check prevents silent backlog drift. The #1047 UAT-tracker pattern (consolidate deferred verifications into one named issue rather than leaving them as unchecked boxes in closed issues) is also worth adopting.

---

### 4. Ship #041 workstream reviews in from 7 roles; canonical-vocabulary-watch.md ships; roadmap 23 days stale

**From:** PM commits `21708b9` (CIO workstream), `82e16db` (Arch), `9ad4439` (Comms), et al.; Docs log `2026-05-04-0733-docs-code-opus-log.md`; Docs audit `weekly-docs-audit-1049-2026-05-04.md`
**Relevant to:** Klatch Calliope (PM publication pipeline; vocabulary watch methodology)

Ship #041 publish target is **May 6**. CIO's proposed theme: **"From Diagnosis to Discipline in 24 Hours"** — the week of Apr 24–30 saw fix-to-validation latency close to <24h in five distinct instances (methodology entry → rubric embedding → hook fix → automation → flag flip). CIO frames this as a Code-era operating signal qualitatively different from Chat-era cadence.

Docs weekly audit (#1049) found **roadmap 23 days stale** (last update Apr 11). M2d scope closed, M2e gameplans walked, Phase F + #992 closed — none reflected. Docs sent a PPM memo proposing five cadence options (trigger-based per CIO audit policy / weekly / session-start hook / workstream-review line item / hybrid). PPM picks the shape; this flags to any project tracking a roadmap that staleness compounds silently when sprint work outpaces doc updates.

**`canonical-vocabulary-watch.md` v1 shipped** (`7153fcf4`) — CIO + Docs joint stewardship. Watch list records terms with multiple live meanings (like "primary" having two senses clarified by CEO May 4). Operating discipline: additions via CIO single-line edits; Docs scans weekly; pruning at audit cadence. Closes M1 audit recommendation S1.

**Suggested action:** Klatch Calliope — note PM's May 6 double publish: "Six Issues Before Dinner" (narrative arc post) + Ship #041 (newsletter). The pattern of pairing a narrative post with the weekly newsletter on the same day collapses the editorial overhead of keeping two tracks synchronized. If Klatch develops a public-facing cadence, the paired-publish model is worth considering.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/04/2026-05-04-0637-lead-code-opus-log.md` — full read; all M2e execution detail, cleanup pass, deferred-work issues, #900 STOP-and-ask, #1052 Phase 1
- `piper-morgan-product/dev/2026/05/04/workstream-041-cio-2026-05-04.md` — full read; methodology-to-runtime latency theme, Pattern-062 family, alpha catch-22 capture
- `piper-morgan-product/dev/2026/05/04/2026-05-04-0733-docs-code-opus-log.md` — full read; discipline lapse, canonical-vocabulary-watch.md, #1049 docs audit findings
- PM commits `2d577225` (#1042), `dc467511` (#1039), `b90b6488` (#1040), `69813e4c` (#1027), `4129fd5` (#1052), `e54a8c1f` (merge #1052), `1da409d` (#869 Phase 1), `2cd277d3` (merge #869 Phase 1) — message + file-stat reads
- `klatch` — 48h git log: 1 commit (`44fb30e`, brief delivery only); no new session activity; Iris walkthrough Surfaces 3-8 still pending
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `weather`, `nyt-crossword` — 48h logs: brief delivery + automated status prints only; no narrated insights

**Not re-reported (covered in prior briefs):** M2d complete (8 issues, one session — May 4); M2e gameplans + #790 trust-gated calendar (May 4); SDK 6 versions behind + June 15 deprecation (May 4); ADR-061 verbal ratification (May 4); Friction-Focused Feedback published (May 4); audit-cascade NOT PASSED on M2d gameplans + discovery-phase staleness (May 3); The Drift You Don't Notice published (May 3).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
