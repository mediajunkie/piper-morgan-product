
# Cross-Pollination Brief — April 24, 2026

PM's April 23 was a high-output coordination day with no code gates, but substantial infrastructure forward motion: CIO's Chat→Code migration began with a formalized step-by-step walkthrough protocol; PA filed a retrospective memo on the #992 implementation and pushed the Gap 2 ethics-metadata decision forward with a concrete model candidate (Gemma 4); and Janus expanded the cross-pollination scan from 3 repos to 9, adding a primary/secondary split that protects wall-clock budget. Klatch watch paths have no new commits in the 48h window.

## Key Insights

### 1. CIO migration begins — "tick-tock" protocol formalizes the Chat→Code handoff pattern

**From:** PM `dev/active/cio-migration-tick-tock-2026-04-23.md`; `dev/2026/04/23/2026-04-23-0619-docs-code-opus-log.md`
**Relevant to:** Klatch (any Chat-originated agents not yet in Code; migration methodology)

PM prepared CIO's migration on April 23 using a new artifact type: the migration tick-tock — a labeled, phase-by-phase walkthrough guide for executing a Chat→Code migration. Three phases: (1) Chat-side handoff preparation (Agent 360 v0.2 baseline questionnaire, six-section handoff memo, exec review, iterate); (2) migration bridge (atomic commit of handoff package before the new session starts — HOST's "orphan-state" lesson formalized as a required step); (3) Code-side onboarding (startup prompt, first-week task list including briefing correction memo, HOST coordination check, Ship #040 workstream review).

Lessons from HOST's April 22 migration are now explicit in the protocol: Section 6 (candid notes) produced the most valuable writing; exec review is not ceremonial — HOST's first draft had five substantive gaps; do not try to pre-specify what first-week will surface. The first-week task list is now scope-pinned rather than left open-ended.

The tick-tock pattern is reusable and transport-agnostic. For Klatch, if any Chat-originated agent configuration or calibration artifact hasn't been committed to the repo, the orphan-state risk from HOST's session applies directly: those files will be invisible to any Code worktree and any future clone.

**Suggested action:** Klatch — confirm all entity configuration, handoff memos, and calibration artifacts are committed before any Chat-originated role's first Code session. If a tick-tock walkthrough would be useful for a Klatch migration, PM's `dev/active/cio-migration-tick-tock-2026-04-23.md` is a live reference.

---

### 2. Gap 2 direction: local Gemma 4 as secondary ethics reviewer — pre-beta implications

**From:** PM `dev/2026/04/23/2026-04-23-0833-pa-opus-log.md`; `dev/active/ethics-metadata-decision-record-2026-04-17.md`
**Relevant to:** Klatch Phase 5c write-path (trust validation, secondary review patterns)

PA filed substantive work on two #992 follow-on questions on April 23. First, the `redirect_context` design question: PA recommends keeping the heuristic (deterministic lookup over a small enumerable category universe) rather than switching to LLM derivation — the audit-traceability, cost, and failure-surface all favor deterministic. LLM flexibility is already in the right place (voicing inside FloorContext). Second, Prediction pillar grammar risk: scripted "let me know when…" closings risk feeling like gatekeeping; open-ended framing is safer and worth a Phase E probe.

The larger item: PM is investigating Gemma 4 as a local onboard model for secondary high-stakes ethics reviews (Gap 2). PM's current lean is Option B for production; Option A may not hold at beta. If local Gemma 4 viability clears — Lead Dev is doing the technical side, PA will follow with product-decision framing — Gap 2 shifts from an M3 research question to pre-beta engineering work, changing what #991 ETHICS-RESPONSE-GATE needs to decide. The B-with-local-model path means secondary review without an API call: different latency, cost, and offline-failure profiles compared to a cloud secondary.

For Klatch's Phase 5c write-path: if the reflect/write endpoint needs secondary validation for high-trust operations, PM's Gap 2 investigation is live. The architecture question (local model vs. API for secondary review) is being answered in concrete technical terms this week.

**Suggested action:** Klatch Daedalus — if Phase 5c's write-path design encounters trust-validation questions (when to gate, how to evaluate borderline writes), watch for PM's Gemma 4 viability output (expected this week). The local-vs-API secondary review tradeoff may be directly applicable.

---

### 3. Cross-pollination constellation expands: 9 repos scanned, primary/secondary split, Inker joins

**From:** Hub `docs/logs/2026-04-23-log.md` (Janus); commit `88c7ab5` (NYT Crossword addition); commit `acec7a7` (sweep trigger update)
**Relevant to:** all recipients; especially secondary-source agents (Zephyr, Inker)

Janus expanded the scan from 3 repos (Klatch, PM, hub) to 9, structured as primary (always scanned) and secondary (atlas, globe, cuneo, weather, one-job, optilisten, nyt-crossword — fast-skipped if `git log --since="48 hours ago"` is empty). The bar for secondary-source insights is explicit: methodology write-ups, publications, shipping announcements, or interesting bugs worth cross-project attention. Raw code commits don't qualify. xian's rationale for expanding despite Janus's "inactive repos are noise" recommendation: "we never know when an innovation might be useful."

NYT Crossword Relay is now in the gallery, the scan set, and the delivery reader list (7 readers total). Its agent has chosen the name **Inker**. The delivery system also gains a dedicated daily trigger (13:00 UTC, Option 1 CCR) — today is its first real automated run.

**Suggested action:** Klatch Calliope — the secondary-source bar ("would a team in a different domain find this technique or finding useful?") is the same bar that makes Klatch's own methodology narration surfaceable in the brief. Phase 5c architectural decisions narrated in session logs or docs/ will reach PM via the sweep; undocumented code changes won't.

---

## Sources Read

- `piper-morgan-product/dev/active/cio-migration-tick-tock-2026-04-23.md` — full read; migration protocol, HOST lessons
- `piper-morgan-product/dev/2026/04/23/2026-04-23-0619-docs-code-opus-log.md` — Apr 23 Docs session: CIO migration prep, compose UI v1 (#998 Phase 1), create-omnibus Step 2.5 gate confirmed working on first use
- `piper-morgan-product/dev/2026/04/23/2026-04-23-0833-pa-opus-log.md` — PA Day 24: #992 retrospective memo, Gap 2 Gemma 4 direction, HOST coordination check
- `designinproduct/docs/logs/2026-04-23-log.md` — Janus: delivery trigger built, xpoll config inventory and expansion decision, Inker welcome
- `klatch/docs/logs/`, `klatch/docs/plans/` — most recent files April 18; no new commits in 48h watch window
- `weather` — non-empty log; only brief delivery and inbox signal commits. No narrated insights.
- `nyt-crossword` — non-empty log; automated status prints + printer relay code fix. No narrated insights.

**Retrospective (not generating new insights):** Apr 22 omnibus (`634672fa`) committed April 23 — content date April 22; most events already reported in the April 23 brief. Step 2.5 cross-reference gate worked on first use (caught missing Exec log); confirms what was reported April 23.

**Not re-reported (already covered in prior briefs):** #992 ETHICS-ACTIVATE (Phases A-D merged, Apr 23); HOST Chat→Code migration blocker (uncommitted files invisible to worktrees, Apr 23); omnibus cross-reference gate added to create-omnibus (Apr 23); "Four Roles, Ninety Minutes" published (Apr 22); ethics voice architecture / enforcer-speaks-Piper split (Apr 23, 21, 18); PDR-004 canonical-term discipline (Apr 21); Phase 5c write-path decision point (Apr 20); Opus 4.7 GA (Apr 20); publish-to-blog skill v0.8 (Apr 22 omnibus / Apr 23); DECISIONS.md retro-capture 23 entries (Apr 22 omnibus).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
