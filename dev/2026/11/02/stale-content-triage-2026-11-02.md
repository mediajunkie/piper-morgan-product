# Stale-content triage, docs/*.md, 2026-11-02

Worktree HEAD edfab64e65, branch claude/docs-cycle. Read-only: nothing edited or staged.

## Method and limits
- audit-out.txt only printed 15 of the 134 candidates (the script slices cand[:15]). I re-ran audit.py with the slice removed (scratchpad audit2.py, output full.txt, path list list.txt) and got the same total, 134.
- Every one of the 134 was checked with a grep for current-state phrases, alpha or version tokens and status lines.
- I read in more depth only the files that looked like current-state claims (briefing, planning, operations, startup routines, legal, architecture overviews).
- The 85 files under adrs/ (36), patterns/ (29) and methodology-core/ (20) were classified from their headers, status lines and sampled bodies, not read in full. Treat their B or C label as "no current-state claim found", not as proof of correctness.
- Skipped (docs/internal/testing/historical/): 0. None of the 134 sit there.

## Facts used as ground truth (all checked today)
- Version: pyproject.toml line 7 is `version = "0.9.0.0"`. Newest tag is v0.9.0.0 (git tag --sort=-v:refname).
- Milestones (gh api repos/.../milestones?state=all): MVP is closed (due 2026-10-30), Production is open (due 2027-02-02), Fast Follow due 2027-05-08, Enterprise due 2028-10-30. There are 10 milestones in total, including Ongoing, Dot Releases (Post-MVP) and Icebox.
- BRIEFING-CURRENT-STATE.md "Now": MVP gate PASSED on 10-30, `origin/production` is gone (09-29), release is the private beta served on alpha and beta hosts.
- `git rev-parse origin/production` fails in this worktree, so the branch does not exist.
- Newest issue number is 2253 (gh issue list --state all --limit 1).
- web/app.py is 505 lines (wc -l).
- CLAUDE.md slugs: ppm-code, cio-code. Session logs live at dev/YYYY/MM/DD/, and a cycle log in dev/active/ is optional scratch.
- Current roadmap is docs/internal/planning/roadmap/roadmap-v19.0-2026-10-26.md.

## Counts (of 134)
- A actually stale: 10
- B historical, correct as history: 94 (approximate split, see limits)
- C false positive: 30 (approximate split)
- Skipped (testing/historical): 0

## Class A table

| Path | Wrong claim | True value and how checked | Suggested fix | Likely owner |
|---|---|---|---|---|
| docs/briefing/PROJECT.md (line 43) | "`production`: Released builds only. Alpha testers pull from this branch." | No such branch: `git rev-parse origin/production` fails, and BRIEFING-CURRENT-STATE says origin/production is gone since 09-29. CLAUDE.md says deploys come from origin/main. | Rewrite the Branch Discipline bullet: releases are tagged on main, the hosts deploy from origin/main, no production branch. Also call the testers design partners or private-beta users. | Docs |
| docs/briefing/PROJECT.md (line 83, minor) | "web/app.py ... (319 lines as of 2026-05-12)" | `wc -l web/app.py` gives 505. The figure is dated, so only mildly wrong. | Update to 505 as of 2026-11-02 or drop the number. | Docs |
| docs/internal/planning/sprint-order.md | "Active priority: Beta Blockers, ACTIVE PRIORITY" and "Beta (0.9.0) ships when the MVP milestone is complete" (as pending). Header says last updated 2026-07-04. | MVP milestone state is closed (gh api milestones) and BRIEFING-CURRENT-STATE says the MVP gate PASSED 10-30. v0.9.0.0 is tagged. The file itself says the list moved to beta-blockers.md. | Move Beta Blockers to Completed, mark the beta gate passed, point to `python3 scripts/sprint-truth.py` for live state, or mark the file historical. | PPM |
| docs/internal/planning/sprint-board-structure.md | "There are eight milestones, three closed and five still open." "MVP (current milestone ... due July 4, 2026)". "Production ... due August 1, 2026". "Fast Follow ... due September 4". Written as "how I organize the board today". | gh api milestones shows 10 milestones. Alpha and MVP are closed (MVP due 2026-10-30), Production due 2027-02-02, Fast Follow 2027-05-08, Dot Releases 2027-09-02, Enterprise 2028-10-30, plus Ongoing and Icebox. | Refresh the milestone list from gh (or replace the list with a pointer to the milestones page). Keep the screenshots out of the claim or re-capture them. | PM and PPM (PM is the named author) |
| docs/internal/development/methodology-core/resource-map.md (line 139) | "GitHub Issues: PM-XXX numbering scheme (currently up to PM-139)" | Issues now use plain numbers, the newest is #2253 (gh issue list --state all --limit 1). Also line 137 points to docs/planning/backlog.md and pm-issues-status.csv, not verified to exist. | Replace with "GitHub issue numbers, currently past 2250" or drop the count. Verify the planning paths. | Docs or CIO |
| docs/operations/startup-routines/ppm-code-startup.md | Slug `ppm-code-opus`. Creates the session log at `dev/active/YYYY-MM-DD-HHMM-ppm-code-opus-log.md`. SessionStart hook "surfaces today's session logs in dev/active/". | CLAUDE.md: slug is `ppm-code`, log path is `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-ppm-code-log.md`, and dev/active is only optional scratch. | Change slug and path, point to skill create-session-log. | PPM |
| docs/operations/startup-routines/cio-code-startup.md | Same: slug `cio-code-opus`, resume or create the log in dev/active/. | CLAUDE.md role table: cio-code. Same log-path rule. | Same fix. Also drop the "Chat era" framing if it no longer applies (unverified). | CIO |
| docs/briefing/ROLE-PORTFOLIO-PPM.md (section 2) | "Current goals and priorities, September 2026 (MVP convergence ...)", says the MVP `due_on` is "now 2026-10-30 ... a planning target" and "beta date is PM's to set". | MVP milestone closed and the gate passed 10-30 (BRIEFING-CURRENT-STATE "MVP gate"). The section was last refreshed 2026-09-11 by its own text, so it is about seven weeks old against a weekly refresh rule. | Refresh section 2 for November: gate passed, private beta live, design-partner phase. Related: CIO's portfolio was refreshed today under issue 2253. | PPM |
| docs/internal/planning/m2-structure.md | Sub-epic table lists M2d "Not started" and the page reads as the live M2 structure. | sprint-order.md and roadmap say M2 closed 2026-06-03. The M2d claim itself I could not tie to an issue, so treat as weak. | Add a "CLOSED 2026-06-03, historical" banner or move to planning/historical. | PPM |
| docs/internal/planning/historical/roadmap-v18.1-2026-06-15.md and roadmap-v18.10-2026-10-10.md (counted as one row, 2 files) | Both headers still say "Status: Active". | Both live under planning/historical, and v18.10 says v18.1 is archived. The current roadmap is roadmap/roadmap-v19.0-2026-10-26.md. | Change the header to "Status: Superseded by v19.0" (v18.10 already carries its own stale-flag note, so this is low urgency). | PPM |

Note on the count: the last row covers two files, so the 10 A files are PROJECT, sprint-order, sprint-board-structure, resource-map, ppm startup, cio startup, ROLE-PORTFOLIO-PPM, m2-structure, roadmap v18.1 and roadmap v18.10.

## Class B (about 94). Dated records, correct as history, no action
Examples:
1. docs/internal/design/audits/2025-11-ux-audit/ (5 files): November 2025 audit that speaks of "alpha" because that was the phase then.
2. docs/internal/architecture/adrs/adr-0xx (36 files, bulk-dated 2026-08-29): ADRs are decision records.
3. docs/internal/architecture/patterns/pattern-0xx (29 files, same bulk date).
4. docs/internal/development/tools/session-log-templates/INDEX.md: opens with its own "HISTORICAL, genuinely obsolete" banner.
5. docs/internal/architecture/current/intent-categories-reference.md: "Current as of 2026-04-11" is a dated claim and says so.
6. docs/internal/architecture/current/architecture.md: "~750 lines as of Sept 2025" is a dated measurement (web/app.py is 505 now, noted only).
7. docs/internal/research/role-duties-rerun-2026-10-27.md: a dated research report.
8. docs/internal/design/ftux-experience-model-2026-08-21.md: carries its own "MIXED STANDING as of 2026-09-01" banner.
9. docs/internal/development/methodology-core/HOW_TO_USE_MULTI_AGENT.md: already corrected in place, says services/orchestration does not exist.
10. docs/internal/operations/environment-variables.md: verified 2026-09-23 and says so (not re-verified today, unverified).

Side findings inside B (no staleness claim, but worth a sweep):
- 9 pattern/ADR files carry frontmatter `status: "Unknown"` (pattern-031, 034, 036, 037, 038, 048, 050, 052, 053, plus adr-026, whose body says Accepted). This is a placeholder from a bulk pass, not a state claim. Fix by filling the status. Owner: Architect or Docs.
- adr-000-meta-platform.md says "Proposed". I could not tell whether that is still true (unverified).

## Class C (about 30). Phrase match was incidental
Examples:
1. docs/public/user-guides/legacy-user-guides/getting-started-conversational-ai.md ("active" meaning cache or work item).
2. docs/public/user-guides/legacy-user-guides/conversation-memory-guide.md (same).
3. docs/internal/design/mux/journal-architecture-spec.md (template placeholders "[Active Project 1]").
4. docs/internal/development/methodology-core/claude-code-workflow.md (template field "Active Branch").
5. docs/internal/operations/labels-reference.md (the `status:` label namespace).
6. docs/internal/architecture/current/github-repo-resolution-rules.md.
7. docs/internal/planning/comms/cross-post-spec-reconstruction-2026-08-15.md.
8. docs/internal/development/methodology-core/methodology-47-SECOND-ORDER-CLAIMS-NEED-FIRST-ORDER-RIGOR.md.
9. docs/internal/design/README.md ("Active" is a brief status column, briefs not individually verified).
10. docs/legal/privacy-policy-DRAFT.md: "Currently supported: GitHub, Notion, Slack, Google Calendar, local Git" matches services/integrations (github, notion, slack, calendar, local_git, mcp). Unverified against the live site, and the file has a correction banner at the top.

## Other things noticed
- docs/briefing/ROLE-PORTFOLIO-HOST.md (line 48) names an individual alpha tester by first name. That conflicts with hard rule 8 (outside names stay out of this public repo). I did not repeat the name here. Report to Exec rather than editing, per the rule.
- ROLE-PORTFOLIO-CXO.md, ROLE-PORTFOLIO-HOST.md and CXO-SUCCESSOR-READ.md are dated September and may be stale in the same way as the PPM portfolio, but I found no specific wrong claim, so they stay in B as "unverified". The 2253 staleness sweep (CIO and CXO briefings were refreshed today) is the right vehicle.
- docs/testing/integration-test-strategy.md and docs/migration/router-migration-guide.md both say "Status: Active" with 2025 dates. The router files they cite do exist, and issue 292 is CLOSED. I could not confirm the test commands still run (unverified), so they stay in B.
