# Prompt audit: Claude Code configuration for this project

**Nothing was edited.** The proposed diff is below, and you can take hunks one at a time.

## Step 0: assumptions
- **Target model:** Claude Sonnet 5.5, the model this session runs on. None of the audited files pin their own model.
- **Audited (all read in full):**
  - Root `CLAUDE.md` (745 lines).
  - Nested `dev/2025/09/21/CLAUDE.md` and `dev/2025/09/21/AGENTS.md`.
  - 35 project skills, each `SKILL.md`, plus the five `piper-*` READMEs.
  - `SKILLS.md` and `SKILL-CREATION-RUNBOOK.md`.
- **Not present:** `CLAUDE.local.md`, `.claude/CLAUDE.md`, and any `.claude/rules/`, `commands/`, `agents/` or `output-styles/`. `CLAUDE.md` has no `@` imports.
- **Not read:**
  - `/home/user/CLAUDE.md`, `~/.claude/*` (which would affect all projects) and `/etc/claude-code/CLAUDE.md`. The read permission was not granted.
  - Plugin-provided skills. No plugin directory was found, but I couldn't list the directory.
  - Settings files and `.mcp.json`, by instruction. This means the `CLAUDE.md` claim that autonomous sessions are allowlisted in `.claude/settings.json` is unverified.
- **Method:** I audited `CLAUDE.md`, the nested files and the index files myself. I split the skills across six read-only reviewers on Sonnet. I re-checked every High finding below against the repo myself, with `git blame`, quotes and path reads. That caught one wrong reviewer claim: they said `.github/ISSUE_TEMPLATE/` didn't exist, but the tracked directory is `.github/issue_template/`.
- **Session log not created:** the project's session-log step would write to the repo, which is outside a read-only audit. Say if you want one.

## Summary
The surface has few old-model prompting habits: almost no "think step by step", no scaffolds, and caps-emphasis only in a few headings. The real problems are staleness and contradictions. The three highest-impact findings:
1. **Instruction files contradict each other and `CLAUDE.md` on actions that matter.**
   - Four skills (`create-session-log`, `cut-release`, `publish-to-blog`, `duty-cycle-tick`) tell agents to `git push origin main`. `CLAUDE.md` says `git push origin HEAD:main`.
   - `check-mailbox` has no `mail-send.sh` path at all.
   - Inside `CLAUDE.md`, the session-log location, the wrap-up checklist and the "hooks possibly not firing" line each contradict a newer rule in the same file.
   - Three blog skills disagree on Ship footers, title case, metrics tables and word counts.
2. **Dead references.**
   - Skill names that don't exist: `draft-issue`, `metrics-review`, `meet-piper`, `record-decision`, `insight-surface`.
   - Missing files: `mailboxes/README.md`, a wrongly-cased `.github/ISSUE_TEMPLATE/`, and a stale `llm_config_service.py:213` pointer.
   - The nested `dev/2025/09/21/CLAUDE.md` and `AGENTS.md` point at five repo paths that no longer exist.
3. **Incident narrative and changelog text inside operative instructions.** This is worst in `duty-cycle-tick`, `cohort-attention-rollup`, `publish-to-blog`, `template-audit` and `CLAUDE.md` itself. Rules carry dates, incident IDs and "previously this said…" framing. `CLAUDE.md` already has a history log for that.

**Counts (findings, not unique files):**
- **Group 1, dated text:** 14 (about 8 history/fossil, 4 pressure-language, 2 numeric-heuristic).
- **Group 2, brittle config:** about 60, split roughly 22 contradictions, 25 wrong or stale specifics, 13 history.
- **Groups 3 and 4:** not applicable. There are no tool definitions or request-building code in scope.
- **Clean:** `deliver-mail` (retired redirect) and `assign-sprint-safely` (exact scripts with reasons, kept).

## Findings, highest confidence first
Edits to Group 2 contradictions and stale facts are proposed only, never auto-applied.

### High: contradictions (quote both sides; `git blame` orders them)
| # | Location | Evidence | Conflict, direction and action |
|---|---|---|---|
| 1 | `CLAUDE.md:33` vs `:74,:291` | `Session logs: dev/active/YYYY-…` vs `dev/YYYY/MM/DD/…` | Line 33 is from 2026-04-01; 74 and 291 are 06-12 and 06-29. **rewrite 33.** |
| 2 | `CLAUDE.md:742` vs `:99` | "project hooks possibly not firing" vs "hooks were dead… now fixed" | 742 is from 07-25; 99 is from 09-22. **rewrite 742.** |
| 3 | `CLAUDE.md:77` | `ls mailboxes/lead/inbox/` in a role-agnostic start protocol | Dates from 2026-01-13; the mailbox workflow uses `mailboxes/{role}/inbox/`. **rewrite.** |
| 4 | `CLAUDE.md:652` | "the whole point of Model-B + push-to-ref" | Written 06-21; Model A is current on Amber (lines 90–95, 681, 738). **rewrite** to "worktree + push-to-ref". |
| 5 | `create-session-log:99-100`, `cut-release:173`, `publish-to-blog:517,563` | `git push origin main` | A local `main` isn't the branch an Amber worktree commits on. Blame for `create-session-log` is 05-17; `CLAUDE.md` standing order is 06-14. **rewrite** to `git push origin HEAD:main`. |
| 6 | `duty-cycle-tick:34,:368` | `…{role}-code-opus-log.md` | Line 34 is from 06-12, before the `-opus` removal on 06-29. **rewrite** to `YYYY-MM-DD-HHMM-{role}-code-log.md`. |
| 7 | `check-mailbox:47-52,:108-113` | `mv … read/`, reply in sender's inbox, no `mail-send.sh` | Mail must land through `scripts/mail-send.sh`. **add** a pointer; no mention exists anywhere in the file. |
| 8 | `create-omnibus:268-275` | "MANDATORY: archive logs from `dev/active/`" | Logs now live in `dev/YYYY/MM/DD/`; Step 2 of the same file already reads there. **remove** the step. |
| 9 | `continue-narrative:70` | "record that in the cycle log" | `CLAUDE.md` says the cycle log is scratch and not a record. **rewrite** to the session log. |
| 10 | `draft-blog-post:159,:243` vs `template-audit:180-183` | "teases the very next item… regardless of category" vs "A Ship carries no footer tease" | The audit rule is the measured, newer one. **rewrite** the drafting skill. |
| 11 | `draft-blog-post:207,:277,:294` vs `draft-weekly-ship:205` | "keep metrics tables rich" vs "bullet list, never a table" | **rewrite** to the Ship rule; Medium and LinkedIn don't render tables. |
| 12 | `draft-weekly-ship:197` vs `template-audit:111` | "sentence case for theme" vs "title case, not sentence case" | **rewrite 197** (the audit is newer). |
| 13 | `draft-blog-post:170,218-221` vs `draft-weekly-ship:261-271` | role-name parenthetical gloss vs "no parenthetical gloss" | Scope the gloss to narratives and insights. **rewrite.** |
| 14 | Ship word count: `draft-weekly-ship:275` (800–1,200), `draft-blog-post:35` (1100–1400), `template-audit:48-51` (~1,630) | Three ranges | The first undercuts every measured Ship. **rewrite** to one range, cited once. |
| 15 | `update-calendar:261` vs `:154` | "Always set … canonicalSite" vs "Leave `canonicalSite` empty" | Line 154 is from 09-29. **rewrite 261.** |
| 16 | `close-issue-properly:66,331` vs `close-issue:53,133` | N/A boxes left `[ ]` vs `[x]` | Both skills and one of them internally disagree. **rewrite** to one convention. |
| 17 | `close-issue:90-103` | Closing template has no `Verified how:` | Required by `CLAUDE.md` and by `close-issue-properly`. **add.** |

### High: stale specifics
- `CLAUDE.md:161` cites `services/config/llm_config_service.py:213`, which is now inside a docstring. The Keychain-then-env resolution is `get_api_key` at line 265 (priorities at ~326 and ~332). **rewrite** to the function name.
- `CLAUDE.md:115,:744` cite `git-worktrees-model-a-setup.md` as current-model setup. That file's header says "DEPRECATED" and "no current exceptions". **flag** (a docs file, outside scope), and add "(header says deprecated; commands still valid)".
- `check-mailbox:146-147` names a missing `mailboxes/README.md`. **rewrite** to `mailboxes/DIRECTORY.md`.
- `audit-cascade:63` names `.github/ISSUE_TEMPLATE/`. The repo's tracked directory is `.github/issue_template/`. **rewrite.**
- `cleanup-dev-active:133` names a missing `agent-360-questionnaire-v0_2.md`. **remove.**
- `doc-sync-sweep:135` cites a mailbox memo that doesn't exist. **remove.**
- `SKILLS.md:164` cites `dev/active/skill-harvest-candidates.md`, which is now at `dev/2026/01/21/`. `:163` cites a memo found nowhere. **rewrite / remove.**
- `SKILLS.md` lists 24 of 35 skills; 11 are missing. It marks `create-omnibus-log` "planned" although `create-omnibus` exists. It shows `duty-cycle-tick` as "PoC 1.0" while that skill is at v1.43. **rewrite.**
- `create-omnibus` and `cut-release` have no frontmatter (`name`/`description`), so their trigger text is just the title. `narrative-verification` has the same gap. **add.**
- Nonexistent skill names:
  - `draft-issue` and `metrics-review` in `piper-draft-spec`, `piper-synthesize-feedback` and `propose-feature:56`.
  - `draft-spec`, `sprint-plan` and `record-decision` in `compost-review:137-138`.
  - `insight-surface` in `trust-check:67`.
  - `meet-piper` and `connect-piper` in `trust-check` and `update-piper`; their location is unverified.

  The `piper-*` names may be deliberate for plugin distribution (a naming-convention memo exists), so treat this as Medium.
- `draft-blog-post:31` and `publish-to-blog:224` name a calendar `category` column. The CSV header has `theme`. **rewrite.**
- `template-audit:333-355` has a 15-row report template for a 16-check list. **add** row 16.
- `update-calendar:80` omits the `not-syndicated` status. **add.**
- **Nested files** `dev/2025/09/21/CLAUDE.md` and `AGENTS.md` point at five paths that no longer exist: `services/config.py`, `services/orchestration/engine.py`, `docs/briefing/CURRENT-STATE.md`, `BRIEFING-ROLE-PROGRAMMER`, and `docs/internal/architecture/current/adrs/`. They also say `web/app.py` is "933 lines" (it is 455), name `config/PIPER.user.md` as the user config, and "Current Focus: CORE-GREAT-1". All are a year old and contradict the root file. They load only under that archive directory. **rewrite or remove the files.**

### Medium
- **Pressure markers** (Group 1a), `CLAUDE.md:69,128,273,495,527`: CRITICAL, MANDATORY and NON-NEGOTIABLE on five separate sections. The reasons are already beside each one, so the markers no longer rank anything. The same pattern appears in `create-session-log` (91, 193, 214), `audit-cascade:30`, `create-omnibus:27,34,134`, `close-issue-properly` (about five instances), `draft-weekly-ship:27,102,145` and `piper-draft-spec:236`. **rewrite** to plain statements with the reason. Keep the heading emphasis for the `NEVER` data-loss rules (`CLAUDE.md:639-651`).
- **Banned-phrase rule** (Group 1e), `CLAUDE.md:302-305`: `Never "You're absolutely right!"` has no provenance beyond an older model's tic. **rewrite** positively: "Give an honest assessment; disagree when warranted."
- **History and migration framing in operative text** (Groups 1d and 2):
  - `CLAUDE.md:90,539,650,738-740`, and the long incident parentheticals at 241-243, 254, 256, 313, 641.
  - `create-session-log:51,105`, `duty-cycle-tick` (many, plus 438-444), `cohort-attention-rollup` (29-67, 92-427), `publish-to-blog:57` and its 60-line changelog, `template-audit`, `draft-weekly-ship`, `update-calendar:50-66`, `cut-release:179-194` and its changelog, `create-omnibus:11-23`, `close-issue-properly:305-361` and `delete-module-safely`.
  - The exception to leave alone: lines that give a reason in one clause. **rewrite** to the rule plus a one-clause reason, and move dates and incident names to the existing history logs.
- `audit-cascade:67-95` pins "Fable" and quotes the dispatch-tier ruling at length. **rewrite** to the current Haiku/Sonnet/Opus rule.
- `brief-coding-agent` never says to set the `model` parameter or log the tier, though `CLAUDE.md:413-419` requires both. **add** one step.
- `duty-cycle-tick:217` runs `git checkout -- mailboxes/*/inbox/MANIFEST.md …` across all roles. `CLAUDE.md:653` says clear MANIFEST noise by explicit path for your own role. **rewrite.**
- `ab-a-isolation:26-34` uses bare `git stash pop`; the shared stash stack makes that unsafe. **rewrite** to the push-by-tag, capture-SHA, `apply` pattern.
- `update-current-state:91` says "Don't delete Recent Progress entries" and "trim old ones (keep 4)" in the same line. The live briefing has about 40 week sections. **rewrite.**
- `cleanup-dev-active:47` points to a "displacement trap" rule in `CLAUDE.md` that isn't there. **remove the pointer.**
- `piper-sprint-plan:44` queries by milestone or label; `assign-sprint-safely` says Sprint is a Projects v2 field. **rewrite.**
- `piper-draft-issue:179-189` hard-codes `mediajunkie` project IDs unconditionally, while Step 1 allows Linear, Jira or no tracker. **rewrite** to scope it.
- `draft-weekly-ship:35-40` loads template v4.1 while its own history says v4.2 superseded it; no v4.2 exists at that path. **flag.**
- `update-piper:56-60` names `get_profile()`/`save_profile()`, and the profile location it describes doesn't match `config/PIPER.md` plus the optional `PIPER.user.md`. Repo-wide absence of those functions is unverified. **rewrite.**

### Low (flag only, not in the diff)
- Numeric heuristics applied literally: `piper-synthesize-feedback:74` (4–8 themes), `piper-sprint-plan:47,143-169` (velocity percentages), `piper-draft-spec:236` (at least 2 non-goals), and the trust-tier session thresholds in `trust-check`.
- `bd` is the live tracker (sessions in 2026-09 still use it), so `CLAUDE.md:267` is consistent. `discovered-work-capture:171` (`bd list --created-by me`) is unverified.
- `CLAUDE.md:47-61` ("Wave pattern": name the "context pressure") is an anthropomorphic ritual with no way to check it works.
- `publish-to-blog` Procedure 262-505 duplicates `publish-post.js`; the script is outside the repo and unverified.
- Hard-coded model names in `create-session-log` templates; IDs and line numbers in `assign-sprint-safely:55-58`, `cut-release:112-157`, `cohort-attention-rollup:219,523` (`decisions.log:1761`).
- **Conflict to decide:** `CLAUDE.md:495-510`, the 03-18 "wrap-up checklist" (`cd /path/to/main/repo; git checkout main; git merge; git push origin main`). It contradicts the newer `HEAD:main` standing order, the HARD RULE and the mandatory checklist at 559-591. The newer text adds a `git fetch`, so I'm flagging this instead of rewriting it. My suggested resolution: delete steps 1–3 and point to "Mandatory sign-off checklist".
- **Clean, kept deliberately:** the data-loss and git-safety prohibitions, the Projects v2 rules, exact scripts for releases and mailbox sends, and the single end recap (`CLAUDE.md:622-630`).

## Proposed diff (unified; hunk per finding)
`CLAUDE.md` hunks are verbatim. For skill files I give the line to replace and its replacement, since I read them via reviewers.

```diff
--- CLAUDE.md
@@ line 33 @@
-**Session logs**: `dev/active/YYYY-MM-DD-HHMM-[role-slug]-log.md`
+**Session logs**: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-[role-slug]-code-log.md`
@@ line 77 @@
-ls mailboxes/lead/inbox/
+ls mailboxes/{role}/inbox/
@@ line 161 @@
-(Keychain first, then env var — see `services/config/llm_config_service.py:213`)
+(Keychain first, then env var — see `LLMConfigService.get_api_key` in `services/config/llm_config_service.py`)
@@ line 302-305 @@
-- Call out bad ideas and mistakes - PM depends on this
-- Never "You're absolutely right!" - be honest
-- STOP and ask for clarification rather than assuming
+- Give an honest assessment. Call out bad ideas and mistakes; PM depends on it.
+- STOP and ask for clarification rather than assuming
@@ line 652 @@
-that's the whole point of Model-B + push-to-ref.
+that's the whole point of per-agent worktrees + push-to-ref.
@@ line 742 @@
-See §"Worktree model" near the top of this file for the operative rules and the two Amber gotchas (silent stale-branch provisioning; project hooks possibly not firing).
+See §"Worktree model" near the top of this file for the operative rules and the two Amber gotchas (silent stale-branch provisioning; hooks that were dead from an invalid matcher, now fixed, and advisory only).
@@ line 744 @@
-- Setup + branch-collision context: `docs/internal/operations/git-worktrees-model-a-setup.md`
+- Setup + branch-collision context: `docs/internal/operations/git-worktrees-model-a-setup.md` (its header says "deprecated"; the commands remain valid for Model A)
@@ lines 128, 273, 495, 527 (marker removal, reasons already adjacent) @@
-### BRIEFING-CURRENT-STATE staleness response (MANDATORY when triggered)
+### BRIEFING-CURRENT-STATE staleness response (when triggered)
-### Session Log Maintenance (NON-NEGOTIABLE)
+### Session Log Maintenance
-## Sign-Off Discipline (CRITICAL — read before ending any session)
+## Sign-Off Discipline (read before ending any session)
```

Skill hunks (replace the quoted text at each line):
- `create-session-log:99-100`, `cut-release:173`, `publish-to-blog:517,563`: `git push origin main` → `git push origin HEAD:main`.
- `duty-cycle-tick:34,368`: `…{role}-code-opus-log.md` → `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{role}-code-log.md`.
- `duty-cycle-tick:217`: glob across roles → `git checkout -- mailboxes/{role}/inbox/MANIFEST.md mailboxes/{role}/read/MANIFEST.md`.
- `check-mailbox` after line 52 and 113 (add): "Send the reply and the inbox move with `scripts/mail-send.sh "mail({role}): {subject}" <every changed path>`; don't `git add` or commit mailbox files."
- `check-mailbox:146-147`: replace the `mailboxes/README.md` lines with `mailboxes/DIRECTORY.md`.
- `create-omnibus:268-285`: remove the archive step; add frontmatter `name`/`description` at line 1.
- `cut-release:1` and `narrative-verification:1`: add frontmatter with a one-sentence trigger description.
- `continue-narrative:70`: "cycle log / standing-items" → "your session log (and the standing-items tracker if one exists)".
- `draft-blog-post:159,243,293`: "teases the very next scheduled item…" → "teases the next scheduled non-Ship post; Ships carry no tease."
- `draft-blog-post:207,277,294`: metrics "kept rich in tables" → "bullet list, never a table."
- `draft-weekly-ship:197`: "sentence case for theme" → "title case (template-audit check 2)".
- `update-calendar:261`: "Always set blogURL + blogPath + canonicalSite" → "Always set blogURL + blogPath (leave canonicalSite empty until syndication runs)". `:80`: add `not-syndicated` to the status values.
- `audit-cascade:63`: `.github/ISSUE_TEMPLATE/` → `.github/issue_template/`. `cleanup-dev-active:133`: remove the line. `doc-sync-sweep:135`: remove the line.
- `template-audit:333-355`: add `16. Typographic residue ✓ PASS`.
- `SKILLS.md`: add the 11 missing rows, drop "planned" for `create-omnibus`, update the `duty-cycle-tick` row and the two reference paths.
- `ab-a-isolation:26-34`: stash recipe → `git stash push -u -m aba-<tag>`; capture SHA; restore with `git stash apply <sha>`; never in the shared main checkout.
- `update-current-state:91`: → "Add new entries at the top; don't delete others' entries unless PM or Docs trims them."
- `brief-coding-agent` (add): "State the model tier: set `model` explicitly and note it in your session log beside the dispatch."
- Nested `dev/2025/09/21/CLAUDE.md` and `AGENTS.md`: delete both, or replace with one line: "Archive directory; follow the root CLAUDE.md."

**Verified how:** I did the `CLAUDE.md` checks myself, with reads of the repo paths, greps of the named symbols, `git blame` on the contested lines, and a read of `get_api_key`. I re-ran the reviewers' High findings the same way: blame, path reads, quotes. Denominator: 41 of 41 in-project instruction files, with a spot-check of the reviewers' High findings only, not every Medium or Low one. I did not run the behavioral before-and-after probes (Step 7), so none of the removals is tested. Every file under `~/.claude`, the ancestor directories and any managed policy was unreadable here, so those are unaudited.