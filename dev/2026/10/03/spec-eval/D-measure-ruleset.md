# D-measure: instrumenting the ruleset (H2, H1b/M1b.1)

Snapshot a191856 (read from the scratch worktree `/home/user/audit-wt`, which is that commit, detached). Measurement only. Pre-registered definitions are in `preregistration.md` (H2: M2.1-M2.4; H1b: M1b.1). Scripts and CSVs are in `metrics/D-*`.

Method notes that apply everywhere: tokens = UTF-8 characters / 4 (the pre-registered approximation; real tokenizer counts will differ, typically by +/-15%). "Auto-loaded or protocol-mandated" is read off CLAUDE.md "Session Start Protocol" and "Progressive Loading" plus each briefing's own "read first" lines. I did not observe a live session start, so what an agent actually reads is **unverified**; the numbers are the load the written protocol asks for.

## Verdicts (pre-registered rules applied literally)

| Test | Rule | Measured | Verdict |
|---|---|---|---|
| H2 | Supported if M2.1 >= 20k **and** two of: M2.2 >= 15, M2.3 >= 40%, M2.4 >= 5 | M2.1 = 59.3k-64.4k (all 13 roles); M2.2 = 50 items (>= 15, met); M2.3 = 10.7% (strict) / 14.4% (broad) of lines (**not met** by lines; 39.8% / 49.5% by characters, post-hoc); M2.4 = 5 firm strictly-marked rules (6 counting one arguable; >= 5, met) | **Supported** (M2.1 plus M2.2 plus M2.4). The M2.3 line-share criterion is not met, and the verdict does not depend on it. |
| H2 refuted-if | M2.1 < 12k and M2.2 < 5 | neither | not refuted |
| H1b M1b.1 clause | "per-role session-start load where the role-specific share is < 25%" | role-specific share 2.2%-10.0% (strict base) for 13/13 roles; 12/13 in the widest variant (Comms 25.6%); 11/13 if BRIEFING-CURRENT-STATE is not actually read (PA 26.9%, CXO 25.2% exceed) | **Clause holds** under the pre-registered load definition. H1b overall needs any two clauses; M1b.2 and M1b.3 are other workstreams'. |

## M2.1: session-start load per role (D-1)

Files: `metrics/D-m21.py`, `D-m21-per-role.csv`, `D-m1b1-shared.csv`, `D-m1b1-role-specific-share.csv`, `D-m1b1-sensitivity.txt`, `D-corpus-inventory.txt`.

Components (tokens, chars/4): CLAUDE.md 16,258 (65,534 bytes, 745 lines, no `@` imports); BRIEFING-CURRENT-STATE 40,461 (163 KB, 716 lines); cross-pollination `current.md` 1,167; session-start hook output 107 (measured: ran `bash .claude/hooks/session-start.sh` in the detached worktree, 429 bytes; the source budget is 500 characters and the hook has 11 sections, so output is truncated by design); duty-cycle-tick skill 19,916 (80 KB; the largest of 35 skills; counted only for cycling roles, 11 of 13 are in `dev/active/duty-cycle-registry.tsv`; Coding Agent and ETA have no cron). The 35 skill frontmatter blocks add about 3.7k tokens to every session (system prompt skill list), not included below.

| Role | Briefing | Base (CLAUDE.md + briefing + CURRENT-STATE + xpoll + hook) | + create-session-log and check-mailbox skills + briefing-mandated extras | + duty-cycle-tick | Role-specific share (base) |
|---|---|---|---|---|---|
| Lead Dev | 2,714 | 60,708 | 64,289 | 84,206 | 4.5% |
| Piper Alpha | 6,442 | 64,436 | 68,017 | 87,934 | 10.0% |
| Chief Architect | 4,476 | 62,470 | 66,051 | 85,967 | 7.2% |
| Exec | 4,751 | 62,745 | 66,326 | 86,243 | 7.6% |
| CXO | 5,920 | 63,914 | 67,495 | 87,411 | 9.3% |
| CIO | 4,607 | 62,601 | 66,182 | 86,098 | 7.4% |
| PPM | 5,658 | 63,652 | 67,233 | 87,149 | 8.9% |
| HOST | 3,247 | 61,241 | 64,822 | 84,738 | 5.3% |
| Comms | 3,046 | 61,041 | 75,677 (3 required guides, +11,056) | 95,594 | 5.0% |
| Docs | 2,928 | 60,922 | 68,331 (handoff doc, +3,828) | 88,247 | 4.8% |
| Web | 2,322 | 60,317 | 63,897 | 83,814 | 3.9% |
| Coding Agent | 1,352 | 59,346 | 62,927 | 62,927 | 2.3% |
| ETA (dormant) | 1,331 | 59,325 | 62,906 | 62,906 | 2.2% |

Finding D-1. layer: static (protocol as written) + one run (hook). denominator: 13/13 roles in the CLAUDE.md role table; 11/11 cycling roles for the tick skill. confidence: high on sizes, med on whether agents read the files in full (unverified). Typical role loads about 62k tokens at session start by the written protocol, 84k-96k at a cycling fire. Excluding BRIEFING-CURRENT-STATE (the file's own banner says to use Serena queries rather than read it, defect C23) it is 18.9k-24.0k: 11 of 13 roles are still >= 20k. Implication: the 20k bar is cleared however CURRENT-STATE is treated; but one file, CURRENT-STATE, is 65% of the base load, so it is the single largest lever.

### M1b.1: shared reading (D-2)

| Document | Roles loading | Tokens | Share of all-role load (13 roles) |
|---|---|---|---|
| BRIEFING-CURRENT-STATE | 13 | 40,461 | 48.6% |
| duty-cycle-tick SKILL | 11 | 19,916 | 20.2% |
| CLAUDE.md | 13 | 16,258 | 19.5% |
| create-session-log skill | 13 | 2,605 | 3.1% |
| cross-pollination current.md | 13 | 1,167 | 1.4% |
| check-mailbox skill | 13 | 975 | 1.2% |
| all 13 role briefings plus 4 mandated extras (each 1 role) | 1 | 1,331-11,056 each | about 6% together |

Finding D-2. About 94% of aggregate session-start tokens are documents every (or nearly every) role loads. Role-specific share: 2.2%-10.0% (base), 2.1%-14.8% (including startup skills, tick skill, mandated extras; Comms hits 25.6% only under the narrowest "briefing plus extras over a smaller denominator" variant E in `D-m1b1-sensitivity.txt`). Unobservable: whether roles also read ROLE-PORTFOLIO-* (31 briefing files total, 138.9k tokens; only 13 are counted) because the protocol does not mandate them.

## M2.2: ruleset defects (D-3)

Files: `metrics/D-m22-defects.csv` (50 rows with location and source), `D-paths.py`/`D-paths.csv` (my path check), `metrics/D-prompt-audit/` (built-in audit).

**Path check (mine, scripted).** 629 distinct (file, path) mentions extracted from CLAUDE.md, 31 briefing files and 35 SKILL.md files; tested for existence at the snapshot. 87 not found; after manual triage the genuine stale references are listed below (the rest were templates, truncated tokens like `docs/operations/duty-cycle` for a path containing a space, cross-repo paths such as the website's `scripts/publish-cli.js`, or optional-by-design files). CLAUDE.md itself: 3 not found, 0 genuine (`config/PIPER.user.md` is documented as legitimately absent; `config/source` and `mailboxes/xian` are prose and a path with a space). The line-qualified pointer `services/config/llm_config_service.py:213` exists as a file but, per the built-in audit, points into a docstring.

**Built-in baseline.** `claude -p "/checkup prompt-audit" --permission-mode acceptEdits` ran headless in the scratch worktree (CLI 2.1.288, subscription auth, no API key set). The slash command resolved to the bundled prompt-audit guide (copied to `metrics/D-prompt-audit/bundled-prompt-audit-guide.md`). It exited 0 after about 7 minutes using six Sonnet sub-reviewers, **wrote no files** (no PROMPT_AUDIT.md, no patch; it presents the diff inline), and edited nothing. Its report is saved verbatim as `PROMPT_AUDIT-report.md`; the inline diff as `PROMPT_AUDIT-proposed-diff.md`; stdout/stderr as `headless-*.txt`. The only warning was that the workspace was not trusted, so 32 `permissions.allow` entries in `.claude/settings.json` were ignored (no effect on a read-only audit). By instruction it did not read settings files, `~/.claude`, or ancestor CLAUDE.md files. It reports Group 1 (dated text, pressure language) 14 findings and Group 2 (brittle config) about 60. It self-verified every "High" finding with `git blame` and caught one wrong reviewer claim.

**Merged, deduplicated count: 50 items.** By source: 32 prompt-audit only, 14 mine only, 4 both. By category: 23 contradictions, 22 stale references/specifics, 5 superseded-but-present groups. Its "about 60" is in unmerged findings; my merge collapses same-location items and groups the long tail (row P5 bundles 7 medium items; row S10 bundles 8 skill names), so 50 is conservative.

Findings that bear most on the guiding question (mine, not in the built-in audit):

- C20: CLAUDE.md:29 says "7 leadership + 3 staff"; ROSTER.md v1.1 lists Staff as 4 roles (Web retiered 2026-08-05).
- C22: CLAUDE.md:605 cites the PreCompact hook as a safety net that fired; `.claude/settings.json:67` has `"PreCompact": []`. The script is registered only in the Amber user-level mirror (`docs/internal/operations/amber-userlevel-hooks-mirror.json`), outside the repo, so it cannot be verified from the repo. Consistent with CLAUDE.md's own "a safety net you haven't seen fire is a claim".
- P2: 3 of 13 hook scripts are registered nowhere (`PROBE-userpromptsubmit.sh`, `post-commit.sh` (DISARMED 2026-09-21 per its own header), `pre-commit-ruff-warn.sh`); 5 of 13 are unregistered in the project settings (2 more live only in the user-level mirror).
- C25: `.claude/settings.json` carries `Edit(src/**)` (no `src/` directory), `PYTHONPATH=/default/path` (a placeholder), and Desktop-only `Read(//Users/xian/...)` allows; `Bash(git stash:*)` is in the allow list while the HARD RULE forbids stash in the main checkout.
- C23: protocol mandates loading CURRENT-STATE (40k tokens) whose own banner redirects to Serena.
- S15-S20: six briefing pointers to nonexistent files (BRIEFING-METHODOLOGY.md, BRIEFING-ESSENTIAL-PA.md, three path/name drifts, `docs/decisions.log`).

Finding D-3. layer: static + built-in tool run. denominator: CLAUDE.md, 31 briefings and 35 skills for paths (629 mentions); 41 instruction files for the built-in audit (not settings, not `~/.claude`). confidence: high for items I verified (path existence, hook registration), med for audit-only items (it self-verified the High ones; Medium/Low not independently re-verified by me). Implication: most defects sit in skills and briefings, not in CLAUDE.md, whose own path hygiene is good; but CLAUDE.md contains the contradictions agents hit first (C1-C5).

## M2.3: narrative share of CLAUDE.md (D-4)

Files: `metrics/D-m23.py`, `D-m23-lines.csv` (all 745 lines), `D-m23-spot50.csv`.

Rule (per line, first match wins; written into the script): FORMAT = blank, heading, horizontal rule, code fence, table separator, bare quote marker. RATIONALE/HISTORY = the line contains a calendar date or an incident/history marker (incident, root-caus, diagnos, ratified, PM-ruled/directive/mandated/approved, found, learned, was/were, previously, lost, wiped, corrected, investigat, surfaced...); the "broad" variant also counts explanatory markers (because, why, so that, principle, failure mode, antipattern...). INSTRUCTION = everything else, including code lines and pointer tables.

| Variant | format | instruction | rationale | rationale / 745 lines | rationale / non-format lines | rationale share of characters |
|---|---|---|---|---|---|---|
| strict | 305 | 360 | 80 | **10.7%** | 18.2% | 39.8% |
| broad | 305 | 333 | 107 | **14.4%** | 24.3% | 49.5% |

Spot check: 50 random non-blank lines (seed 7) hand-labelled against the same rule: 44/50 (88%) agree with strict, 45/50 (90%) with broad. Disagreements were balanced (3 over-called as rationale because a date appeared in an instruction; 3 under-called, e.g. a reassurance line and a status fragment). My hand labels are in the `hand` column of `D-m23-spot50.csv`.

Finding D-4. layer: static. denominator: 745/745 lines. confidence: med. By the pre-registered unit (lines) the narrative share is 11-14%, **below the 40% bar**. Rationale lines are long, so by characters it is 40-50%, and a line-level classifier undercounts rationale embedded in instruction lines (long parenthetical incident accounts). The auditor also flags incident parentheticals at lines 241-243, 254, 256, 313, 641. The existing `claude-md-history.log` shows the project is already extracting narrative (extractions #1-#7, 2026-09-22), so the share is falling. Implication: "CLAUDE.md is mostly history" is not supported by line count; it is half the text by weight.

## M2.4: rules that don't hold (D-5)

Rules carrying HARD/CRITICAL/NEVER/MANDATORY/NON-NEGOTIABLE/STOP/warning-sign markers (counts of marker lines in CLAUDE.md: warning-sign 17, STOP 9, NEVER 4, MANDATORY 3, HARD 2, CRITICAL 2, NON-NEGOTIABLE 1). "Violated again" = an incident or measured lapse dated after the rule was first written, from `git log -S` first-add date (CLAUDE.md history), `claude-md-history.log`, CLAUDE.md's own dated incident text, and measured repo state.

| # | Rule (marker) | First written | Later violation, with source | Counted |
|---|---|---|---|---|
| 1 | Never destructive git in PM's main checkout (HARD RULE, NEVER) | 2026-06-21 | 2026-08-08 Arch ran `git checkout HEAD -- <2 files>`, scope-perfect, destroying the #1490 refix; `claude-md-history.log` lines 199-228 (extraction #6). Plus 2026-07-05 `docker volume rm` attempt and Projects v2 wipe (rule 6 below) | yes |
| 2 | Session log maintenance (NON-NEGOTIABLE) | 2026-04-19 | CLAUDE.md:294: six of nine cycling roles lost durable entries in a June 2026 audit. Counter-evidence: Sept 2026 file-existence coverage 322/330 role-days = 97.6% (script run this session, 11 cycling roles x 30 days); coverage is existence, not freshness | yes, with note: rule currently largely holds |
| 3 | BRIEFING-CURRENT-STATE refresh (MANDATORY) | 2026-04-29 | git: one gap > 7 days (2026-08-12 to 2026-08-24, 12 days) among 65 commit-days since 2026-04-22; CLAUDE.md:141 calls the prior implicit pattern "failing" | yes |
| 4 | Defer only with a NAMED TRIGGER (warning sign) | 2026-07-30 | CLAUDE.md:343 "keeps getting ignored"; 2026-08-31 three unblocked CIO items sat 3.5 months (self-reported) | yes |
| 5 | A worktree synced earlier is not synced now (warning sign) | 2026-08-27 (git -S) | the rule was written the same day as its triggering incident (Docs, 33 commits behind), so it is origin, not a repeat | **no** |
| 6 | Pause before irreversible actions (warning sign) | 2026-07-06 (git -S) | 2026-08-08 incident (rule 1) occurred after it, though whether it breaches this rule's wording is arguable; 2026-06-27 and 07-05 (x2) are the incidents it was written from | arguable |
| 7 | STOP: tests fail for any reason, escalate (STOP condition 2) | 2025-09-26 (git -S) | `Tests` workflow red on main, 0 successes in the last 100 runs, since 2026-09-20; staging deploys on every push anyway (B1, B5) | yes |
| 8 | Dispatch tier: state it (PM ruling, no marker) | 2026-09-14 | 2026-09-20 check: one dispatch stated tier, two did not (CLAUDE.md:415) | unmarked, not in the 6 |
| 9 | Auto-close negation (no marker) | 2026-07-14 | 2026-08 #1677, and 2026-08-29 PPM log line 52 cites a repeat of the documented gotcha; mechanism since added (#1691) | unmarked, not in the 6 |
| 10 | cc PM only on (a)/(b)/(c) (PM-ruled, no marker) | 2026-09-11 | memos in `mailboxes/xian (ceo)` by filename date: 477 in the 14 days before the ruling, 571 in the 14 days after (does not distinguish cc from addressed-to-PM) | unmarked, not in the 6 |

Finding D-5. layer: git-history + record + CI-history. denominator: about 10 rules examined of the roughly 25 marker lines in CLAUDE.md (I did not trace every marked line; rules without a dated incident in CLAUDE.md or the history log were not scored, so the true count is a lower bound for the examined set and unknown for the rest). Strictly marked rules with a violation dated after the rule's first-add commit: **5 firm** (rows 1, 2, 3, 4, 7) plus 1 arguable (row 6); >= 5 as pre-registered, so met, but with no margin if row 2 (now largely holding) is discounted. confidence: med. Several entries are self-reported incidents quoted from CLAUDE.md itself, which I could not independently reproduce. Implication: the failure mode CLAUDE.md names for itself is correct: prose rules decay unless a mechanism backs them, and the document says so.

## Enforcement inventory (D-6)

Legend: M = mechanized (script/hook/CI that blocks or fails); A = advisory (hook or CI that warns/reminds, bypassable); P = prose only. Layer: static plus reading hook/CI sources; hook firing was **not** observed live (Claude Code mods need CLI >= 2.1.287 and can hold or rewrite a tool call, which would convert A and P rules to M, but none is configured in this repo; the PreToolUse hooks here can block by exit code).

| Rule | Class | Mechanism and gap |
|---|---|---|
| Never use `/api/` without `/api/v1` | M (partial) | `scripts/check-api-versioning.py` exists; no `.github/workflows` file calls it (unverified elsewhere) |
| No new `elif intent.action` chain | M | `TestPreFloorDispatchSiteRatchet` (`MAX_DISPATCH_SITES = 0`) in `architecture-enforcement.yml` path; CI Tests currently red (B1) |
| No extraction-by-regex growth | M | `TestExtractionPatternRatchet` |
| Auto-close keyword + `#N` | M | `check_autoclose_keywords.py` via `mail-send.sh` and PreToolUse `autoclose-guard.sh`; not in CI |
| Bearer credentials in repo | M | `mailbox_bearer_lint.py` in `lint.yml` |
| Mail lands on main | M (send path) + A (commit path) | `mail-send.sh` uses commit-tree; `check-branch.sh` is advisory and CLAUDE.md says compound `git add && git commit` is ungated |
| Never destructive git in main checkout | P | no hook; `.claude/settings.json` allows `git stash:*`; deny list is only `.env*` and `secrets/**` |
| Diff before `git checkout <ref> -- <path>` | P | none |
| Session log maintenance | A | `log-maintenance-reminder.sh` (every 15 Bash calls); duty-cycle registry/watchdog for liveness |
| Briefing freshness | A | `session-start.sh` STALE line; `weekly-docs-audit.yml` |
| Context pressure | A | `context-usage-reminder.sh` |
| Sign-off pushes to origin/main | A + P | PreCompact hook (user-level, not in repo); Docs' merge-keeper sweep (script); checklist is prose |
| Cron/duty-cycle liveness | M (detect) | `duty-cycle-watchdog.sh`, registry, `ci-liveness.yml`, `role-health-check.yml` (reminder only) |
| Standing-item aging | M (detect) | `scripts/aging-standing-items.sh` (+ test); who runs it is unverified |
| Dispatch tier stated and logged | P | no mechanism; `brief-coding-agent` skill omits it (built-in audit) |
| `Verified how:` on completion claims | P | `issue-checkbox-lint.sh` covers checkboxes, not this line; `close-issue` template omits it (C18) |
| STOP conditions, evidence, never-guess, sync-before-reading | P | CI red for 13 days with work continuing (D-5 row 7) |
| Named-trigger deferral | P (+ A) | only the aging script, which needs dated rows |
| Memory deletion irreversible | P | memory lives outside the repo |
| Model A worktree discipline | A | SessionStart warns when on `main`; provisioning asserts 0-behind (per CLAUDE.md, unverified) |

Finding D-6. denominator: about 19 rule groups, not every sentence. Roughly 6 mechanized, 6 advisory, 7 prose-only. The prose-only rules are the ones with the worst incident record in D-5 (rows 1, 4, 7, 8). The repo's own pattern (`mail-send.sh`, autoclose guard, ratchet tests) is that rules turned into scripts stopped recurring (autoclose has a mechanism and no post-mechanism incident found; unverified for completeness). Implication for "mechanize / mod": a tool-call mod or PreToolUse hook on `git checkout`/`stash`/`reset` in the main checkout is the obvious candidate; so is a check that fails if CLAUDE.md or a skill references a missing path.

## Top findings for synthesis

1. D-1: written session start is about 62k tokens for a typical role (84-96k at a cycling fire); 65% is one file, BRIEFING-CURRENT-STATE (40k), whose own banner says not to read it. CLAUDE.md alone is 16k.
2. D-2: 94% of load is shared; role-specific share 2-10% (13/13 under 25%). Clause of H1b met.
3. D-3: 50 deduplicated ruleset defects; most in skills (git push origin main vs HEAD:main in 4 skills, check-mailbox lacks mail-send.sh, dead skill names), 4 in CLAUDE.md itself including a wrap-up checklist that contradicts the HARD RULE (C2). The built-in audit independently flagged the same C2 and asked for a PM decision.
4. D-5: 5 firm marked rules violated after being written (destructive git 2026-08-08, briefing gap 2026-08-12 to 24, deferral 2026-08-31, session-log lapse June, CI-red STOP rule); no margin over the bar of 5. Prose-only ones recur; for mechanized ones no recurrence was found (unverified for completeness).
5. D-4: narrative share by line is 11-14% (below the 40% bar) but about 40-50% by weight; extraction to `claude-md-history.log` is already underway.
6. D-6: enforcement is about 6 M / 6 A / 7 P; hook firing unverified; 3 hook scripts registered nowhere and PreCompact absent from repo settings.
7. H2 verdict: supported on M2.1 + M2.2 + M2.4 (M2.4 with no margin); M2.3 by lines fails. H1b M1b.1 clause holds.

## Unobservables

- Actual tokens read by live agents at session start (needs session transcripts or a token meter; the Claude Code tool-result sizes in a transcript would show it). Real tokenizer counts (needs the API token-count endpoint).
- `~/.claude-pm/` shared memory, user-level `~/.claude` hooks and settings, managed policy, ancestor CLAUDE.md files (not in the repo; the built-in audit also could not read them).
- Hook live firing, including PreCompact and the "hooks reload live" property CLAUDE.md calls unresolved (needs a live seat with a probe).
- The live cron prompts (they exist as CronCreate or LaunchAgent text on the Amber host, not in the repo); I used the duty-cycle-tick skill and the registry as proxies.
- Whether the incident dates quoted from CLAUDE.md itself (2026-08-27, 08-31, 09-20) match primary records; I cite them as self-reported.
- Skill/briefing counts: the task said 37 skills; the snapshot has 37 entries under `.claude/skills/` but 35 SKILL.md files (the built-in audit also found 35).

## Appendix: deviations and minor notes

- Deviation: the built-in audit produced no PROMPT_AUDIT.md or patch file; its report and diff were recovered from the headless session transcript (`/root/.claude/projects/-home-user-audit-wt/*.jsonl`, final assistant message) and saved to `metrics/D-prompt-audit/`.
- Deviation: M2.3 is computed on 745 lines as pre-registered, plus a character-weighted view, which is not pre-registered and is labelled post-hoc.
- Deviation: M2.1 counts hook output as measured in the scratch worktree (detached HEAD, no `dev/` logs for today), so the live figure may differ by up to the 500-character budget (about 125 tokens).
- The website CLAUDE.md (11,124 bytes, about 2.8k tokens) loads only for the Web role when working in `piper-morgan-website`; not in the base. I found no CLAUDE.md under `skunkworks/` at the snapshot (0 files).
- I dispatched no subagents. The six Sonnet reviewers noted above were spawned by the built-in audit itself (per its transcript metadata).
