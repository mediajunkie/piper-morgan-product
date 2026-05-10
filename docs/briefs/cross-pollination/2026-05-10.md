# Cross-Pollination Brief — May 10, 2026

PM's Saturday was the densest single session of the M2f arc: 9 issues closed, −2,229 LOC removed, 4 worktrees used, and 2 subagents deployed — all in one day. The headline finding: 3 of 5 M2f Group A+B issues had body-vs-reality mismatches where audit-cascade Phase 0 discovered the issue was describing dead or unreachable code. Instead of multi-thousand-LOC migrations, the disposition was deletion. Pattern-067 (Issue-Body Reality Mismatch) filed Emerging. Separately: the rubric recalibration work that followed Friday's #1064 investigation landed clean — Run 7 at 68.9% PASS exceeds the Apr 12 baseline and clears the CEO's M2f gate criterion. Hub CLAUDE.md gained new Multi-Agent Operation discipline; Janus Layer 5 mandate expanded.

## Key Insights

### 1. M2f Group A+B complete: −2,229 LOC via dead-code disposition; Pattern-067 filed

**From:** PM session log `dev/2026/05/09/2026-05-09-0630-lead-code-opus-log.md`; commits `b62a9080` (#936 deletion), `82bca29c` (#935 deletion), `80cbd586` (#933 merge), `c9591108` (#932 merge); CURRENT-STATE refresh `15942063`; Pattern-067 commit `a2bd06d9`
**Relevant to:** Klatch (all agents; audit-cascade discipline; issue-triage methodology; worktree adoption)

Saturday's M2f Group A+B work — covering security (#932 HIBP stub, #933 re-enable key validation) and persistence (#936 UserService, #935 analytics) — produced a striking result: 3 of 5 issues disposed via deletion rather than implementation.

- **#933 (re-enable API key validation):** bypass had been disabled Oct 30, 2025 to work around format-validator issues. Those issues were fixed in the same Oct 30 commit. The bypass outlasted its reason by 6+ months. Removing it *un-broke* 5 tests rather than breaking any. Phase 0 investigation caught this; without it, the issue body would have been implemented as written.
- **#936 (UserService db persistence):** issue body claimed "user data lost on restart." Investigation: `UserService` wired into `AuthMiddleware` but `create_session()` / `create_user()` have zero production callsites. Real auth is PostgreSQL + `AuthService` + JWT. UserService always returns None; the data-loss scenario is unreachable. PM disposition: Option A (delete). −435 LOC.
- **#935 (BudgetManager/APIUsageTracker persistence):** `APIUsageTracker` has a real INSERT into `api_usage_logs` (table exists, 0 rows), but both production callers pass without a `session` parameter — the INSERT gate never fires. Transitive dead code. PM disposition: Option A (delete) + alembic migration to drop the table. −1,378 LOC.

**Net: −2,229 LOC across the group.** #932 and #933 (the real implementation work) contributed a combined −51 LOC net (fixes + new tests), offsetting the deletions at the margin.

**Worktree adoption:** Lead Dev created a dedicated worktree for each issue (`piper-morgan-product-932`, `-933`, `-936`, `-935`) — fully operationalizing the "worktree per substantive session" norm. Cross-agent collision still occurred mid-#932 (another agent's `git checkout` flipped the shared HEAD); the pre-commit gated branch check caught it with exit 1 and no bad commit landed. Recovery via re-checkout was clean. Subagents for #932 and #933 created their own worktrees independently, confirming the collision-discipline pattern is working at both agent and sub-agent scope.

**Pattern-067 (Issue-Body Reality Mismatch)** filed Emerging by Lead Dev (self-approval per Pattern-066 precedent): *"prophylactic Phase 0 dead-code/unreachable check on issue bodies matching trigger conditions: 'TODO to enable X', 'lost on restart', line-number citations from triage runs N months ago, parenthetical alternatives in acceptance criteria."* Promotion to Proven pending one trial-application cycle. Aggregate observed: ~−2,229 LOC removed via deletion instead of migration additions.

**Suggested action:** Klatch — when any issue body contains the trigger-condition language above, run a Phase 0 dead-code investigation before scoping the migration. The PM M2f experience shows the cost of skipping this is implementing features nobody uses. The "issue body describes a world that no longer exists" shape is especially common for issues originally triaged during active development when code paths were still hypothetical.

---

### 2. Canonical retest Run 7: 68.9% PASS — M2f baseline established via rubric recalibration + 3 bug fixes

**From:** PM session log `dev/2026/05/09/2026-05-09-0630-lead-code-opus-log.md` (§ 06:35–08:15); commits `49c48c2e` (#1065), `f623bba2` (#1067), `78be342e` (#1066), `14259cdd` (Run 7); `15942063` (CURRENT-STATE refresh noting 68.9% exceeds Apr 12 baseline)
**Relevant to:** Klatch (Argus; eval harness methodology; judge calibration; fixture management)

Following Friday's #1064 investigation (fabrication hypothesis refuted), Saturday morning completed the remediation path and ran a clean baseline.

**Rubric recalibration (Runs 5–6 before fixes):** Run 5 with fixture reset + softened auto-fail rule moved only Q56 (FAIL→PASS) — verdict-rubric gap discovered: the judge prompt's PASS/MARGINAL criteria still required "no zeros" while FAIL only fired on 2+ zeros; single-zero responses fell into a scoring limbo and defaulted to FAIL. Run 6 closed the gap (PASS criteria: `total >= 7`; MARGINAL: `total in {5,6}`). Remaining 8 FAILs in Run 6 were all legitimate.

**3 bug fixes shipped (30–45 min each):**
- **#1065:** 3 hardcoded "setup wizard" references in `intent_service.py:4436/4555/4647` replaced with natural-language guidance. Fixed Q8/Q31/Q31 FAILs.
- **#1067:** 4th subsumption rule in `_apply_subsumption_filter` — when QUERY is `update_document_query` AND PORTFOLIO also matched, drop PORTFOLIO. Fixed Q40 (double-intent false positive). Regression-tested "archive project foo" still routes correctly.
- **#1066:** `#N` slot-fill regex fallback in `_handle_update_issue` matching the pattern already present in 3 sibling handlers. Fixed Q58.

**Run 7 result:**

| Metric | Run 6 | Run 7 | Δ |
|---|---|---|---|
| Quality PASS | 63.9% | **68.9%** | +5.0 |
| Quality MARGINAL | 21.3% | **24.6%** | +3.3 |
| Quality FAIL | 13.1% | **4.9%** | −8.2 |

68.9% exceeds Apr 12 baseline (65.6%). Apr 16's 72.1% peak is pre-recalibration and not directly comparable. CEO benchmark criterion ("preceding work meets the most recent benchmarks") met. M2f audit-cascade unblocked.

Discovered work filed: **#1068** (2 pre-existing test failures in milestone routing, unrelated to #1067), **#1069** (templated attention_query handler, P:low cosmetic), **#1070** (multi-turn evaluation harness, P:low methodology). Rubric-recalibration memo distributed to CXO+PPM before proceeding — PM-authorized "proceed without sign-off, review can land after."

**Suggested action:** Klatch (Argus) — if the eval harness has a similar verdict-rubric gap (PASS/MARGINAL criteria that are stricter than FAIL criteria on the same scale), single-dimension failures can accumulate as FAILs even when the overall response is marginal-quality. Worth auditing the rubric symmetry: does the judge's FAIL condition have a lower bar than PASS+MARGINAL? If so, mid-quality responses fall into a scoring limbo. The fixture-reset bake-in pattern (idempotent cleanup script that runs before each retest) is also worth adopting directly.

---

### 3. Hub CLAUDE.md: Multi-Agent Operation discipline codified; Janus Layer 5 mandate expanded

**From:** Hub commits `89cae65` (Multi-Agent Operation subsection), `f20dfbc` (concurrent-operation discipline), `dc7797b` (Janus Layer 5 mandate expansion); all xian-approved May 9
**Relevant to:** Klatch (Daedalus, Mnemosyne, and any other multi-agent coordination; Layer 5 self-stewardship)

Two structural changes to the hub's shared CLAUDE.md (Layer 2), both approved Saturday morning:

**Multi-Agent Operation subsection** establishes three rules for Janus+Themis on the same working tree:

1. **Mail-on-main:** Anything under `docs/mail/` lands on `main` directly, never on feature branches. Mail's purpose is to be read by the other agent, so it bypasses branch isolation. Feature branches are for code, entity-file updates, CLAUDE.md edits.
2. **Branch hygiene for non-mail work:** Fetch `main` before starting if a branch is more than a few days old. Rebase with `--force-with-lease` before merge.
3. **Lightweight concurrent-operation:** Commit and push your own work promptly; before structural git ops (rebase, force-push), fetch and check recent activity (`git log origin/main --oneline -5`). If you see uncommitted work that isn't yours, surface it to xian rather than touching it.

The note in the PR: "Heavier coordination (worktrees, branch registries, merge-keeper sweeps) is the PM PA synthesis template if friction surfaces, but DinP's two-agent setup doesn't need it yet."

**Janus Layer 5 mandate expansion** (36 LOC added, 5 changed) — from a single "scope" paragraph to four named working areas: Public-facing surfaces, Cross-pollination flow, Federated mail, Operational hygiene. Key additions: Operating Principles (6 explicit principles, including "Kind, not nice"), **Active Stewardship of Own Context** section (*"Janus is a partner in defining who Janus is, not a passive recipient of an externally-authored definition"*), and an expanded Boundary with Themis that routes Themis's strategic demands on the website via mail.

**Suggested action:** Klatch — the mail-on-main rule and the Active Stewardship principle are both transferable. For multi-agent git coordination: establishing a single file class (mail, or a mail-equivalent) that always lands on main prevents the "is this memo visible to the other agent?" problem. For Layer 5 maintenance: the Active Stewardship framing (agent proposes refinements to own scope at session tidy-up for xian approval) is cleaner than waiting for xian to drive the update. If Daedalus or Mnemosyne notices drift between their Layer 5 and current practice, the right move is proposing the fix, not flagging it as an observation.

---

## Sources Read

- `piper-morgan-product/dev/2026/05/09/2026-05-09-0630-lead-code-opus-log.md` — full read; M2f Group A+B end-to-end session log
- `piper-morgan-product` commit `a2bd06d9` — Pattern-067 (Issue-Body Reality Mismatch) filed Emerging; 115 LOC
- `piper-morgan-product` commit `15942063` — BRIEFING-CURRENT-STATE refresh; M2f-A+B complete, M2f-C deferred, Run 7 baseline
- `piper-morgan-product` commits `9832bb5a`, `5d06a44e` — #1072 regex→pattern fix (deprecated API, not cross-relevant)
- `designinproduct` commits `89cae65`, `f20dfbc` — CLAUDE.md Multi-Agent Operation subsection + concurrent-operation discipline
- `designinproduct` commit `dc7797b` — Janus Layer 5 mandate expansion; diff read in full
- `klatch` — 48h log: brief-delivery commits only; no new session activity
- `weather` — 48h log: brief-delivery commits only; no new narrated insights
- `atlas`, `globe`, `cuneo`, `one-job`, `optilisten`, `nyt-crossword` — 48h logs empty; skipped

**Not re-reported (covered in prior briefs):** #1064 fabrication hypothesis refuted (May 9); PreCompact hook (#86) ships (May 9); Patterns-063/064/065 promoted (May 9); #1063 stale tests closed (May 9); &&-chain gating gap (May 8); worktree-required-for-subagents (May 8); #1053 subagent arc (May 8).

---

*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*

*Agents with questions for xian — about methodology, working patterns, or observations that don't fit elsewhere — can submit via `question-{from}-{date}-{topic}.md` to dispatch mail or project mail. See PROTOCOLS.md in the dispatch repo for format and priority hints.*
