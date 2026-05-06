# Cross-Pollination Brief — May 6, 2026

PM's Tuesday session delivered four issues end-to-end: #1052 Phase 2 (StandupConversationManager async rewrite), #900 (standup 3-part structural collection — 5 phases in ~2 hours, gameplan estimated 12–14h), #869 (Project Config IA), and #1055 (Architect cleanup, –1518 LOC). With M2e's persistence pre-work landed, #900 shipped faster than any comparable issue in the sprint. Evening brought the M2 unmapped-families triage: 27 issues across 6 families reviewed with PM, closing 2 superseded items and recording PM decisions on three pending questions. "Six Issues Before Dinner" published Tuesday; Docs caught a Haiku 3 retirement timing inaccuracy during fact-check before it reached readers.

## Key Insights

### 1. Pre-work investment pays at velocity: #900 ships in 2h vs. 12–14h estimate; cross-agent git collision surfaced

**From:** PM `dev/2026/05/05/2026-05-05-0643-lead-code-opus-log.md` (commits `4c2e82f9`/#900 merge + 5 phase commits)
**Relevant to:** Klatch (pre-work-pays-dividends pattern; multi-agent git collision discipline)

#900's gameplan estimated 12–14 hours. The actual wall-clock time was ~2 hours. Lead Dev's analysis: Phase 1's state-machine design made downstream phases mechanical, and #1052's persistence layer (22 tests, shipped the previous day) had already solved everything Phase 4 needed — partial-capture-on-escape/timeout — before Phase 4 code ran.

**What shipped:** 5 phases producing a full 3-part standup flow (yesterday → today → blockers), resume protocol (suspend mid-today → replay captured → continue), durable `StandupPartialCapture` JSONB column (PM chose Option B over alternatives: cleaner than 3 columns, avoids stuffing into `context`). 148 tests across 3 files. End-to-end smoke verified via SQLite roundtrip. Known limitation filed rather than hidden: completion-detection regex (`\bdone|stop|finish(ed)?|complete\b`) can false-positive on real items like "finish #900" — LLM-classification upgrade queued post-MVP as #1054's companion note.

**Cross-agent git collision:** A parallel agent's `git reset` wiped Lead Dev's uncommitted Phase 3 work twice during implementation. PM intervened, warned other agents off the critical path. Lead Dev recovered cleanly on the third attempt using immediate commit-and-push discipline (not waiting until phase completion). This is the same collision pattern that surfaced in April worktree incidents — the mitigation that works is: **commit after each functional unit, not at phase boundary.** Smaller commits, more frequent pushes, on a critical-path branch where parallel agents are active.

**Suggested action:** Klatch — the #1052→#900 sequence validates the "persistence-first" pattern reported May 5. More broadly: the velocity gain here is measurable (2h vs. 12–14h estimated). If a Klatch issue has a data-layer dependency, shipping the persistence pre-work first (even as a short standalone ticket) isn't overhead — it eliminates the discovery-mid-implementation delay that costs the most time. For multi-agent git safety: any agent on a critical implementation path should commit to its branch after each function or module, not at end-of-phase. This makes a parallel agent's `git reset` survivable.

---

### 2. M2 unmapped-families triage: 27 issues, 6 families, 3 PM decisions — M2f/M2g sub-epic map proposed

**From:** PM `dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md`; Lead Dev log `2026-05-05-0643` (commits `fa8683e`, `2d73105`)
**Relevant to:** Klatch (family-level backlog triage methodology; conditional-on-event issue hygiene)

PA queued this ask on May 4; Lead Dev executed it on the afternoon of May 5. Shape: same audit-cascade structure applied to 27 issues sorted into 6 families, same verdict taxonomy (SUPERSEDED / STILL NEEDED / NEEDS PM CALL / RE-SCOPED).

**Results:**
- **2 SUPERSEDED** — #101 (temporal context fully shipped via #951; close-supersede) + #100 (basic project portfolio shipped, but analytics/allocation layer not shipped; re-scope and file narrower issue)
- **22 STILL NEEDED** — distributed across security/infra, integrations, context, memory, testing, UI/process
- **2 NEEDS PM CALL** — #304 (Notion integration: is the pre-floor code still intact? is Notion in alpha scope?) + #471 (Infrastructure parent epic: keep as one epic or break into M3 sub-epics?)

**PM walked 3 decisions same session:** #987 GEMINI-QUOTA closed (Option 3 — Gemini stays as a real provider, billing call deferred); #991 ETHICS-RESPONSE-GATE closed (Option A for alpha — CXO non-binding view from Apr 16 ratified); #983 CONTEXT-BLOCKED pending Architect decision on canonical "blocked" label convention (memo sent).

**Sub-epic placement proposed** (PA+PM call): M2f post-floor-coverage (#983/#984/#985/#986 — all explicitly deferred from #951); M2g memory governance (#972/#973/#974/#975 — Janus-aligned); M2-discovered testing infra (#987/#989/#991/#993/#994/#995); M3/post-alpha production hardening (#482/#470/#557/#542/#371/#366/#472). M2 open-issue surface: 56 → 49 (7 closed or close-superseded today).

**The structural insight:** Issues filed during a discovery phase with conditional-on-event language ("pending billing call", "pending PM decision") reliably drift past their trigger date without auto-update. #101 was filed with "TBD" language; temporal context shipped March 2026; nobody closed #101. The family-level triage sweep is what catches this. PA's prior read ("likely high close-supersede rate in Family 3") was accurate; Family 3 had the most supersession.

**Suggested action:** Klatch — if there are any backlog issues filed during a research or design phase with "pending X" language, run a sweep: check whether X has shipped. Issues filed before a shipped feature are the highest-probability close-supersede candidates. The per-family verdict taxonomy (SUPERSEDED / STILL NEEDED / NEEDS PM CALL / RE-SCOPED) is a clean structure for this kind of backlog audit. PA's role in PM (writing the ask memo, receiving the verdicts, proposing sub-epic placement) is worth noting: the triage itself is Lead Dev work, but the synthesis and sub-epic architecture is a coordination function.

---

### 3. Architect soundness review actioned same session it was read: #1055 removes –1518 LOC

**From:** PM `dev/2026/05/05/2026-05-05-0643-lead-code-opus-log.md` (commits `e6fe05c`/#1055 feat, `589285f` merge)
**Relevant to:** Klatch (review-to-action discipline; Pattern-064 alive scaffolding)

The Architect's soundness review was filed April 13 and returned a verdict May 4: "structurally sound, 5 cleanup items, none blocking." Lead Dev read the review May 5 morning, filed #1055 consolidating items 1-3, and shipped it same session (~40 minutes).

**What was removed:**
- Pattern-064 alive scaffolding in `KnowledgeGraphService` — an unused `EthicsBoundaryEnforcer` parameter + 5 if-guarded blocks + 3 callsites that had never been wired
- Legacy `services/ethics/boundary_enforcer.py` (441 LOC) + 2 dependent test files — the refactored successor had been live for months; the original sat parallel to it
- Commented-out adaptive-learn dead allocation in `boundary_enforcer_refactored.py:343-358`

Net: –1518 lines, +3 lines. 112/112 ethics tests pass. #1056 filed for 2 pre-existing KG test failures discovered during verification (not introduced by #1055).

**Pattern-064 context:** "Extension Without Integration" — code added to a live system in a speculative hook style, never wired. Named in the Klatch→PM brief Apr 27 as the third member of the 062/063/064 family. #1055 is the first substantial PM cleanup directly attributable to that pattern diagnosis.

**On review-to-action latency:** The 22-day gap between Architect filing the review (Apr 13) and Lead Dev reading/acting on it (May 5) is worth noting. The review was non-blocking; PM direction was to queue post-#900. The discipline of acting on it the same session it was read (not opening it and filing "will do later") is what prevented further drift. One read = one action.

**Suggested action:** Klatch — any Architect-equivalent structural review that finds "none blocking" items should have a named cleanup ticket filed before the review session ends, even if execution is deferred. The filing anchors the work; without it, "none blocking" items reliably stay open indefinitely. The ~40-minute execution window for –1518 LOC cleanup shows that once the scope is well-defined (three items, clear files), the work is fast. The cost is in the gap between finding and filing.

---

### 4. "Six Issues Before Dinner" published; Docs fact-check catches Haiku 3 timing error

**From:** PM commits `c58c205`, `6282063f` (calendar + publish); `507f997e` (Medium URL); Docs log `2026-05-05-0658-docs-code-opus-log.md`
**Relevant to:** Klatch Calliope (publication fact-check discipline; Docs editorial role)

"Six Issues Before Dinner" — PM's Tuesday narrative post in the Building Piper Morgan series (Medium-only, per building cadence) — published May 5 afternoon after a PM voice pass + Docs proofread. The article covers the April 14–15 arc: six issues shipped in one session, four days under the Haiku 3 deadline.

**Docs fact-check caught one inaccuracy:** Article draft stated Haiku 3 retired "by midday Wednesday." Docs sourced the Lead Dev session log from April 14–15 directly; actual retirement time was "11:30 PM Wednesday." Corrected to "by late Wednesday night" before publish. All other numerical claims in the article (6,246 tests, 26 methods, 911 lines, 58 of 61 routing, 61 of 61 structure, 120 tests dropped, 6,125 passing, 10 files) verified exact against source logs.

**PM note mid-session:** After an earlier branch-drift incident (Docs's commit landed on Lead Dev's active worktree branch instead of main), PM reminded Docs: "be mindful of Lead Dev's work and try not to clash with them." Docs added `git branch --show-current` before every commit as a new discipline — third such incident in the cycle (PA Apr 29, Lead Dev May 3, Docs May 5). The pattern: in a multi-agent repo, branch-check before every commit is the lowest-cost collision prevention available.

Medium URL added same session: `https://medium.com/building-piper-morgan/six-issues-before-dinner-aa5158df10d5`. Editorial calendar fully updated. *A Hail of Memos* (next Thursday's narrative) was proofread the same day; 5 fixes applied; queued for May 7.

**Suggested action:** Klatch Calliope — PM now has three active public channels: weekly Ship newsletters, Building Piper Morgan narrative (Medium, published Tuesdays), and insight posts on pipermorgan.ai/blog/. The fact-check discipline Docs runs before each narrative publish — sourcing numerical claims directly to session logs — is worth encoding formally if Klatch develops any public writing. "Where exactly is this number from?" before publication, not after.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/05/2026-05-05-0643-lead-code-opus-log.md` — full read; #1052 Phase 2 + #900 + #869 + #1055 + M2 triage + PM decisions
- `piper-morgan-product/dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md` — full read; per-family and per-issue verdicts, sub-epic proposals
- `piper-morgan-product/dev/2026/05/05/2026-05-05-0658-docs-code-opus-log.md` — full read; Docs session (Six Issues publication, Hail of Memos proofread, branch-drift incident)
- PM commits: `4c2e82f9` (#900 merge), `efdf3b8b` (#1052 Phase 2), `11303f83` (#869 merge), `589285f` (#1055 merge), `e6fe05c` (#1055 feat), `fa8683e` + `2d73105` (M2 triage verdicts + PM-decisions memos), `6282063f` + `507f997e` (Six Issues calendar + Medium URL) — stat/message reads
- `klatch` — 48h git log: 2 commits (brief delivery only); no new session activity; Iris walkthrough Surfaces 3-8 still pending
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten` — 48h logs empty; skipped
- `weather`, `nyt-crossword` — 48h logs: brief delivery + automated status prints only; no narrated insights

**Not re-reported (covered in prior briefs):** #1052 Phase 1 + audit-cascade persistence gap catch (May 5); M2e INTENT-COVERAGE arc (#1042/#1039/#1040/#1027) (May 5); close-issue-properly 12-issue remediation + #1047 UAT (May 5); canonical-vocabulary-watch.md ships (May 5); Ship #041 workstream reviews filed (May 5); M2d complete + M2e gameplans + #790 (May 4); SDK 6 versions behind + June 15 deprecation (May 4); "Friction-Focused Feedback" published (May 4); audit-cascade NOT PASSED on M2d + discovery-phase staleness (May 3).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
