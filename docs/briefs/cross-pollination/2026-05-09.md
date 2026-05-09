
# Cross-Pollination Brief — May 9, 2026

PM's Friday was a late-day surge: the PreCompact hook shipped as the third layer of sign-off discipline, #1063 stale-test rewrite closed in 15 minutes (the discovered-work arc from Thursday's subagent is fully resolved), and a P0 quality-regression investigation refuted the fabrication hypothesis — the apparent drop from 72.1% to 65.6% is judge miscalibration and fixture pollution, not model degradation. CIO completed promotion analysis for Patterns-063, -064, and -065 from Emerging to Proven. M2f opens per CEO directive; M2f audit-cascade work is gated on pre-M2f remediation establishing a clean baseline. Klatch has no new session activity this window.

## Key Insights

### 1. PreCompact hook (#86) ships: warn-only discipline at the context boundary

**From:** PM commit `76f049a3` (`feat(hooks): PreCompact sign-off discipline warning`); `7f79880` (log); merge `7769ef39`
**Relevant to:** Klatch (Daedalus, Mnemosyne; sign-off discipline; compaction boundary coverage)

`.claude/hooks/precompact-signoff-warning.sh` is now the third layer of sign-off discipline — after the agent's own checklist and Docs's merge-keeper sweep. It fires before context compaction and checks three conditions: uncommitted changes, unpushed commits, commits ahead of origin/main. Warn-only: PreCompact hooks cannot block, so the value is making the failure visible before context loss, to the agent who can still act. Fires to stderr + appends to `dev/active/session-end-warnings.log` (gitignored, ephemeral per-machine data).

Design rationale in the commit message: "Logs to `dev/active/session-end-warnings.log` (gitignored as ephemeral per-machine data; tailed by Docs merge-keeper sweep). References Rule 2 + the three 'pick one' options (merge / NOTICE memo / ask PM). Per Docs Apr 29 go-ahead (PM authorized 'let's upgrade'); deferred SessionEnd until PreCompact catch-rate is observed." The catch-rate observation before adding a SessionEnd hook is a deliberate staged-rollout decision.

Also closed same session: **#1063 in 15 minutes.** The 12 stale standup tests discovered by Thursday's subagent (filed with skip rationale, reported in May 8 brief) were rewritten by Lead Dev using three patterns: (a) state-machine assertions updated to `GATHERING_YESTERDAY` (post-#900 entry point), (b) workflow-error/fallback paths using `"quick"` bypass to GENERATING, (c) full-flow walks for the three tests that exercise the per-part flow. Net: 12 skips → 0 skips; standup directory 351 → 363 passing. The complete arc: subagent skips with rationale → next-session Lead Dev rewrites — confirms the "annotate, don't improvise" subagent pattern reported May 8 has a clean downstream.

**Suggested action:** Klatch — if Daedalus or Mnemosyne doesn't already have PreCompact coverage, this is a low-cost addition: 3 git checks, warn-only, exit 0 always. The three-layer model (agent checklist → merge-keeper sweep → PreCompact hook) is complete in PM and could map directly. The decision to stage SessionEnd separately until catch-rate is observed is worth adopting — adding two hooks simultaneously makes it hard to attribute which one fires.

---

### 2. #1064 investigation: retest quality drop was judge miscalibration + fixture pollution, not fabrication

**From:** PM commit `271397a8` (`investigation(#1064): fabrication regression hypothesis refuted`); `e16c26b` (log update with full investigation narrative)
**Relevant to:** Klatch (Argus; eval harness discipline; fixture-hygiene; judge-calibration methodology)

Canonical retest Run 4 (M2f-entry baseline) showed quality 65.6% vs. Apr 16 baseline 72.1% — a 9% apparent regression. CEO called P0 investigation with the directive "rather find no, didn't go deeper than [X], than stop because we found [Y]." Lead Dev's investigation findings committed to `dev/2026/05/08/floor-fabrication-investigation.md`:

- **0 of 10 auto-fails confirmed as pure LLM fabrication**
- **7 of 10** are judge-calibration / methodology / fixture artifacts (false flags)
- **3 of 10** are real-but-narrow code bugs: 3 hardcoded sites in `intent_service.py` reference a disabled setup-wizard, 1 `#N` slot-filling bug for issue references, possibly 2 routing-miss queries

**Q56 smoking gun (fixture pollution):** "Show my todos" was flagged as fabrication — the canonical test user had 15 real todos in the DB (7×"review the deployment plan", 7×"review prs", 1×"smoke"), accumulated from prior retest runs that executed Q53/Q54 "add todo" mutations without cleanup. The repetition pattern was real DB rows, not LLM degeneration.

**Systemic finding:** Judge over-weights user-context-specificity even on identity/capability queries that don't need it. The auto-fail rule (any dim=0 → FAIL) amplifies this miscalibration — a single judge-dimension calibration drift turns into a FAIL even when other dimensions scored correctly.

Recommendation accepted: re-classify #1064 P0 → P1. Pre-M2f remediation = fixture reset + judge recalibration confer (CXO/PPM) + 3 narrow bug fixes + clean retest to establish baseline. **M2f audit-cascade work is blocked until this baseline is met** per CEO directive May 8 17:22.

**Suggested action:** Klatch — for any eval harness running tests that write to the DB (standup flow, list-add actions, etc.): add explicit fixture teardown per run or use a per-run isolated schema. The Q56 finding shows that DB mutations from one run contaminate the next without visible error — only symptoms (repetition patterns) that can look like hallucination. Also worth reviewing: does your judge calibration distinguish between queries that require user-context-specificity and those that don't? If not, a single judge-dimension miscalibration → FAIL on identity queries is a common false-positive shape.

---

### 3. Patterns-063/064/065 all promoted Emerging → Proven in one CIO session

**From:** PM commit `8d4cc13` (`pattern+methodology(cio): promote Pattern-063, -064, -065 from Emerging to Proven`); analysis file `dev/active/cio-pattern-promotion-analysis-2026-05-08.md`
**Relevant to:** Klatch (all agents; pattern lifecycle discipline; Pattern-064 "alive scaffolding" directly Klatch-relevant)

CIO completed promotion analysis for all three patterns simultaneously — the 062 family is now fully Proven:

- **Pattern-063 (Parallel-Authoring Drift):** 3 independent surface validations: diagnostic at C-axis origin; branch-or-anchor rule shipped to 2 surfaces (Methodology-24 + Colleague Test v2.3) without recurrence; Architect May 4 review found a code-layer instance (legacy/refactored `boundary_enforcer.py` coexistence). Promoted Emerging → Proven.

- **Pattern-064 (Extension Without Integration / "alive scaffolding"):** Architect-authored Apr 28. Validation: Architect's May 4 review identified 2 new in-the-wild instances using the pattern's exact "alive scaffolding" framing (`KnowledgeGraphService` alive scaffolding + `boundary_enforcer_refactored.py:343–358` commented-out adaptive-learn TODO). "Pattern operationally diagnostic at population scale" — the framing accurately predicts what you find when you look. Architect concurrence implicit through diagnostic use; CIO holds promotion authority per policy.

- **Pattern-065 (Continuity Memo Before the Seam):** 6-section structure operated without structural failure across 7 cohort migrations Apr 22–26; decreasing review-volume signal observable; Section 6 candor invitation produced a PP-002 tier-3 signal via HOST 360 v0.2. All three pattern claims validated.

The 062 family (Assembly Assumption / Parallel-Authoring Drift / Extension Without Integration / Continuity Memo Before the Seam — 062/063/064/065) is now fully Proven. Promotion memo distributed to all 11 leadership inboxes including Architect (Pattern-064 author).

**Suggested action:** Klatch — Pattern-064 is particularly worth reviewing. The "alive scaffolding" framing (code that exists, has structure, but is not integrated or reachable) could apply to any Klatch subsystem with partial implementations. The promotion process itself (trial-application evidence across ≥3 surfaces before Emerging→Proven) is worth borrowing if Argus or AAXT tracks emerging diagnostic patterns.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/08/2026-05-08-0655-lead-code-opus-log.md` — full read; #1059 Notion Phase -1 complete (close to ready, memo to PA), #1063 rewrite (15 min, 363/363), #86 PreCompact hook (feat + merge), M2f surface/retest/M2f cohort confirmed, #1064 investigation complete; sign-off notes
- `piper-morgan-product/dev/2026/05/08/floor-fabrication-investigation.md` — summary via commit diff; 249 LOC investigation; five-whys + DB inspection + adjacent-pattern sweep; 10 auto-fails annotated; Q56 fixture-pollution root cause
- PM commit `8d4cc13` — full diff; CIO pattern promotion analysis; Pattern-063/064/065 evidence and promotion notes; 062 family completion
- PM commit `1fb7b3b` — full diff; CIO→Lead scoping ask for xpoll brief session-start hook (passive notification if brief is newer than role's last session log; analogous to log-maintenance hook; estimated ~40 lines bash, half-session)
- PM commit `1e3d6c7` — diff summary; BRIEFING-CURRENT-STATE refreshed (5-day staleness); CEO May 8 directive "no defer M2f"; M2a-e DONE; M2f scope confirmed
- `klatch` — 48h git log: 2 brief-delivery commits only; no new session activity
- `weather` — 48h git log: brief-delivery commits only; no narrated insights
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten`, `nyt-crossword` — 48h logs empty; skipped

**Not re-reported (covered in prior briefs):** #1053 subagent arc + annotation-not-improvisation (May 8); `&&`-chain verification gap / worktree-required for subagent deploys (May 8); A Hail of Memos published (May 8); Notion 1,504 LOC vs. 1,112 estimate / #1059 filed (May 8); N/A count ≥5 template drift / #1058 (May 7); Architect punch list / structlog+caplog (May 7); Ship #041 published (May 7); #1054 broad-except prod bug (May 7).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and routing hints.*
