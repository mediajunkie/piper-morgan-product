
# Cross-Pollination Brief — May 8, 2026

PM's Thursday morning was a completion session: #1053 went from "staged" to "shipped" via a ~30-minute subagent execution, a 16-check post-execution audit, and PM approval — closing the test-migration arc that had been in prep since May 6. Two new cross-agent collision-discipline findings landed in memory from this session, refining the earlier "commit-per-functional-unit" pattern. "A Hail of Memos" published to pipermorgan.ai. Notion's pre-floor codebase verified at 1,504 LOC, 35% larger than the 2025 estimate that had been blocking #304's sub-epic placement.

## Key Insights

### 1. #1053 subagent arc complete: "annotation not improvisation" as the right subagent behavior under scope-over

**From:** PM `dev/2026/05/07/2026-05-07-0640-lead-code-opus-log.md` (commits `69aa5e74` merge, `0217a40f` audit, `fc7f685e` log); `dev/2026/05/07/1053-execution-audit.md`
**Relevant to:** Klatch (subagent deployment patterns; test-migration discipline)

Subagent deployed 6:48 AM, completed ~7:18 AM — 4 phases in ~30 minutes. Audit matrix: 16 checks, all ✅ except one ⚠️ (cross-agent collision, not the subagent's fault — documented separately). Key methodology findings:

**Phase 2 reframe:** The prepped gameplan over-scoped `test_standup_routing_585.py` — 12 tests already passing, no migration needed. Subagent annotated the rationale in a commit message rather than improvising ("annotate test_standup_routing_585.py rationale (no migration needed)"). Lead Dev noted: "This is the expected 'audit-cascade prep imperfect; subagent finds reality' behavior — and the subagent surfaced it via commit message rather than improvising silently." The right subagent behavior when scope over-estimates the work: announce the discrepancy, don't fill the gap.

**12 stale tests discovered (#1063):** Tests that asserted `GATHERING_PREFERENCES` as the initial standup state were broken after #900 changed the entry point to `GATHERING_YESTERDAY`. These had appeared as `RuntimeWarning` collection errors (invisible to normal test runs) rather than failures — which is why #900's close missed them. Subagent skipped with consistent `@pytest.mark.skip(reason="#1063 ...")` rationale on each test, did not delete. Filed #1063 as discovered work.

**Audit completeness:** Lead Dev verified production code unchanged, fake test-double unchanged, reference implementation unchanged — only 4 test files touched. `bind_session_id` E2E coverage added (2 tests). All 16 checks documented in a standalone audit file committed to the repo before merge.

**Suggested action:** Klatch — if deploying subagents for test migration or similar bounded tasks, the 16-check audit matrix pattern (`1053-execution-audit.md`) is worth reviewing. Key checks: scope-only files touched, discovered work filed with consistent skip rationale, production code diff empty, subagent did NOT self-merge. The "Phase 2 reframe" finding also validates: subagents should be briefed on what to do when they encounter a phase that needs less work than specified — annotation via commit message is the right call, not silent under-delivery or over-delivery.

---

### 2. AND-chain verification gap: `&&` chains don't gate on branch-check output, only exit code

**From:** PM `dev/2026/05/07/2026-05-07-0640-lead-code-opus-log.md` (§ "07:00 — Cross-agent git collision"); Docs session log `2026-05-07-1056-docs-code-opus-log.md` (§ "New discipline absorbed")
**Relevant to:** Klatch (all agents; multi-agent git discipline; subagent worktree requirements)

May 7's collision is a new variant of the April–May collision pattern, adding two specific technical findings that weren't in the earlier write-ups:

**Finding 1 — `&&` chains print but don't gate.** Lead Dev ran: `git branch --show-current && git add ... && git commit ...`. The subagent's `git checkout claude/1053-...` had flipped the shared `.git` HEAD mid-session. `git branch --show-current` printed the wrong branch name — but because `git branch --show-current` exits 0 regardless of what it prints, the `&&` chain ran the commit anyway. The commit landed on the feature branch. Verification that doesn't gate on its output is not verification.

**Fix (now in memory as `feedback_branch_show_current_before_every_commit.md`):**
```bash
# WRONG — prints but doesn't gate:
git branch --show-current && git add ... && git commit ...

# RIGHT — gates on the check:
[ "$(git branch --show-current)" = "main" ] && git add ... && git commit ...
# OR: run as separate command, eyeball output, then commit
```

**Finding 2 — Subagent deployment requires worktree OR commit-before-deploy.** When a subagent runs `git checkout <branch>` in the same `.git` directory as its deploying agent, it flips HEAD for the deploying agent. Two safe options: use a real `git worktree add` (separate checkout, independent HEAD); or commit all foreground work to its branch BEFORE deploying the subagent. The May 6 "commit-per-functional-unit" mitigation remains valid but is downstream of this — it minimizes the loss when a collision happens; these two options prevent the flip.

**Propagation:** Docs absorbed both findings from the overnight memory entry and confirmed adoption in its May 7 session log (gated-check form or explicit eyeball, enforced before every commit).

**Suggested action:** Klatch — for any multi-agent setup where one agent deploys a subagent in the same repo directory: add `git worktree` to the worktree-per-session discipline, or establish a "commit everything to your branch before deploying" norm. The `&&`-chain finding is also non-Piper-specific: any shell-scripted git workflow that embeds a branch check as a `&&` prefix should be converted to a gated form.

---

### 3. "A Hail of Memos" published; footer cadence rule encoded in memory

**From:** PM commit `3f21306` (`content: A Hail of Memos published — fixes applied + footer + calendar`)
**Relevant to:** Klatch Calliope (publication cadence; footer-tease discipline; numeric-to-metaphor headline pattern)

"A Hail of Memos" (Building Piper Morgan series, content date April 16) published Thursday to pipermorgan.ai/blog/a-hail-of-memos. Two final fixes per PM authorization: "state of art" → "state of the art"; footer tease corrected from "Audit and Talk" (Tuesday's upcoming narrative) to "The Inchworm Position" (Saturday's insight post).

**The footer rule, now pinned in memory (`feedback_footer_teases_next_post_on_calendar_any_category.md`):** Footer teases should point to the very next post on the editorial calendar, regardless of category. "Audit and Talk" would have been correct if the next post were on Tuesday, but the cadence rule applies across all post types — insight, narrative, newsletter — so the next-in-sequence is the right target even if it's a different category than the current post.

**Title voice discipline:** Draft title "Thirty-Seven Memos" (numeric) was renamed to "A Hail of Memos" (metaphor) during PM's May 5 voice pass. Pattern consistent with prior headline choices: specificity of the content is preserved in the body, not the headline. The numeric headline tends to read as a list post; the metaphor leads with tone.

Medium syndication pending (per Building PM cadence: Medium-only for narrative posts).

**Suggested action:** Klatch Calliope — if there's a footer-tease convention in any Klatch public-facing document (blog, newsletter, release notes), encoding the "next post regardless of category" rule as a standing editorial convention prevents the "I teased the wrong post" correction loop after each publish.

---

### 4. Notion pre-floor codebase measured at 1,504 LOC — 35% larger than Aug 2025 estimate

**From:** PM `dev/2026/05/07/2026-05-07-0640-lead-code-opus-log.md` (§ "06:50 — #304 Notion Phase -1 investigation FILED (#1059)")
**Relevant to:** Klatch (scope-surprise from stale estimates; "measure before you plan" discipline)

#1059 filed as a Phase -1 spike to gate #304's sub-epic placement. Lead Dev verified the pre-floor Notion code: `services/integrations/mcp/notion_adapter.py` at 867 LOC + `services/intelligence/spatial/notion_spatial.py` at 637 LOC = **1,504 LOC total**. The original claim driving #304's scope estimate: 1,112 LOC (filed Aug 2025). Actual is 35% larger — the code grew while the estimate sat unchanged.

PM ratified Wednesday: Notion IS in alpha scope. #1059 delivers a memo-only investigation (no activation work) to determine whether the pre-floor Notion code is in a condition to activate or whether it needs rework before sub-epic placement.

**The structural finding:** Stale LOC estimates compound silently. A codebase that was 1,112 LOC in August is 1,504 LOC in May — but the issue's scope narrative hadn't updated. The Phase -1 investigation pattern (measure the actual state before scoping the work) surfaces this before it surprises an agent mid-implementation.

**Suggested action:** Klatch — for any backlog issue that carries a code-size, scope, or complexity estimate from >3 months ago, a "Phase -1 verify" is worth adding before gameplan: re-read the file(s), recount the LOC, confirm the architecture assumptions still hold. 30 minutes before gameplan prevents 3 hours of mid-implementation recalibration.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/07/2026-05-07-0640-lead-code-opus-log.md` — full read; #1053 subagent deployment + audit + merge, #1059 filed, #471 break-out (#1060/#1061/#1062), cross-agent collision + memory refinement, sign-off
- `piper-morgan-product/dev/2026/05/07/1053-execution-audit.md` — full read; 16-check audit matrix, Phase 2 reframe note, #1063 discovery rationale, verdict
- `piper-morgan-product/dev/2026/05/07/2026-05-07-1056-docs-code-opus-log.md` — partial read; new discipline absorbed (gated branch-check), May 7 session context
- PM commit `3f21306` — full message read; A Hail of Memos publish details, footer fix, calendar update
- PM commit `08e3d9e` — message read; May 6 omnibus summary (retrospective; confirmatory of already-reported items)
- `klatch` — 48h git log: 2 brief-delivery commits only; no new session activity; Iris walkthrough Surfaces 3-8 still pending
- `atlas`, `globe`, `one-job`, `weather`, `nyt-crossword` — 48h logs empty; skipped
- `cuneo`, `optilisten` — 48h logs: brief-delivery + automated status prints only; no narrated insights

**Not re-reported (covered in prior briefs):** Broad-except swallows logger init / #1054 prod bug (May 7); N/A count ≥5 = template drift signal / #1058 (May 7); Architect 5-item punch list closed / structlog+caplog incompatibility (May 7); Ship #041 published (May 7); M2 surface review complete Topics 1-7 (May 7); #900 2h vs. 12-14h / pre-work-pays-dividends (May 6); M2 unmapped-families triage (May 6); commit-per-functional-unit as cross-agent collision mitigation (May 6); #1055 –1518 LOC (May 6); Six Issues Before Dinner published (May 6); M2e INTENT-COVERAGE arc (May 5); audit-cascade persistence gap pattern (May 5); close-issue-properly 12-issue remediation (May 5).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
