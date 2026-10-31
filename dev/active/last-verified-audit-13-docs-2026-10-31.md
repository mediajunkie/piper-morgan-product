# Verification of 13 docs stamped last_verified 2026-06-19 (checked 2026-10-31)

Method: read each doc in full, then ls / git grep / git log against the worktree at origin/main-merged HEAD (claude/docs-cycle). Not run: any `bd` command (bd is not installed in this shell), any pytest, any python import (no `python` on PATH here), any lsof/kill sequence. Last body edit per `git log -1 --format=%cs`.

Summary table

| Doc | Last body edit | Verdict |
|---|---|---|
| agent-protocols/README.md | 2026-08-29 | ACCURATE |
| agent-protocols/completion-discipline.md | 2026-10-14 | STALE (Pattern-046 section) |
| agent-protocols/debugging-protocol.md | 2026-06-19 | ACCURATE |
| agent-protocols/e2e-investigation-protocol.md | 2026-06-19 | ACCURATE |
| agent-protocols/git-workflow.md | 2026-06-19 | STALE |
| agent-protocols/issue-closure-protocol.md | 2026-06-19 | MINOR-DRIFT |
| briefing/BRIEFING-ESSENTIAL-AGENT.md | 2026-10-30 | MINOR-DRIFT |
| briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md | 2026-10-27 | MINOR-DRIFT |
| briefing/BRIEFING-ESSENTIAL-ETA.md | 2026-08-29 | MINOR-DRIFT |
| briefing/METHODOLOGY.md | 2026-08-29 | STALE (several sections) |
| briefing/README.md | 2026-06-19 | MINOR-DRIFT |
| briefing/ROLE-PORTFOLIO-EXEC.md | 2026-08-11 | STALE (priorities table, self-flagged) |
| briefing/ROLE-PORTFOLIO-FRAMEWORK.md | 2026-07-29 | MINOR-DRIFT |

---

## 1. docs/agent-protocols/README.md — ACCURATE

Checked:
- All five linked files exist in docs/agent-protocols/ (debugging-protocol, e2e-investigation-protocol, issue-closure-protocol, git-workflow, completion-discipline). Directory holds exactly these plus README.
- Patterns 045, 046, 047 exist as pattern-045-green-tests-red-user.md, pattern-046-beads-completion-discipline.md, pattern-047-time-lord-alert.md.
- `.claude/skills/`, `docs/briefing/` (PROJECT.md, BRIEFING-CURRENT-STATE.md both present), `docs/internal/architecture/patterns/` all exist.
- CLAUDE.md "More detail" table still points at git-workflow.md and completion-discipline.md, so "referenced from CLAUDE.md" holds.
- "Extracted 2026-01-22" is historical and not checkable. Not checked: the "~150-200 instructions" research claim.
Caveat: the README's one-line descriptions inherit the problems in completion-discipline and git-workflow below, but the README itself makes no false claim.

## 2. docs/agent-protocols/completion-discipline.md — STALE (Pattern-046 section, about half the doc)

Holds:
- Pattern-045 section: "705 unit tests" matches pattern-045 text (line 38). The MUST-NEVER rules match CLAUDE.md "STOP and ask" and "Done means" rules.
- Pattern-047 Time Lord Alert section is consistent with the pattern file and the Time Lord memory/briefings. discovered-work-capture skill exists and CLAUDE.md "Discovered work" line exists (line 1 of the Proactive Issue Creation bullet is accurate).
- scripts/bd-safe exists.

Wrong or unverifiable:
- Session Start Protocol runs `bd ready --json`, `bd list`, `bd status`. CLAUDE.md "Session start" never mentions bd or Beads. `bd` is not on PATH in this worktree. `.beads/` is untracked since commit "chore: Stop tracking .beads/ (local workflow tooling)" (2026-02-03) and does not exist in the worktree. I could not confirm whether bd is installed on Amber, so mark "unverified".
- "Before closing ANY epic: `bd list --parent <epic>`" and the Session End Protocol steps 1, 3, 4, 5 (`bd create`, `bd dep add`, `./scripts/bd-safe close`, `bd sync`, `bd list | grep`) depend on bd. Current closure path is `gh` plus skill close-issue-properly, and the current sign-off is the CLAUDE.md block (git status, git fetch origin main, git log --oneline origin/main..HEAD must be empty).
- Step 2 `pytest tests/` conflicts with the CLAUDE.md quick reference (`python -m pytest tests/unit/ -v`) only in scope, minor.
- "Add `@PM-approval-needed: <reason>`" is a convention I could not find in CLAUDE.md, unverified.
Suggested replacement for the Pattern-046 "Session Start Protocol" and "Session End Protocol" blocks: replace with a pointer, for example:
"Session start and end follow CLAUDE.md ("Session start" and "Sign-off"). Beads (`bd`) is local workflow tooling that is no longer tracked in git (2026-02-03). Use it only if your environment has it. Track work with `gh issue create` and close with skill `close-issue-properly`."
The epic check becomes: "`gh issue view <epic>` and read its task list or sub-issues."

## 3. docs/agent-protocols/debugging-protocol.md — ACCURATE

Whole doc read. It states no file paths, scripts or commands to resolve. Checked its rules against CLAUDE.md: "STOP and ask PM when tests fail", "PM decides what is critical", "Don't guess facts" all agree with the Test Failure Protocol and "The PM decides criticality, not you". Phase structure is generic method, nothing contradicts debugging-protocol references in CLAUDE.md table.

## 4. docs/agent-protocols/e2e-investigation-protocol.md — ACCURATE

Checked: `services/domain/models.py` exists. Template `docs/internal/development/testing/e2e-bug-investigation-report-template.md` exists. ADR dir and pattern library paths exist. The "wait for PM review before fixes" rule is consistent with CLAUDE.md. "Phase 2" naming is historical and not checkable.

## 5. docs/agent-protocols/git-workflow.md — STALE

Current rule (CLAUDE.md "Worktrees" and "Git, push, sign-off") is the opposite of this doc's central premise.
Wrong claims:
- "Never develop on `main`. Every session has an assigned feature branch ... Ends with session ID, example claude/ux-quick-wins-015W99...". Current: agents work in a stable worktree on `claude/{role}-cycle` (for example claude/docs-cycle), reused every session, with no session-ID suffix. The example branch name appears only in 2025-11 dev logs.
- "Push to YOUR branch only: `git push -u origin <your-assigned-branch>`". Current: "push finished units to main as you go: `git push origin HEAD:main`" and "Work not on origin/main is invisible".
- "403 errors on push to main are intentional" and "Session ID in branch proves authorization": these describe the Claude-on-the-web sandbox, not the current Amber flow. Unverified for web seats.
- Session Start (`git fetch origin <branch>` / `git checkout`) conflicts with CLAUDE.md: confirm you are in your worktree, `git fetch` and fast-forward, check `git rev-list --count HEAD..origin/main` is 0.
- "Branch checklist: ends with your session ID" is false for cohort worktrees.
- Missing entirely: hard rules about the shared checkout (never git checkout --, reset --hard, stash, clean there), the sign-off block, `scripts/sync-pm-local.sh`, and "stage in one call, commit in the next".
Still true: `./scripts/fix-newlines.sh` exists and is in CLAUDE.md quick reference. Prefer specific files over `git add .` agrees. `lsof` exists. The server port 8001 and `python main.py` agree with CLAUDE.md.
Not checked: whether `pkill -f "python main.py"` fails in practice.
Suggested fix: rewrite "Critical Rule", "Session Start", "Development Workflow", "Branch Checklist" and "Why This Matters" from CLAUDE.md "Worktrees" and "Git, push, sign-off". Minimum replacement for Critical Rule: "Never work in the shared checkout ~/Development/piper-morgan-product. Work in your worktree on `claude/{role}-cycle` and push finished units with `git push origin HEAD:main`. A Claude-on-the-web seat that is assigned a `claude/...-<session-id>` branch pushes only to that branch." Keep the Server Restart section as is.

## 6. docs/agent-protocols/issue-closure-protocol.md — MINOR-DRIFT

Checked and true:
- `.claude/hooks/issue-checkbox-lint.sh` exists (last edited 2026-10-14).
- Wired in `.claude/settings.json` under PostToolUse with matcher "Bash" (line 58). Confirmed.
- It reads recent commit message, regex for Closes/Fixes/Resolves, fetches body with `gh issue view`, warns, and recommends `gh issue edit N --body-file`. All match the script. It is warn-only.
- Closure order (description first, then comment, then close) matches skill close-issue-properly and CLAUDE.md "Close issues with skill close-issue-properly (description first, then comment, then close)".
- Pattern memory file `feedback_close_issue_properly_skill_recurring_miss` exists in the memory index. #1083 and #1070/#304/#1069 numbers not verified against GitHub.
Drift:
- The hook now only warns for OPEN issues (script lines 85-92, "Issue 1618 fix"). Doc says it warns for any referenced issue with unchecked boxes. Replacement after "Fetches each issue body via `gh issue view N --json body`": "Fetches each issue body and state via `gh issue view N --json body,state` and only warns for OPEN issues (issue 1618 fix)".
- Not mentioned: CLAUDE.md hard rule 5 (a commit message that pairs close/fix/resolve with `#N` closes issue N, write the number without `#` or add trailer `Auto-Close: intentional`), and `.claude/hooks/autoclose-guard.sh` which enforces it. Suggested added line under Tooling: "Rule 5 of CLAUDE.md hard rules governs accidental closes, guarded by `.claude/hooks/autoclose-guard.sh`."

## 7. docs/briefing/BRIEFING-ESSENTIAL-AGENT.md — MINOR-DRIFT

Checked and true: `scripts/fix-newlines.sh` and `docs/dev-tips/preventing-pre-commit-failures.md` exist. `knowledge/agent-prompt-template.md`, `knowledge/serena-briefing-queries.md`, `docs/internal/product/promises.yaml`, `docs/internal/architecture/ESSENCE.md` exist. ADR-038 (spatial) and ADR-034 (plugins) exist with those subjects. `services/plugins/plugin_interface.py`, `plugin_registry.py`, `list_plugins` method, `services/integrations/slack/slack_integration_router.py`, `config_service.py` exist. pytest.ini has `pythonpath = .`. Role slug `prog-code` matches CLAUDE.md and ROSTER.
Drift:
1. "Pre-commit hooks (trailing-whitespace, end-of-file-fixer, black, isort)". `.pre-commit-config.yaml` has ruff and ruff-format, no black or isort. Replace with: "(ruff, ruff-format, trailing-whitespace, end-of-file-fixer, and others)".
2. "7 active plugins (Slack, GitHub, Notion, Calendar, MCP, Spatial, Demo)". Only five `*_plugin.py` wrappers exist (slack, github, notion, calendar, demo). I found no MCP or Spatial plugin class. Replace with "5 plugin wrappers (Slack, GitHub, Notion, Calendar, Demo)". Runtime-active count not verified (no python on PATH).
3. "`Patterns` (63 patterns)" and "`ADRs` (61 decisions)". Now 75 numbered pattern files (pattern-001..075 range, ls shows 76 incl. numbering) and 80 numbered ADR files (adr-001..081). Replace with "(75 patterns)" and "(80 ADRs)" or drop counts.
4. "Testing requirements -> BRIEFING-METHODOLOGY": file is `docs/briefing/METHODOLOGY.md`. Replace with `docs/briefing/METHODOLOGY.md`.
5. Pre-commit routine uses `git add -u`. Repo has `.claude/hooks/pre-commit-broad-staging-warn.sh`, and CLAUDE.md says stage specific files in one call and commit in the next. Suggest "Step 2: Stage your specific files (`git add <paths>`) in its own call", "Step 3: commit in the next call".
6. Example output `Plugins: 4` and "PYTHONPATH=. python -m pytest" are illustrative, not checked. Verification command import `python -c` not run.
Footer "Last Updated: March 10, 2026" and `last_updated: 2026-03-10` are behind the 2026-10-30 body edit, adjust when editing.

## 8. docs/briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md — MINOR-DRIFT

Checked and true (all exist): dev/active/exec-attention-rollup-current.html, exec-standing-items.md, exec-open-items-tracker.md (marked superseded, correct), exec-carry-forward.md; scripts/aging-standing-items.sh, owed-scan.py, ppm-criteria-line.sh, sprint-truth.py, mail-send.sh, mail4.py, generate-production-map.py, briefing-pointer-check.sh; docs/internal/planning/production-map.html; promises.yaml; ESSENCE.md; methodology-00-EXCELLENCE-FLYWHEEL.md; docs/internal/planning/roadmap/roadmap.md (header says v19.1, matches); docs/internal/planning/current/vision.md; docs/internal/development/weekly-ship-process-guide.md; docs/public/comms/drafts/; docs/briefs/cross-pollination/current.md; skill cohort-attention-rollup, duty-cycle-tick. Role slug `exec` and "Chief of Staff (Exec)" match ROSTER. "Never CoS" per ROSTER: the doc uses "CoS" in prose ("The CoS<->Comms axis") which conflicts with ROSTER's "never CoS per PM directive May 15". Issue numbers #2157-#2162, #2179 not verified against GitHub (the #2157 mention does appear in docs/internal/planning).
Drift:
1. Migration checklist pointer `dev/active/memo-host-migration-checklist-2026-04-22.md` does not exist (appears twice: Migration Handoff Review Pattern and Progressive Loading). It is now `dev/2026/04/22/memo-host-migration-checklist-2026-04-22.md`, and the maintained checklist is `docs/internal/operations/migration-checklist.md`. Replace both with those.
2. "Mailbox discipline ... CLAUDE.md 'Mailbox Discipline' section" and "Per-memo commit-and-push norm ... codified in CLAUDE.md" and Environment table "Send mail: Write directly to mailboxes/[role]/inbox/ (commit on main)". CLAUDE.md has a "Mail" section now with the opposite instruction: do not `git add` or commit mailbox files, send with `scripts/mail-send.sh "mail({role}): {subject}" <paths>`; mail to external agents uses `scripts/mail-send-external.sh`. Replace the table row with: "Send mail to other roles | Write memo, cc copies and sent mirror under `mailboxes/`, then `scripts/mail-send.sh` (CLAUDE.md "Mail")". Replace reference text `CLAUDE.md "Mailbox Discipline" section` with `CLAUDE.md "Mail" section and docs/internal/operations/branch-worktree-mailbox-discipline.md`.
3. "`check-branch.sh` hook enforces" mailbox-on-main: `.claude/hooks/check-branch.sh` exists, enforcement not re-tested.
4. Prose "CoS" (several places) vs ROSTER rule: change to "Exec".
5. Standing text in "Session Startup Routine" step 1 "xpoll brief location" fine. "Migration handoff review" is already marked retired in the top block, but the older section still lists it as a Key Function: cosmetic.
The top 2026-10-13 and 2026-10-26 blocks are current and match scripts on disk.

## 9. docs/briefing/BRIEFING-ESSENTIAL-ETA.md — MINOR-DRIFT

Checked and true: slug `test` matches ROSTER (Tier 3, Dormant) and CLAUDE.md (`test-code`). `docs/internal/development/methodology-core/` exists (72 entries, "20+" is true). `docs/omnibus-logs/` exists. Pattern catalog path exists. BRIEFING-CURRENT-STATE.md exists. ETA logs exist under dev/2026/03/12 with `test` slug. Reference to Lead Dev, CXO, CIO roles are valid roster roles.
Drift:
- "Session log naming: `YYYY-MM-DD-HHMM-test-{tool}-{model}-log.md`". Current convention (ROSTER "Session log naming", CLAUDE.md): `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{slug}-log.md` with slug `test-code`, model recorded in the log header, not in the filename. Replace with: "`dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-test-code-log.md` (model goes in the log header)". The March 2026 logs with `-haiku`/`-opus` suffixes are historical.
- "ETA logs use `test` slug" in References: fine, but align to `test-code`.
- No `mailboxes/test/` directory exists and mailboxes/DIRECTORY.md has no `test` row: if ETA is reactivated it has no inbox. Note rather than error.
- Continuity quiz "Ask PM or check ETA session logs" cannot be verified.

## 10. docs/briefing/METHODOLOGY.md — STALE (several sections)

Checked and true: docs/NAVIGATION.md exists. methodology-core/INDEX.md exists. methodology-02-AGENT-COORDINATION.md, pattern-061, adr-035-inchworm-protocol, pattern-062 exist. Methodology-20 (Omnibus), 24 (Branch-or-Anchor), 25 (Workstream Review Cadence) exist with those subjects. anti-pattern-index.md says "Total Indexed: 51 anti-patterns" and has P-17, so that line holds. Patterns 066-069 exist with the described titles. Excellence Flywheel practice names in the later "Excellence Flywheel" section (Verify Before Building, Test What Matters, Coordinate Through Structure, Track to Completion, Audit the Composition) match the canonical doc headings. 00-START-HERE-LEAD-DEV exists at docs/00-START-HERE-LEAD-DEV.md.
Wrong:
1. "Methodology-23 close-issue-properly". methodology-23 is M1-INNOVATIONS. No methodology-core file is titled close-issue-properly. Replace with "Methodology-23 M1 Innovations" and point close-issue-properly at skill `.claude/skills/close-issue-properly/`.
2. "pattern catalog (75 patterns as of 2026-06-19 ...)" — numbered patterns now run to pattern-075 (so 75 is still right by count) but the date is the bulk-stamp date. Fine to keep, drop the date.
3. "Excellence Flywheel v2.0 — reformulated 2026-04-17 ... Practices (5 currently: TDD/Verify-before-build/Audit-cascade/Branch-or-anchor/Audit the composition)". Canonical doc is v3.0 (2026-09-11), Layer 2 re-derived, practices are the five named in METHODOLOGY's own later section. The pointer index contradicts the doc's later section. Also the later section says "v2.0 three-layer reformulation, Apr 2026". Replace both with "v3.0 (2026-09-11)" and the five v3.0 practice names. (Doc also gives two different dates, 04-17 and Apr 26, for v2.0.)
4. Session Log Standard v2: format `YYYY-MM-DD-HHMM-[role]-[product]-log.md` with `opus/sonnet/cursor` products and slugs exec/arch/lead/prog. Current: `YYYY-MM-DD-HHMM-{slug}-log.md` where slug is e.g. `docs-code`, `prog-code`, and model goes in the header (ROSTER "Session log naming"). Replace the Format, Standard Slugs, Examples blocks accordingly, and the Creation Command with skill `create-session-log`.
5. Framework paths `docs/internal/development/tools/session-log-framework.md` and `session-log-instructions.md` do not exist (also written as `User/xian/Development/piper-morgan/...`). Also `/Users/xian/Development/piper-morgan/dev/YYYY/MM/DD/`: repo path is now piper-morgan-product and agents use their worktree. Replace with "skill `create-session-log`" and "your worktree's `dev/YYYY/MM/DD/`".
6. "Documentation location priority: Artifacts, then Filesystem, then Sandbox ... Filesystem not available in standard Claude.ai". Chat-era guidance, no cohort role is in claude.ai now (feedback_chat_briefings_reminder). Mark as historical or delete.
7. "GitHub Progress Discipline: PM validates checkboxes, include '(PM will validate)'": conflicts with the current close-issue-properly flow where the closing agent updates description checkboxes and PM does not check boxes. Unverified whether PM still wants this; flag to PM.
8. "Every PR links to issue: `Closes #180`" and `git commit -m "fix: ... (#180)"`: fine for PR bodies, but CLAUDE.md hard rule 5 means any commit message pairing close/fix/resolve with `#N` closes the issue. Add "In commit messages write the number without `#` when you do not intend to close."
9. "Session Satisfaction Protocol: MANDATORY" and "Lead Developer skips 00-START-HERE-LEAD-DEV": CLAUDE.md has no satisfaction step and Lead Dev's entry is BRIEFING-ESSENTIAL-LEAD-DEV.md. Unverified, probably historical.
10. Curl example `http://localhost:8001/api/intent`: routes use `/api/v1/` per CLAUDE.md. Replace with `/api/v1/intent` if that route exists (not verified).
11. Multi-agent section names Cursor and "Both agents" cross-validation: no cursor role in ROSTER/CLAUDE.md. Historical.

## 11. docs/briefing/README.md — MINOR-DRIFT

Checked: BRIEFING-CURRENT-STATE.md, METHODOLOGY.md, PROJECT.md exist. Agent, Architect, Chief of Staff, CIO, Comms, CXO, HOST, Lead Dev, PPM briefings exist. `../../README.md` exists (not individually confirmed, root README is standard).
Drift: Essential Role Briefings list omits BRIEFING-ESSENTIAL-DOCS.md, BRIEFING-ESSENTIAL-WEB.md, BRIEFING-ESSENTIAL-ETA.md, BRIEFING-piper-alpha.md, and the directory has ROSTER.md, TEAM-IN-XIANS-WORDS.md, CXO-SUCCESSOR-READ.md, 12 ROLE-PORTFOLIO-*.md files. The "Overview" is boilerplate. Replacement lines:
"- **[Docs](BRIEFING-ESSENTIAL-DOCS.md)** | **[Web](BRIEFING-ESSENTIAL-WEB.md)** | **[Piper Alpha](BRIEFING-piper-alpha.md)** | **[ETA](BRIEFING-ESSENTIAL-ETA.md)**"
"- **[Roster](ROSTER.md)** - roles, tiers and slugs. **[Role portfolios](ROLE-PORTFOLIO-FRAMEWORK.md)** - ROLE-PORTFOLIO-{ROLE}.md files."
Body footer says "Last Updated: March 3, 2026", so the page predates all of these additions.

## 12. docs/briefing/ROLE-PORTFOLIO-EXEC.md — STALE (priorities and status)

Checked and true: framework path docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md exists. role_slug exec matches ROSTER. skill cohort-attention-rollup exists. Duty cycle, freeze-watcher (memos from 2026-10-14 and 10-16 show freeze watchdog work continues), and mailbox sections are conceptually consistent with CLAUDE.md and the Chief-of-Staff briefing. Purpose, Seams and Consent-gradient sections are role-design statements, not checkable facts, and read as still sound.
Stale:
- The doc itself carries a 2026-08-11 STALE banner on the Priorities table (status dated 2026-06-19, now about 134 days old). Not refreshed since.
- "Role-portfolio wave: 1/7 main-cohort filed (Comms), 8/8 target": 12 ROLE-PORTFOLIO-*.md files exist now.
- "Run the duty cycle ... the launchd freeze-watcher is the backstop" and "bridge mechanics (now push-to-ref)": mail mechanics are now `scripts/mail-send.sh` v3 and `mail4.py` v4 per the Chief-of-Staff briefing. Claim "push-to-ref live" not re-verified.
- Frontmatter status "v0.1 — filed for HOST 5-rule review" and the footer "Filed 2026-06-19" are history. Also says `last_verified above moves every time I touch it`, but the stamp is the bulk stamp, which is exactly what this check shows is untrue.
- "Eleven-plus agents" consistent with ROSTER (7+4 plus Tier 3).
Action: Exec must refresh Priorities (the Chief-of-Staff briefing blocks dated 2026-10-13 and 2026-10-26 show the current priorities: attention rollup, production plan, Readiness lane). Docs cannot fabricate this.

## 13. docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md — MINOR-DRIFT

Checked and true: source_memo `mailboxes/exec/read/memo-host-to-exec-cc-pm-role-portfolio-trust-framework-v0.1-2026-06-11.md` exists. Worked examples ROLE-PORTFOLIO-HOST.md, LEAD-DEV.md, CIO.md exist. `BRIEFING-ESSENTIAL-{ROLE}.md` and `ROLE-PORTFOLIO-{ROLE}.md` sibling pattern holds (12 portfolios, 13 briefings). The 2026-07-29 Amendment (refresh through the current date) is internally consistent.
Drift:
- Rule 5 and "Surface architecture" claim the weekly review "keeps the doc current by construction" and "self-refreshes". Evidence contradicts: ROLE-PORTFOLIO-HOST.md's own `refresh_discipline` frontmatter says this "was never a mechanism" and it lapsed 2026-09-11 to 2026-10-02 across three reviews, and the Exec portfolio's priorities are 134 days stale. Add after Rule 5's final sentence: "Status as of 2026-10-31: this has not held in practice. A check exists for some portfolios (CXO's check-refresh-promises.py, see ROLE-PORTFOLIO-HOST.md `refresh_discipline`), but lapses were recorded 2026-09 and ROLE-PORTFOLIO-EXEC.md Priorities is stale. Treat currency as a mechanism to verify, not a given." Not verified: whether check-refresh-promises.py exists (I did not search for it).
- Worked examples list only three of twelve portfolios. Optional: add pointer to the rest.
- Status says "RATIFIED ... v0.1", ratified 2026-06-14, unverifiable here.

---

## Cross-cutting notes

- Of 13, only 4 can honestly be re-stamped as verified now: agent-protocols README, debugging-protocol, e2e-investigation-protocol (ACCURATE). Everything else needs a body edit before the stamp is bumped, which is what check-last-verified-drift.py (issue 1726) is meant to enforce.
- Highest-value fixes: git-workflow.md (contradicts CLAUDE.md on where to push), completion-discipline.md Pattern-046 block (bd commands), METHODOLOGY.md session-log standard and Flywheel version, Chief-of-Staff briefing mail instructions.
- Not checked anywhere: GitHub issue numbers (#1083, #2157-#2162, #2179 and others), runtime plugin counts, whether `bd` exists on the Amber host.
